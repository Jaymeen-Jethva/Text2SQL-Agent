from service.llm_service import LLMService
from service.prompt_builder_service import PromptBuilderService
from service.sql_execution_service import SQLExecutionResult

class AnswerGenerationService:
    def __init__(self, llm_service: LLMService, prompt_builder: PromptBuilderService):
        self.llm_service = llm_service
        self.prompt_builder = prompt_builder
        
    def stream_answer(self, question: str, sql_query: str, execution_result: SQLExecutionResult):
        if execution_result.error:
            results_str = f"Error during execution: {execution_result.error}"
        elif execution_result.row_count == 0:
            results_str = "No results found."
        else:
            limit = min(20, execution_result.row_count)
            results_str = f"Columns: {', '.join(execution_result.columns)}\n"
            results_str += f"Rows (Showing {limit} of {execution_result.row_count}):\n"
            for row in execution_result.rows[:limit]:
                results_str += str(row) + "\n"
                
        prompt = self.prompt_builder.build_answer_prompt(
            question=question, 
            sql_query=sql_query, 
            results=results_str
        )
        
        system_prompt = "You are a helpful and expert data analyst assistant. Answer concisely and accurately."
        
        return self.llm_service.stream(system_prompt, prompt)
