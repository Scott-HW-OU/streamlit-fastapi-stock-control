# File: generate_data.py
import json
import random

CATEGORIES = ["Men's", "Women's", "Children's", "Accessories"]
SUPPLIERS = ["Supplier A", "Supplier B", "Supplier C"]
PRODUCT_TYPES = {
    "Men's": ["T-Shirt", "Jeans", "Jacket", "Shoes"],
    "Women's": ["Dress", "Blouse", "Skirt", "Sandals"],
    "Children's": ["Onesie", "Sweater", "Sneakers", "Pajamas"],
    "Accessories": ["Hat", "Scarf", "Belt", "Sunglasses"]
}
COLORS = ["Red", "Blue", "Green", "Black", "White", "Grey", "Brown"]

inventory = []
for i in range(600):  # Create 600 products
    category = random.choice(CATEGORIES)
    product_base = random.choice(PRODUCT_TYPES[category])
    color = random.choice(COLORS)
    
    sku = f"{category[:3].upper()}-{product_base[:3].upper()}-{color[:3].upper()}-{i:03}"
    name = f"{color} {product_base}"
    
    current_stock = random.randint(0, 150)
    reorder_level = random.randint(20, 40) # A threshold
    
    inventory.append({
        "id": sku,
        "name": name,
        "category": category,
        "current_stock": current_stock,
        "reorder_level": reorder_level,
        "price": round(random.uniform(15.99, 99.99), 2),
        "supplier": random.choice(SUPPLIERS)
    })

# Write the data to a file
with open("inventory.json", "w") as f:
    json.dump(inventory, f, indent=2)

print("✅ Successfully generated inventory.json with 600 items.")