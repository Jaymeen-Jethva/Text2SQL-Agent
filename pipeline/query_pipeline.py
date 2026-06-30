from service.retriever_service import RetrieverService
from service.vector_store_service import VectorStoreService
from service.llm_service import LLMService
from service.prompt_builder_service import PromptBuilderService
from service.sql_generation_service import SQLGenerationService
from service.sql_execution_service import SQLExecutionService
from service.answer_generation_service import AnswerGenerationService
from service.chart_service import ChartService
from config import DATABASE_DIR
from utils.logger import get_logger

logger = get_logger("QueryPipeline")

def run_query(db_name: str, question: str, history: str):
    # Initialize services
    vector_store = VectorStoreService(index_name=f"{db_name}_index")
    retriever = RetrieverService(vector_store)
    
    llm_service = LLMService()
    prompt_builder = PromptBuilderService()
    
    db_path = DATABASE_DIR / f"{db_name}.db"
    exec_service = SQLExecutionService(db_path)
    
    sql_gen_service = SQLGenerationService(llm_service, prompt_builder, exec_service)
    answer_service = AnswerGenerationService(llm_service, prompt_builder)
    chart_service = ChartService()
    
    
    # 1. Retrieve Context
    logger.info(f"Retrieving context for question: {question}")
    context = retriever.retrieve_context(question)
    
    # 2. Generate and Execute SQL
    logger.info("Generating and executing SQL...")
    sql_query, exec_result = sql_gen_service.generate_and_execute(context, history, question)
    logger.info(f"Execution complete. Time: {exec_result.execution_time_ms:.2f}ms, Rows: {exec_result.row_count}")
    
    # 3. Generate Chart
    logger.info("Generating chart...")
    chart = chart_service.generate_chart(exec_result)
    
    # 4. Stream Answer
    logger.info("Streaming answer...")
    answer_generator = answer_service.stream_answer(question, sql_query, exec_result)
    
    return {
        "context": context,
        "sql_query": sql_query,
        "exec_result": exec_result,
        "chart": chart,
        "answer_generator": answer_generator
    }
