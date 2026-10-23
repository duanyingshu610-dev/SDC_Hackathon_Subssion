# Byte Force — Orbyte MessagePilot

## Team Information

| Field | Details |
|---|---|
| **Team Name** | Byte Force |
| **Team Domain** | Domain 2 |
| **SDG Track (1–17)** | **To confirm:** add the assigned SDG number and official name |
| **Team Leader** | Huang Jinyin |
| **University** | Xiamen University Malaysia |
| **Number of Members** | 5|

## Links

| Resource | Link / Status |
|---|---|
| **GitHub Repository** | https://github.com/duanyingshu610-dev/SDC_Hackathon_Subssion |
| **Replit Project** | Not used |
| **Live Demo** | [Open the Streamlit demo](https://sdchackathonsubssion-f3ojkr2fxgrc96alvkgttr.streamlit.app/) — deployment/access has not yet been confirmed |
| **RunPod Endpoint** | Not deployed |
| **Slide Deck** | https://docs.google.com/presentation/d/1ONOJE0iE_Gdzn94LzSrXGfR9inUiAhtO/edit?usp=sharing&ouid=107510550339817740715&rtpof=true&sd=true |
| **Pitching / Demo Video** | https://youtu.be/ZSBHZQQ-LNk?feature=shared |

## Overview

Orbyte MessagePilot is a prototype for helping customer-facing teams review incoming messages, identify messages that may need prompt attention, and prepare reply drafts for human review. It demonstrates a message-triage workflow using synthetic examples.

The prototype is for demonstration and training. It does not connect to real messaging accounts, send messages, or provide production monitoring.

## Features

- Classifies example messages using transparent, hand-written keyword and sender-role rules.
- Highlights urgency and risk indicators to support human review.
- Demonstrates draft review and approval flows in the browser prototypes.
- Includes a separate local SQLite workflow demo.
- Uses synthetic sample messages; no real customer messages are included.

## Project Structure

```text
runpod/       RunPod handler and container recipe (not currently deployed)
src/          Triage logic, local workflow, sample data, and web interfaces
tests/        Unit test files
submission/   Competition submission materials and checklist
README.md     Project overview and setup instructions
requirements.txt
LICENSE
```

## Run the Project

### Browser prototypes

Open `src/web/Sample/index.html` for the version with simulated inbox data, or `src/web/Empty/index.html` for the version without preloaded simulated messages. These are local training simulations and do not send messages.

### Streamlit workbench

On Windows, run `src/web/Workbench/START_HERE.bat` to start the local Streamlit interface. The first launch may need internet access to install the dependencies listed in `requirements.txt`.

### Launch menu and local backend demos

Run `src/START_HERE.bat` for the project launch menu. From the project root, the rule-based triage can also be run with:

```bash
python -c "from src.main import triage_message; print(triage_message({'message_id':'MSG-1','platform':'email','sender_role':'customer','content':'No rush, please share service hours.'}))"
```

Run the local SQLite workflow demo with:

```bash
python src/run_demo.py
```

## Technical Approach and Scope

The triage logic uses deterministic, hand-written rules. The project does not currently embed, train, or call an AI model or external AI API. The Streamlit interface, browser simulations, rule-based triage code, and SQLite demo are prototype components; they are not connected as a deployed end-to-end production service. The RunPod files are deployment scaffolding only, and no RunPod endpoint is active.

All supplied message examples are synthetic. A human should review any priority classification or reply draft before acting on it. The prototype does not send messages to email, WhatsApp, Discord, or other services.

## Submission Items to Complete

Before submitting, add the confirmed SDG track, team leader, university, member count, and public GitHub repository URL. Add the slide deck and pitching/demo video links when available. Verify that the Streamlit demo is publicly accessible before presenting it as a working live demo, and replace the placeholder license with the license chosen by the team.
