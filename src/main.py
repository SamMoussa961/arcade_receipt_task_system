import re
import json
from llm_backend import get_llm
from datetime import datetime

user_prompt_file = "user_prompt.txt"
system_prompt_file = "system_prompt.txt"

with open(user_prompt_file, encoding="utf-8") as f:
    user_prompt = f.read()

with open(system_prompt_file, encoding="utf-8") as f:
    system_prompt = f.read()

current_date = datetime.now().strftime("%B %d, %Y")
if "current date" not in user_prompt.lower():
    user_prompt = f"Current date: {current_date}\n\n{user_prompt}"

llm = get_llm()

resp = llm.create_chat_completion(
    messages=[
        {"role": "system", "content": system_prompt},
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
