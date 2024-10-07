from fastapi import APIRouter, HTTPException
from app.core.db import SessionDep
from app.crud.gitlab import get_gitlab_merge_requests
from app.models import GitlabMergeRequestResponse, ErrorResponse
import logging

router = APIRouter()

@router.get("/merge-requests", response_model=GitlabMergeRequestResponse, responses={
    200: {"description": "Successful response", "model": GitlabMergeRequestResponse},
    500: {"description": "Internal server error", "model": ErrorResponse},
    503: {"description": "GitLab API error", "model": ErrorResponse}
})
def read_gitlab_merge_requests(db: SessionDep):
    try:
        merge_requests, count = get_gitlab_merge_requests(db)
        return GitlabMergeRequestResponse(merge_requests=merge_requests, count=count)
    except RuntimeError as e:
        logging.error(f"GitLab API error: {e}")
        raise HTTPException(status_code=503, detail={"message": str(e)})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={"message": "Internal server error"})
