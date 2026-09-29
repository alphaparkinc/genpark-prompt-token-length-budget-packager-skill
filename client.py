"""Prompt Token Length Budget Packager.
100% Python Standard Library.
"""

import re

class TokenBudgetPacker:
    """Optimizes packing of variable-length training examples into fixed token budget windows."""
    @staticmethod
    def estimate_tokens(text: str) -> int:
        words = re.findall(r'\S+', text)
        return max(1, int(len(words) * 1.3 + len(text) * 0.05))

    @staticmethod
    def pack_examples(examples: list, max_budget: int = 4096) -> list:
        items = []
        for ex in examples:
            tokens = ex.get("tokens") or TokenBudgetPacker.estimate_tokens(ex.get("text", ""))
            items.append({**ex, "tokens": tokens})

        # First-Fit Decreasing (FFD) heuristic
        items_sorted = sorted(items, key=lambda x: x["tokens"], reverse=True)
        bins = []

        for item in items_sorted:
            placed = False
            for b in bins:
                if b["current_tokens"] + item["tokens"] <= max_budget:
                    b["examples"].append(item)
                    b["current_tokens"] += item["tokens"]
                    placed = True
                    break
            if not placed:
                bins.append({
                    "bin_id": len(bins) + 1,
                    "max_budget": max_budget,
                    "current_tokens": item["tokens"],
                    "examples": [item]
                })

        for b in bins:
            b["utilization_pct"] = round((b["current_tokens"] / max_budget) * 100, 2)
            b["waste_tokens"] = max(0, max_budget - b["current_tokens"])
            b["oversized"] = b["current_tokens"] > max_budget

        return bins
