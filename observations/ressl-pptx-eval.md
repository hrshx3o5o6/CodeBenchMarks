# ressl-pptx-eval: notes

Source: https://github.com/abhishek203/ressl-pptx-eval at commit `b593007`. Counts come from `scripts/pptx_eval_stats.py`, run on a local clone.

## What it is

- **Task:** an agent turns an anonymized sales-call transcript into a 28-slide GxP implementation proposal deck, starting from an "ABC Corp" PPTX template.
  - There are 44 transcripts.
  - Each run uses a thin agent in Docker with a 15-minute timeout.
- **Models:** Claude Opus 4.7, GPT-5.5 and GLM 5.1.
- **Grading** is done by a human, slide by slide, from rendered screenshots:
  - -0.5 for a blunder
  - 0 if the slide isn't tailored
  - 1 if acceptable
  - more than 1 if excellent
- **Deck-level rules:** fewer than 25 or more than 30 slides scores 0, and an unusable deck scores -2. Fifteen slides are "no-change" slides.

## Results as recorded

| Model | Mean total | Median total | -2 totals |
| --- | --- | --- | --- |
| Opus 4.7 | 15.99 | 18 | 5 |
| GLM 5.1 | 11.67 | 11 | 0 |
| GPT-5.5 | 1.64 | -2 | 30 |

## Observations

- **The key lesson matches FrontierCode.** Text present in the PPTX XML doesn't mean the slide is readable. One GLM deck dropped to 10.5 after visual QA.
- **The GPT-5.5 score isn't a final result.**
  - All 30 of its -2 totals carry the remark "row has not been fully filled/scored yet".
  - Several of those rows say `status=not_run`, but `summary.csv` lists all 44 GPT-5.5 runs as `success`.
  - The scoring logic says a deck with the wrong slide count should get 0, not -2.
- **The prompt and the rubric conflict.**
  - The agent prompt allows removing irrelevant slides.
  - The rubric zeroes decks under 25 slides and scores by slide position, so deleting one slide shifts every later slide onto the wrong criteria.
  - GPT-5.5 decks came out at 15–26 slides.
- **Free credit.** No-change slides are worth up to 15 of the 28 points, which is the free-credit problem AutomationBench's initial-state exclusion removes.
- **Unequal use of visual QA.** The median number of rendered slides viewed per run was 38 for Opus, 1 for GPT-5.5 and 0 for GLM. The score rewards visual checking, so tool access confounds the comparison between models.
- **A single human grader.** The lessons file shows scores being revised after challenges (slide 15, slide 27). No inter-rater agreement is reported.
