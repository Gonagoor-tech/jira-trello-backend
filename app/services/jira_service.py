import httpx
import os
from fastapi import HTTPException

JIRA_BASE_URL = os.getenv("JIRA_BASE_URL")
JIRA_EMAIL = os.getenv("JIRA_EMAIL")
JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")

if not all([JIRA_BASE_URL, JIRA_EMAIL, JIRA_API_TOKEN]):
    raise RuntimeError("❌ Missing Jira configuration in .env file")

auth = (JIRA_EMAIL, JIRA_API_TOKEN)

async def fetch_jira_projects():
    async with httpx.AsyncClient() as client:
        resp = await client.get(f"{JIRA_BASE_URL}/rest/api/3/project/search", auth=auth)
        resp.raise_for_status()
        return resp.json()

async def fetch_jira_issues(project_key: str):
    async with httpx.AsyncClient() as client:
        url = f"{JIRA_BASE_URL}/rest/api/3/search?jql=project={project_key}"
        resp = await client.get(url, auth=auth)
        if resp.status_code != 200:
            raise HTTPException(status_code=resp.status_code, detail=resp.text)
        return resp.json()
