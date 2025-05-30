import os
from typing import Dict, List, Optional
from datetime import datetime, timedelta
from github import Github, GithubIntegration, Auth
from github.Repository import Repository
from github.PullRequest import PullRequest
import pandas as pd
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class GitHubService:
    """Service for interacting with GitHub API to fetch team velocity metrics."""
    
    def __init__(self, token: Optional[str] = None, org_name: Optional[str] = None):
        """Initialize GitHub service with authentication.
        
        Args:
            token: GitHub personal access token. If not provided, will use GITHUB_TOKEN from env.
            org_name: GitHub organization name. If not provided, will use GITHUB_ORG from env.
        """
        self.token = token or os.getenv('GITHUB_TOKEN')
        self.org_name = org_name or os.getenv('GITHUB_ORG')
        
        if not self.token:
            raise ValueError("GitHub token is required. Set GITHUB_TOKEN environment variable.")
            
        if not self.org_name:
            raise ValueError("GitHub organization name is required. Set GITHUB_ORG environment variable.")
        
        # Initialize GitHub client
        self.github = Github(self.token)
        self.org = self.github.get_organization(self.org_name)
    
    def get_pr_metrics(
        self, 
        days: int = 30,
        repo_names: Optional[List[str]] = None
    ) -> Dict:
        """Get PR metrics for the specified repositories.
        
        Args:
            days: Number of days to look back for PRs
            repo_names: List of repository names to include. If None, includes all repos in the org.
            
        Returns:
            Dictionary containing PR metrics
        """
        since = datetime.now() - timedelta(days=days)
        pr_metrics = {
            'total_prs': 0,
            'merged_prs': 0,
            'open_prs': 0,
            'avg_pr_cycle_time_hours': 0,
            'pr_cycle_times': [],
            'prs_by_author': {},
            'prs_by_repo': {}
        }
        
        # Get repositories to analyze
        repos = []
        if repo_names:
            for repo_name in repo_names:
                try:
                    repo = self.org.get_repo(repo_name)
                    repos.append(repo)
                except Exception as e:
                    print(f"Error accessing repository {repo_name}: {e}")
        else:
            repos = list(self.org.get_repos())
        
        # Process PRs for each repository
        for repo in repos:
            repo_name = repo.name
            prs = repo.get_pulls(state='all', sort='created', direction='desc')
            
            for pr in prs:
                if pr.created_at < since:
                    continue
                    
                pr_metrics['total_prs'] += 1
                
                # Track PR state
                if pr.state == 'open':
                    pr_metrics['open_prs'] += 1
                elif pr.state == 'closed' and pr.merged:
                    pr_metrics['merged_prs'] += 1
                
                # Calculate cycle time for merged PRs
                if pr.state == 'closed' and pr.merged and pr.created_at and pr.merged_at:
                    cycle_time = (pr.merged_at - pr.created_at).total_seconds() / 3600  # in hours
                    pr_metrics['pr_cycle_times'].append(cycle_time)
                
                # Track PRs by author
                author = pr.user.login
                if author not in pr_metrics['prs_by_author']:
                    pr_metrics['prs_by_author'][author] = 0
                pr_metrics['prs_by_author'][author] += 1
                
                # Track PRs by repository
                if repo_name not in pr_metrics['prs_by_repo']:
                    pr_metrics['prs_by_repo'][repo_name] = 0
                pr_metrics['prs_by_repo'][repo_name] += 1
        
        # Calculate average PR cycle time
        if pr_metrics['pr_cycle_times']:
            pr_metrics['avg_pr_cycle_time_hours'] = sum(pr_metrics['pr_cycle_times']) / len(pr_metrics['pr_cycle_times'])
        
        return pr_metrics
    
    def get_commit_activity(
        self,
        days: int = 30,
        repo_names: Optional[List[str]] = None
    ) -> Dict:
        """Get commit activity metrics.
        
        Args:
            days: Number of days to look back for commits
            repo_names: List of repository names to include. If None, includes all repos in the org.
            
        Returns:
            Dictionary containing commit metrics
        """
        since = datetime.now() - timedelta(days=days)
        commit_metrics = {
            'total_commits': 0,
            'commits_by_author': {},
            'commits_by_repo': {},
            'daily_commits': {},
        }
        
        # Get repositories to analyze
        repos = []
        if repo_names:
            for repo_name in repo_names:
                try:
                    repo = self.org.get_repo(repo_name)
                    repos.append(repo)
                except Exception as e:
                    print(f"Error accessing repository {repo_name}: {e}")
        else:
            repos = list(self.org.get_repos())
        
        # Process commits for each repository
        for repo in repos:
            repo_name = repo.name
            commits = repo.get_commits(since=since)
            
            for commit in commits:
                if not commit.author:
                    continue
                    
                commit_metrics['total_commits'] += 1
                
                # Track commits by author
                author = commit.author.login if commit.author else 'unknown'
                if author not in commit_metrics['commits_by_author']:
                    commit_metrics['commits_by_author'][author] = 0
                commit_metrics['commits_by_author'][author] += 1
                
                # Track commits by repository
                if repo_name not in commit_metrics['commits_by_repo']:
                    commit_metrics['commits_by_repo'][repo_name] = 0
                commit_metrics['commits_by_repo'][repo_name] += 1
                
                # Track daily commits
                commit_date = commit.commit.author.date.date()
                if commit_date not in commit_metrics['daily_commits']:
                    commit_metrics['daily_commits'][commit_date] = 0
                commit_metrics['daily_commits'][commit_date] += 1
        
        # Convert daily_commits to a sorted list of tuples
        commit_metrics['daily_commits'] = sorted(commit_metrics['daily_commits'].items())
        
        return commit_metrics
    
    def get_team_velocity(
        self,
        days: int = 30,
        repo_names: Optional[List[str]] = None
    ) -> Dict:
        """Get team velocity metrics.
        
        Args:
            days: Number of days to look back
            repo_names: List of repository names to include. If None, includes all repos in the org.
            
        Returns:
            Dictionary containing team velocity metrics
        """
        pr_metrics = self.get_pr_metrics(days=days, repo_names=repo_names)
        commit_metrics = self.get_commit_activity(days=days, repo_names=repo_names)
        
        # Calculate active contributors (those with commits or PRs)
        contributors = set()
        contributors.update(pr_metrics['prs_by_author'].keys())
        contributors.update(commit_metrics['commits_by_author'].keys())
        
        return {
            'pr_cycle_time_days': pr_metrics.get('avg_pr_cycle_time_hours', 0) / 24,  # Convert to days
            'daily_commits': commit_metrics.get('total_commits', 0) / days if days > 0 else 0,
            'active_contributors': len(contributors),
            'prs_merged': pr_metrics.get('merged_prs', 0),
            'prs_open': pr_metrics.get('open_prs', 0),
            'total_commits': commit_metrics.get('total_commits', 0),
            'prs_by_author': pr_metrics.get('prs_by_author', {}),
            'commits_by_author': commit_metrics.get('commits_by_author', {}),
            'daily_commits_data': commit_metrics.get('daily_commits', [])
        }
