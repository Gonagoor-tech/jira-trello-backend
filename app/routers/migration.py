from fastapi import APIRouter
import uuid

router = APIRouter()

@router.post("/start")
async def start_migration():
    job_id = str(uuid.uuid4())
    return {"job_id": job_id, "status": "started", "message": "Migration initiated"}

@router.get("/status/{job_id}")
async def get_migration_status(job_id: str):
    return {
        "job_id": job_id,
        "status": "running",
        "progress": 45,
        "total_issues": 100,
        "processed_issues": 45,
        "errors": []
    }

@router.get("/history")
async def get_migration_history():
    return [{"job_id": "sample-job-1", "status": "completed", "created_at": "2025-08-20T02:00:00"}]
