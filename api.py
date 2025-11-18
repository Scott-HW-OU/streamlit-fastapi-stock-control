# File: api.py
import json
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List

app = FastAPI()

# --- CORS (Same as before) ---
origins = ["http://localhost", "http://localhost:8501"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# --- Data Loading ---
INVENTORY_FILE = "inventory.json"
inventory_db = []

def load_inventory():
    """Reads the inventory data from the JSON file into memory."""
    global inventory_db
    try:
        with open(INVENTORY_FILE, "r") as f:
            inventory_db = json.load(f)
    except FileNotFoundError:
        inventory_db = []
        print("WARNING: inventory.json not found. API will start with empty data.")

def save_inventory():
    """Saves the current in-memory inventory back to the JSON file."""
    with open(INVENTORY_FILE, "w") as f:
        json.dump(inventory_db, f, indent=2)

# Load data on startup
@app.on_event("startup")
def startup_event():
    load_inventory()

# --- Pydantic Models ---
class ReorderRequest(BaseModel):
    item_ids: List[str] # A list of item IDs (SKUs) to reorder

# --- API Endpoints ---
@app.get("/api/inventory")
def get_inventory():
    """
    Returns the entire product inventory.
    """
    return {"inventory": inventory_db}

@app.post("/api/reorder")
def place_reorder(request: ReorderRequest):
    """
    Simulates placing a reorder.
    It finds the items by ID and adds 50 to their stock.
    """
    items_reordered = []
    
    for item_id in request.item_ids:
        found = False
        for item in inventory_db:
            if item["id"] == item_id:
                # Simulate reorder by adding 50 to stock
                item["current_stock"] += 50
                items_reordered.append(item["name"])
                found = True
                break
        if not found:
            raise HTTPException(status_code=404, detail=f"Item ID {item_id} not found.")
            
    # Save the updated inventory back to the file
    save_inventory()
    
    return {
        "message": "Reorder placed successfully!",
        "items_restocked": items_reordered,
        "new_stock_count": len(request.item_ids)
    }