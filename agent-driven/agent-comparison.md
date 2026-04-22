# AI Coding Agent Comparison (Agent Driven Approach)

This document compares five AI coding agents head-to-head, all using the same **Agent Driven** approach applied to the same benchmark program. For context on the benchmark program and methodology, see the [main case study](../README.md).

---

| Rank | Agent | Time | Key Strength | Key Weakness |
|:---|:---|:---|:---|:---|
| #1 | Claude Code (w/Sonnet 4.5) | 7h 0m | Best first-shot code quality, idiomatic Python | Expensive; CLI-first UI quirks |
| #2 | Anti Gravity (w/Gemini 3 Pro) | 7h 29m | Strong planning UI, reads any webpage via full browser rendering | Minor first-pass code quality flaws |
| #3 | Cursor (w/Sonnet 4.5) | 6h 10m | Most polished UI, fastest time | Less Pythonic, tends to overcomplicate logic |
| #4 | Cline (w/Sonnet 4.5) | 7h 14m | Open source, highly configurable | No processing feedback, cumbersome setup |
| #5 | Copilot (w/Sonnet 4.5) | 7h 36m | None notable | Only agent to generate functionally incorrect code |

*Ranking is by overall code quality and reliability, not by time.*

One notable finding: Claude Code, Cursor, Cline, and Copilot all used the same underlying model (Claude Sonnet 4.5), yet produced significantly different results. Claude Code was the clear standout, Cursor and Cline were in the middle, and Copilot was dramatically worse. This suggests that beyond the underlying model, the agent harness — how the agent manages context, plans, executes, and self-corrects — plays a significant role in overall effectiveness.

---

### Common Observations Across Agents

**Strengths:** All agents asked good clarifying questions before generating code, though Anti Gravity and Copilot needed an initial prompt before doing so. Code quality was generally functional, and all agents attempted to test and self-correct their implementations. All five were able to one-shot the analysis script. Agents also proposed and successfully implemented some approaches that I hadn't considered myself.

**Weaknesses:** Agents universally struggled with self-directed optimization: when tuning puzzle generation times or finding optimal clue batch sizes, they often ran experiments without proper controls and got stuck in loops. By default, most added unnecessary fallback and retry logic rather than diagnosing root causes. Almost all defaulted to the older OpenAI Chat Completion API instead of the Response API, which is required to configure model reasoning effort. Without explicit guidance, agents also introduced security issues — one stored an API token in a .env file committed to the source repo. They also had a bit of trouble maintaining coherence across the codebase, making mistakes like generating too few attribute values for a 20×20 puzzle, or changing how the execution script wrote log files without updating how the analysis script read them. 

---

### Claude Code (w/Claude Sonnet 4.5)

**Total Time Taken:** 7h 0m

Claude Code produces the best code overall on the first shot, but it is also the most expensive. I can trust it to produce functionally correct and stylistically good code with minimal human intervention. There are also some UI quirks when using it as a VSCode extension, since it came out initially as a CLI tool. If costs are no issue, this is what I would pick as the best AI coding assistant.

**Raw Coding & Problem Solving:**
Claude Code stands out with its natural use of Pythonic, procedural coding styles, entirely avoiding unnecessary class structures without needing explicit prompting. It exhibits high autonomy and trustworthiness, eagerly running the program to iteratively verify its own fixes, and reliably handling minor refactors independently. Furthermore, it demonstrated strong algorithmic creativity by devising a deterministic method for generating uniquely solvable clue sets—an approach I had considered but abandoned. However, this creativity sometimes worked against it. It tried to replace the CSP solver with custom uniqueness checking code — technically impressive, but far more complex than necessary. A simple heuristic to initialize a large batch of clues before calling the solver would have been sufficient, which is what I had to explicitly instruct it to use. The only other minor drawback was its occasional use of strings and regex to manage clue attributes rather than proper data structures.

**Interface & Workflow:**
Claude Code's workflow operates smoothly alongside human interventions, allowing users to interrupt operations without the agent losing tracking of its context. Because of its CLI roots, the VSCode extension is missing some polish. The transition indicator between planning and implementation modes can feel unclear, and the chat interface fails to anchor visually to the beginning of lengthy generated plans. It also currently lacks a built-in checkpoint rollback feature. Although Git serves as an adequate workaround. Finally, its high quality comes at a price. I exhausted the Claude Pro plan token limit in just three days of coding.

---

### Anti Gravity (w/Gemini 3 Pro)

**Total Time Taken:** 7h 29m

In general, Anti Gravity produced pretty good code and had some useful features that the other AI editors lacked, such as dedicated UI support for plans and todo lists. Additionally, it's the only editor that uses a web browser to read documentation, which allows it to read documentation that the other agents can't access. Overall I'd place it as #2 in terms of overall quality.

