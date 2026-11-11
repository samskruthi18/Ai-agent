import json
import sqlite3
from datetime import datetime, timezone
from pathlib import Path

DB_PATH = Path(__file__).with_name("workspace_audit.db")


def _connect():
    conn = sqlite3.connect(DB_PATH)
    conn.execute("""CREATE TABLE IF NOT EXISTS audit (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp_utc TEXT NOT NULL,
        user_role TEXT NOT NULL,
        department TEXT NOT NULL,
        action TEXT NOT NULL,
        target_department TEXT NOT NULL,
        decision TEXT NOT NULL,
        reason TEXT NOT NULL
    )""")
    conn.commit()
    return conn


def check_and_log(role: str, department: str, action: str, target_department: str) -> tuple[bool, str]:
    role, department = role.lower(), department.strip()
    allowed = False
    reason = "Action is outside the current role permissions."
    if action == "view_workspace" and target_department == department:
        allowed, reason = True, "User may view their own department workspace."
    elif action == "view_workspace" and role == "admin" and target_department in {"Company Overview", department}:
        allowed, reason = True, "Admin may view workspace metadata."
    elif action == "create_task" and target_department == department and role in {"employee", "manager", "admin"}:
        allowed, reason = True, "Task creation is allowed in the user's own department."
    elif action == "request_approval" and target_department == department and role in {"employee", "manager", "admin"}:
        allowed, reason = True, "Request may be submitted for human review."
    elif action in {"approve_payment", "change_permissions", "delete_company_data", "send_external_email"}:
        reason = "Sensitive action is not enabled in this prototype; human approval and real identity controls are not implemented."
    decision = "allow" if allowed else "deny"
    with _connect() as conn:
        conn.execute(
            "INSERT INTO audit(timestamp_utc,user_role,department,action,target_department,decision,reason) VALUES(?,?,?,?,?,?,?)",
            (datetime.now(timezone.utc).isoformat(timespec="seconds"), role, department, action, target_department, decision, reason),
        )
    return allowed, reason


def recent_events(limit: int = 100) -> list[dict]:
    with _connect() as conn:
        rows = conn.execute("SELECT id,timestamp_utc,user_role,department,action,target_department,decision,reason FROM audit ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    return [dict(id=r[0], timestamp_utc=r[1], user_role=r[2], department=r[3], action=r[4], target_department=r[5], decision=r[6], reason=r[7]) for r in rows]
