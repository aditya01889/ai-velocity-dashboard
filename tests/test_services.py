import os
import pytest
from datetime import datetime, timedelta
from dotenv import load_dotenv

# Load environment variables for testing
load_dotenv()

# Check if required environment variables are set
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
GITHUB_ORG = os.getenv("GITHUB_ORG")
LANGSMITH_API_KEY = os.getenv("LANGSMITH_API_KEY")
LANGSMITH_PROJECT = os.getenv("LANGSMITH_PROJECT")

# Skip tests if required environment variables are not set
pytestmark = pytest.mark.skipif(
    not all([GITHUB_TOKEN, GITHUB_ORG, LANGSMITH_API_KEY, LANGSMITH_PROJECT]),
    reason="Required environment variables not set"
)

class TestGitHubService:
    """Tests for GitHubService."""
    
    def test_github_service_initialization(self):
        """Test GitHub service initialization with environment variables."""
        from app.services.github_service import GitHubService
        
        # Test initialization with environment variables
        service = GitHubService()
        assert service.token == GITHUB_TOKEN
        assert service.org_name == GITHUB_ORG
        
        # Test initialization with explicit parameters
        custom_token = "test_token"
        custom_org = "test_org"
        service = GitHubService(token=custom_token, org_name=custom_org)
        assert service.token == custom_token
        assert service.org_name == custom_org
    
    def test_get_pr_metrics(self):
        """Test fetching PR metrics from GitHub."""
        from app.services.github_service import GitHubService
        
        service = GitHubService()
        metrics = service.get_pr_metrics(days=7)
        
        assert isinstance(metrics, dict)
        assert 'total_prs' in metrics
        assert 'merged_prs' in metrics
        assert 'open_prs' in metrics
        assert 'avg_pr_cycle_time_hours' in metrics
        assert 'prs_by_author' in metrics
        assert 'prs_by_repo' in metrics
    
    def test_get_commit_activity(self):
        """Test fetching commit activity from GitHub."""
        from app.services.github_service import GitHubService
        
        service = GitHubService()
        activity = service.get_commit_activity(days=7)
        
        assert isinstance(activity, dict)
        assert 'total_commits' in activity
        assert 'commits_by_author' in activity
        assert 'commits_by_repo' in activity
        assert 'daily_commits' in activity
    
    def test_get_team_velocity(self):
        """Test getting team velocity metrics."""
        from app.services.github_service import GitHubService
        
        service = GitHubService()
        velocity = service.get_team_velocity(days=7)
        
        assert isinstance(velocity, dict)
        assert 'pr_cycle_time_days' in velocity
        assert 'daily_commits' in velocity
        assert 'active_contributors' in velocity
        assert 'prs_merged' in velocity
        assert 'prs_open' in velocity
        assert 'total_commits' in velocity
        assert 'prs_by_author' in velocity
        assert 'commits_by_author' in velocity
        assert 'daily_commits_data' in velocity

class TestLangSmithService:
    """Tests for LangSmithService."""
    
    def test_langsmith_service_initialization(self):
        """Test LangSmith service initialization with environment variables."""
        from app.services.langsmith_service import LangSmithService
        
        # Skip if LangSmith is not available
        try:
            from langsmith import Client
        except ImportError:
            pytest.skip("LangSmith client not available")
        
        # Test initialization with environment variables
        service = LangSmithService()
        assert service.api_key == LANGSMITH_API_KEY
        assert service.project_name == LANGSMITH_PROJECT
        
        # Test initialization with explicit parameters
        custom_key = "test_key"
        custom_project = "test_project"
        service = LangSmithService(api_key=custom_key, project_name=custom_project)
        assert service.api_key == custom_key
        assert service.project_name == custom_project
    
    def test_get_prompt_coverage(self):
        """Test fetching prompt coverage from LangSmith."""
        from app.services.langsmith_service import LangSmithService
        
        # Skip if LangSmith is not available
        try:
            from langsmith import Client
        except ImportError:
            pytest.skip("LangSmith client not available")
        
        service = LangSmithService()
        coverage = service.get_prompt_coverage(days=7)
        
        assert isinstance(coverage, dict)
        assert 'prompt_coverage' in coverage
        assert 'test_success_rate' in coverage
        assert 'prompts_tracked' in coverage
        assert 'prompts_tested' in coverage
        assert 'total_runs' in coverage
        assert 'successful_runs' in coverage
        assert 'error_runs' in coverage
        assert 'regression_failures' in coverage
        assert 'prompt_templates' in coverage
    
    def test_get_test_results(self):
        """Test fetching test results from LangSmith."""
        from app.services.langsmith_service import LangSmithService
        
        # Skip if LangSmith is not available
        try:
            from langsmith import Client
        except ImportError:
            pytest.skip("LangSmith client not available")
        
        service = LangSmithService()
        test_results = service.get_test_results(days=7)
        
        assert isinstance(test_results, dict)
        assert 'total_tests' in test_results
        assert 'passed' in test_results
        assert 'failed' in test_results
        assert 'error' in test_results
        assert 'pass_rate' in test_results
        assert 'avg_execution_time' in test_results
        assert 'execution_times' in test_results
        assert 'failures_by_test_case' in test_results
        assert 'test_history' in test_results

class TestIntegration:
    """Integration tests for the application."""
    
    def test_github_integration(self):
        """Test GitHub integration end-to-end."""
        from app.services.github_service import GitHubService
        
        service = GitHubService()
        velocity = service.get_team_velocity(days=7)
        
        # Basic validation of the response
        assert isinstance(velocity, dict)
        assert 'pr_cycle_time_days' in velocity
        assert isinstance(velocity['daily_commits'], (int, float))
        assert isinstance(velocity['active_contributors'], int)
    
    def test_langsmith_integration(self):
        """Test LangSmith integration end-to-end."""
        from app.services.langsmith_service import LangSmithService
        
        # Skip if LangSmith is not available
        try:
            from langsmith import Client
        except ImportError:
            pytest.skip("LangSmith client not available")
        
        service = LangSmithService()
        coverage = service.get_prompt_coverage(days=7)
        
        # Basic validation of the response
        assert isinstance(coverage, dict)
        assert 'prompt_coverage' in coverage
        assert 0 <= coverage['prompt_coverage'] <= 100
        assert 'test_success_rate' in coverage
        assert 0 <= coverage['test_success_rate'] <= 100
