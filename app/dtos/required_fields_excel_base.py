from pydantic import BaseModel, field_validator

class RequiredFieldsExcelBase(BaseModel):
    record_id: str
    file:str
    download_url: str
    date: str
    uploaded_by: str