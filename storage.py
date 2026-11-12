import json, sqlite3, uuid
from pathlib import Path
DB_PATH = Path(__file__).with_name("workspaces.db")

def init_db():
    with sqlite3.connect(DB_PATH) as db:
        db.execute("CREATE TABLE IF NOT EXISTS workspaces (tenant_id TEXT PRIMARY KEY, company_name TEXT NOT NULL, config_json TEXT NOT NULL, created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP)")

def save_workspace(config):
    tenant_id = str(uuid.uuid4())
    company = config.get("company", {})
    name = company.get("name") or "My Company"
    with sqlite3.connect(DB_PATH) as db:
        db.execute("INSERT INTO workspaces (tenant_id, company_name, config_json) VALUES (?, ?, ?)", (tenant_id, name, json.dumps(config)))
    return tenant_id

def load_workspace(tenant_id):
    if not tenant_id: return None
    with sqlite3.connect(DB_PATH) as db:
        row = db.execute("SELECT tenant_id, company_name, config_json FROM workspaces WHERE tenant_id=?", (tenant_id,)).fetchone()
    if not row: return None
    return {"tenant_id": row[0], "company_name": row[1], "config": json.loads(row[2])}
