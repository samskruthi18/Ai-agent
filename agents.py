from crewai import Agent
from config import llm

organization_agent = Agent(role="Organization Architect", goal="Design departments, teams, roles and reporting hierarchy from the supplied company onboarding answers.", backstory="You design practical organizational structures for companies in any industry.", llm=llm, verbose=False, allow_delegation=False)
workflow_agent = Agent(role="Workflow Specialist", goal="Design useful business workflows, tasks, approvals and notifications.", backstory="You convert business processes into practical application modules.", llm=llm, verbose=False, allow_delegation=False)
security_agent = Agent(role="Security Architect", goal="Define role-based permissions, data boundaries and sensitive-action approvals.", backstory="You design least-privilege access for multi-department applications.", llm=llm, verbose=False, allow_delegation=False)
integration_agent = Agent(role="Integration Specialist", goal="Identify requested integrations and the authorization each requires.", backstory="You plan realistic integrations and never claim a service is connected without credentials.", llm=llm, verbose=False, allow_delegation=False)
workspace_agent = Agent(role="Workspace Configuration Architect", goal="Combine specialist findings into valid JSON that can be rendered as a company workspace.", backstory="You create structured dashboard and module configurations for business applications.", llm=llm, verbose=False, allow_delegation=False)
