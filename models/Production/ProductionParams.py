from pydantic import BaseModel, Field

class ProductionParams(BaseModel):
    year : int = Field(ge=1970, le=2023)