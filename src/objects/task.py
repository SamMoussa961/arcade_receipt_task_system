from dataclasses import dataclass

""" 
DESC: Task object
PARAM: $name: string, $points: int
    """
@dataclass(frozen=True)
class Task:
    name: str
    points: int
