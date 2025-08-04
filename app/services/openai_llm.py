from langchain_community.chat_models import ChatOpenAI
from app.utils.logger import get_logger
import os

logger = get_logger()

def get_llm():
    logger.info("Initializing OpenRouter LLM: deepseek/deepseek-r1-0528-qwen3-8b")
    return ChatOpenAI(
        openai_api_key=os.getenv("OPENROUTER_API_KEY"),
        openai_api_base="https://openrouter.ai/api/v1",
        model="deepseek/deepseek-r1-0528-qwen3-8b",
        temperature=0
    )
