# crm.py
from datetime import datetime
from uuid import uuid4

# In-memory CRM (replace with DB in Phase 2)
projects_db = {}

def create_project(data: dict, user: dict):
    project_id = str(uuid4())
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    
    project = {
        "id": project_id,
        "created_by": user["email"],
        "business_name": data.get("name"),
        "contact_email": data.get("email"),
        "status": "demo_sent",
        "theme": data.get("theme", "minimalist"),
        "preview_url": data.get("preview_url"),
        "deposit_paid": False,
        "final_sent": False,
        "created_at": now
    }

    projects_db[project_id] = project
    return {"message": "Project created", "project": project}

def get_projects(user: dict):
    return [p for p in projects_db.values() if p["created_by"] == user["email"]]

def update_project_status(project_id: str, status: str, user: dict):
    project = projects_db.get(project_id)
    if not project:
        return {"error": "Project not found"}
    
    project["status"] = status
    if status == "deposit_received":
        project["deposit_paid"] = True
    if status == "final_delivered":
        project["final_sent"] = True

    return {"message": "Project updated", "project": project}
