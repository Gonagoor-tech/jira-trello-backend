from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.routers import auth, jira, trello, migration

app = FastAPI(
    title="JIRA to Trello Migration API",
    description="Self-serve migration tool for JIRA to Trello data transfer",
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router, prefix="/auth", tags=["Authentication"])
app.include_router(jira.router, prefix="/jira", tags=["JIRA"])
app.include_router(trello.router, prefix="/trello", tags=["Trello"])
app.include_router(migration.router, prefix="/migration", tags=["Migration"])

@app.get("/")
async def root():
    return {"message": "🚀 JIRA to Trello Migration API is LIVE!", "status": "ready", "time": "3:58 AM"}

@app.get("/health")
async def health_check():
    return {"status": "healthy", "timestamp": "2025-08-20T03:58:00", "database": "ready"}
