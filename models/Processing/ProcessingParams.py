from pydantic import BaseModel, Field
from typing import Optional
from models.Processing.ProcessingEnum import EnumClassification


class ProcessingParams(BaseModel):
    year : int = Field(ge=1970, le=2023)
    classification: Optional[EnumClassification] = None