import json
from crewai import Agent, Task, Crew, Process
from config import llm

def ask_workspace_assistant(prompt, company_config, role, history=None):
    company_name = (company_config.get("company") or {}).get("name", "the company")
    context = {
        "company": company_config.get("company", {}),
        "departments": company_config.get("departments", []),
        "workflows": company_config.get("workflows", []),
        "integrations": company_config.get("integrations", []),
        "notifications": company_config.get("notifications", [])
    }
    agent = Agent(
        role="Company Workspace AI Assistant",
        goal="Help the signed-in employee with company work, explanations, drafting, planning and analysis.",
        backstory="You are a practical workplace copilot. You use only the company context provided and clearly state when information or an integration is unavailable.",
        llm=llm,
        verbose=False,
        allow_delegation=False
    )
    task = Task(
        description=f"""
You are assisting a user signed in as: {role}
Company: {company_name}

Company workspace context:
{json.dumps(context, ensure_ascii=False)}

Recent conversation:
{json.dumps(history or [], ensure_ascii=False)}

User request:
{prompt}

Instructions:
- Give a useful, direct answer.
- Tailor the answer to the user's role and company context.
- Do not claim to have read emails, files, calendars, databases or external services.
- Do not claim to have performed actions or connected integrations.
- If the user asks for an action requiring an external service, explain that the integration and authorization must be implemented first.
- For drafts, provide a complete draft the user can copy.
""",
        expected_output="A clear and useful workplace assistant response.",
        agent=agent
    )
    result = Crew(agents=[agent], tasks=[task], process=Process.sequential, verbose=False).kickoff()
    return str(result)
