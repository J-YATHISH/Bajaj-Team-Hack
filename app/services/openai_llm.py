from langchain_community.chat_models import ChatOpenAI
from app.utils.logger import get_logger
import os

logger = get_logger()

def get_llm():
    logger.info("Initializing OpenRouter LLM: qwen/qwen-2.5-72b-instruct")
    return ChatOpenAI(
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        model="qwen/qwen-2.5-72b-instruct",
        temperature=0
    )
