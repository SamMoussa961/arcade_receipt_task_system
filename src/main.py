from llama_loader import llm
import json

prompt_file = 'prompt.txt'

with open(prompt_file, encoding="utf-8") as template:
            prompt = template.read()

resp = llm(prompt, max_tokens=200)
text = resp["choices"][0]["text"]

# Remove leading/trailing whitespace and newlines
text = text.strip()

try:
    data = json.loads(text)
except json.JSONDecodeError:
    print("Output is not valid JSON. Raw text:", text)
    data = None

print(data)

