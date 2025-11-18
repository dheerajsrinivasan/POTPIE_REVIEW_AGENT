import requests
from typing import Dict, List, Optional
from app.config import settings
import logging

class GitHubService:
    def __init__(self, token: Optional[str] = None):
        self.token = token or settings.GITHUB_DEFAULT_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Accept": "application/vnd.github.v3+json"
        }

    def get_pr_details(self, repo_url: str, pr_number: int) -> Dict:
        """Get PR details from GitHub API"""
        api_url = self._get_api_url(repo_url, f"pulls/{pr_number}")
        response = requests.get(api_url, headers=self.headers)
        response.raise_for_status()
        return response.json()

    def get_pr_diff(self, repo_url: str, pr_number: int) -> str:
        """Get the diff for a PR"""
        api_url = self._get_api_url(repo_url, f"pulls/{pr_number}", accept="diff")
        headers = self.headers.copy()
        headers["Accept"] = "application/vnd.github.v3.diff"
        response = requests.get(api_url, headers=headers)
        response.raise_for_status()
        return response.text

    def get_changed_files(self, repo_url: str, pr_number: int) -> List[str]:
        """Get list of changed files in a PR"""
        api_url = self._get_api_url(repo_url, f"pulls/{pr_number}/files")
        response = requests.get(api_url, headers=self.headers)
        response.raise_for_status()
        return [file["filename"] for file in response.json()]

    def _get_api_url(self, repo_url: str, endpoint: str, accept: str = "json") -> str:
        """Convert repository URL to API URL"""
        if not repo_url.startswith("https://github.com/"):
            raise ValueError("Invalid GitHub repository URL")

        repo_path = repo_url.replace("https://github.com/", "")
        return f"https://api.github.com/repos/{repo_path}/{endpoint}"