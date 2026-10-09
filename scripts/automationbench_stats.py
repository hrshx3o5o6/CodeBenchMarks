"""Summarise AutomationBench assertion counts per domain and negative text checks.

Usage: python3 -I scripts/automationbench_stats.py path/to/AutomationBench
"""

import re
import statistics
import sys
from collections import Counter
from pathlib import Path


def main(root: Path) -> None:
    domains = root / "automationbench" / "domains"
    negatives = Counter()
    for tasks_py in sorted(domains.glob("*/tasks.py")):
        src = tasks_py.read_text()
        blocks = re.findall(r'"assertions": \[(.*?)\n            \],', src, re.S)
        sizes = [b.count('"type":') for b in blocks]
        negatives.update(re.findall(r'"(body_not_contains|text_not_contains)"', src))
        print(
            f"{tasks_py.parent.name:<11} tasks {len(sizes):>3}  "
            f"assertions/task median {statistics.median(sizes):>4}  max {max(sizes)}"
        )
    print("negative text checks:", dict(negatives), "total", sum(negatives.values()))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
