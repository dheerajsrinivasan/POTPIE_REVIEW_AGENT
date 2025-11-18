from typing import Dict, List
from ..config import settings
import ollama
import openai
import json
import logging

class LLMService:
    def __init__(self):
        self.llm_provider = settings.LLM_PROVIDER
        self.llm_model = settings.LLM_MODEL

    def analyze_code(self, code_context: str, analysis_type: str) -> List[Dict]:
        prompt = self._build_prompt(code_context, analysis_type)

        try:
            if self.llm_provider == "ollama":
                response = ollama.generate(
                    model=self.llm_model,
                    prompt=prompt,
                    format="json"
                )
                return self._parse_response(response["response"])

            elif self.llm_provider == "openai":
                response = openai.ChatCompletion.create(
                    model=self.llm_model,
                    messages=[{"role": "user", "content": prompt}],
                    response_format={"type": "json_object"}
                )
                return self._parse_response(response.choices[0].message.content)

            else:
                raise ValueError(f"Unsupported LLM provider: {self.llm_provider}")

        except Exception as e:
            logging.error(f"Error in LLM analysis: {str(e)}")
            raise

    def _build_prompt(self, code_context: str, analysis_type: str) -> str:
        prompts = {
            "style": """Analyze the following code for style and formatting issues.
                Look for: inconsistent indentation, naming conventions, line length,
                import organization, and other style concerns.
                Return JSON format with: line, description, suggestion""",
            "bug": """Identify potential bugs or errors in the following code.
                Look for: null references, type mismatches, logical errors,
                exception handling issues, and other potential bugs.
                Return JSON format with: line, description, suggestion""",
            "performance": """Suggest performance improvements for the following code.
                Look for: inefficient algorithms, unnecessary computations,
                memory leaks, database query optimizations.
                Return JSON format with: line, description, suggestion""",
            "best_practices": """Evaluate the following code against best practices.
                Look for: SOLID principles, DRY violations, proper encapsulation,
                proper error handling, and other architectural concerns.
                Return JSON format with: line, description, suggestion"""
        }
        return f"{prompts[analysis_type]}\n\nCode:\n{code_context}"

    def _parse_response(self, response: str) -> List[Dict]:
        try:
            data = json.loads(response)
            if isinstance(data, list):
                return data
            elif "issues" in data:
                return data["issues"]
            return []
        except json.JSONDecodeError:
            logging.error(f"Failed to parse LLM response: {response}")
            return []