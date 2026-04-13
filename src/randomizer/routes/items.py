import random
from uuid import UUID

from fastapi import APIRouter, HTTPException

from ..database import items_db
from ..schemas import (
    ItemDeleteResponse,
    ItemListResponse,
    ItemRequest,
    ItemResponse,
    ItemUpdateResponse,
)

router = APIRouter(prefix="/items", tags=["Random Items Management"])


@router.post("", response_model=ItemResponse)
def create_item(item: ItemRequest):
    existing = items_db.get_by_name(item.name)
    if existing:
        raise HTTPException(status_code=400, detail="Item already exists.")

    items_db.add(item)
    return ItemResponse(message="Item created successfully.", item=item.name)


@router.get("", response_model=ItemListResponse)
def get_randomized_items():
    all_items = items_db.get_all()
    randomized_items = all_items.copy()
    random.shuffle(randomized_items)

    return ItemListResponse(
        original_order=all_items,
        randomized_order=randomized_items,
        count=len(all_items),
    )


@router.put("/{item_id}", response_model=ItemUpdateResponse)
def update_item(item_id: UUID, item: ItemRequest):
    item_to_update = items_db.get_by_id(str(item_id))

    if not item_to_update:
        raise HTTPException(status_code=404, detail="Item not found")

    new_name: str | None = item.name
    if not new_name:
        raise HTTPException(
            status_code=400, detail="'name' field is required in request body"
        )

    existing_with_name = next(
        (i for i in items_db.get_all() if i.name == new_name and i.id != item_id),
        None,
    )
    if existing_with_name:
        raise HTTPException(
            status_code=409, detail="An item with that name already exists"
        )

    updated = items_db.update(str(item_id), new_name)

    return ItemUpdateResponse(
        message="Item updated successfully",
        old_item=item_to_update.name,
        new_item=updated.name if updated else new_name,
    )


@router.delete("/{item_id}", response_model=ItemDeleteResponse)
def delete_item(item_id: UUID):
    item_to_delete = items_db.get_by_id(str(item_id))

    if not item_to_delete:
        raise HTTPException(status_code=404, detail="Item not found")

    items_db.delete(str(item_id))

    return ItemDeleteResponse(
        message="Item deleted successfully",
        deleted_item_id=item_id,
        remaining_items_count=len(items_db.get_all()),
    )
