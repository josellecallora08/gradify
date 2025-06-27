from pydantic import BaseModel, field_validator
from datetime import datetime
from typing import Optional

class TraineeEvaluation(BaseModel):
    date: datetime
    username: str
    email: str
    status: str
    result: Optional[str]
    agent: str
    user_rating: Optional[float]
    name: str

    @field_validator('user_rating')
    def validate_user_rating(cls, v):
        if v is not None and (v < 0 or v > 100):
            raise ValueError("User rating must be between 0 and 100")
        return v 