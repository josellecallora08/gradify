from enum import Enum

class BubbleRecordStatus(Enum):
    DONE = "done"
    FAILED = "failed"
    FILE_DELETED = "file deleted"

    def __str__(self) -> str:
        return str(self.value)
