# ORBYTE AI Commercial Customer Message Workbench — v1.4

## Windows start (Python 3.14 supported)
1. Extract the entire ZIP to a normal folder. Do not run files from inside the ZIP preview.
2. Double-click `START_HERE.bat`.
3. The launcher prefers Python 3.14, then checks 3.13 and 3.12. It checks pip, installs the listed dependencies, and starts Streamlit.
4. If the browser does not open automatically, visit http://localhost:8501.
5. Keep the command window open while using the app. Press Ctrl+C to stop.

The first run requires internet access to install packages. This launcher does not create a virtual environment, so it avoids the previous broken `.venv`/missing-pip path.

## What this is
A local interactive prototype with dashboard, message workbench, account labels, AI reply drafting mock-up, send-safety simulation, and audit log export.

## Limits
Demo content and scores are simulated. No real WhatsApp/email/Discord connections, no external AI model API, and no real sending. A successful simulated send is not a real delivery. Audit logs are session-only.
