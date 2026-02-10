import os
from dotenv import load_dotenv
from llama_cpp import Llama

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH", "./models/Qwen2.5-7B-Instruct-GGUF")
MAX_CONTEXT = int(os.getenv("MAX_CONTEXT", 3072))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 384))

n_gpu_layers = int(os.getenv("N_GPU_LAYERS", 22))

print(f"Initializing model with GPU offload hint n_gpu_layers={n_gpu_layers}")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=MAX_CONTEXT,
    n_batch=BATCH_SIZE,
    n_gpu_layers=n_gpu_layers,
    verbose=True
)
