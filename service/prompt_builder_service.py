from pathlib import Path
from config import BASE_DIR

class PromptBuilderService:
    def __init__(self):
        self.prompts_dir = BASE_DIR / "prompts"
        self.prompts_dir.mkdir(parents=True, exist_ok=True)
        
    def _read_prompt(self, filename: str) -> str:
        path = self.prompts_dir / filename
        if not path.exists():
            raise FileNotFoundError(f"Prompt file not found: {path}")
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
            
    def build_sql_prompt(self, context: str, history: str, question: str) -> str:
        template = self._read_prompt("sql_prompt.md")
        return template.format(context=context, history=history, question=question)
        
    def build_answer_prompt(self, question: str, sql_query: str, results: str) -> str:
        template = self._read_prompt("answer_prompt.md")
        return template.format(question=question, sql_query=sql_query, results=results)
