import json
import streamlit as st
from crew import generate_workspace
from storage import init_db, save_workspace, load_workspace
from workspace_builder import build_role_view
from assistant_chat import ask_workspace_assistant

st.set_page_config(page_title="AI Workspace", page_icon="✦", layout="wide")
init_db()

st.markdown("""
<style>
  .block-container {max-width: 1380px; padding-top: 1.5rem; padding-bottom: 3rem;}
  [data-testid="stSidebar"] {background: #111827;}
  [data-testid="stSidebar"] * {color: #f3f4f6;}
  .hero {padding: 1.35rem 1.5rem; border: 1px solid rgba(128,128,128,.25);
         border-radius: 16px; background: linear-gradient(120deg, rgba(70,105,180,.16), rgba(120,90,190,.08));}
  .muted {color: #8b93a1;}
  .app-card {border: 1px solid rgba(128,128,128,.25); border-radius: 14px;
             padding: 1rem; min-height: 115px;}
  .app-icon {font-size: 1.45rem;}
  div.stButton > button {border-radius: 10px; min-height: 2.55rem;}
  [data-testid="stChatMessage"] {border-radius: 14px;}
</style>
""", unsafe_allow_html=True)

STAGES = [
("Company Information", [("company_name","Company name","text"),("industry","Industry","text"),("location","Company location","text"),("employee_count","Number of employees","text"),("business_model","Business model","text"),("description","What does your company do?","area"),("objectives","Primary business objectives","area")]),
("Organizational Structure", [("departments","Departments and approximate employee counts","area"),("hierarchy","Reporting hierarchy","area"),("teams","Teams within each department","area")]),
("Roles & Responsibilities", [("roles","Employee roles and role counts","area"),("responsibilities","Responsibilities by role","area"),("access_rules","Who can access which information?","area"),("approvals","Actions that require approval","area")]),
("Business Workflows", [("daily_work","Describe daily operations","area"),("task_tracking","How are tasks assigned and tracked?","area"),("communication","How do departments communicate?","area"),("pain_points","Current problems or repetitive work","area"),("automation","What should be automated?","area")]),
("AI Requirements", [("ai_tasks","What should AI assistants help with?","area"),("department_ai","AI assistant needs by department","area"),("reports","Reports and summaries required","area"),("ai_permissions","What can AI do, and what needs human approval?","area")]),
("Applications & Integrations", [("email_calendar","Email and calendar applications","text"),("communication_apps","Communication applications","text"),("project_apps","Project management and development tools","text"),("storage_cloud","Documents, databases and cloud services","text"),("other_integrations","Other integrations and their purpose","area")]),
("Security & Access", [("department_spaces","How should department spaces be separated?","area"),("confidential_data","What information is confidential?","area"),("manager_access","What can managers view or approve?","area"),("security","Security requirements","area")]),
("Dashboard & Deployment", [("branding","Branding, logo and colors","text"),("layout","Preferred dashboard layout","text"),("analytics","What should leadership monitor?","area"),("notifications","Required notifications","area"),("day_one","Features required on day one","area"),("deployment","Preferred deployment (local/cloud)","text")])
]

