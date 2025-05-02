from dataclasses import dataclass
from typing import Dict, Any
from datetime import datetime
from uuid import uuid4

@dataclass
class Task:
    payload: Dict[str, Any]
    type: str
    uuid: str = uuid4()
    failed_at: datetime = None
    no_of_retries: int = 0
    
    def increment_retry(self):
        self.no_of_retries += 1

    def refresh_failed_at(self):
        self.failed_at = None
    
    def update_failed_at(self):
        self.failed_at = datetime.now()