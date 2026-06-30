from langchain_ollama import ChatOllama
from langchain_core.messages import HumanMessage, SystemMessage
from tenacity import retry, stop_after_attempt, wait_exponential
from config import OLLAMA_BASE_URL, DEFAULT_MODEL


class LLMService:
    def __init__(self, model: str = DEFAULT_MODEL, temperature: float = 0.0):
        self.llm = ChatOllama(
            base_url=OLLAMA_BASE_URL,
            model=model,
            temperature=temperature,
            timeout=120
        )
        
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def invoke(self, system_prompt: str, user_prompt: str) -> str:
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        response = self.llm.invoke(messages)
        return response.content
        
    def stream(self, system_prompt: str, user_prompt: str):
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        for chunk in self.llm.stream(messages):
            yield chunk.content
            
    @retry(stop=stop_after_attempt(3), wait=wait_exponential(multiplier=1, min=2, max=10))
    def invoke_structured(self, system_prompt: str, user_prompt: str, pydantic_schema):
        llm_with_structure = self.llm.with_structured_output(pydantic_schema)
        messages = [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_prompt)
        ]
        return llm_with_structure.invoke(messages)
