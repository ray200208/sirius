import re
from typing import Any, Optional
from deepdiff import DeepDiff
import numpy as np
from scipy import stats

from app.config import settings
from app.services.extractors import (
    extract_price, extract_currency, extract_keywords, normalize_headline
)


# --------------------------------------------------------------------------- #
#  Result type                                                                  #
# --------------------------------------------------------------------------- #

class ChangeResult:
    def __init__(
        self,
        change_type: str,
        severity: str,
        description: str,
        diff: Optional[dict] = None,
        old_value: Optional[str] = None,
        new_value: Optional[str] = None,
    ):
        self.change_type = change_type
        self.severity = severity
        self.description = description
        self.diff = diff
        self.old_value = old_value
        self.new_value = new_value


# --------------------------------------------------------------------------- #
#  1. Pricing change detection                                                  #
# --------------------------------------------------------------------------- #

def detect_price_changes(
    old_plans: list[dict], new_plans: list[dict]
) -> list[ChangeResult]:
    """
    Compare two lists of pricing plans and emit a ChangeResult for every
    plan whose price moved, was added, or was removed.
    """
    results: list[ChangeResult] = []

    old_by_name = {p.get("name", "").lower(): p for p in old_plans}
    new_by_name = {p.get("name", "").lower(): p for p in new_plans}

    all_plan_names = set(old_by_name) | set(new_by_name)

    for plan in all_plan_names:
        old_plan = old_by_name.get(plan)
        new_plan = new_by_name.get(plan)

        # Plan removed
        if old_plan and not new_plan:
            results.append(ChangeResult(
                change_type="price",
                severity="high",
                description=f"Plan '{plan}' was removed from pricing page",
                old_value=str(old_plan.get("price")),
                new_value=None,
            ))
            continue

        # Plan added
        if not old_plan and new_plan:
            results.append(ChangeResult(
                change_type="price",
                severity="medium",
                description=f"New plan '{plan}' added at {new_plan.get('price')}",
                old_value=None,
                new_value=str(new_plan.get("price")),
            ))
            continue

        # Price changed
        old_price = extract_price(str(old_plan.get("price", "")))
        new_price = extract_price(str(new_plan.get("price", "")))

        if old_price is not None and new_price is not None and old_price != new_price:
            pct = abs((new_price - old_price) / old_price) * 100 if old_price else 0
            severity = _price_severity(pct)
            direction = "increased" if new_price > old_price else "decreased"
            currency = extract_currency(str(new_plan.get("price", "")))

            results.append(ChangeResult(
                change_type="price",
                severity=severity,
                description=(
                    f"Plan '{plan}' price {direction} by {pct:.1f}% "
                    f"({currency} {old_price:.0f} → {new_price:.0f})"
                ),
                old_value=str(old_price),
                new_value=str(new_price),
                diff={"plan": plan, "old": old_price, "new": new_price, "pct_change": round(pct, 2)},
            ))

        # Feature list diff for same plan
        if old_plan and new_plan:
            old_features = set(old_plan.get("features", []))
            new_features = set(new_plan.get("features", []))
            added = new_features - old_features
            removed = old_features - new_features
            if added or removed:
                results.append(ChangeResult(
                    change_type="price",
                    severity="low",
                    description=f"Plan '{plan}' features changed",
                    diff={"added_features": list(added), "removed_features": list(removed)},
                ))

    return results


def _price_severity(pct_change: float) -> str:
    if pct_change >= 25:
        return "critical"
    if pct_change >= 10:
        return "high"
    if pct_change >= settings.PRICE_CHANGE_THRESHOLD_PCT:
        return "medium"
    return "low"


# --------------------------------------------------------------------------- #
#  2. Keyword change detection                                                  #
# --------------------------------------------------------------------------- #

