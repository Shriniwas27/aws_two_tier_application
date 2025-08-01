# =================================================================================
# Pydantic Schemas (Data Transfer Objects)
# =================================================================================
# These Pydantic models define the shape of the data for your API. They are used
# for request validation, response serialization, and documentation. This ensures
# that the data flowing in and out of your API is well-structured.
# =================================================================================

from pydantic import BaseModel

class ItemBase(BaseModel):
    name: str
    description: str | None = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        from_attributes = True # Changed from orm_mode = True