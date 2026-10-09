# Agent benchmark review

A review of three agent benchmarks — **ITSMBench**, **AutomationBench** and **FrontierCode** — covering what each measures, what works, what doesn't, and ideas for evaluating vertical AI agents.

## Contents

| Path | What it is |
| --- | --- |
| [`writeup.md`](writeup.md) | The brief write-up |
| [`observations/itsmbench.md`](observations/itsmbench.md) | Detailed notes and evidence for ITSMBench |
| [`observations/automationbench.md`](observations/automationbench.md) | Detailed notes and evidence for AutomationBench |
| [`observations/frontiercode.md`](observations/frontiercode.md) | Notes on FrontierCode, from public material only |
| [`observations/ressl-pptx-eval.md`](observations/ressl-pptx-eval.md) | Notes on the ressl-pptx-eval proposal-deck benchmark |
| [`scripts/`](scripts) | Scripts that reproduce the counts quoted in the notes |

## Reproducing the numbers

```bash
git clone https://github.com/new-measure/ITSMBench.git
git clone https://github.com/zapier/AutomationBench.git
git clone https://github.com/abhishek203/ressl-pptx-eval.git

python3 -I scripts/itsmbench_stats.py ITSMBench
python3 -I scripts/automationbench_stats.py AutomationBench
python3 -I scripts/pptx_eval_stats.py ressl-pptx-eval
```

Reviewed at ITSMBench `30da745`, AutomationBench `4a8e106` and ressl-pptx-eval `b593007`. No agents were run for this review. All model scores are the benchmark authors' own.
