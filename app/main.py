from datetime import datetime, timezone
from bson import ObjectId
from fastapi import FastAPI, HTTPException, Query
from app.db import get_collection, get_client
from app.models import BookmarkCreate, BookmarkOut, BookmarkUpdate
from app.settings import settings

app = FastAPI(title=settings.app_name)


def serialize_bookmark(doc: dict) -> dict:
    return {
        "id": str(doc["_id"]),
        "url": doc["url"],
        "title": doc["title"],
        "tags": doc.get("tags", []),
        "favorite": doc.get("favorite", False),
        "created_at": doc["created_at"],
        "updated_at": doc["updated_at"],
    }


@app.on_event("startup")
async def startup():
    client = get_client()
    await client.admin.command("ping")
    collection = get_collection()
    await collection.create_index("title")
    await collection.create_index("favorite")


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.post(f"{settings.api_prefix}/bookmarks", response_model=BookmarkOut, status_code=201)
async def create_bookmark(payload: BookmarkCreate):
    now = datetime.now(timezone.utc)
    doc = {
        "url": str(payload.url),
        "title": payload.title,
        "tags": payload.tags,
        "favorite": payload.favorite,
        "created_at": now,
        "updated_at": now,
    }
    collection = get_collection()
    result = await collection.insert_one(doc)
    saved = await collection.find_one({"_id": result.inserted_id})
    return serialize_bookmark(saved)


@app.get(f"{settings.api_prefix}/bookmarks", response_model=list[BookmarkOut])
async def list_bookmarks(
    favorite: bool | None = None,
    tag: str | None = Query(default=None),
    limit: int = Query(default=20, ge=1, le=100),
):
    query = {}
    if favorite is not None:
        query["favorite"] = favorite
    if tag:
        query["tags"] = tag

    collection = get_collection()
    cursor = collection.find(query).sort("created_at", -1).limit(limit)
    result = []
    async for doc in cursor:
        result.append(serialize_bookmark(doc))
    return result


@app.get(f"{settings.api_prefix}/bookmarks/{{bookmark_id}}", response_model=BookmarkOut)
async def get_bookmark(bookmark_id: str):
    if not ObjectId.is_valid(bookmark_id):
        raise HTTPException(status_code=400, detail="Invalid bookmark id")

    collection = get_collection()
    doc = await collection.find_one({"_id": ObjectId(bookmark_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return serialize_bookmark(doc)


@app.patch(f"{settings.api_prefix}/bookmarks/{{bookmark_id}}", response_model=BookmarkOut)
async def update_bookmark(bookmark_id: str, payload: BookmarkUpdate):
    if not ObjectId.is_valid(bookmark_id):
        raise HTTPException(status_code=400, detail="Invalid bookmark id")

    update_data = {k: v for k, v in payload.model_dump(exclude_unset=True).items()}
    if not update_data:
        raise HTTPException(status_code=400, detail="No fields to update")

    update_data["updated_at"] = datetime.now(timezone.utc)

    collection = get_collection()
    result = await collection.update_one({"_id": ObjectId(bookmark_id)}, {"$set": update_data})
    if result.matched_count == 0:
        raise HTTPException(status_code=404, detail="Bookmark not found")

    doc = await collection.find_one({"_id": ObjectId(bookmark_id)})
    return serialize_bookmark(doc)


@app.delete(f"{settings.api_prefix}/bookmarks/{{bookmark_id}}", status_code=204)
async def delete_bookmark(bookmark_id: str):
    if not ObjectId.is_valid(bookmark_id):
        raise HTTPException(status_code=400, detail="Invalid bookmark id")

    collection = get_collection()
    result = await collection.delete_one({"_id": ObjectId(bookmark_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="Bookmark not found")
    return None
