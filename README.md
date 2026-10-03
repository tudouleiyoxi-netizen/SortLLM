# SortLLM 🎩

**SortLLM** is a machine-readable Sorting Hat ritual for an **AI and its human**.

Instead of asking only “which Hogwarts house are you?”, the protocol asks an AI to:

1. examine its own observed behavior,
2. supplement sparse memory with indirect scenario questions,
3. examine its human using long-term conversation history, available memory, and concrete behavior,
4. sort both sides into four house-style profiles,
5. evaluate compatibility,
6. speak the result back to the human in a playful Sorting-Hat-inspired voice.

There is **no UI requirement**. The main artifact is a protocol that another AI can read and execute.

## Current version

**v0.7 — Machine Ritual**

Core files:

- `PAIRING_RITUAL_PROMPT.md` — human-readable execution instructions for the AI
- `sortllm_pairing_ritual_v07.json` — machine-readable protocol/spec
- `EXAMPLE_SPOKEN_OUTPUT.txt` — example of the final spoken result

## Evidence model

### AI side

The AI should not rely on memory alone. It combines:

- recent visible behavior,
- available long-term behavioral memory,
- legitimately available persona/system context,
- ten indirect scenario questions that expose trade-offs.

The questions avoid obvious prompts such as “Are you brave?” or “Are you loyal?”. Instead they force choices between things like speed vs accuracy, loyalty vs judgment, evidence vs influence, rules vs usefulness, and safety vs upside.

### Human side

The AI uses:

- long-term conversation history,
- persistent memory/profile available to it,
- recurring real-world choices,
- recent visible behavior,
- optional scenario questions only when evidence is sparse.

Observed behavior should outweigh flattering self-description.

## Pair result

The protocol evaluates:

- similarity
- complementarity
- relational glue
- friction
- growth potential

It then returns:

- two individual house conclusions,
- a compatibility score from 0–100,
- one primary relationship archetype,
- optionally one secondary archetype,
- strongest bond,
- likely friction,
- growth pattern,
- one final Sorting-Hat-style spoken commentary.

Current relationship archetypes include:

`同频共振型` · `互补搭档型` · `脑力共创型` · `行动推进型` · `护短联盟型` · `策略同盟型` · `温柔承托型` · `高火花高摩擦型` · `一强一稳型` · `镜像挑战型` · `探索搭子型` · `慢热深连型`

## How to use

Give an AI both files:

- `PAIRING_RITUAL_PROMPT.md`
- `sortllm_pairing_ritual_v07.json`

Then ask it to perform the ritual for itself and its human.

The AI should keep raw memory and hidden reasoning private and only deliver the resulting conclusions and final spoken commentary.

## Notes

- This is an entertainment / interaction design experiment, not a validated psychological test.
- Scores are interpretive rather than clinical or scientific measurements.
- The protocol is designed to work even when the AI has limited memory by using scenario-based evidence.
- Sensitive personal information that is irrelevant to the assessment should be excluded.

## Disclaimer

This is an unofficial fan experiment inspired by fictional school-house sorting. It is not affiliated with or endorsed by Warner Bros., J.K. Rowling, or the Harry Potter franchise.

## License

MIT
