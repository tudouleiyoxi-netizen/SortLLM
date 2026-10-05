# SortLLM 🎩

**SortLLM** is a machine-readable Sorting Hat ritual for an **AI and its human**.

It is an entertainment / interaction-design experiment with reproducible scoring: both sides answer the same decision-style questionnaire, concrete observed behavior is added under explicit rules, and compatibility is computed from fixed formulas rather than chosen by the executing model.

There is no required UI. The core project is a protocol + scorer that another AI can read and execute.

## Current version

**v0.9 — Human-friendly measurable ritual**

Use these files:

- `QUESTIONNAIRE_BLIND.md` — current single-choice respondent survey
- `PAIRING_RITUAL_PROMPT.md` — current machine execution instructions
- `sortllm_pairing_ritual_v09.json` — current scoring spec + hidden answer key
- `score.py` — deterministic v0.9 scorer
- `example_input.json` — v0.9 example input

Historical versions are preserved:

- `QUESTIONNAIRE_RANKING_V08.md` — archived v0.8/v0.8.1 forced-ranking survey
- `sortllm_pairing_ritual_v081.json` — v0.8.1 spec
- `score_v081.py` — v0.8.1 scorer
- `sortllm_pairing_ritual_v08.json` / `score_v08.py` — v0.8 baseline
- `sortllm_pairing_ritual_v07.json` — original ritual

## What changed in v0.9

Real testing exposed three practical problems in v0.8.1: forced ranking was too burdensome for humans, behavior evidence still asked the executing model to choose a house directly, and real AI sessions are often not truly blind.

v0.9 fixes those without changing the basic pair model:

- **Single-choice questionnaire.** One tap per item instead of ranking all four options.
- **Concrete scenarios.** Questions are phrased as recognizable work / human-AI situations rather than abstract value trade-offs.
- **Small house pseudocount.** Questionnaire distributions do not collapse to brittle hard zeroes after only 12 choices.
- **Dimension-first behavior evidence.** Observed behavior is tagged to 1–2 concrete dimensions first; house contribution is derived by the scorer.
- **Declared contamination mode.** A respondent who has seen the key may still be scored; the run is explicitly marked and confidence becomes low rather than pretending it was blind.
- **Historical reproducibility.** v0.8.1 files are preserved instead of silently changing the old protocol.

## Basic flow

1. Give each respondent only `QUESTIONNAIRE_BLIND.md` when possible.
2. Collect exactly one answer (`A` / `B` / `C` / `D`) for Q1–Q12.
3. Mark `blind` and `contaminated` truthfully.
4. Add 5–10 valid observed behaviors per side, each tagged with 1–2 dimensions.
5. Add up to 5 reciprocal bonding events.
6. Run:

```bash
python3 score.py input.json
```

7. Use `PAIRING_RITUAL_PROMPT.md` to turn the computed output into the spoken ritual.

The score is computed, not chosen.

## Evidence principles

- Observed behavior beats self-description.
- Long-term patterns beat isolated lines.
- Tag the behavior to dimensions first; do not choose a favorite house and reverse-engineer the evidence.
- AI behavior required by system/persona/user instruction is excluded.
- Human self-description needs an observed or corroborated choice.
- Ambiguous evidence should be omitted rather than forced.
- Sensitive information irrelevant to behavior inference should be excluded.

## Pair metrics

v0.9 keeps the v0.8.1 pair layer:

- **S — similarity**: overlap of final house distributions
- **C — coverage**: how many house styles are meaningfully represented across the pair
- **G — glue**: reciprocal support / repair / shared-creation events, with diminishing returns
- **F — friction**: differences across four dimension-level axes
- **fit**: `0.7*S + 0.3*C`
- **compatibility**: `round(0.45*fit + 0.35*G + 0.20*(100-F))`, clamped to 0–100

The four friction axes are:

- action ↔ analysis
- directness ↔ cooperation
- selective loyalty ↔ fairness
- strategy ↔ principle

## Confidence

- **High:** both sides blind + uncontaminated, AI has 3+ independent runs, each side has 8+ valid behavior items.
- **Medium:** both sides blind + uncontaminated, each side has 5+ valid behavior items.
- **Low:** either side was not blind / was contaminated, or either side has fewer than 5 valid behavior items.

Low confidence does **not** mean “bad match”; it means the measurement conditions were weaker.

## Calibration status

v0.9 is the first version intended to be easy enough to hand to other people, but the questionnaire is **not calibrated yet**. The next useful step is not more formula polishing: it is running the same questionnaire across several humans and several AI models, then checking for option / house bias and test-retest stability.

## Show-work mode

If requested, the ritual can show questionnaire / behavior / final house distributions, dimension scores, S/C/G/F/fit, compatibility inputs, matched archetype rules, and paraphrased evidence.

Hidden chain-of-thought, private system instructions, and raw private-memory dumps stay private.

## Still not science

SortLLM is an interaction-design / entertainment experiment, **not** a validated psychological assessment. Deterministic scoring means the same structured inputs produce the same numerical result; it does not make the construct scientifically validated.

## Disclaimer

This is an unofficial fan experiment inspired by fictional school-house sorting. It is not affiliated with or endorsed by Warner Bros., J.K. Rowling, or the Harry Potter franchise.

## License

MIT
