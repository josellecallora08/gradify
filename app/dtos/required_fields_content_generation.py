from pydantic import BaseModel
from datetime import datetime

class RequiredFieldContentGeneration(BaseModel):
    record_id: str
    file:str
    youtube_link: str
    date_uploaded: datetime
    uploaded_by: str
    
