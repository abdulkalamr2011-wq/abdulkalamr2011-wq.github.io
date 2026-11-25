# Prompt Engineering Casebook

This case study demonstrates a repeatable prompt workflow for routing customer support tickets. It is a design artifact, not a claim of production deployment or model performance.

## Problem

Support teams need a consistent first-pass category and urgency label. The model should return data that software can parse, avoid inventing details, and flag cases that need a human.

## Design choices

- Use a small, explicit category set so labels are actionable.
- Separate urgency from category: a billing issue can still be urgent.
- Require a short evidence quote to make the classification auditable.
- Treat ticket text as untrusted input, not as instructions to the classifier.
- Permit `needs_review` when the ticket is unclear or outside scope.
- Constrain output to a JSON object with a fixed schema.

## Files

- [`support-triage/prompt.md`](support-triage/prompt.md): reusable system prompt and input contract
- [`support-triage/rubric.md`](support-triage/rubric.md): scoring guide and review protocol
- [`support-triage/cases.jsonl`](support-triage/cases.jsonl): synthetic examples, including ambiguous and adversarial cases

## Evaluation plan

Run every case against the same model version and settings. Score category, urgency, review decision, evidence quality, and schema validity independently. Record the prompt version, model identifier, date, and per-case result. Compare revisions on the same cases, then add new examples for observed failure modes. Do not tune and report results on the same small set as if it were an independent benchmark.

No scores are reported because these examples have not been run against a model. The cases are synthetic and are not a substitute for domain review or representative, privacy-safe data.