VOLT_FLEET = {
"company_name":"VoltFleet Technologies Pvt. Ltd.","industry":"Electric Mobility, Fleet Management and SaaS","location":"Bengaluru, Karnataka, India","employee_count":"55","business_model":"B2B subscription-based SaaS","description":"Cloud-based fleet software for delivery companies operating electric vehicles. Live vehicle tracking, maintenance schedules, charging analytics and operational reporting.","objectives":"Improve software delivery; streamline operations; reduce repetitive work; improve productivity and interdepartmental communication; centralize company information; maintain secure access; scale efficiently.",
"departments":"Software Development: 15; Vehicle Operations: 10; Customer Support: 8; Sales & Marketing: 8; HR: 4; Finance: 4; IT Administration: 6.","hierarchy":"Founder/CEO → Department Heads → Team Leads/Managers → Employees and specialists.","teams":"Development: Frontend, Backend, QA, DevOps. Operations: Fleet Monitoring, Maintenance, Charging. Support: Technical, General, Escalations. Sales & Marketing: Sales, Marketing, Content. HR: Recruitment, Employee Relations. Finance: Accounting, Payments, Reporting. IT: Systems, Infrastructure, Security.",
"roles":"CEO; CTO; Operations Manager; Support Manager; Sales & Marketing Head; HR Manager; Finance Manager; IT Head; team leads; developers; QA; DevOps; fleet analysts; maintenance executives; support executives; sales and marketing executives; recruiters; accountants; system administrators; IT support engineers; employees.","responsibilities":"Department heads manage outcomes and approvals. Team leads assign and review work. Employees execute assigned tasks. IT maintains infrastructure and security.","access_rules":"CEO: company-wide overview. Department heads and managers: their department. Team leads: their teams. Employees: own tasks and authorized team resources. IT administrators monitor infrastructure and audit events without unrestricted access to HR/Finance confidential records.","approvals":"Payments: Finance Manager or CEO. Hiring: HR Manager and management. Employee record changes: HR Manager. Production deployments: CTO or engineering lead. Permission changes: IT Head. Sensitive deletion: designated manager.",
"daily_work":"Development builds and tests software; Operations monitors fleets and maintenance; Support resolves tickets; Sales & Marketing manages leads and campaigns; HR handles recruitment and employee matters; Finance handles invoices and payments; IT manages infrastructure and accounts.","task_tracking":"Managers and team leads assign tasks. Employees update progress. Managers review status. Current tracking uses spreadsheets, email and basic task boards.","communication":"Email, team chat, video calls and shared documents. Development coordinates with Operations; Support escalates product issues to Development; Sales coordinates customer requirements with Operations.","pain_points":"Scattered information, switching between apps, missed emails and tasks, manual reporting, difficulty finding department information and limited manager visibility.","automation":"Task tracking, report summaries, email triage, meeting summaries, employee requests, invoice/expense assistance, fleet summaries and document search.",
"ai_tasks":"Email drafting and summarization; document search; task assistance; reports; meeting summaries; department-specific support; repetitive workflow automation.","department_ai":"Development: coding and documentation. Operations: fleet and maintenance summaries. Support: ticket categorization and response drafts. Sales & Marketing: lead and campaign support. HR: recruitment and policy search. Finance: invoice and expense summaries. IT: troubleshooting and monitoring.","reports":"Daily, weekly and monthly summaries for relevant teams and managers.","ai_permissions":"AI may suggest and perform low-risk internal tasks. Human approval required for payments, hiring decisions, employee record changes, sensitive deletion, production deployments, permissions and policy-controlled external emails.",
"email_calendar":"Gmail, Outlook, Google Calendar, Outlook Calendar","communication_apps":"Slack, Microsoft Teams","project_apps":"Jira, GitHub, VS Code","storage_cloud":"Google Drive, PostgreSQL, AWS","other_integrations":"Connect only after the relevant OAuth/API credentials and authorization are provided.","department_spaces":"Each department has a dedicated workspace and only authorized shared company resources.","confidential_data":"HR: employee and recruitment records. Finance: payroll, bank and financial reports. Development: source code and credentials. Operations: fleet and maintenance data. Support: customer data and ticket history.","manager_access":"Managers view department progress, assign work, review activity and approve requests within their authority.","security":"Secure login, role-based access, MFA where configured, encryption in transit and at rest, tenant isolation, audit logs, session management, backups and recovery.","branding":"VoltFleet logo and brand colors; modern professional appearance.","layout":"Modern dashboard with sidebar navigation, department hubs and a central productivity workspace.","analytics":"Department performance, task progress, workflow completion, AI usage, automation time saved, system performance and integration health.","notifications":"New messages, task assignments and deadlines, meeting reminders, approval requests, department announcements and system alerts.","day_one":"Common productivity tools and role-specific department modules.","deployment":"Cloud-hosted environment"
}

if "answers" not in st.session_state: st.session_state.answers = {}
if "stage" not in st.session_state: st.session_state.stage = 0
if "page" not in st.session_state: st.session_state.page = "onboarding"
if "chat_history" not in st.session_state: st.session_state.chat_history = []

def load_volt_fleet():
    """Load the VoltFleet example into saved answers and all form widget states."""
    st.session_state.answers = VOLT_FLEET.copy()

    # Update widget values before Streamlit recreates the onboarding form.
    for key, value in VOLT_FLEET.items():
        st.session_state[f"input_{key}"] = value


def go(page):
    st.session_state.page = page
    st.rerun()

