import json
import os
from pathlib import Path

import streamlit as st
import requests
from dotenv import load_dotenv

from local_llm import answer_workspace_question, generate_blueprint
from security import check_and_log, recent_events

load_dotenv(Path(__file__).with_name(".env"))
DEPARTMENTS = ["Software Development", "Vehicle Operations", "Customer Support", "Sales & Marketing", "Human Resources", "Finance", "IT Administration"]
DEFAULT_BASE_URL = os.getenv("LM_STUDIO_BASE_URL", "http://localhost:1234/v1")
DEFAULT_MODEL = os.getenv("LM_STUDIO_MODEL", "qwen3.5-9b")

st.set_page_config(page_title="AI Workspace Generator", page_icon="🏢", layout="wide")
st.title("🏢 AI Workspace Generator")
st.caption("Local Qwen prototype | Company intake → blueprint → role-based workspace")
st.info("Prototype mode: workspace content is generated locally. Connected apps, sign-in, email, payments, and deployments are simulated or disabled.")

with st.sidebar:
    st.subheader("Local AI")
    base_url = st.text_input("LM Studio server URL", DEFAULT_BASE_URL)
    model = st.text_input("Served model ID", DEFAULT_MODEL, help="Use the exact identifier shown in LM Studio's Local Server tab.")
    api_key = st.text_input("Local API key", "lm-studio", type="password")
    st.divider()
    st.caption("Start LM Studio's local server and load Qwen before generating a blueprint.")

if "blueprint" not in st.session_state:
    st.session_state.blueprint = None
if "approved_blueprint" not in st.session_state:
    st.session_state.approved_blueprint = False
if "assistant_answer" not in st.session_state:
    st.session_state.assistant_answer = None

intake_tab, blueprint_tab, workspace_tab, audit_tab = st.tabs(["1 · Company intake", "2 · Blueprint review", "3 · Team workspace", "4 · Security activity"])

with intake_tab:
    st.header("Tell us about the company")
    with st.form("company_intake"):
        company = st.text_input("Company name", "VoltFleet Technologies")
        industry = st.text_input("Industry", "Electric vehicle fleet management")
        business = st.text_area("What does the company do?", "A fictional EV fleet management SaaS startup.")
        employee_count = st.number_input("Number of employees", min_value=1, max_value=100000, value=55)
        departments = st.multiselect("Departments", DEPARTMENTS, default=DEPARTMENTS)
        workflows = st.text_area("Important workflows and pain points", "Support triage, fleet reports, reimbursement approval, product releases. Information is spread across email, spreadsheets, and team tools.")
        apps = st.multiselect("Existing tools (prototype records preferences only)", ["Google Drive", "Gmail", "Outlook", "Slack", "Microsoft Teams", "Jira", "GitHub", "PostgreSQL", "AWS"], default=["Google Drive", "Gmail", "Slack", "Jira", "GitHub"])
        confidential = st.multiselect("Restricted data areas", ["HR records", "Finance and payroll", "Source code and credentials", "Customer information", "Fleet operations"], default=["HR records", "Finance and payroll", "Source code and credentials", "Customer information"])
        approvals = st.multiselect("Actions requiring human approval", ["External email", "Payments", "Hiring decisions", "Employee record changes", "File deletion", "Production deployment", "Permission changes"], default=["External email", "Payments", "Hiring decisions", "Employee record changes", "File deletion", "Production deployment", "Permission changes"])
        submitted = st.form_submit_button("Generate workspace blueprint", type="primary", use_container_width=True)
    if submitted:
        intake = {"company": company, "industry": industry, "business": business, "employee_count": employee_count, "departments": departments, "workflows": workflows, "preferred_apps": apps, "restricted_data": confidential, "approval_required": approvals}
        try:
            with st.spinner("Qwen is drafting the company blueprint..."):
                st.session_state.blueprint = generate_blueprint(intake, base_url, model, api_key)
            st.session_state.approved_blueprint = False
            st.session_state.assistant_answer = None
            st.success("Blueprint generated. Review it in the next tab before activating the demo workspace.")
        except requests.exceptions.ConnectionError:
            st.error("Cannot reach LM Studio. Start its Local Server, load Qwen, and verify the URL and served model ID in the sidebar.")
        except requests.exceptions.Timeout:
            st.error("LM Studio timed out. Try again with a shorter workflow description or a smaller context setting.")
        except Exception as exc:
            st.error(f"Blueprint generation failed: {exc}")

