from dataclasses import dataclass, field
from queue import Queue
from typing import List, Dict, Any
from ._task import Task
from datetime import datetime, timedelta
# test

@dataclass
class TaskQueue:
    tasks: Queue = Queue()

    def push(self, task: Task) -> None:
        self.tasks.put(task)

    def pop(self) -> Task:
        return self.tasks.get()

    def remaining(self):
        return self.tasks.qsize()
    
    def enqueue_many(self, tasks: List[Dict[str, Any]]):
        for task in tasks:
            type = task['assessment_type']
            created_task = Task(payload=task, type=type)
            self.tasks.put(created_task)

    def list_queued_items(self):
        return list(self.tasks.queue)
    
    def is_empty(self) -> bool:
        return self.tasks.empty()


