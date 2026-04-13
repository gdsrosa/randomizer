from uuid import UUID, uuid4

from pydantic import BaseModel, Field


class ItemRequest(BaseModel):
    id: UUID = Field(default_factory=lambda: uuid4())
    name: str = Field(min_length=1, max_length=100, description="The name of the item")


class ItemResponse(BaseModel):
    message: str
    item: str


class ItemListResponse(BaseModel):
    original_order: list[ItemRequest]
    randomized_order: list[ItemRequest]
    count: int


class ItemUpdateResponse(BaseModel):
    message: str
    old_item: str
    new_item: str


class ItemDeleteResponse(BaseModel):
    message: str
    deleted_item_id: UUID
    remaining_items_count: int
