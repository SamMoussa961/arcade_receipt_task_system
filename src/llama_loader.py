import os
from dotenv import load_dotenv
from llama_cpp import Llama

load_dotenv()

MODEL_PATH = os.getenv("MODEL_PATH")
MAX_CONTEXT = int(os.getenv("MAX_CONTEXT", 1024))
BATCH_SIZE = int(os.getenv("BATCH_SIZE", 512))

n_gpu_layers = -1

print(f"Initializing model with GPU offload hint n_gpu_layers={n_gpu_layers}")

llm = Llama(
    model_path=MODEL_PATH,
    n_ctx=MAX_CONTEXT,
    n_batch=BATCH_SIZE,
    n_gpu_layers=n_gpu_layers,
    verbose=True
)
