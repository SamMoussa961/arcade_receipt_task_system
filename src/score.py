import json
import os

SCORE_FILE = "score.json"

def load_score() -> int:
    if not os.path.exists(SCORE_FILE):
        return 0
    with open(SCORE_FILE, "r") as f:
        data = json.load(f)
        return data.get("total_score", 0)


def save_score(score: int):
    with open(SCORE_FILE, "w") as f:
        json.dump({"total_score": score}, f)


def score_bar(score: int) -> str:
    total_length = 24
    score_str = f"{score} PTS"
    
    bar_length = total_length - len(score_str) - 1
    
    max_score = 250
    
    filled_length = int((min(score, max_score) / max_score) * bar_length)
    
    filled_length = min(filled_length, bar_length)
    
    empty_length = bar_length - filled_length
    bar = "█" * filled_length
    
    if empty_length >= 3:
        gradient = "▓▒░"
        gradient = gradient[:empty_length]
    else:
        gradient = " " * empty_length
    
    return f"{bar}{gradient} {score_str}\n"