**Raw Coding & Problem Solving:**
Anti Gravity's initial implementation plan matched closely with my own human-created strategy. It demonstrated strong logical reasoning by catching inconsistencies in my prompt and proactively validating its own changes through code execution. However, the agent's first-pass code quality had some minor flaws, including unused variables and small amounts of overly complex logic. It required some explicit guidance to use the OpenAI Response API rather than the Chat Completion API.

**Interface & Workflow:**
The agent has a strong organizational UI that automatically manages implementation plans and allows users to comment on them directly. It also asked strong upfront clarifying questions. The workflow has some limitations: agent initiated terminal commands are difficult to track in the chat window, and users cannot ask the agent to explain a code change without accepting it first. Its browser-based approach to reading documentation is effective but noticeably slower than standard HTML parsing.

---

### Cursor (w/Claude Sonnet 4.5)

**Total Time Taken:** 6h 10m

Cursor is 3rd in code quality generation, but it is much better than Copilot and the quality is good enough that I would trust it to generate code without extensive human review. It does have overall the most polished UI of all the AI IDEs I tested and I found it enjoyable to use.

**Raw Coding & Problem Solving:**
Cursor's code is generally trustworthy but not as clean as Claude Code's. It defaults to class-based structures, leaves unused variables, and uses non-idiomatic patterns like `while` loops with indexes. Solutions tend to be overcomplicated and required explicit prompts to simplify. It also occasionally chose poor architecture, such as a brute-force clue generation method that did not guarantee unique puzzle solutions.

**Interface & Workflow:**
Cursor boasts highly polished UI features that make the AI workflow fluid and enjoyable. It excels at managing context, maintaining full conversation histories better than most competitors, and seamlessly accepting terminal text via simple UI clicks. The interface also supports intuitive multi-file review and smoothly handles being interrupted with new suggestions mid-task. However, I did encounter a significant UI bug. Clicking the "undo" button occasionally deleted the entire file.

---

### Cline (w/Claude Sonnet 4.5)

**Total Time Taken:** 7h 14m

Like Cursor, Cline generates code that is good enough to be used without extensive human review, but I wouldn't choose it over the other options except Copilot. Its UI is much less polished than most of the other AI IDEs I tested. It is open source and offers a lot of configuration options, which allows more customizability compared to the other options.

**Raw Coding & Problem Solving:**
Cline correctly applied the `python-constraint` library to the puzzle generation problem and proactively attempted to test its code. However, the resulting constraint code is somewhat difficult to read and its overall code generation quality has room for improvement. It failed to verify its clue generation strategy without explicit prompting and proposed poorly solutions for optimization the puzzle generation time. It also had some poor coding practices, such as assigning a default `None` value to an `int` parameter.

**Interface & Workflow:**
Cline's interface is less polished than the other agents and sometimes disrupts the workflow. The UI provides no indication when the LLM is processing, making it hard to tell if the agent is working. Setup also requires detailed configuration, such as manually setting a model thinking budget. The UI for answering clarifying questions presents only a single set of answer choices even when the LLM asks multiple questions, which requires the user to respond in free-form text.

---

### Copilot (w/Claude Sonnet 4.5)

**Total Time Taken:** 7h 36m

Overall, Copilot was the worst of the all the AI IDEs I tested with Approach #1, even though it used the same underlying model (Claude Sonnet 4.5) as Claude Code, Cursor, and Cline. The code generation quality was just much worse than any of the other agents. It's the only agent that I wouldn't trust to generate functionally correct code without extensive human review.

**Raw Coding & Problem Solving:**
Copilot struggled significantly with basic code generation and logical reasoning. Its initial code derived from the plan was extremely poor, failing even simple logic tasks like randomly picking two items from a list, and generating highly inefficient code with unnecessary calls to the CSP solver. Furthermore, the agent displayed low autonomy, never attempting to independently test its code and repeatedly defaulting to writing fallback logic instead of analyzing and fixing root causes. Even when explicitly provided with documentation for the OpenAI Response API, the agent initially claimed it couldn't access the URLs, then generated incorrect logic utilizing the Chat Completion API instead. This poor logical consistency extended to its analysis scripts, where it wrote logic inherently incapable of ever signaling an error.

**Interface & Workflow:**
Copilot's workflow is more rigid than the other agents. It cannot edit files while in plan mode and does not automatically switch modes. Unlike other agents, which allow a new prompt while changes are pending, Copilot requires you to accept or reject each change before proceeding and its "Keep/Undo" widget hides a portion of the code diff during that decision. The agent is also noticably slow when it needs to compact its conversation history.
