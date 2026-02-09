import os
from dotenv import load_dotenv

load_dotenv()

def get_llm():
    backend = str(os.getenv("LLM_BACKEND"))

    if backend.lower() == "llama_cpp":
        from llama_loader import llm
        return llm

    if backend.lower() == "vllm":
        from vllm_loader import llm
        return llm

    raise ValueError(f"Unknown LLM_BACKEND: {backend}")
