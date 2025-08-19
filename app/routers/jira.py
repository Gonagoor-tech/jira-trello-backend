from fastapi import APIRouter

router = APIRouter()

@router.get("/projects")
async def get_jira_projects():
    return [
        {"key": "TEST", "name": "Test Project", "id": "10001"},
        {"key": "DEMO", "name": "Demo Project", "id": "10002"}
    ]

@router.post("/test-connection")
async def test_jira_connection():
    return {"status": "success", "message": "JIRA connection successful"}

@router.get("/issues/{project_key}")
async def get_jira_issues(project_key: str):
    return {
        "project": project_key,
        "total": 25,
        "issues": [{"key": f"{project_key}-1", "summary": "Sample issue", "status": "To Do"}]
    }
