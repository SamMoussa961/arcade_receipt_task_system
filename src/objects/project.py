from dataclasses import dataclass
from typing import List
from task import Task

@dataclass
class Project:
    title: str
    category: str
    tasks: List[Task]
    deadline: str

    @property
    def total_points(self) -> int:
        return sum(task.points for task in self.tasks)

    def add_task(self, task: Task) -> None:
        self.tasks.append(task)
