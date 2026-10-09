"""Summarise ressl-pptx-eval run status and per-model deck scores.

Usage: python3 -I scripts/pptx_eval_stats.py path/to/ressl-pptx-eval
"""

import csv
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path


def main(root: Path) -> None:
    run = next((root / "runs").glob("benchmark_*"))

    by_model = defaultdict(list)
    with open(run / "summary.csv") as f:
        for row in csv.DictReader(f):
            by_model[row["model_key"]].append(row)
    for model, rows in by_model.items():
        status = Counter(r["status"] for r in rows)
        views = statistics.median(int(r["view_image_count"] or 0) for r in rows)
        print(f"{model:<20} runs {len(rows)}  status {dict(status)}  median rendered-slide views {views}")

    print()
    for path in sorted((run / "eval_by_model_csv").glob("*.csv")):
        with open(path) as f:
            rows = list(csv.DictReader(f))
        totals = [float(r["Total"]) for r in rows if r["Total"].strip()]
        placeholders = sum("not been fully filled" in r["Remarks"] for r in rows)
        print(
            f"{path.stem:<36} mean {statistics.mean(totals):5.2f}  median {statistics.median(totals):5.1f}  "
            f"-2 totals {sum(t == -2 for t in totals)}  placeholder rows {placeholders}"
        )


if __name__ == "__main__":
    main(Path(sys.argv[1]))
