import os
from vllm_mlx.models import MLXLanguageModel

MODEL_PATH = os.getenv("MODEL_PATH")
MAX_TOKENS = int(os.getenv("MAX_TOKENS"))
TEMPERATURE = float(os.getenv("TEMPERATURE"))
TOP_P = float(os.getenv("TOP_P"))
STOP_TOKENS = os.getenv("STOP_TOKENS").split(",")


class VllmMlxChatModel:
    def __init__(self, model_path: str) -> None:
        self._model = MLXLanguageModel(model_path)
        self._model.load()

    def create_chat_completion(
        self,
        messages,
        max_tokens=MAX_TOKENS,
        temperature=TEMPERATURE,
        top_p=TOP_P,
        stop=None,
        repeat_penalty=None,
        **kwargs,
    ):
        output = self._model.chat(
            messages=messages,
            max_tokens=max_tokens,
            temperature=temperature,
            top_p=top_p,
            stop=STOP_TOKENS if stop is None else stop,
        )

        return {
            "choices": [
                {
                    "message": {
                        "content": output.text,
                    }
                }
            ]
        }


llm = VllmMlxChatModel(MODEL_PATH)