with blueprint_tab:
    st.header("Blueprint review")
    if not st.session_state.blueprint:
        st.write("Complete the company intake first.")
    else:
        bp = st.session_state.blueprint
        intake = bp.get("intake", {})
        col1, col2, col3 = st.columns(3)
        col1.metric("Company", intake.get("company", "-"))
        col2.metric("Employees", intake.get("employee_count", "-"))
        col3.metric("Departments", len(intake.get("departments", [])))
        st.subheader("Executive summary")
        st.write(bp.get("executive_summary", ""))
        st.subheader("Department workspaces")
        for item in bp.get("department_workspaces", []):
            with st.expander(str(item.get("department", "Department")), expanded=False):
                st.write(item.get("purpose", ""))
                st.write("**Modules:**", ", ".join(map(str, item.get("modules", []))))
        left, right = st.columns(2)
        with left:
            st.markdown("**Shared tools**")
            st.write(", ".join(map(str, bp.get("shared_tools", []))))
            st.markdown("**Approval actions**")
            st.write(", ".join(map(str, bp.get("approval_actions", []))))
        with right:
            st.markdown("**Security notes**")
            for note in bp.get("security_notes", []):
                st.write("•", note)
        if st.button("Approve blueprint and activate demo workspace", type="primary"):
            st.session_state.approved_blueprint = True
            st.success("Blueprint approved for this demo session.")
        st.download_button("Download blueprint JSON", json.dumps(bp, indent=2, ensure_ascii=False), file_name="company-blueprint.json", mime="application/json")

with workspace_tab:
    st.header("Department workspace")
    if not st.session_state.approved_blueprint:
        st.warning("Review and approve the blueprint first.")
    else:
        bp = st.session_state.blueprint
        available_departments = bp.get("intake", {}).get("departments", [])
        if not available_departments:
            st.warning("No departments were selected in the intake.")
        else:
            selected_department = st.selectbox("Sign in to a demo workspace", available_departments)
            role = st.selectbox("Demo role", ["Employee", "Manager", "Admin"])
            view_scope = (role, selected_department)
            if st.session_state.get("last_view_scope") != view_scope:
                ok, reason = check_and_log(role, selected_department, "view_workspace", selected_department)
                st.session_state.last_view_scope = view_scope
            else:
                ok, reason = True, "User may view their own department workspace."
            if ok:
                st.success(reason)
                card1, card2 = st.columns(2)
                dept_info = next((x for x in bp.get("department_workspaces", []) if x.get("department") == selected_department), {})
                with card1:
                    st.subheader(f"{selected_department} assistant")
                    st.write(dept_info.get("purpose", "Department assistant for the selected team."))
                    q = st.text_input("Ask about this approved blueprint", key="workspace_question")
                    if st.button("Ask local Qwen", disabled=not q):
                        with st.spinner("Qwen is answering from the approved blueprint..."):
                            try:
                                # Only the selected department's generated details are sent to this assistant.
                                scoped_context = {"department": selected_department, "workspace": dept_info, "shared_tools": bp.get("shared_tools", [])}
                                answer = answer_workspace_question(q, scoped_context, selected_department, base_url, model, api_key)
                                st.session_state.assistant_answer = {"text": answer, "department": selected_department, "role": role}
                            except Exception as exc:
                                st.error(f"Assistant request failed: {exc}")
                    saved_answer = st.session_state.assistant_answer
                    if saved_answer and saved_answer.get("department") == selected_department and saved_answer.get("role") == role:
                        st.write(saved_answer.get("text", ""))
                with card2:
                    st.subheader("Team modules")
                    for module in dept_info.get("modules", ["Tasks", "Knowledge", "Team updates"]):
                        st.write("•", module)
                    st.subheader("Try a protected action")
                    action = st.selectbox("Action", ["Create a task", "Request an approval", "Approve a payment", "Change permissions", "Send external email"], key="protected_action")
                    if st.button("Check permissions"):
                        action_key = {"Create a task": "create_task", "Request an approval": "request_approval", "Approve a payment": "approve_payment", "Change permissions": "change_permissions", "Send external email": "send_external_email"}[action]
                        allowed, message = check_and_log(role, selected_department, action_key, selected_department)
                        (st.success if allowed else st.error)(message)
            else:
                st.error(reason)

with audit_tab:
    st.header("Security activity log")
    st.caption("Records demo workspace access and protected-action decisions in a local SQLite file.")
    events = recent_events()
    if events:
        st.dataframe(events, use_container_width=True, hide_index=True)
    else:
        st.caption("No security events yet.")

st.divider()
st.caption("Three-person prototype scope: onboarding and blueprint generation, department workspace preview, and role-aware security/audit. All integrations and effects remain simulated.")


