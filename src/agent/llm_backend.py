import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    backend = str(os.getenv("LLM_BACKEND"))

    if backend.lower() == "llama_cpp":
        from src.agent.llama_loader import llm
        return llm

    if backend.lower() == "vllm":
        from src.agent.vllm_loader import llm
        return llm

    raise ValueError(f"Unknown LLM_BACKEND: {backend}")
