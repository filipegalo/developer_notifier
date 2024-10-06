from typing import List, Tuple, Set
from sqlalchemy.orm import Session
from sqlalchemy.exc import SQLAlchemyError
from app.crud.settings import get_settings_value
from app.models import GithubPullRequest
from gql import gql, Client
from gql.transport.requests import RequestsHTTPTransport
import logging

def get_github_pull_requests(db: Session) -> Tuple[List[GithubPullRequest], int]:
    """
    Fetches open GitHub pull requests where the user is an author or reviewer,
    updates the local database accordingly, and returns the list of pull requests.

    Args:
        db (Session): SQLAlchemy database session.

    Returns:
        Tuple[List[GithubPullRequest], int]: A tuple containing the list of pull requests and the count.
    """
    transport = RequestsHTTPTransport(
        url='https://api.github.com/graphql',
        headers={'Authorization': f'Bearer {get_settings_value(db, "github_access_token")}'},
        retries=3,  # Added retry mechanism
    )
    client = Client(transport=transport, fetch_schema_from_transport=False)

    query = gql('''
    query($org: String!) {
      organization(login: $org) {
        repositories(first: 100) {
          nodes {
            name
            pullRequests(states: OPEN, first: 100) {
              nodes {
                number
                title
                body
                state
                url
                author {
                  login
                }
                reviewRequests(first: 10) {
                  nodes {
                    requestedReviewer {
                      ... on User {
                        login
                      }
                    }
                  }
                }
              }
            }
          }
        }
      }
    }
    ''')

    try:
        result = client.execute(query, variable_values={'org': get_settings_value(db, "github_org")})
    except Exception as e:
        if 'API rate limit exceeded' in str(e):
            logging.error(f"GitHub API rate limit exceeded: {e}")
            issues = db.query(GithubPullRequest).all()
            count = len(issues)
            return issues, count
        else:
            logging.error(f"Failed to fetch pull requests from GitHub: {e}")
            raise RuntimeError("GitHub API request failed") from e

    current_pr_numbers: Set[int] = set()
    github_user = get_settings_value(db, "github_user")
    pr_data_list = []

    for repo in result.get('organization', {}).get('repositories', {}).get('nodes', []):
        repo_name = repo.get('name')
        for pr in repo.get('pullRequests', {}).get('nodes', []):
            pr_number = pr.get('number')
            if pr_number is None:
                continue

            pr_author_login = pr.get('author', {}).get('login', '')
            is_author = pr_author_login == github_user

            review_requests = pr.get('reviewRequests', {}).get('nodes', [])
            is_reviewer = any(
                rr.get('requestedReviewer', {}).get('login') == github_user
                for rr in review_requests
                if rr.get('requestedReviewer')
            )

            if is_author or is_reviewer:
                current_pr_numbers.add(pr_number)

                pr_data = {
                    'pull_request': pr_number,
                    'title': pr.get('title', ''),
                    'description': pr.get('body', ''),
                    'status': pr.get('state', ''),
                    'repository': repo_name,
                    'url': pr.get('url', ''),
                    'is_assigned': is_author,
                }
                pr_data_list.append(pr_data)

    try:
        existing_pr_numbers = set(
            pr[0] for pr in db.query(GithubPullRequest.pull_request).all()
        )

        pr_numbers_to_update = existing_pr_numbers & current_pr_numbers
        pr_numbers_to_add = current_pr_numbers - existing_pr_numbers
        pr_numbers_to_delete = existing_pr_numbers - current_pr_numbers

        for pr_data in pr_data_list:
            pr_number = pr_data['pull_request']
            if pr_number in pr_numbers_to_update:
                db.query(GithubPullRequest).filter(
                    GithubPullRequest.pull_request == pr_number
                ).update(pr_data)
            elif pr_number in pr_numbers_to_add:
                db_pr = GithubPullRequest(**pr_data)
                db.add(db_pr)

        if pr_numbers_to_delete:
            db.query(GithubPullRequest).filter(
                GithubPullRequest.pull_request.in_(pr_numbers_to_delete)
            ).delete(synchronize_session=False)

        db.commit()
    except SQLAlchemyError as e:
        logging.error(f"Database operation failed: {e}")
        db.rollback()
        raise RuntimeError("Database operation failed") from e

    issues = db.query(GithubPullRequest).all()
    count = len(issues)

    return issues, count
