import random
from typing import Annotated

from fastapi import APIRouter, HTTPException, Query

router = APIRouter(prefix="", tags=["Random Playground"])


@router.get("/random/{max_value}")
def get_random_number(max_value: int):
    if max_value < 1:
        return {"error": "max_value must be greater than 0."}

    random_number = random.randint(1, max_value)

    return {"random_number": random_number, "max_value": max_value}


@router.get("/random-between/")
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
