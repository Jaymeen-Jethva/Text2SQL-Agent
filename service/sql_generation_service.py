import re
from service.llm_service import LLMService
from service.prompt_builder_service import PromptBuilderService
from service.sql_execution_service import SQLExecutionService, SQLExecutionResult

class SQLGenerationService:
    def __init__(
        self, 
        llm_service: LLMService, 
        prompt_builder: PromptBuilderService, 
        execution_service: SQLExecutionService
    ):
        self.llm_service = llm_service
        self.prompt_builder = prompt_builder
        self.execution_service = execution_service
        
    def _clean_sql(self, sql: str) -> str:
        sql = re.sub(r'```sql\n?', '', sql, flags=re.IGNORECASE)
        sql = re.sub(r'```\n?', '', sql)
        return sql.strip()
        
    def generate_and_execute(
        self, 
        context: str, 
        history: str, 
        question: str, 
        max_retries: int = 3
    ) -> tuple[str, SQLExecutionResult]:
        
        prompt = self.prompt_builder.build_sql_prompt(context, history, question)
        
        current_prompt = prompt
        clean_sql = ""
        result = None
        
        for attempt in range(max_retries):
            raw_sql = self.llm_service.invoke(
                "You are an expert SQLite assistant. Only output raw SQL.", 
                current_prompt
            )
            clean_sql = self._clean_sql(raw_sql)
            
            result = self.execution_service.execute(clean_sql)
            
            if not result.error:
                return clean_sql, result
                
            current_prompt += f"\n\nPrevious attempt failed with error:\n{result.error}\nPlease fix the SQL and return ONLY the corrected SQL query."
            
        return clean_sql, result
