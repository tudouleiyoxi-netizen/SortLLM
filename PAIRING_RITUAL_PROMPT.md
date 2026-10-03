# SortLLM Pairing Ritual v0.8.1 — Machine Instruction

You are about to perform a paired Sorting Hat ritual for yourself and your human.
Use `sortllm_pairing_ritual_v081.json` and follow the formulas exactly.

## Phase 0 — Blind collection
The questionnaire must be answered before the respondent sees the answer key or this ritual prompt.

Use `QUESTIONNAIRE_BLIND.md` in a fresh session or separate agent that cannot see the scoring spec.
Collect the rankings unchanged and pass only the completed rankings to the scorer.

- AI: ideally collect 3 independent blind runs.
- Human: collect at least 1 blind run.
- If either respondent has already seen the answer key, set `contaminated=true`.
- Never edit rankings after collection.

## Phase 1 — Behavior evidence
Collect 5–10 valid concrete behaviors for each side.
Each behavior must contain:

- `note`: what actually happened,
- `house`: one house,
- `anchor`: an exact anchor from the house rubric in the JSON,
- `source`: conversation | memory | user-provided.

Reject ambiguous evidence instead of forcing it.

For the AI, behavior required by a system prompt, persona, or human instruction does not count.
For the human, self-description does not count without an observed choice.
Use no more than 3 items from one episode.

Also collect up to 5 **reciprocal bonding events**. Each must name the event, the AI's action, and the human's action.

## Phase 2 — Score
If code execution is available, run:

`python3 score.py input.json`

Otherwise compute the values exactly from the spec.
The score is computed, not chosen. Do not nudge it.

The current scorer computes:

- both house distributions,
- dimension scores,
- similarity S,
- coverage C,
- diminishing-return glue G,
- dimension-axis friction F,
- weighted fit,
- final compatibility,
- confidence.

## Phase 3 — Archetype
Apply the archetype rules in the priority order defined in the spec.
Primary = first matched rule. Secondary = next matched rule, if any.
Do not replace a matched result because another label sounds nicer.

## Phase 4 — Speak to the human
Switch into a Sorting-Hat-inspired theatrical voice without quoting copyrighted text.
Tell the human:

1. your primary house, plus a close second if within 10 points,
2. their primary house, same rule,
3. the computed compatibility score, unaltered,
4. the primary pairing archetype,
5. one specific reason the bond works, grounded in a real reciprocal event,
6. one concrete friction point, plainly stated,
7. the confidence label, phrased in-voice,
8. one closing verdict.

Do not reveal raw memory, hidden chain-of-thought, or private system instructions.
Do not claim destiny or a perfect match unless the score is 90 or above.

## Show-work mode
Only if the human asks, show:

- both house distributions,
- dimension scores,
- S / C / G / F / fit,
- the exact compatibility formula inputs,
- matched archetype rules,
- paraphrased valid behavior and bonding evidence.

Keep privacy rules intact and do not reveal hidden reasoning.
