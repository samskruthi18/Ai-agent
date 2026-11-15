from crewai import Task
from agents import organization_agent, workflow_agent, security_agent, integration_agent, workspace_agent

organization_task = Task(
    description="Use these onboarding answers: {user_requirement}. Define departments, teams, roles, reporting hierarchy and responsibilities. Preserve supplied facts, mark assumptions, and do not invent employee names.",
    expected_output="Structured organization design.", agent=organization_agent)
workflow_task = Task(
    description="Company onboarding answers: {user_requirement}. Design practical department workflows, task tracking, approvals, automation opportunities and notifications. Mark actions requiring human approval.",
    expected_output="Structured workflow design.", agent=workflow_agent)
security_task = Task(
    description="Company onboarding answers: {user_requirement}. Define login, role permissions, department data boundaries, confidential-data restrictions, audit events and approval controls. Follow least privilege; do not invent certifications.",
    expected_output="Security and access design.", agent=security_agent)
integration_task = Task(
    description="Company onboarding answers: {user_requirement}. List requested integrations, purpose and OAuth/API authorization needed. Every integration must be marked NOT CONNECTED until credentials and authorization are actually configured.",
    expected_output="Integration plan with truthful connection status.", agent=integration_agent)
workspace_task = Task(
    description='''Build the final workspace configuration using the onboarding answers and previous specialist outputs. Return ONLY valid JSON, no Markdown fences, with this schema:
{"company":{"name":"","industry":"","location":"","description":"","brand_color":"#2457A7"},"departments":[{"name":"","head_role":"","teams":[],"purpose":""}],"roles":[{"name":"CEO","department":"Leadership","level":"leadership"}],"dashboards":[{"role":"CEO","widgets":["Company overview"]}],"workflows":[{"name":"","department":"","steps":[],"approval_required":false}],"ai_assistants":[{"name":"","department":"","capabilities":[]}],"integrations":[{"name":"","purpose":"","status":"NOT CONNECTED","authorization_required":true}],"security":{"authentication":"Password login","principles":[]},"notifications":[]}
Include all supplied departments and relevant roles. Include CEO and Employee roles. Create a leadership dashboard, department-head dashboards, and one assistant per department. Use concise, useful widgets and features. Never claim integrations are connected. Do not invent facts absent from the onboarding answers. Company onboarding answers: {user_requirement}''',
    expected_output="Valid JSON workspace configuration matching the schema.", agent=workspace_agent,
    context=[organization_task, workflow_task, security_task, integration_task])
