from typing import List, Tuple
import requests
from sqlalchemy.orm import Session
from app.crud.settings import get_settings_value
from app.models import JiraIssue
from datetime import datetime
import base64
from fastapi import HTTPException
from requests.exceptions import RequestException
from sqlalchemy.exc import SQLAlchemyError

def get_jira_issues(db: Session) -> Tuple[List[JiraIssue], int]:
    try:
        url = f"{get_settings_value(db, 'jira_api_url')}search"
        
        auth_string = f"{get_settings_value(db, 'jira_api_email')}:{get_settings_value(db, 'jira_api_key')}"
        encoded_auth = base64.b64encode(auth_string.encode()).decode()
        
        headers = {
            "Authorization": f"Basic {encoded_auth}",
            "Accept": "application/json"
        }
        params = {
            "jql": "assignee=currentUser() AND statusCategory!=Done",
            "fields": "summary,status,created,updated"
        }

        response = requests.get(url, headers=headers, params=params)
        response.raise_for_status()
        data = response.json()

        api_issues = set()

        for issue in data.get("issues", []):
            issue_key = issue["key"]
            api_issues.add(issue_key)

            existing_issue = db.query(JiraIssue).filter(JiraIssue.issue == issue_key).first()

            issue_data = {
                "issue": issue_key,
                "title": issue["fields"]["summary"],
                "url": f"{get_settings_value(db, 'jira_api_url').rsplit('/', 4)[0]}/browse/{issue_key}",
                "description": issue["self"],
                "status": issue["fields"]["status"]["name"],
                "created_at": datetime.strptime(issue["fields"]["created"], "%Y-%m-%dT%H:%M:%S.%f%z"),
                "updated_at": datetime.strptime(issue["fields"]["updated"], "%Y-%m-%dT%H:%M:%S.%f%z")
            }

            if not existing_issue:
                db.add(JiraIssue(**issue_data))
            else:
                for key, value in issue_data.items():
                    setattr(existing_issue, key, value)

        db_issues = db.query(JiraIssue).all()
        for db_issue in db_issues:
            if db_issue.issue not in api_issues:
                db.delete(db_issue)

        db.commit()

        issues = db.query(JiraIssue).all()
        count = len(issues)

        return issues, count

    except RequestException as e:
        raise HTTPException(status_code=503, detail=f"Jira API error: {str(e)}")
    except SQLAlchemyError as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Unexpected error: {str(e)}")