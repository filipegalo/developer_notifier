from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.models import GitlabMergeRequest, Settings
import requests
from datetime import datetime
import logging

def get_gitlab_merge_requests(db: Session):
    settings = db.query(Settings).first()
    if not settings or not settings.gitlab_access_token or not settings.gitlab_api_url:
        raise RuntimeError("GitLab settings are not configured")

    headers = {
        "Authorization": f"Bearer {settings.gitlab_access_token}",
        "Content-Type": "application/json",
    }

    try:
        response = requests.get(
            f"{settings.gitlab_api_url}/merge_requests?state=opened",
            headers=headers
        )
        response.raise_for_status()
        merge_requests_data = response.json()
    except requests.RequestException as e:
        logging.error(f"Error fetching GitLab merge requests: {e}")
        raise RuntimeError(f"Failed to fetch GitLab merge requests: {str(e)}")

    merge_requests = []
    for mr_data in merge_requests_data:
        merge_request = GitlabMergeRequest(
            title=mr_data['title'],
            description=mr_data['description'],
            status=mr_data['state'],
            created_at=datetime.strptime(mr_data['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            updated_at=datetime.strptime(mr_data['updated_at'], "%Y-%m-%dT%H:%M:%S.%fZ"),
            merge_request=mr_data['iid'],
            repository=mr_data['references']['full'].split('!')[0],
            url=mr_data['web_url'],
        )
        merge_requests.append(merge_request)

    try:
        # Get existing merge requests from the database
        existing_mrs = db.query(GitlabMergeRequest).all()
        existing_mr_dict = {mr.merge_request: mr for mr in existing_mrs}

        # Update or add new merge requests
        for mr_data in merge_requests_data:
            mr_iid = mr_data['iid']
            if mr_iid in existing_mr_dict:
                # Update existing merge request
                existing_mr = existing_mr_dict[mr_iid]
                existing_mr.title = mr_data['title']
                existing_mr.description = mr_data['description']
                existing_mr.status = mr_data['state']
                existing_mr.updated_at = datetime.strptime(mr_data['updated_at'], "%Y-%m-%dT%H:%M:%S.%fZ")
                existing_mr.repository = mr_data['references']['full'].split('!')[0]
                existing_mr.url = mr_data['web_url']
            else:
                # Add new merge request
                new_mr = GitlabMergeRequest(
                    title=mr_data['title'],
                    description=mr_data['description'],
                    status=mr_data['state'],
                    created_at=datetime.strptime(mr_data['created_at'], "%Y-%m-%dT%H:%M:%S.%fZ"),
                    updated_at=datetime.strptime(mr_data['updated_at'], "%Y-%m-%dT%H:%M:%S.%fZ"),
                    merge_request=mr_iid,
                    repository=mr_data['references']['full'].split('!')[0],
                    url=mr_data['web_url'],
                )
                db.add(new_mr)

        # Delete merge requests that no longer exist in GitLab
        current_mr_iids = {mr['iid'] for mr in merge_requests_data}
        for mr_iid, mr in existing_mr_dict.items():
            if mr_iid not in current_mr_iids:
                db.delete(mr)

        db.commit()
    except SQLAlchemyError as e:
        logging.error(f"Database operation failed: {e}")
        db.rollback()
        raise RuntimeError("Database operation failed") from e

    issues = db.query(GitlabMergeRequest).all()
    count = len(issues)

    return issues, count
