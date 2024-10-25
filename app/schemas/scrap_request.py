from enum import Enum

from pydantic import BaseModel, Field


class ScrapRequestStatus(Enum):
    REQUEST_CREATED = "request_created"
    IN_PROGRESS = "in_progress"
    COMPLETED = "completed"
    FAILED = "failed"


class ScrapRequestConfig(BaseModel):
    page_number: int = Field(..., description="Number of pages to extract")



class ScrapRequestCreate(BaseModel):
    user: int = Field(..., description="ID of the user making the request")
    page_url: str = Field(..., description="URL of the page to scrape")
    config: ScrapRequestConfig = Field(
        ...,
        description="Configuration parameters",
        example={"page_number": 5, "keys": ["product_name", "product_price", "product_image"]}
    )


class ScrapRequestData(BaseModel):
    id: int
    user: int
    page_url: str
    status: ScrapRequestStatus
    config: ScrapRequestConfig

    class Config:
        from_attributes = True
        from_orm = True
