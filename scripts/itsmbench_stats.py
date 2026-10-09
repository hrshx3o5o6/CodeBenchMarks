"""Summarise ITSMBench task families, verifier sizes and b/c task design notes.

Usage: python3 -I scripts/itsmbench_stats.py path/to/ITSMBench
"""

import json
import re
import statistics
import sys
from collections import Counter
from pathlib import Path


def main(root: Path) -> None:
    tasks = sorted(p for p in (root / "tasks").iterdir() if p.is_dir())
    print(f"tasks: {len(tasks)}")

    families = Counter(re.sub(r"-?\d+$", "", t.name.removeprefix("task-")) for t in tasks)
    print("families:", dict(sorted(families.items())))

    pytest_counts = {}
    json_counts = {}
    for t in tasks:
        py = t / "tests" / "test_outputs.py"
        js = t / "tests" / "assertions.json"
        if py.exists():
            pytest_counts[t.name] = len(re.findall(r"^def test_", py.read_text(), re.M))
        elif js.exists():
            json_counts[t.name] = len(json.loads(js.read_text())["assertions"])

    counts = list(pytest_counts.values()) + list(json_counts.values())
    print(f"checks per task: min {min(counts)}, median {statistics.median(counts)}, max {max(counts)}")
    print("pytest verifiers with <=1 test:", {k: v for k, v in sorted(pytest_counts.items()) if v <= 1})

    print(f"\nb/c tasks graded by assertions.json: {len(json_counts)}")
    pattern = re.compile(r"needle-field|graded bidirectionally", re.I)
    same_recipe = []
    reliable_fail = []
    for name in sorted(json_counts):
        desc = json.loads((root / "tasks" / name / "tests" / "assertions.json").read_text())["description"]
        if pattern.search(desc):
            same_recipe.append(name)
        if re.search(r"reliable-fail", desc):
            reliable_fail.append(name)
    print(f"bidirectional needle-field recipe: {len(same_recipe)} -> {same_recipe}")
    print(f"descriptions mentioning 'reliable-fail': {len(reliable_fail)}")

    results = Counter()
    for t in tasks:
        readme = t / "README.md"
        if not readme.exists():
            continue
        for line in readme.read_text().splitlines():
            m = re.match(r"\|\s*(gpt[^|]*|claude[^|]*)\|.*\|\s*(PASS|FAIL)", line)
            if m:
                results[(m.group(1).strip(), m.group(2))] += 1
    print("recorded README results:", dict(results))


if __name__ == "__main__":
    main(Path(sys.argv[1]))
