import re
import json
from llama_loader import llm

user_prompt_file = "user_prompt.txt"
system_prompt_file = "system_prompt.txt"

with open(user_prompt_file, encoding="utf-8") as f:
    user_prompt = f.read()

with open(system_prompt_file, encoding="utf-8") as f:
    system_prompt = f.read()

resp = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_prompt}
    ],
    max_tokens=500,
    temperature=0.3,
    top_p=0.85,
    repeat_penalty=1.15
)

text = resp["choices"][0]["message"]["content"].strip()

# Regex to extract all JSON objects
matches = re.findall(r'\{.*?\}', text, re.DOTALL)
data = []

for m in matches:
    try:
        data.append(json.loads(m))
    except json.JSONDecodeError:
        print("Failed to parse JSON object:")
        print(m)

for category_obj in data:
    print(json.dumps(category_obj, indent=2))
