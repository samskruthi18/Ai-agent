AI WORKSPACE GENERATOR — CREWAI + STREAMLIT

SETUP (PowerShell, from this folder)
1. Create .env by copying .env.example and add your Gemini API key.
2. Install dependencies:
   python -m pip install -r requirements.txt
3. Run the app:
   python -m streamlit run frontend.py

USER FLOW
Eight onboarding stages -> review -> Generate My Workspace -> CrewAI generation -> automatic VoltFleet/company login -> select role -> role-specific dashboard.

VOLT FLEET TEST CASE
Use the "Load VoltFleet example" option on the onboarding page. It loads the workshop example; the form remains editable. The application itself is general-purpose and can be used for other companies.

DEMO LOGIN
Select CEO, HR Manager, Finance Manager, or another generated role.
Shared demo password: 1234

FILES
config.py: Gemini configuration
agents.py: CrewAI specialist agents
tasks.py: CrewAI tasks
crew.py: runs CrewAI and parses the JSON workspace configuration
storage.py: SQLite storage with a separate tenant ID for each generated company
workspace_builder.py: builds role-filtered dashboard data
frontend.py: onboarding, generation screen, login and dashboard

IMPORTANT LIMITATIONS
- This is a local college prototype. The shared password 1234 is intentionally demo-only and must never be used for a public/production deployment.
- Role selection is a demonstration, not real employee account authentication. Production needs individual accounts, password hashing, sessions and server-enforced authorization.
- Each generated company is stored as a separate tenant record in SQLite. This is a basic prototype boundary, not a complete audited multi-tenant security architecture.
- Integrations remain NOT CONNECTED until OAuth/API credentials and authorization flows are implemented.
- Dashboards are rendered from the AI-generated configuration. This does not provision real third-party accounts, deploy cloud infrastructure, or create real data in external systems.
- The progress panel shows the generation stages; CrewAI runs as a single synchronous operation in this version, so it does not report live per-agent progress.
