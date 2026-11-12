import json, re
from crewai import Crew, Process
from agents import organization_agent, workflow_agent, security_agent, integration_agent, workspace_agent
from tasks import organization_task, workflow_task, security_task, integration_task, workspace_task

def _parse_json(result):
    raw = str(result).strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.I)
    raw = re.sub(r"\s*```$", "", raw)
    start, end = raw.find("{"), raw.rfind("}")
    if start < 0 or end < start:
        raise ValueError("CrewAI did not return JSON. Please retry generation.")
    data = json.loads(raw[start:end + 1])
    if not isinstance(data, dict) or not isinstance(data.get("company"), dict):
        raise ValueError("The generated workspace configuration is incomplete. Please retry.")
    return data

def generate_workspace(user_requirement):
    crew = Crew(
        agents=[organization_agent, workflow_agent, security_agent, integration_agent, workspace_agent],
        tasks=[organization_task, workflow_task, security_task, integration_task, workspace_task],
        process=Process.sequential, verbose=False, memory=False)
    return _parse_json(crew.kickoff(inputs={"user_requirement": user_requirement}))
