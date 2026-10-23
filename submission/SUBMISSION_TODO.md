# Submission To-do

## Must complete with the team

- Replace `[Official Team Name]` in the root `README.md` and rename the project folder to the exact official team-name format.
- Obtain the complete template and confirm the exact four required submission filenames, formats, and Replit/RunPod deliverables; the screenshots truncate the names.
- Replace the placeholder `LICENSE` with the team's approved license, or confirm the template's required licensing text.
- Review and approve the draft documents under `submission/`; add the required final PDFs, links, and evidence using the official filenames.
- Confirm whether RunPod deployment is mandatory. The handler and Dockerfile are prepared, but no image has been published and no endpoint has been deployed.
- Decide whether judges expect an actual ML model. The current handler uses deterministic keyword rules, not a trained model; update implementation and claims if an ML model is required.
- Run `python -m unittest discover -s tests -v` from the project root and fix any failures before delivery.

## Prepared

- Template folders: `runpod/`, `src/`, `submission/`, `tests/`.
- Rule-based triage entry point and RunPod adapter.
- Sample, Empty, and Streamlit prototypes plus synthetic handoff data under `src/`.
- Root `requirements.txt`, `LICENSE`, and README; `runpod/Dockerfile`; tests in `tests/`.

The prior source-layout backup is kept outside this project folder and is not part of the submission.
