from pydantic import BaseModel, field_validator
from datetime import datetime

class RequiredFieldsExcelBase(BaseModel):
    record_id: str
    file:str
    download_url: str
    date: datetime
    uploaded_by: str
    
    @field_validator('download_url')
    def validate_download_url(cls, v):
        if not v.startswith("http"):
            raise ValueError("download_url must be a valid URL starting with http or https")
        return v