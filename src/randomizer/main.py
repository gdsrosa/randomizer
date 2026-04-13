from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .routes import items as items_router
from .routes import random as random_router

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

app.include_router(random_router.router)
app.include_router(items_router.router)


@app.get("/", tags=["Random Playground"])
def home():
    return {"message": "Welcome to the Randomizer API!"}
