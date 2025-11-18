from pydantic import BaseModel
from typing import List, Optional, Literal, Dict, Union


class PRRequest(BaseModel):
    repo_url: str
    pr_number: int
    github_token: Optional[str] = None

class Issue(BaseModel):
    type: Literal["style", "bug", "performance", "best_practice"]
    line: int
    description: str
    suggestion: str

class FileAnalysis(BaseModel):
    name: str
    issues: List[Issue]

class AnalysisSummary(BaseModel):
    total_files: int
    total_issues: int
    critical_issues: int = 0

class AnalysisResult(BaseModel):
    task_id: str
    status: str
    results: Dict[str, Union[List[FileAnalysis], AnalysisSummary]]