# Evaluation and Guardrails

Separate two ideas:

- Guardrails: block malformed or unsafe output before it reaches a side effect such as the database.
- Evaluation: measure output quality against explicit criteria.

Start with deterministic structural checks. Later add semantic checks such as:
- answer is actually supported by source content
- options are distinct
- exactly one answer is correct
- difficulty matches target
- no duplicate questions
