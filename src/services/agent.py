import os
import re
import requests
import time
import json
from dotenv import load_dotenv
from pathlib import Path

load_dotenv()
BASE_DIR = Path(__file__).resolve().parent.parent.parent

ACCESS_KEY = os.getenv("AGENT_ACCESS_KEY")
AGENT_URL = os.getenv("AGENT_URL")
MODEL = os.getenv("AGENT_MODEL")
CONFIG_DIR = BASE_DIR / "config"
INPUT_DIR = BASE_DIR / "inputs"
SYSTEM_PROMPT_FILE = CONFIG_DIR / "system_prompt.txt"
USER_PROMPT_FILE = INPUT_DIR / "user_prompt.txt"


user_prompt_file = "user_prompt.txt"

with open(USER_PROMPT_FILE, encoding="utf-8") as f:
    user_prompt = f.read()

with open(SYSTEM_PROMPT_FILE, encoding="utf-8") as f:
    SYSTEM_PROMPT = f.read()

def ask_agent(user_input: str):
    prompt = user_prompt + user_input
    t0 = time.monotonic()

    try:
        resp = requests.post(AGENT_URL, 
            headers={"Authorization": "Bearer " + ACCESS_KEY},
            json={
                "model": MODEL,
                "messages": [
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": prompt}
                ],
                "temperature":0.0,
                "chat_template_kwargs": {"enable_thinking": False},
            }, timeout=60)
        
        resp.raise_for_status()

        body = resp.json()

        text = body["choices"][0]["message"]["content"].strip()

        

        text = re.sub(r'<think>.*?</think>', '', text, flags=re.DOTALL)
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
            tokens_used = body.get("usage", {}).get("total_tokens")
            finish_reason = body["choices"][0].get("finish_reason")
            if finish_reason == "length":
                print(f"Response was truncated (finish_reason=length, total_tokens={tokens_used}). Increase max_new_tokens on the server.")
            print("\nRaw response:")
            print(text)

        tokens_used = body.get("usage", {}).get("total_tokens")
        print(f"token used: {tokens_used}")
    except Exception as e:
        latency_ms = int((time.monotonic() - t0) * 1000)
        print(f"    [ERROR] {e}")
        
    latency_ms = int((time.monotonic() - t0) * 1000)

if __name__ == '__main__':
    ask_agent("Clean room")