def onboarding():
    st.title("AI Workspace Generator")
    st.caption("Complete the eight stages to create a dedicated workspace for your company.")
    idx = st.session_state.stage
    st.progress((idx + 1) / len(STAGES), text=f"Stage {idx+1} of 8")
    title, fields = STAGES[idx]
    st.subheader(title)
    with st.form(f"stage_form_{idx}"):
        for key, label, kind in fields:
            current = st.session_state.answers.get(key, "")
            if kind == "area": st.text_area(label, value=current, key=f"input_{key}", height=100)
            else: st.text_input(label, value=current, key=f"input_{key}")
        c1, c2 = st.columns(2)
        with c1: back = st.form_submit_button("Back", disabled=idx == 0, use_container_width=True)
        with c2: forward = st.form_submit_button("Save & Continue" if idx < 7 else "Review answers", type="primary", use_container_width=True)
        if back or forward:
            for key, _, _ in fields: st.session_state.answers[key] = st.session_state.get(f"input_{key}", "")
            st.session_state.stage += -1 if back else (1 if idx < 7 else 0)
            if forward and idx == 7: go("review")
            st.rerun()
    with st.expander("Use the VoltFleet test case"):
        st.write("Loads the workshop's VoltFleet example into all eight stages. You can edit the answers.")
        st.button(
            "Load VoltFleet example",
            on_click=load_volt_fleet,
            use_container_width=True
        )

def review():
    st.title("Review your company details")
    for title, fields in STAGES:
        with st.expander(title):
            for key, label, _ in fields:
                st.markdown(f"**{label}**")
                st.write(st.session_state.answers.get(key) or "Not provided")
    a, b = st.columns(2)
    with a:
        if st.button("Back to onboarding"): st.session_state.stage = 7; go("onboarding")
    with b:
        if st.button("Generate My Workspace", type="primary", use_container_width=True): go("generating")

def generating():
    st.title("Creating your company workspace")
    st.write("Your CrewAI specialists are configuring the organization, workflows, security and dashboards.")
    try:
        with st.status("Generating your workspace…", expanded=True) as status:
            st.write("Analyzing company requirements")
            st.write("Designing departments and roles")
            st.write("Configuring workflows and approvals")
            st.write("Designing access and security rules")
            st.write("Planning integrations")
            config = generate_workspace(json.dumps(st.session_state.answers, ensure_ascii=False, indent=2))
            company = config.setdefault("company", {})
            company.setdefault("name", st.session_state.answers.get("company_name") or "My Company")
            company.setdefault("industry", st.session_state.answers.get("industry", ""))
            company.setdefault("location", st.session_state.answers.get("location", ""))
            roles = config.setdefault("roles", [])
            for default_role in [{"name":"CEO","department":"Leadership","level":"leadership"},{"name":"Employee","department":"General","level":"employee"}]:
                if not any(str(r.get("name","")).casefold() == default_role["name"].casefold() for r in roles):
                    roles.append(default_role)
            tenant_id = save_workspace(config)
            st.session_state.tenant_id = tenant_id
            status.update(label="Workspace created successfully", state="complete", expanded=False)
        go("login")
    except Exception as exc:
        st.error(f"Generation failed: {exc}")
        st.warning("Your onboarding answers are saved in this session. Retry without filling the form again.")
        if st.button("Retry generation", type="primary"): go("generating")
        if st.button("Return to review"): go("review")

def login():
    tenant = load_workspace(st.session_state.get("tenant_id"))
    if not tenant:
        st.error("No generated workspace found. Return to onboarding and generate it first.")
        if st.button("Back to onboarding"): go("onboarding")
        return
    company = tenant["config"].get("company", {})
    st.markdown("<div class='hero'>", unsafe_allow_html=True)
    st.title(company.get("name", tenant["company_name"]))
    st.subheader("Sign in to your company workspace")
    st.caption("Choose a demo role to preview its workspace.")
    roles = [r.get("name") for r in tenant["config"].get("roles", []) if r.get("name")]
    if not any(r.casefold() == "ceo" for r in roles): roles.insert(0, "CEO")
    if not any(r.casefold() == "employee" for r in roles): roles.append("Employee")
    role = st.selectbox("Continue as", list(dict.fromkeys(roles)))
    password = st.text_input("Password", type="password", placeholder="Demo password")
    if st.button("Sign in", type="primary", use_container_width=True):
        if password == "1234":
            st.session_state.logged_in_role = role
            st.session_state.chat_history = []
            go("workspace")
        else: st.error("Incorrect password.")
    st.caption("Demo password: 1234")
    st.markdown("</div>", unsafe_allow_html=True)

