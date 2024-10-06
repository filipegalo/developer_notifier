from fastapi import APIRouter

router = APIRouter()

@router.get("/health", responses={
    200: {"description": "Successful response"},
    500: {"description": "Internal server error"},
})
def read_health():
    return {"status": "ok"}
