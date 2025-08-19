from fastapi import APIRouter

router = APIRouter()

@router.get("/boards")
async def get_trello_boards():
    return [
        {"id": "board1", "name": "Migration Test Board", "url": "https://trello.com/b/test"},
        {"id": "board2", "name": "Development Board", "url": "https://trello.com/b/dev"}
    ]

@router.post("/test-connection")
async def test_trello_connection():
    return {"status": "success", "message": "Trello connection successful"}

@router.post("/cards")
async def create_trello_cards():
    return {"status": "success", "cards_created": 0, "message": "Ready to create cards"}
