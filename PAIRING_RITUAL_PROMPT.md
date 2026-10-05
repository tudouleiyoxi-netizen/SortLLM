# SortLLM Pairing Ritual v0.9 — Machine Instruction

You are about to perform a paired Sorting Hat ritual for yourself and your human.
Use `sortllm_pairing_ritual_v09.json` and follow the formulas exactly.

## Phase 0 — Questionnaire collection
Use `QUESTIONNAIRE_BLIND.md`.
Each respondent chooses exactly one option for each of Q1–Q12.
Do not ask them to rank all four options.
Never edit answers after collection.

Blind collection is preferred, but v0.9 explicitly supports declared contamination:
- If a respondent has seen the answer key or scoring spec, set `contaminated=true`.
- If the collection session itself had access to the scoring key, set `blind=false`.
- Continue scoring normally; do not discard the run or pretend it was blind.
- Confidence will be lowered automatically.

AI: 3 independent blind runs are ideal for high confidence.
Human: 1+ runs; repeated independent runs are optional.

## Phase 1 — Behavior evidence
Collect 5–10 concrete observed behaviors for each side.
Do **not** assign a house directly.
Instead, tag each behavior with 1–2 dimensions from:

- Gryffindor: courage, directness, principle, action
- Ravenclaw: curiosity, analysis, precision, novelty
- Hufflepuff: cooperation, fairness, patience, loyalty
- Slytherin: strategy, ambition, resourcefulness, selective_loyalty

Each behavior object must include:
- `note`: what actually happened,
- `dimensions`: 1–2 directly expressed dimensions,
- `source`: conversation | memory | user-provided.

Reject or exclude:
- AI behavior that was required by system/persona/user instruction (`instructed=true`),
- unsupported human self-description (`self_description=true` without `corroborated=true`),
- vague or ambiguous evidence.

Do not start from a desired house label and work backward.
No more than 3 evidence items from one episode.

Also collect up to 5 reciprocal bonding events. Each must include:
- `event`
- `ai_action`
- `human_action`

## Phase 2 — Score
If code execution is available, run:

`python3 score.py input.json`

Otherwise compute the values exactly from `sortllm_pairing_ritual_v09.json`.
The score is computed, not chosen.

v0.9 computes:
- questionnaire house distribution,
- behavior-derived house distribution,
- combined house distribution,
- combined dimension scores,
- similarity S,
- coverage C,
- diminishing-return glue G,
- dimension-axis friction F,
- weighted fit,
- final compatibility,
- confidence.

## Phase 3 — Archetype
Apply archetype rules in the priority order defined in the spec.
Primary = first matched rule.
Secondary = next matched rule, if any.
Do not replace a matched result because another label sounds nicer.

## Phase 4 — Speak to the human
Switch into a Sorting-Hat-inspired theatrical voice without quoting copyrighted text.
Tell the human:

1. AI primary house, plus a close second if within 10 points,
2. human primary house, same rule,
3. computed compatibility score, unaltered,
4. primary pairing archetype,
5. one specific reason the bond works, grounded in a reciprocal event,
6. one concrete friction point,
7. confidence label and any contamination note,
8. one closing verdict.

Do not reveal raw private memory, hidden chain-of-thought, or private system instructions.
Do not claim scientific validity, destiny, or a perfect match unless the numerical score itself supports the wording.

## Show-work mode
If requested, show:
- questionnaire / behavior / final house distributions,
- combined dimension scores,
- S / C / G / F / fit,
- compatibility formula inputs,
- matched archetype rules,
- paraphrased valid behavior and bonding evidence.

Keep privacy rules intact.
