import uuid
from datetime import datetime
from sqlmodel import Field, SQLModel
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from pydantic import BaseModel

Base = declarative_base()

class BaseModel(SQLModel):
    id: uuid.UUID = Field(default_factory=uuid.uuid4, primary_key=True)
    title: str = Field(index=True)
    description: str
    status: str = Field(index=True)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)

class JiraIssue(BaseModel, table=True):
    __tablename__ = "jira_issues"
    issue: str = Field(index=True, unique=True)
    url: str = Field(nullable=False)

class GithubPullRequest(BaseModel, table=True):
    __tablename__ = "github_pull_requests"
    pull_request: int = Field(index=True, unique=True)
    repository: str = Field(nullable=False)
    url: str = Field(nullable=False)
    is_assigned: bool = Field(default=False)

class JiraIssueResponse(SQLModel):
    issues: list[JiraIssue]
    count: int

class GithubPullRequestResponse(SQLModel):
    pull_requests: list[GithubPullRequest]
    count: int

class Settings(SQLModel, table=True):
    __tablename__ = "settings"

    id: int = Field(default=None, primary_key=True)
    jira_api_email: str | None = Field(index=True, nullable=True)
    jira_api_key: str | None = Field(nullable=True)
    jira_api_url: str | None = Field(nullable=True)
    github_access_token: str | None = Field(nullable=True)
    github_org: str | None = Field(nullable=True)
    github_user: str | None = Field(nullable=True)
    github_api_url: str | None = Field(nullable=True)
    user_name: str

class SettingsResponse(SQLModel):
    jira_api_email: str | None = None
    jira_api_url: str | None = None
    github_api_url: str | None = None
    github_org: str | None = None
    github_user: str | None = None
    user_name: str

class ErrorResponse(BaseModel):
    message: str

