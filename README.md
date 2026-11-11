# AI Workspace Generator — Local Qwen MVP

A small working model of the submitted product idea: collect company requirements, ask a local LM Studio/Qwen model for a company blueprint, let an admin review and approve it, then preview a department workspace under role-aware checks.

The prototype intentionally does **not** connect to Google, Microsoft, Slack, GitHub, Jira, AWS, databases, or real employee data. Actions such as sending mail, approving payments, changing permissions, hiring, deleting files, and deployments are disabled. All data entered should be fictional.

## Start in Windows PowerShell

From this project folder:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
Copy-Item .env.example .env
streamlit run app.py
```

If you are currently at `C:\Windows\System32`, first change to the full project path:

```powershell
cd "C:\Users\MUEEZ AHMED\Documents\Codex\2026-11-10\referenced-chatgpt-conversation-this-is-an\outputs\ai-workspace-generator-mvp"
```

In LM Studio, load Qwen and start the Local Server. In the app sidebar, set the server URL and the exact served model ID shown by LM Studio. The default URL is `http://localhost:1234/v1`.

## Demo sequence

1. Enter fictional company information, choose departments, tools, restricted data areas, and approval-required actions.
2. Select **Generate workspace blueprint**. Local Qwen writes the summary and recommended team modules as JSON.
3. Review the result, download the blueprint if useful, and approve it for the demo session.
4. Select a department and demo role. Ask the department assistant about the approved blueprint.
5. Try a routine task or a protected action. The policy check records allow/deny decisions in a local SQLite audit log.
6. Open Security activity to review events.

## Build split for three people

| Team member | Owns | Integration contract |
|---|---|---|
| **Person 1 — Onboarding and interface** | `app.py` intake form, blueprint review, department workspace screens | Produces a validated intake dictionary and displays the blueprint / workspace states. |
| **Person 2 — Local AI and blueprint** | `local_llm.py`, prompt shape, JSON extraction and validation | Accepts intake plus LM Studio settings; returns a bounded blueprint dictionary or clear error. Never enforces access permissions. |
| **Person 3 — Security and audit** | `security.py`, permission decisions, SQLite event log, demo scenarios | Exposes `check_and_log(role, department, action, target_department)` and `recent_events()`. All sensitive actions default to deny. |

Work in parallel after agreeing on the intake and blueprint JSON fields. Person 1 integrates the modules and owns the end-to-end demo. Each person contributes one normal-use and one denied-action scenario. Keep changes within the owned files until integration.

## Prototype limits

The role selector is a demonstration control, not authentication. The SQLite database is local and not tamper-proof. Blueprint generation is advisory and requires human review. No real deployment or integration is performed. This is a classroom prototype, not a production security system.
