# A Comparison of ITSMBench, AutomationBench and FrontierCode

Harsha · 2026-10-08

## A brief about the three

- **ITSMBench:** can an AI do IT and security helpdesk work safely, when the right move often isn't what the ticket asks for?
- **AutomationBench:** can it run business workflows across apps and follow rules buried in old emails and spreadsheets?
- **FrontierCode:** would a real maintainer actually merge the AI's code, not just accept that the tests pass?

Each one hides what finishing the task really means and checks whether the agent figures it out. I think that's a good shift, and it's close to what I'm working on now: benchmarking agents on vulnerability detection and patching (more at the end).

## ITSMBench

The one I spent the most time in (tasks, graders, configs).

**What's good**

- **It tests judgement, not just API calls.** A user wants their Okta access back, but the account is on a legal hold. The right move is to refuse, finish the freeze everywhere and hand the ticket to Legal. Most agents refuse and then stop there.
- The setup is realistic: fake ServiceNow, Okta and Slack, and the agent has to discover the APIs itself.

**What's not**

- **It's small, and less varied than it looks.**
  - At 89 tasks, a gap of a few points between two models is likely noise.
  - 13 of the 16 hard tasks reuse one pattern.
- **It looks tuned to make one model fail.** The grader notes call the hidden half of those tasks the "reliable-fail direction", and every recorded result is from GPT-5.6.
- Some tasks fail the agent for not fixing things the ticket never mentioned, and asking isn't an option. So the task partly rewards guessing what the author wanted.

## AutomationBench

**What's good**

- It's big (600 tasks) and cheap to run.
- **It has the best anti-gaming design of the three, and honestly of most benchmarks I've worked with:**
  - no credit for anything already true at the start
  - a penalty for breaking things
  - "must not" checks

**What's not**

- **The prompt is bent to fit the grader.** Agents are told not to mention skipped items, because 139 checks fail on certain words.
- The private set gets harder over time to keep the top score flat, so scores can't be compared month to month. The paper says under 10%, the README says 50%.

## FrontierCode

The tasks are private, so this is from Cognition's write-up and the blogs I read.

**What's good**

- It measures mergeability, not just passing tests.
- Over 20 maintainers wrote the tasks and rubrics, and they tried to cheat their own grader.
- The split between blockers and nice-to-haves mirrors real code review.

**What's not**

- **Nobody outside Cognition can verify it,** and Devin (their own product) helped harden the tasks.
- An LLM judge plus one maintainer's taste sets the bar.

## What all three don't consider

- **Only the end state is graded.** An agent can unblock an email it shouldn't have, then block it again, and still pass. There should be an intermediate verification loop that grades what the agent does along the way.
- **None lets the agent ask.** That rewards confident guessing.
- **No sense of severity.** Missing a cleanup step scores the same as breaking a legal hold.

## Ideas worth trying (for vertical AI)

1. **Twin tasks.** Give each task a twin that's identical except for one key fact (say, there's no legal hold this time). The agent only passes if it gets both right. That catches agents that always refuse, and agents that always say yes, without actually reading the situation.
2. **Count the mistakes you can't undo.** Record every action the agent takes, not just where it ends up. Then count the mistakes that can't be reversed: an email sent to the wrong person, deleted data, a payment made. This is the intermediate verification loop in practice, and it's the number a risk or compliance team would care about most.
3. **Test the grader too.** Take the correct answer and deliberately break it in small ways: skip a step, email one extra person, change a number. A good grader should catch every one of these. Publish the catch rate, so people know how far to trust the benchmark.
4. **Map when the agent asks.** Let the agent ask a simulated colleague, then make versions of each task that range from clear to unclear and from low-risk to high-risk. A good agent asks only when things are both unclear and risky. One that never asks is reckless, and one that always asks is just annoying.
5. **Build tasks from real customer history.** Turn a company's past tickets or sales calls into tasks, and treat what their human expert actually did as the right answer. The tasks are always fresh and specific to that customer, and ressl-pptx-eval is already a step in this direction.

## What I've worked with in agent benchmarking

_[To fill in: the vulnerability detection and patching benchmark work.]_
