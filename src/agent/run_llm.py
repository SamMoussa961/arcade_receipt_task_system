import os
import requests
import time
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent.parent

AGENT_URL = os.getenv("AGENT_URL")
MODEL = os.getenv("AGENT_MODEL")
CONFIG_DIR = BASE_DIR / "config"
INPUT_DIR = BASE_DIR / "input"
SYSTEM_PROMPT_FILE = CONFIG_DIR / "system_prompt.txt"


user_prompt_file = "user_prompt.txt"
system_prompt_file = os.getenv("")

with open(user_prompt_file, encoding="utf-8") as f:
    user_prompt = f.read()

with open(SYSTEM_PROMPT_FILE, encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

def ask_agent():
    resp = requests.post(URL, json={
        "model": MODEL,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_prompt}
        ],
        max_tokens=1000,
        temperature=0.2,
        top_p=0.9,
        repeat_penalty=1.1
    )

text = resp["choices"][0]["message"]["content"].strip()

text = re.sub(r'^```(?:json)?\s*', '', text, flags=re.MULTILINE)
text = re.sub(r'\s*```$', '', text)
text = text.strip()

if not text.startswith('['):
    if text.startswith('{'):
        objects = re.split(r'\n(?={)', text)
        text = '[' + ','.join(objects) + ']'
        print("The response was not a JSON array.")

try:
    data = json.loads(text)

    if not isinstance(data,list):
        raise ValueError("Response must be a JSON array")
    
    if len(data) == 0:
        raise ValueError("Response array is empty")
    
    valid_categories = {"MAINTENANCE", "ASSIGNMENTS", "FOCUS", "WELLNESS", "ERRANDS"}

    breakdown_warnings = []

    for idx, category_obj in enumerate(data):
        if not all(key in category_obj for key in ["category", "tasks", "deadline"]):
            raise ValueError(f"Object {idx} missing required keys")
        
        if category_obj.get("category") not in valid_categories:
            print(f"Invalid category '{category_obj['category']}' in object {idx}")

        if not isinstance(category_obj["tasks"], list) or len(category_obj["tasks"]) == 0:
            raise ValueError(f"Object {idx} has invalid tasks array")
        
        for task in category_obj["tasks"]:
            if "name" not in task or "points" not in task:
                raise ValueError(f"Task in object {idx} missing name or points")
            
            if task["points"] >= 20:
                breakdown_warnings.append(
                    f"Task '{task['name']}' has {task['points']} points but wasn't broken down"
                )

        print(json.dumps(category_obj, indent=2))

    if breakdown_warnings:
        print("\n" + "\n".join(breakdown_warnings))

except json.JSONDecodeError as e:
    print(f"Failed to parse JSON: {e}")
    print("\nRaw response:")
    print(text)
except ValueError as e:
    print(f"Validation error: {e}")
    print("\n Parsed data:")
    print(json.dumps(data, indent=2))
