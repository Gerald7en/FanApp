from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from . import models, schemas, crud
from .database import SessionLocal, engine

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spurs Fan App API",
    description="Backend API for tracking Tottenham Hotspur performance, media, and stats.",
    version="1.0.0"
)

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"message": "Welcome to the Spurs Fan App API! COYS! ⚽🤍"}

# --- UPDATED ENDPOINTS ---

@app.get("/players", response_model=List[schemas.PlayerResponse])
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    players = crud.get_players(db, skip=skip, limit=limit)
    return players

@app.post("/players", response_model=schemas.PlayerResponse)
def create_new_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    return crud.create_player(db=db, player=player)