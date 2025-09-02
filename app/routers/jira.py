from fastapi import APIRouter
from app.services import jira_service

router = APIRouter(prefix="/jira", tags=["JIRA"])

@router.get("/projects")
async def get_jira_projects():
    return await jira_service.fetch_jira_projects()

@router.get("/issues/{project_key}")
async def get_jira_issues(project_key: str):
    return await jira_service.fetch_jira_issues(project_key)

@router.post("/test-connection")
async def test_jira_connection():
    try:
        projects = await jira_service.fetch_jira_projects()
        return {"status": "success", "project_count": projects.get("total", 0)}
    except Exception as e:
        return {"status": "error", "message": str(e)}
