from langchain_core.messages import HumanMessage, SystemMessage
from tenacity import retry, stop_after_attempt, wait_exponential
from config import OLLAMA_BASE_URL, DEFAULT_MODEL, LLM_PROVIDER, HF_TOKEN, HF_MODEL_ID


class LLMService:
    def __init__(self, temperature: float = 0.0):
        if LLM_PROVIDER == "huggingface":
            from langchain_huggingface import ChatHuggingFace, HuggingFaceEndpoint
            
            # Hugging Face Serverless API Endpoint
            llm = HuggingFaceEndpoint(
                repo_id=HF_MODEL_ID,
                huggingfacehub_api_token=HF_TOKEN,
                temperature=temperature if temperature > 0 else 0.01,
                task="text-generation",
                max_new_tokens=1024
            )
            self.llm = ChatHuggingFace(llm=llm)
        else:
            from langchain_ollama import ChatOllama
            
            self.llm = ChatOllama(
                base_url=OLLAMA_BASE_URL,
                model=DEFAULT_MODEL,
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
