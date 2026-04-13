import random
from typing import Annotated
from uuid import UUID, uuid4

from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field

tags_metadata = [
    {
        "name": "Random Playground",
        "description": "Generate random numbers",
    },
    {
        "name": "Random Items Management",
        "description": "Create, shuffle, read, update and delete items",
    },
]

app = FastAPI(
    title="Randomizer API",
    description="An API for generating random numbers and managing random items.",
    version="1.0.0",
    openapi_tags=tags_metadata,
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET, POST, PUT, DELETE"],
    allow_headers=["*"],
)


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


items_db: list[ItemRequest] = []


@app.get("/", tags=["Random Playground"])
def home():
    return {"message": "Welcome to the Randomizer API!"}


@app.get("/random/{max_value}", tags=["Random Playground"])
def get_random_number(max_value: int):
    if max_value < 1:
        return {"error": "max_value must be greater than 0."}

    random_number = random.randint(1, max_value)

    return {"random_number": random_number, "max_value": max_value}


@app.get("/random-between/", tags=["Random Playground"])
def get_random_number_between(
    min_value: Annotated[
        int,
        Query(
            title="Minimum value",
            description="The minimum value for the random number",
            ge=1,
            le=1000,
        ),
    ] = 1,
    max_value: Annotated[
        int,
        Query(
            title="Maximum value",
            description="The maximum value for the random number",
            ge=1,
            le=1000,
        ),
    ] = 99,
):
    if min_value > max_value:
        raise HTTPException(
            status_code=400, detail="min_value must be less than or equal to max_value."
        )

    random_number = random.randint(min_value, max_value)

    return {
        "random_number": random_number,
        "min_value": min_value,
        "max_value": max_value,
    }


@app.post("/items", response_model=ItemResponse, tags=["Random Items Management"])
def create_item(item: ItemRequest):

    if [item for i in items_db if i.name == item.name]:
        raise HTTPException(status_code=400, detail="Item already exists.")

    item = ItemRequest(id=item.id, name=item.name)
    items_db.append(item)

    return ItemResponse(message="Item created successfully.", item=item.name)


@app.get("/items", response_model=ItemListResponse, tags=["Random Items Management"])
def get_randomized_items():
    randomized_items = items_db.copy()

    random.shuffle(randomized_items)

    return ItemListResponse(
        original_order=[item for item in items_db],
        randomized_order=[item for item in randomized_items],
        count=len(items_db),
    )


@app.put(
    "/items/{item_id}",
    response_model=ItemUpdateResponse,
    tags=["Random Items Management"],
)
def update_item(item_id: UUID, item: ItemRequest):
    item_to_update = [i for i in items_db if i.id == item_id]

    if not item_to_update:
        raise HTTPException(status_code=404, detail="Item not found")

    new_name: str | None = item.name
    if not new_name:
        raise HTTPException(
            status_code=400, detail="'name' field is required in request body"
        )

    if new_name in [i.name for i in items_db if i.name != item_to_update[0].name]:
        raise HTTPException(
            status_code=409, detail="An item with that name already exists"
        )

    index: int = items_db.index(item_to_update[0])
    items_db[index] = ItemRequest(id=item_id, name=new_name)

    return ItemUpdateResponse(
        message="Item updated successfully",
        old_item=item_to_update[0].name,
        new_item=new_name,
    )


@app.delete(
    "/items/{item_id}",
    response_model=ItemDeleteResponse,
    tags=["Random Items Management"],
)
def delete_item(item_id: UUID):
    item_to_delete = [item for item in items_db if item.id == item_id]

    if not item_to_delete:
        raise HTTPException(status_code=404, detail="Item not found")

    items_db.remove(item_to_delete[0])

    return ItemDeleteResponse(
        message="Item deleted successfully",
        deleted_item_id=item_id,
        remaining_items_count=len(items_db),
    )
