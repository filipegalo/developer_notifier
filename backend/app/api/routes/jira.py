from fastapi import APIRouter, HTTPException

from app.core.db import SessionDep
from app.crud.jira import get_jira_issues
from app.models import JiraIssueResponse, ErrorResponse
import logging

router = APIRouter()

@router.get("/issues", response_model=JiraIssueResponse, responses={
    200: {"description": "Successful response", "model": JiraIssueResponse},
    500: {"description": "Internal server error", "model": ErrorResponse},
    503: {"description": "Jira API error", "model": ErrorResponse}
})
def read_jira_issues(db: SessionDep):
    try:
        issues, count = get_jira_issues(db)
        return JiraIssueResponse(issues=issues, count=count)
    except HTTPException as e:
        logging.error(f"Jira API error: {e.detail}")
        raise HTTPException(status_code=e.status_code, detail={"message": str(e.detail)})
    except Exception as e:
        logging.error(f"Unexpected error: {e}")
        raise HTTPException(status_code=500, detail={"message": "Internal server error"})