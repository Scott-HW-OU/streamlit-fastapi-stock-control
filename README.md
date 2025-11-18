# 👕 Full-Stack Stock Control System (FastAPI + Streamlit)

This project is a complete, full-stack inventory management application built entirely in Python. It uses a **FastAPI** backend to serve data and handle logic, and a **Streamlit** frontend to provide a user-friendly dashboard for viewing inventory and placing reorders.

This application is a demo of how these two powerful frameworks can be combined to create a robust, interactive, and data-driven web application.

## 🚀 Core Technologies

* **Backend:** FastAPI, Uvicorn
* **Frontend:** Streamlit
* **Data Handling:** Pandas (in Streamlit), Pydantic (in FastAPI)
* **API Communication:** Requests
* **"Database":** A simple `inventory.json` file to simulate data persistence.

## ✨ Features

* **FastAPI Backend:**
    * Serves the entire inventory from the `inventory.json` "database".
    * Provides a `POST /api/reorder` endpoint to simulate placing an order, which updates the stock levels.
    * Automatically re-saves the updated inventory back to the JSON file, persisting changes.
* **Streamlit Frontend:**
    * Displays the full inventory in a clean, filterable, and searchable table.
    * Uses color-coding to **highlight low-stock items** that are below their reorder level.
    * Identifies items needing a reorder and groups them by supplier.
    * Allows users to "Place Reorder" with a single button, which calls the backend API and updates the stock.
    * Caches data for performance but automatically refreshes after an order is placed.

## 📁 Project Structure

project-root/ 
│ 
├── api.py # The FastAPI backend server 
├── app.py # The Streamlit frontend application 
├── generate_data.py # One-time script to create the inventory.json 
├── inventory.json # Our JSON "database" file 
├── requirements.txt # All Python dependencies 
└── README.md # This file

## ⚙️ Installation & Setup

Follow these steps to get the application running on your local machine.

### 1. Clone the Repository

(If this were on GitHub, you would clone it. For now, just ensure all your files are in the same directory.)

### 2. Create a Virtual Environment (Recommended)

```bash
# Create a new virtual environment
python -m venv venv

# Activate it

# On macOS/Linux:
source venv/bin/activate

# On Windows:
.\venv\Scripts\activate
```

3. Install Dependencies
Install all the required packages from the requirements.txt file.

```Bash
pip install -r requirements.txt
```

4. Generate Initial Data
Before you can run the servers, you need to create the inventory.json file. Run the generate_data.py script once.

```Bash
python generate_data.py
```

You should now see an inventory.json file in your directory.

▶️ How to Run the Application
You must run the backend and frontend in two separate terminal windows.

1. Terminal 1: Run the Backend (FastAPI)
In your first terminal, start the Uvicorn server to run your FastAPI app.

```Bash
uvicorn api:app --reload
```
You should see a message indicating the server is running, typically at http://127.0.0.1:8000.

2. Terminal 2: Run the Frontend (Streamlit)
In your second terminal (with the virtual environment still active), run the Streamlit app.

```Bash
streamlit run app.py
```

Streamlit will automatically open your default web browser and navigate to the application, typically at http://localhost:8501.

You can now use the Stock Control System!

API Endpoints
The FastAPI backend provides the following endpoints:

GET /api/inventory

Description: Fetches the complete list of all inventory items.

Response: {"inventory": [...]}

POST /api/reorder

Description: Simulates a reorder for a list of item IDs. It adds 50 to the stock of each item provided.

Request Body: {"item_ids": ["SKU-123", "SKU-456"]}

Response: {"message": "Reorder placed successfully!", ...}