from fastapi import FastAPI
import os
import pandas as pd
import uuid
import time
import threading

app = FastAPI()

# In-memory store for migration jobs
migration_jobs = {}

# ===== CSV Paths =====
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
jira_csv_path = os.path.join(BASE_DIR, "mock_jira_issues.csv")
trello_csv_path = os.path.join(BASE_DIR, "mock_trello_cards.csv")

# ===== Load CSVs safely =====
try:
    jira_df = pd.read_csv(jira_csv_path)
except Exception as e:
    print(f"Error loading Jira CSV: {e}")
    jira_df = pd.DataFrame()  # empty DataFrame to prevent crashes

try:
    trello_df = pd.read_csv(trello_csv_path)
except Exception as e:
    print(f"Error loading Trello CSV: {e}")
    trello_df = pd.DataFrame()  # empty DataFrame

# ===== Transform Jira issue to Trello-ready format =====
def transform_jira_to_trello(issue):
    return {
        "name": issue.get("summary", "No Summary"),
        "desc": issue.get("description", ""),
        "labels": [issue.get("custom_field_1", "")],
        "members": [issue.get("assignee", "")],
        "list_name": issue.get("status", "To Do"),
    }

# ===== Worker function to simulate migration =====
def migration_worker(job_id, trello_ready):
    total_issues = len(trello_ready)
    processed_issues = 0
    errors = []

    for card in trello_ready:
        try:
            print(f"Creating Trello card: {card['name']}")
            processed_issues += 1
            time.sleep(0.1)  # simulate processing
        except Exception as e:
            errors.append({"card": card.get("name", "unknown"), "error": str(e)})

        # Update job progress
        migration_jobs[job_id]["progress"] = int((processed_issues / total_issues) * 100)
        migration_jobs[job_id]["processed_issues"] = processed_issues
        migration_jobs[job_id]["errors"] = errors

    migration_jobs[job_id]["status"] = "completed"

# ===== Endpoint to start migration =====
@app.post("/start")
async def start_migration():
    if jira_df.empty:
        return {"error": "Jira CSV is empty or missing"}

    job_id = str(uuid.uuid4())
    trello_ready = [transform_jira_to_trello(row) for _, row in jira_df.iterrows()]

    migration_jobs[job_id] = {
        "status": "running",
        "progress": 0,
        "total_issues": len(trello_ready),
        "processed_issues": 0,
        "errors": []
    }

    # Run migration in a separate thread
    thread = threading.Thread(target=migration_worker, args=(job_id, trello_ready))
    thread.start()

    return {"job_id": job_id, "status": "started", "message": "Migration initiated"}

# ===== Endpoint to check migration status =====
@app.get("/status/{job_id}")
async def get_migration_status(job_id: str):
    job = migration_jobs.get(job_id)
    if not job:
        return {"error": "Job ID not found"}
    return job
