# =================================================================================
# Main FastAPI Application
# =================================================================================
# This file ties everything together. It creates the FastAPI app, sets up the
# database, defines the API endpoints for CRUD operations, and serves a simple
# HTML UI for interaction.
# =================================================================================

from fastapi import FastAPI, Depends, Request, Form, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.orm import Session
import os

from . import models, schemas
from .database import SessionLocal, engine, get_db

# Create all database tables defined in models.py
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

# Setup for Jinja2 templates to render HTML
templates = Jinja2Templates(directory="templates")

# A simple environment variable to show how you might pass configuration
STAGE = os.environ.get("STAGE", "local")

# --- API Endpoints (for programmatic access) ---

@app.post("/api/items/", response_model=schemas.Item)
def create_item(item: schemas.ItemCreate, db: Session = Depends(get_db)):
    """
    Create a new item in the database.
    """
    db_item = models.Item(name=item.name, description=item.description)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item

@app.get("/api/items/", response_model=list[schemas.Item])
def read_items(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    Retrieve a list of items from the database.
    """
    items = db.query(models.Item).offset(skip).limit(limit).all()
    return items

@app.get("/api/items/{item_id}", response_model=schemas.Item)
def read_item(item_id: int, db: Session = Depends(get_db)):
    """
    Retrieve a single item by its ID.
    """
    db_item = db.query(models.Item).filter(models.Item.id == item_id).first()
    if db_item is None:
        raise HTTPException(status_code=404, detail="Item not found")
    return db_item

# --- HTML UI Endpoints (for browser interaction) ---

@app.get("/", response_class=HTMLResponse)
async def get_items_ui(request: Request, db: Session = Depends(get_db)):
    """
    Renders the main UI page, displaying a list of items and a form to add new ones.
    """
    items = db.query(models.Item).all()
    return templates.TemplateResponse("index.html", {"request": request, "items": items, "stage": STAGE})

@app.post("/add-item", response_class=RedirectResponse)
async def add_item_ui(name: str = Form(...), description: str = Form(""), db: Session = Depends(get_db)):
    """
    Handles the form submission from the UI to create a new item.
    """
    new_item = models.Item(name=name, description=description)
    db.add(new_item)
    db.commit()
    # Redirect back to the main page to see the updated list
    return RedirectResponse(url="/", status_code=303)

@app.get("/health")
def health_check():
    """
    Health check endpoint used by the Application Load Balancer.
    """
    return {"status": "ok"}