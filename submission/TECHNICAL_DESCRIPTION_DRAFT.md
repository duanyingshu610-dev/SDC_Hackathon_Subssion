# Technical Description — Draft

## Components

- `src/utils.py` contains deterministic role and keyword scoring.
- `src/main.py` validates one normalized message and returns its tier, scores, risk, and human-review requirement.
- `runpod/handler.py` adapts a RunPod job envelope to the triage function.
- `web/Sample/` and `web/Empty/` are standalone HTML demonstrations. `web/Workbench/` is a separate Streamlit prototype.
- `data/data_handoff/` contains synthetic normalized messages and reference files.

## Input and output

Input: a JSON object containing `message_id`, `platform`, `sender_role`, and `content`; optional fields include `is_starred` and `manual_bonus`.

Output: message identity, computed importance/urgency/total scores, P1–P4 tier, risk level, `requires_human_review`, and `sending_enabled: false`.

## Safety and limits

The handler only classifies a message. It does not send, approve, or persist any message. Scores are explainable keyword rules and require human review; they are not validated model accuracy claims. All example data is synthetic.
