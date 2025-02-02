from fastapi import FastAPI, HTTPException

app = FastAPI()

items = []

@app.get("/")
def root():
    return {"Hello" : "World"}

@app.post("/items")
def create_items(item : str):
    items.append(item)
    return items

@app.get("/items/{item_id}")
def show_items(item_id : int) -> str:
    item = items[item_id]
    return item

@app.delete("/items/{item_id}")
def delete_items(item_id: int):
    if item_id < 0 or item_id >= len(items):
        raise HTTPException(status_code=404, detail="Item not found")
        
    deleted_item = items.pop(item_id)
    return {"message": "Item deleted", "deleted_item": deleted_item, "remaining_items": items}