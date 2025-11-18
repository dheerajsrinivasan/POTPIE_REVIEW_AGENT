from fastapi import FastAPI, HTTPException, status
from fastapi.responses import JSONResponse
from celery.result import AsyncResult
from app.models import PRRequest, AnalysisResult
from app.tasks.analyze_pr import analyze_pr_task
from app.config import settings

app = FastAPI(title="Autonomous Code Review Agent")

@app.post("/analyze-pr", response_model=dict, status_code=status.HTTP_202_ACCEPTED)
async def analyze_pr(pr_request: PRRequest):
    """Endpoint to submit a PR for analysis"""
    try:
        task = analyze_pr_task.delay(
            repo_url=pr_request.repo_url,
            pr_number=pr_request.pr_number,
            github_token=pr_request.github_token or settings.GITHUB_DEFAULT_TOKEN
        )
        return {"task_id": task.id, "status": "Processing started"}
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error submitting task: {str(e)}"
        )

@app.get("/status/{task_id}", response_model=dict)
async def get_task_status(task_id: str):
    """Check the status of an analysis task"""
    task_result = AsyncResult(task_id)
    return {
        "task_id": task_id,
        "status": task_result.status,
        "result": task_result.result if task_result.ready() else None
    }

@app.get("/results/{task_id}", response_model=AnalysisResult)
async def get_task_results(task_id: str):
    """Retrieve the analysis results"""
    task_result = AsyncResult(task_id)
    if not task_result.ready():
        raise HTTPException(
            status_code=status.HTTP_202_ACCEPTED,
            detail="Task still processing"
        )
    if task_result.failed():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Task failed during processing"
        )
    return task_result.result