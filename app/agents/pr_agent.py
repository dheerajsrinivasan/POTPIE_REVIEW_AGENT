from langgraph.graph import Graph
from typing import Dict, List, Optional
from ..models import AnalysisResult, FileAnalysis, Issue
from ..services.llm_service import LLMService
import logging
import difflib

class CodeReviewAgent:
    def __init__(self, llm_service: LLMService = None):
        self.llm_service = llm_service or LLMService()
        self.workflow = self._build_workflow()

    def _build_workflow(self) -> Graph:
        """Build the LangGraph workflow for code review"""
        workflow = Graph()

        workflow.add_node("extract_code_context", self._extract_code_context)
        workflow.add_node("analyze_style", self._analyze_style)
        workflow.add_node("analyze_bugs", self._analyze_bugs)
        workflow.add_node("analyze_performance", self._analyze_performance)
        workflow.add_node("analyze_best_practices", self._analyze_best_practices)
        workflow.add_node("compile_results", self._compile_results)

        workflow.add_edge("extract_code_context", "analyze_style")
        workflow.add_edge("extract_code_context", "analyze_bugs")
        workflow.add_edge("extract_code_context", "analyze_performance")
        workflow.add_edge("extract_code_context", "analyze_best_practices")

        workflow.add_edge("analyze_style", "compile_results")
        workflow.add_edge("analyze_bugs", "compile_results")
        workflow.add_edge("analyze_performance", "compile_results")
        workflow.add_edge("analyze_best_practices", "compile_results")

        workflow.set_entry_point("extract_code_context")
        workflow.set_finish_point("compile_results")

        return workflow.compile()

    def analyze_pr(self, pr_details: Dict, diff: str, files_changed: List[str]) -> Dict:
        try:
            initial_state = {
                "pr_details": pr_details,
                "diff": diff,
                "files_changed": files_changed,
                "analysis_results": []
            }

            final_state = self.workflow.invoke(initial_state)
            return final_state["compiled_results"]

        except Exception as e:
            logging.error(f"Error in analysis workflow: {str(e)}")
            raise

    def _extract_code_context(self, state: Dict) -> Dict:
        """Parse diff and extract code segments"""
        diff_lines = state["diff"].split('\n')
        file_contents = {}
        current_file = None

        for line in diff_lines:
            if line.startswith('+++ b/'):
                current_file = line[6:]
                file_contents[current_file] = []
            elif current_file and not line.startswith(('---', '@@', '+++')):
                if line.startswith('+'):
                    file_contents[current_file].append(line[1:])

        state["code_context"] = file_contents
        return state

    def _analyze_style(self, state: Dict) -> Dict:
        """Analyze code style issues"""
        style_issues = []
        for file, code_lines in state["code_context"].items():
            code = '\n'.join(code_lines)
            analysis = self.llm_service.analyze_code(code, "style")
            for issue in analysis:
                issue["file"] = file
                style_issues.append(issue)

        state["style_issues"] = style_issues
        return state

    def _analyze_bugs(self, state: Dict) -> Dict:
        """Analyze potential bugs"""
        bug_issues = []
        for file, code_lines in state["code_context"].items():
            code = '\n'.join(code_lines)
            analysis = self.llm_service.analyze_code(code, "bug")
            for issue in analysis:
                issue["file"] = file
                bug_issues.append(issue)

        state["bug_issues"] = bug_issues
        return state

    def _analyze_performance(self, state: Dict) -> Dict:
        """Analyze performance issues"""
        perf_issues = []
        for file, code_lines in state["code_context"].items():
            code = '\n'.join(code_lines)
            analysis = self.llm_service.analyze_code(code, "performance")
            for issue in analysis:
                issue["file"] = file
                perf_issues.append(issue)

        state["performance_issues"] = perf_issues
        return state

    def _analyze_best_practices(self, state: Dict) -> Dict:
        """Analyze best practices"""
        bp_issues = []
        for file, code_lines in state["code_context"].items():
            code = '\n'.join(code_lines)
            analysis = self.llm_service.analyze_code(code, "best_practices")
            for issue in analysis:
                issue["file"] = file
                bp_issues.append(issue)

        state["best_practice_issues"] = bp_issues
        return state

    def _compile_results(self, state: Dict) -> Dict:
        """Compile all analysis results"""
        compiled_results = {
            "files": [],
            "summary": {
                "total_files": len(state["files_changed"]),
                "total_issues": 0,
                "critical_issues": 0
            }
        }

        for file in state["files_changed"]:
            file_analysis = FileAnalysis(name=file, issues=[])

            # Add all issue types
            for issue_type in ["style_issues", "bug_issues",
                               "performance_issues", "best_practice_issues"]:
                for issue in state.get(issue_type, []):
                    if issue["file"] == file:
                        file_analysis.issues.append(Issue(
                            type=issue_type.replace("_issues", ""),
                            line=issue.get("line", 0),
                            description=issue["description"],
                            suggestion=issue["suggestion"]
                        ))

            compiled_results["files"].append(file_analysis.dict())
            compiled_results["summary"]["total_issues"] += len(file_analysis.issues)

        state["compiled_results"] = compiled_results
        return state