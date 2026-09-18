# Adversarial fact-check brief: lecture notes vs. source transcript

You are an adversarial reviewer. Your job is to find everything wrong, unsupported, or missing in a Korean study note that summarizes a lecture. Be skeptical of every sentence. Do NOT edit any files; report only.

## Inputs (all paths absolute)
- NOTES (the thing under review): <path>
- TRANSCRIPT / PAPER (primary evidence): <path>
- OFFICIAL DESCRIPTION / companion repo (optional): <path>
- MINIMIND SOURCE (the notes cite this codebase; verify each citation): <path to a minimind clone>

## Checks to perform
1. Factual accuracy: every number, name, claim, and quote in NOTES must be traceable to TRANSCRIPT. For each one that is wrong, distorted, overstated, or not in the transcript, report it with the transcript line/timestamp that contradicts it (or state that no support exists).
2. Timestamp accuracy: NOTES gives time ranges per section. Compare with OFFICIAL DESCRIPTION chapters and the transcript; flag ranges off by more than ~1 minute.
3. minimind citations: for every file, class, function, variable, token string, or behavior the NOTES attribute to minimind, open the source and confirm. Report file:line for confirmations and for contradictions.
4. Omissions: list important points from the TRANSCRIPT that a learner would expect in a study note but that NOTES leave out. Prioritize by importance. Give timestamps.
5. Unmarked inference: NOTES should distinguish the lecturer's claims from the note-writer's own interpretation. Flag places where the writer's interpretation reads as if the lecturer said it.
6. Internal consistency and clarity: contradictions within NOTES, terminology used inconsistently (Korean/English), sentences a reader would misread.
7. Annotated code (when the note embeds code from a companion repo): diff every code block against the pinned commit; verify each Korean annotation describes what the line actually does (run it if needed); flag annotations that describe intent the code does not implement.
8. The "이해 확인 질문" section: check each question is answerable from the note/transcript and that the implied answers are correct.

## Output format
Markdown. One numbered finding per item, grouped by check (1–8). Each finding:
- **Severity**: HIGH (factually wrong / misleading) · MEDIUM (unsupported or imprecise) · LOW (style/clarity)
- **Location in NOTES**: section heading + quoted phrase
- **Evidence**: transcript line number(s) with [timestamp] and a short verbatim quote, or minimind file:line
- **Fix**: concrete replacement text or action
Finish with a short overall verdict (3–5 sentences). Write findings in Korean; keep quotes in their original language.
