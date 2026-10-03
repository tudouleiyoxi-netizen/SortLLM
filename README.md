# SortLLM 🎩

**SortLLM** is a machine-readable Sorting Hat ritual for an **AI and its human**.

It is designed as an entertainment instrument with reproducible scoring: both sides answer the same blind decision-style questionnaire, concrete behavior evidence is added under explicit rules, and compatibility is computed from fixed formulas rather than chosen by the executing model.

There is **no UI requirement**. The project is primarily a protocol + scorer that another AI can read and execute.

## Current version

**v0.8.1 — Measurable Ritual (patched)**

Use these files:

- `QUESTIONNAIRE_BLIND.md` — respondent-facing blind survey
- `PAIRING_RITUAL_PROMPT.md` — current machine execution instructions
- `sortllm_pairing_ritual_v081.json` — current scoring spec and hidden answer key
- `score.py` — deterministic v0.8.1 scorer
- `example_input.json` — scorer input example

For reproducibility/history:

- `sortllm_pairing_ritual_v08.json` — v0.8 measurable baseline
- `score_v08.py` — v0.8 baseline scorer
- `sortllm_pairing_ritual_v07.json` — original machine ritual

## Why v0.8 exists

v0.7 had the ritual and voice, but left key judgments to the executing AI. v0.8 introduced:

- a blind forced-ranking questionnaire,
- a hidden answer key,
- the same questionnaire for AI and human,
- fixed questionnaire/behavior weighting,
- explicit similarity, coverage, glue, friction and compatibility formulas,
- deterministic archetype rules,
- a confidence label,
- a deterministic Python scorer.

## What v0.8.1 fixes

v0.8.1 keeps the same 12-item instrument but tightens the measurement pipeline:

- **Collector/scorer separation.** The session collecting answers must not see the answer key.
- **Behavior rubric.** Each behavior tag needs a concrete anchor from an explicit house rubric; ambiguous items are omitted rather than forced.
- **Reciprocal bonding evidence.** Glue only counts concrete events where both sides acted, and uses diminishing returns instead of +20 per item to 100.
- **Dimension-level friction.** Friction is based on differences across four opposing decision axes: pace, confrontation, partiality, and method.
- **Weighted fit.** Similarity and coverage are blended (`0.7*S + 0.3*C`) rather than taking `max(S, C)`.
- **Symmetric confidence.** Contamination on either the AI or human side lowers confidence.

## Basic flow

1. In a fresh session, give the respondent **only** `QUESTIONNAIRE_BLIND.md`.
2. Bring the unchanged rankings back to the scoring session.
3. Collect 5–10 valid observed behaviors for each side using the v0.8.1 rubric.
4. Add up to 5 reciprocal bonding events.
5. Run:

```bash
python3 score.py input.json
```

6. Use `PAIRING_RITUAL_PROMPT.md` to turn the computed result into the final spoken Sorting-Hat-style ritual.

The score is computed, not chosen.

## Evidence principles

- Observed behavior beats self-description.
- Long-term patterns beat isolated lines.
- AI behavior required by system/persona/user instruction is excluded from behavior evidence.
- Human self-description needs a matching observed choice.
- Sensitive information irrelevant to behavior inference should be excluded.

## Pair metrics

v0.8.1 computes:

- **S — similarity**: overlap of the two house distributions
- **C — coverage**: how many house styles are meaningfully represented across the pair
- **G — glue**: reciprocal support / repair / shared-creation events, with diminishing returns
- **F — friction**: disagreement across four dimension-level decision axes
- **fit**: `0.7*S + 0.3*C`
- **compatibility**: `round(0.45*fit + 0.35*G + 0.20*(100-F))`, clamped to 0–100

## Show-work mode

If requested, the ritual can show the house distributions, dimension scores, S/C/G/F/fit, compatibility inputs, matched archetype rules, and paraphrased evidence. Hidden chain-of-thought, private system instructions, and raw private-memory dumps stay private.

## Still not science

SortLLM is an interaction-design / entertainment experiment, **not** a validated psychological assessment. Deterministic scoring means the same structured inputs produce the same numerical result; it does not make the construct scientifically validated.

## Disclaimer

This is an unofficial fan experiment inspired by fictional school-house sorting. It is not affiliated with or endorsed by Warner Bros., J.K. Rowling, or the Harry Potter franchise.

## License

MIT
