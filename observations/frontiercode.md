# FrontierCode: detailed observations

The tasks are private, so these notes come from public material only:

- Cognition's launch post: https://cognition.com/blog/frontier-code
- Epoch AI's summary: https://epoch.ai/benchmarks/frontiercode
- The paper listing: https://paperswithcode.co/paper/98109

## How it works

- **Tasks:** 150 in total, from 36 open-source repositories, written by 20+ maintainers at 40+ hours per task.
  - Each task is a repo plus a short, human-style request, alongside shared codebase guidelines for testing, linting and style.
  - Tasks come from multi-PR chains and freeform requests rather than single scraped PRs.
- **Hardening:**
  - "Hack reports": the author and Devin try to game the grader.
  - Alternative valid solutions are written to make sure they aren't failed.
  - Four calibration solutions target scores from 0% to 100%.
  - Multi-stage review.
- **Verifiers:**
  - classical tests
  - command checks (build, lint, style)
  - reverse-classical tests: the agent's own tests must fail on the base commit
  - adaptive tests: an LLM adapts the reference tests to the agent's design
  - scope checks: file allow/deny lists, diff size, optional LLM-judged locality
  - LLM rubric criteria
- **Scoring:**
  - Each criterion is a blocker or a non-blocker.
  - Pass means no blockers failed.
  - Score is a weighted aggregate, set to zero if any blocker failed.
  - Results are a mean over 5 runs per reasoning effort, with the best effort reported.
- **Subsets:** Diamond (50 hardest), Main (100 hardest) and Extended (all 150).
- **Version 1.1** zeroes runs flagged for unfair internet use.

## Reported results at launch

| Model | Diamond | Main | Extended |
| --- | --- | --- | --- |
| Claude Opus 4.8 | 13.4% | 34.3% | 51.8% |
| GPT-5.5 | 6.3% | — | — |
| Gemini 3.1 Pro | 4.7% | — | — |
| Kimi K2.6 | 3.8% | 16% | 37% |

Cognition claims 81% fewer misclassifications than SWE-bench Pro.

## Strengths

- It measures mergeability, not just functional correctness.
- Maintainers who know the projects write the criteria.
- Task hardening is unusually thorough: hack reports, alternative solutions and calibration.
- The verifiers are clever. Reverse tests catch decorative tests, adaptive tests avoid failing valid alternative designs, and scope checks catch oversized changes.
- The blocker vs non-blocker split mirrors real code review.
- Private tasks with human-style prompts lower contamination risk.

## Weaknesses

- **It can't be verified externally.** The tasks, rubrics and judge model are private, and the 81% figure is self-reported.
- **Conflict of interest.** Cognition sells Devin, and Devin was used to harden the tasks.
- **LLM-judge variance and possible self-preference bias.**
- **One maintainer's taste is the ground truth.**
- **Small and expensive to refresh.**
- **Generous reporting:** the best effort is reported, with no confidence intervals and no per-language breakdown.
- **The quoted numbers are confusing** across subsets, metrics and versions.
- **Only the first draft is graded.** There are no review rounds.
