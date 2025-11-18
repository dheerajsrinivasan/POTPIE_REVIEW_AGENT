from celery import Celery
from app.agents.pr_agent import CodeReviewAgent
from app.services.github_service import GitHubService
from app.config import settings
from app.models import AnalysisResult
import logging

# Initialize Celery
celery_app = Celery(
    'tasks',
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND
)

@celery_app.task(bind=True, name="analyze_pr_task")
def analyze_pr_task(self, repo_url: str, pr_number: int, github_token: str):
    """Celery task to analyze a GitHub PR"""
    try:
        self.update_state(state='PROCESSING')

        # Initialize services
        github_service = GitHubService(github_token)
        review_agent = CodeReviewAgent()

        # Fetch PR details
        pr_details = github_service.get_pr_details(repo_url, pr_number)
        diff = github_service.get_pr_diff(repo_url, pr_number)
        files_changed = github_service.get_changed_files(repo_url, pr_number)

        # Analyze with AI agent
        analysis_results = review_agent.analyze_pr(
            pr_details=pr_details,
            diff=diff,
            files_changed=files_changed
        )

        return AnalysisResult(
            task_id=self.request.id,
            status="completed",
            results=analysis_results
        ).dict()

    except Exception as e:
        logging.error(f"Error processing PR {pr_number}: {str(e)}")
        raise self.retry(exc=e, countdown=60)