def setup_sidebar(company_name, role):
    with st.sidebar:
        st.markdown(f"## {company_name}")
        st.caption(f"Signed in as {role}")
        st.divider()
        nav = {
            "Home": "home",
            "AI Assistant": "assistant",
            "Mail": "mail",
            "Calendar": "calendar",
            "Documents": "documents",
            "Projects & Tasks": "tasks",
            "People": "people",
            "Departments": "departments",
            "Integrations": "integrations",
            "Settings": "settings"
        }
        current = st.session_state.get("workspace_section", "home")
        for label, key in nav.items():
            if st.button(("✦  " if key == "assistant" else "") + label,
                         key=f"nav_{key}", use_container_width=True,
                         type="primary" if current == key else "secondary"):
                st.session_state.workspace_section = key
                st.rerun()
        st.divider()
        if st.button("Log out", use_container_width=True):
            st.session_state.logged_in_role = None
            st.session_state.workspace_section = "home"
            go("login")


def home_page(tenant, role):
    config = tenant["config"]
    company = config.get("company", {})
    view = build_role_view(config, role)

    st.markdown(
        f"<div class='hero'><h1>{view['headline']}</h1>"
        f"<p class='muted'>{company.get('name', tenant['company_name'])} · {role}</p>"
        f"<p>{view['description']}</p></div>",
        unsafe_allow_html=True
    )

    st.write("")
    st.subheader("Your overview")
    focus_items = view["focus"]
    cols = st.columns(min(4, max(1, len(focus_items))))
    for index, item in enumerate(focus_items):
        with cols[index % len(cols)]:
            with st.container(border=True):
                st.markdown(f"**{item}**")
                st.caption("Workspace module")
                st.write("Ready to use")

    st.write("")
    st.subheader("Quick access")
    # These common applications stay available to every role.
    common_apps = [
        ("✉️", "Mail", "View and manage connected email", "mail"),
        ("📅", "Calendar", "Meetings and schedules", "calendar"),
        ("📁", "Documents", "Company files and knowledge", "documents"),
        ("✓", "Projects & Tasks", "Assignments and project progress", "tasks"),
        ("✦", "AI Assistant", "Ask, create, summarize and analyze", "assistant")
    ]
    cols = st.columns(3)
    for i, (icon_text, name, description, target) in enumerate(common_apps):
        with cols[i % 3]:
            with st.container(border=True):
                st.markdown(f"### {icon_text}  {name}")
                st.caption(description)
                if st.button(f"Open {name}", key=f"open_{target}", use_container_width=True):
                    st.session_state.workspace_section = target
                    st.rerun()

    st.write("")
    st.subheader("Your role-based workspace")
    department = view.get("department", {})
    if department:
        st.markdown(f"**{department.get('name', view['department_name'])}**")
        st.write(department.get("purpose", view["description"]))
        if department.get("teams"):
            st.caption("Teams: " + ", ".join(department["teams"]))
    elif role.strip().casefold() in {"ceo", "founder", "owner", "admin"}:
        st.write("You have a company-wide view across all departments.")
        dept_names = [d.get("name", "Department") for d in view.get("departments", [])]
        if dept_names:
            st.caption("Departments: " + " · ".join(dept_names))
    else:
        st.info("Your department details will appear here when configured.")

    st.markdown("**Suggested actions**")
    action_cols = st.columns(min(3, max(1, len(view["quick_actions"]))))
    for i, action in enumerate(view["quick_actions"]):
        with action_cols[i % len(action_cols)]:
            st.button(action, key=f"role_action_{i}", use_container_width=True, disabled=True)

    if role.strip().casefold() in {"ceo", "founder", "owner", "admin"}:
        with st.expander("Company departments"):
            for dept in view.get("departments", []):
                st.markdown(f"**{dept.get('name', 'Department')}**")
                st.caption(dept.get("purpose", "Department workspace"))
    with st.expander("Workspace setup details"):
        st.write(f"Industry: {company.get('industry', 'Not specified')}")
        st.write(f"Location: {company.get('location', 'Not specified')}")
        st.caption("Common apps stay consistent. Overview cards and department content change according to the selected role.")

