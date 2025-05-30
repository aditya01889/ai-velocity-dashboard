"""Pytest configuration and fixtures."""
import os
import pytest
from datetime import datetime, timedelta
from unittest.mock import MagicMock, patch

# Add the project root to the Python path
import sys
from pathlib import Path

# Add the parent directory to the Python path
sys.path.insert(0, str(Path(__file__).parent.parent))

# Load environment variables for testing
from dotenv import load_dotenv
load_dotenv()

# Fixtures

@pytest.fixture
github_service_mock():
    """Mock GitHub service for testing."""
    with patch('app.services.github_service.Github') as mock_github:
        # Create a mock organization
        mock_org = MagicMock()
        mock_github.return_value.get_organization.return_value = mock_org
        
        # Create a mock repository
        mock_repo = MagicMock()
        mock_repo.name = "test-repo"
        mock_org.get_repos.return_value = [mock_repo]
        mock_org.get_repo.return_value = mock_repo
        
        # Mock PRs
        mock_pr = MagicMock()
        mock_pr.state = 'closed'
        mock_pr.merged = True
        mock_pr.created_at = datetime.now() - timedelta(days=1)
        mock_pr.merged_at = datetime.now()
        mock_pr.user.login = "testuser"
        
        # Mock commits
        mock_commit = MagicMock()
        mock_commit.author.login = "testuser"
        mock_commit.commit.author.date = datetime.now()
        
        # Set up return values
        mock_repo.get_pulls.return_value = [mock_pr]
        mock_repo.get_commits.return_value = [mock_commit]
        
        yield mock_github

@pytest.fixture
github_service(github_service_mock):
    """GitHub service instance with mocked GitHub API."""
    from app.services.github_service import GitHubService
    return GitHubService(token="test-token", org_name="test-org")

@pytest.fixture
def langsmith_service_mock():
    """Mock LangSmith service for testing."""
    with patch('app.services.langsmith_service.Client') as mock_client:
        # Mock the client methods used in the service
        mock_instance = MagicMock()
        mock_client.return_value = mock_instance
        
        # Mock list_runs response
        mock_run = MagicMock()
        mock_run.id = "test-run-id"
        mock_run.prompt = "test prompt"
        mock_run.error = None
        mock_run.tags = []
        mock_run.name = "test-run"
        mock_run.outputs = {"evaluation": {"score": 0.9}}
        mock_run.start_time = datetime.now()
        mock_run.end_time = datetime.now() + timedelta(seconds=10)
        
        mock_instance.list_runs.return_value = [mock_run]
        
        yield mock_client

@pytest.fixture
def langsmith_service(langsmith_service_mock):
    """LangSmith service instance with mocked LangSmith API."""
    from app.services.langsmith_service import LangSmithService
    return LangSmithService(api_key="test-key", project_name="test-project")

@pytest.fixture
def mock_velocity_data():
    """Mock velocity data for testing."""
    return {
        'pr_cycle_time_days': 2.5,
        'daily_commits': 15.3,
        'active_contributors': 5,
        'prs_merged': 12,
        'prs_open': 3,
        'total_commits': 107,
        'prs_by_author': {'user1': 5, 'user2': 7},
        'commits_by_author': {'user1': 30, 'user2': 40, 'user3': 37},
        'daily_commits_data': [
            ((datetime.now() - timedelta(days=i)).date(), i + 5) 
            for i in range(7, -1, -1)
        ]
    }

@pytest.fixture
def mock_coverage_data():
    """Mock coverage data for testing."""
    return {
        'prompt_coverage': 75.0,
        'test_success_rate': 92.5,
        'prompts_tracked': 124,
        'prompts_tested': 93,
        'total_runs': 542,
        'successful_runs': 501,
        'error_runs': 41,
        'regression_failures': 3,
        'prompt_templates': [
            {
                'template': 'test prompt 1',
                'runs': 10,
                'success': 9,
                'errors': 1,
                'tested': True
            },
            {
                'template': 'test prompt 2',
                'runs': 15,
                'success': 14,
                'errors': 1,
                'tested': False
            }
        ]
    }

# Configure pytest to use these fixtures for all tests
@pytest.fixture(autouse=True)
def setup_test_environment(monkeypatch):
    """Set up test environment."""
    # Set environment variables for testing
    monkeypatch.setenv("GITHUB_TOKEN", "test-token")
    monkeypatch.setenv("GITHUB_ORG", "test-org")
    monkeypatch.setenv("LANGSMITH_API_KEY", "test-key")
    monkeypatch.setenv("LANGSMITH_PROJECT", "test-project")
    monkeypatch.setenv("ENVIRONMENT", "test")
    monkeypatch.setenv("LOG_LEVEL", "INFO")
    
    # Ensure we don't make real API calls during tests
    monkeypatch.setattr('requests.get', MagicMock())
    monkeypatch.setattr('requests.post', MagicMock())
    
    # Set up test database if needed
    # ...
    
    yield
    
    # Clean up after tests
    # ...
