# AutomationBench: detailed observations

Source: https://github.com/zapier/AutomationBench at commit `4a8e106`, plus the paper at https://arxiv.org/abs/2604.18934. Counts come from `scripts/automationbench_stats.py`.

## How it works

- Six scored domains with 100 tasks each: sales, marketing, operations, support, finance and HR. There is also an unscored `simple` warm-up set of 200 tasks.
  - `domains/sales/tasks.py` defines 106 `example_id`s; the README counts 100.
- The world is an in-memory Pydantic `WorldState` covering 47 simulated SaaS apps. There are no containers.
- In the default `api` toolset the agent gets three tools:
  - `api_search`, a BM25 search over API schemas
  - `api_fetch`, which routes real-looking URLs to the simulated apps
  - `base64_encode`
- Calls to apps outside a task's scope return a credentials error (`compute_allowed_services`).
- The system prompt says not to ask clarifying questions, gives a budget of about 50 turns, and says not to enumerate skipped or excluded items.
- **Noise injection** (`domains/*/_noise.py`) adds deterministic filler records seeded by task ID.
  - Policy and lookup worksheets are skipped by name tokens and by size (8 rows or fewer).

## Scoring

The scoring code is in `rubric/__init__.py`.

- **`partial_credit`** is the fraction of counted assertions that pass.
  - Assertions already true in the initial state are excluded.
  - If such an assertion becomes false, it counts as a failure.
  - `"excluded": false` forces an assertion to count, which matters for do-nothing tasks.
- **`task_completed_correctly`** is 1 only when partial credit is 1.0. The official pass rate is the mean of this, with `simple` excluded.
- **Doc vs code mismatch:** `rubric/registry.py` says negative assertions earn credit only when all positive assertions pass. Nothing in `partial_credit` calls `is_negative`, so that rule is not enforced.

## Assertions per task

| Domain | Median | Max |
| --- | --- | --- |
| finance | 7 | 16 |
| hr | 9 | 21 |
| sales | 10 | 24 |
| operations | 13 | 28 |
| marketing | 18 | 57 |
| support | 32 | 64 |
| simple | 1 | 2 |

There are 139 negative text checks: 128 `body_not_contains` and 11 `text_not_contains`.

## Scores

- The paper (April 2026) reports the best model below 10%. That figure is on the private set.
- The README reports public-set pass rates: Claude Opus 5 at 50.3% and GLM 5.2 at 26.17%.
- The official leaderboard uses a held-out private set, which is "purposely harder". The CHANGELOG for 1.0.6 says private tasks were made harder to compensate for bug fixes.

## Strengths

- Scale: 600 scored tasks across six functions.
- It's cheap and fast to run, and partial credit makes it usable as an RL reward.
- It has strong anti-gaming measures:
  - initial-state exclusion
  - a penalty for breaking things
  - negative checks
  - the service fence
- Noise injection is realistic, with fairness rules so the noise can't change the right answer.
- It is actively maintained: CHANGELOG, fairness fixes and a large test suite.

## Weaknesses

- **The system prompt is shaped around the grader.** The instruction not to mention skipped items exists because of the 139 negative text checks.
- **Exact text matching**, e.g. `"$156,000"`. Version 1.0.6 admits some tasks were too strict about formatting.
- **No clarifying questions** are allowed.
- **The private set is a moving target**, so scores aren't comparable over time.
- **Tasks lean towards logic puzzles** rather than operational mess like auth failures, pagination and retries.
- **Single run by default**, with no variance reported.
- **Hard to audit:** about 210k lines of hand-written task dicts.