def assistant_page(tenant, role):
    company = tenant["config"].get("company", {})
    st.title("✦  AI Assistant")
    st.caption(f"Your AI workspace assistant · {company.get('name', tenant['company_name'])}")
    st.markdown("<div class='hero'><h3>How can I help you today?</h3><p class='muted'>Ask questions, draft content, analyze information or plan your work.</p></div>", unsafe_allow_html=True)
    prompts = [
        "Summarize the company's objectives",
        "Draft a professional email to my team",
        "Create a weekly department report",
        "Suggest ways to automate repetitive work"
    ]
    cols = st.columns(2)
    for i, prompt in enumerate(prompts):
        with cols[i % 2]:
            if st.button(prompt, key=f"prompt_{i}", use_container_width=True):
                st.session_state.pending_prompt = prompt
    for message in st.session_state.chat_history:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])
    prompt = st.chat_input("Ask anything or tell me what to do...")
    if st.session_state.get("pending_prompt"):
        prompt = st.session_state.pop("pending_prompt")
    if prompt:
        st.session_state.chat_history.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                try:
                    answer = ask_workspace_assistant(
                        prompt=prompt,
                        company_config=tenant["config"],
                        role=role,
                        history=st.session_state.chat_history[-8:]
                    )
                except Exception as exc:
                    answer = f"I couldn't generate a response: {exc}"
                st.markdown(answer)
        st.session_state.chat_history.append({"role": "assistant", "content": answer})

def integrations_page(tenant):
    st.title("Integrations")
    st.caption("Connect the services your company already uses. Each connection needs authorization.")
    services = [
        ("Gmail", "Email and message access"), ("Yahoo Mail", "Email and message access"),
        ("Microsoft Outlook", "Email and calendar"), ("Google Calendar", "Meetings and schedules"),
        ("Outlook Calendar", "Meetings and schedules"), ("Slack", "Team communication"),
        ("Microsoft Teams", "Team communication"), ("Jira", "Projects and issue tracking"),
        ("GitHub", "Repositories and development activity"), ("Google Drive", "Company documents"),
        ("PostgreSQL", "Company database"), ("AWS", "Cloud infrastructure")
    ]
    cols = st.columns(2)
    for i, (name, purpose) in enumerate(services):
        with cols[i % 2]:
            with st.container(border=True):
                st.markdown(f"**{name}**")
                st.caption(purpose)
                st.caption("Status: NOT CONNECTED")
                st.button("Connection setup required", key=f"connect_{i}", disabled=True, use_container_width=True)
    st.info("The integration catalogue is displayed, but OAuth/API connection flows have not been implemented yet. No service is connected.")

def module_page(title, description, role):
    st.title(title)
    st.caption(description)
    if title == "Mail":
        st.info("Connect Gmail, Yahoo Mail or Outlook to read, search, summarize and draft messages here.")
    elif title == "Calendar":
        st.info("Connect Google Calendar or Outlook Calendar to view events, schedule meetings and manage availability.")
    elif title == "Documents":
        st.info("A company document library and search experience will live here. Connect Google Drive or upload files.")
    elif title == "Projects & Tasks":
        st.info("This area will hold task boards, assignments, deadlines, approvals and project updates.")
    elif title == "People":
        st.info("Employee accounts, teams, invitations and role administration will live here.")
    elif title == "Departments":
        st.info("Department-specific hubs, team resources, workflows and assistant shortcuts will live here.")
    elif title == "Settings":
        st.info("Company profile, branding, user access, security and workspace preferences will live here.")
    st.caption("This section is a UI foundation. Its live data and actions will be implemented with the relevant backend/integrations.")

def workspace():
    tenant = load_workspace(st.session_state.get("tenant_id"))
    if not tenant:
        st.error("Workspace not found.")
        if st.button("Return to onboarding"): go("onboarding")
        return
    role = st.session_state.get("logged_in_role")
    if not role: go("login"); return
    company_name = tenant.get("company_name", "Company")
    setup_sidebar(company_name, role)
    section = st.session_state.get("workspace_section", "home")
    if section == "home": home_page(tenant, role)
    elif section == "assistant": assistant_page(tenant, role)
    elif section == "integrations": integrations_page(tenant)
    else:
        titles = {
            "mail": ("Mail", "Your company email workspace"),
            "calendar": ("Calendar", "Your meetings and schedule"),
            "documents": ("Documents", "Company files and knowledge"),
            "tasks": ("Projects & Tasks", "Work assignments and project tracking"),
            "people": ("People", "Employees, teams and access"),
            "departments": ("Departments", "Your company's department spaces"),
            "settings": ("Settings", "Manage your company workspace")
        }
        title, desc = titles[section]
        module_page(title, desc, role)

if st.session_state.page == "onboarding": onboarding()
elif st.session_state.page == "review": review()
elif st.session_state.page == "generating": generating()
elif st.session_state.page == "login": login()
elif st.session_state.page == "workspace": workspace()