def detect_keyword_changes(
    old_keywords: list[str], new_keywords: list[str], context_text: str = ""
) -> list[ChangeResult]:
    """Detect added / removed tracked keywords and surface new keyword signals from text."""
    results: list[ChangeResult] = []

    old_set = set(k.lower() for k in old_keywords)
    new_set = set(k.lower() for k in new_keywords)

    added = new_set - old_set
    removed = old_set - new_set

    if added:
        results.append(ChangeResult(
            change_type="keyword",
            severity="medium",
            description=f"New keywords added: {', '.join(sorted(added))}",
            diff={"added": list(added)},
            new_value=", ".join(sorted(added)),
        ))

    if removed:
        results.append(ChangeResult(
            change_type="keyword",
            severity="low",
            description=f"Keywords removed: {', '.join(sorted(removed))}",
            diff={"removed": list(removed)},
            old_value=", ".join(sorted(removed)),
        ))

    # Surface any AI/product keywords appearing in free-text (headlines, descriptions)
    if context_text:
        discovered = extract_keywords(context_text) - old_set - new_set
        if discovered:
            results.append(ChangeResult(
                change_type="keyword",
                severity="low",
                description=f"Tracked keywords discovered in content: {', '.join(sorted(discovered))}",
                diff={"discovered_in_text": list(discovered)},
            ))

    return results


# --------------------------------------------------------------------------- #
#  3. Headline / messaging change detection                                     #
# --------------------------------------------------------------------------- #

def detect_messaging_changes(
    old_data: dict[str, Any], new_data: dict[str, Any]
) -> list[ChangeResult]:
    """
    Compare headline and any top-level string fields for messaging changes.
    Uses DeepDiff for structured diff + normalised string comparison.
    """
    results: list[ChangeResult] = []

    # Headline comparison
    old_headline = normalize_headline(old_data.get("headline", ""))
    new_headline = normalize_headline(new_data.get("headline", ""))

    if old_headline and new_headline and old_headline != new_headline:
        results.append(ChangeResult(
            change_type="messaging",
            severity="high",
            description="Primary headline / messaging changed",
            old_value=old_headline,
            new_value=new_headline,
        ))

    # Deep structural diff for the rest of the payload (excludes plans list noise)
    exclude_paths = {"root['plans']", "root['keywords']", "root['headline']"}
    diff = DeepDiff(old_data, new_data, ignore_order=True, exclude_paths=exclude_paths)

    if diff:
        # Summarise the diff into human-readable lines
        lines = _summarise_deepdiff(diff)
        if lines:
            results.append(ChangeResult(
                change_type="messaging",
                severity="medium",
                description="Messaging / copy changes detected: " + "; ".join(lines[:3]),
                diff=diff.to_dict(),
            ))

    return results


def _summarise_deepdiff(diff: DeepDiff) -> list[str]:
    lines = []
    for change_key, changes in diff.items():
        if change_key == "values_changed":
            for path, detail in changes.items():
                field = re.sub(r"root\[(['\"])(.*?)\1\]", r"\2", path)
                lines.append(f"'{field}' changed")
        elif change_key == "dictionary_item_added":
            lines.append(f"{len(changes)} field(s) added")
        elif change_key == "dictionary_item_removed":
            lines.append(f"{len(changes)} field(s) removed")
    return lines


# --------------------------------------------------------------------------- #
#  4. Anomaly detection (Z-score on price history)                             #
# --------------------------------------------------------------------------- #

def detect_price_anomaly(
    plan_name: str, price_history: list[float], latest_price: float
) -> Optional[ChangeResult]:
    """
    Z-score based anomaly detection over historical prices.
    Requires at least 5 data points for a meaningful signal.
    """
    if len(price_history) < 5:
        return None

    arr = np.array(price_history)
    z = float(stats.zscore(arr)[-1]) if len(arr) > 1 else 0.0

    # Recompute z for the latest price against the history (excluding itself)
    mean = np.mean(arr[:-1])
    std = np.std(arr[:-1])
    if std == 0:
        return None

    z_latest = abs((latest_price - mean) / std)

    if z_latest >= settings.ANOMALY_ZSCORE_THRESHOLD:
        severity = "critical" if z_latest >= 4.0 else "high"
        return ChangeResult(
            change_type="anomaly",
            severity=severity,
            description=(
                f"Price anomaly on plan '{plan_name}': "
                f"₹{latest_price:.0f} is {z_latest:.1f}σ from mean ₹{mean:.0f}"
            ),
            diff={"z_score": round(z_latest, 2), "mean": round(mean, 2), "std": round(std, 2)},
            new_value=str(latest_price),
        )

    return None
