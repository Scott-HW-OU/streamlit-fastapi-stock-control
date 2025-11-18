# File: app.py
import streamlit as st
import requests
import pandas as pd

# --- Page Configuration ---
st.set_page_config(
    page_title="Stock Control System",
    layout="wide"
)

API_URL = "http://127.0.0.1:8000/api"

# --- Data Loading Function ---
@st.cache_data(ttl=60) # Cache data for 1 minute
def load_data():
    """Fetches the full inventory from the FastAPI backend."""
    try:
        response = requests.get(f"{API_URL}/inventory")
        response.raise_for_status()
        data = response.json().get("inventory", [])
        return pd.DataFrame(data)
    except requests.exceptions.RequestException as e:
        st.error(f"Failed to load data from API: {e}")
        return pd.DataFrame() # Return empty dataframe on error

# --- Main Application ---
st.title("👕 Clothing Store Stock Control")

# --- Load Data ---
df = load_data()

if df.empty:
    st.warning("Could not load inventory. Is the backend API running?")
else:
    # --- Styling Function ---
    def highlight_low_stock(row):
        """Highlights a row red if stock is below reorder level."""
        if row['current_stock'] <= row['reorder_level']:
            return ['background-color: #FFA07A'] * len(row) # Light Salmon
        return [''] * len(row)

    # --- 1. Main Inventory Dashboard ---
    st.header("Inventory Dashboard")
    
    # Filters
    category_filter = st.multiselect(
        "Filter by Category:",
        options=df['category'].unique(),
        default=df['category'].unique()
    )
    
    filtered_df = df[df['category'].isin(category_filter)]
    
    # Display the styled DataFrame
    st.dataframe(
        filtered_df.style.apply(highlight_low_stock, axis=1),
        use_container_width=True,
        height=400,
        column_config={
            "id": "SKU",
            "name": "Product Name",
            "current_stock": "Stock",
            "reorder_level": "Reorder At"
        }
    )

    st.divider()

    # --- 2. Ordering Section ---
    st.header("🛒 Pending Reorders")
    
    # Find all items that need reordering
    low_stock_items = df[df['current_stock'] <= df['reorder_level']]
    
    if low_stock_items.empty:
        st.success("✅ All stock levels are healthy. No reorders needed.")
    else:
        st.warning(f"You have {len(low_stock_items)} items that need reordering.")
        
        # Group by supplier for easier ordering
        suppliers = low_stock_items['supplier'].unique()
        
        for supplier in suppliers:
            with st.expander(f"**{supplier}** ({len(low_stock_items[low_stock_items['supplier'] == supplier])} items)"):
                
                items_to_order_from_supplier = low_stock_items[
                    low_stock_items['supplier'] == supplier
                ]
                
                st.dataframe(items_to_order_from_supplier)
                
                if st.button(f"Place Reorder with {supplier}", key=supplier):
                    # Get the list of item IDs (SKUs) for this supplier
                    item_ids = items_to_order_from_supplier['id'].tolist()
                    
                    try:
                        # Call the POST endpoint
                        payload = {"item_ids": item_ids}
                        response = requests.post(f"{API_URL}/reorder", json=payload)
                        response.raise_for_status()
                        
                        st.success(f"Reorder placed for {supplier}! Items are being restocked.")
                        
                        # Clear cache and rerun to show new stock levels
                        st.cache_data.clear()
                        st.rerun()
                        
                    except requests.exceptions.RequestException as e:
                        st.error(f"Failed to place reorder: {e}")