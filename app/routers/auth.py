from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter()

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(request: LoginRequest):
    if request.email == "rahul.goudar@gonagoor.com" and request.password == "password":
        return {"access_token": "fake-jwt-token", "token_type": "bearer", "user_email": request.email}
    raise HTTPException(status_code=401, detail="Invalid credentials")

@router.get("/me")
async def get_current_user():
    return {"email": "test@example.com", "id": 1, "status": "authenticated"}
