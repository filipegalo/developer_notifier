from fastapi import APIRouter, HTTPException
from app.core.db import SessionDep
from app.crud.github import get_github_pull_requests
from app.models import GithubPullRequestResponse, ErrorResponse
import logging

router = APIRouter()

@router.get("/pull-requests", response_model=GithubPullRequestResponse, responses={
    200: {"description": "Successful response", "model": GithubPullRequestResponse},
    500: {"description": "Internal server error", "model": ErrorResponse},
    503: {"description": "GitHub API error", "model": ErrorResponse}
})
def read_github_pull_requests(db: SessionDep):
    try:
        pull_requests, count = get_github_pull_requests(db)
        return GithubPullRequestResponse(pull_requests=pull_requests, count=count)
    except RuntimeError as e:
        logging.error(f"GitHub API error: {e}")
        raise HTTPException(status_code=503, detail={"message": str(e)})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={"message": "Internal server error"})
