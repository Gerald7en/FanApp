import io
import pandas as pd
import os
import shutil
from fastapi import FastAPI, Depends, HTTPException, File, UploadFile, Form
from fastapi.staticfiles import StaticFiles
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

# --- NEW: Setup Upload Directory ---
UPLOAD_DIRECTORY = "./uploads"
os.makedirs(UPLOAD_DIRECTORY, exist_ok=True)

# This allows us to access files in the browser like: http://127.0.0.1:8000/uploads/my_photo.jpg
app.mount("/uploads", StaticFiles(directory=UPLOAD_DIRECTORY), name="uploads")

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

@app.get("/players", response_model=List[schemas.PlayerResponse])
def read_players(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    players = crud.get_players(db, skip=skip, limit=limit)
    return players

@app.post("/players", response_model=schemas.PlayerResponse)
def create_new_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    return crud.create_player(db=db, player=player)

# --- NEW: MEDIA UPLOAD ENDPOINT ---
@app.post("/media/upload")
async def upload_media(
    file: UploadFile = File(...),
    description: str = Form(None),
    media_type: str = Form("photo"),
    db: Session = Depends(get_db)
):
    # 1. Save the physical file to the uploads folder
    file_location = f"{UPLOAD_DIRECTORY}/{file.filename}"
    with open(file_location, "wb") as file_object:
        shutil.copyfileobj(file.file, file_object)
    
    # 2. Save the file info to the database
    db_media = models.Media(
        filename=file.filename, 
        description=description, 
        media_type=media_type
    )
    db.add(db_media)
    db.commit()
    db.refresh(db_media)
    
    return {
        "message": f"Successfully uploaded '{file.filename}'!", 
        "file_url": f"http://127.0.0.1:8000/uploads/{file.filename}",
        "id": db_media.id
    }

# --- NEW: GET ALL MEDIA ---
@app.get("/media", response_model=List[schemas.MediaResponse])
def get_all_media(db: Session = Depends(get_db)):
    return db.query(models.Media).all()
# --- NEW: CSV DATA INGESTION ENDPOINT ---
@app.post("/stats/upload-csv")
async def upload_stats_csv(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # 1. Read the CSV file using Pandas
    contents = await file.read()
    df = pd.read_csv(io.BytesIO(contents))
    
    stats_added = 0
    
    # 2. Loop through each row in the CSV
    for index, row in df.iterrows():
        # Find the player in our database by their name
        player_name = row.get('name')
        player = db.query(models.Player).filter(models.Player.name == player_name).first()
        
        # If the player exists, create their stats
        if player:
            stat = models.PlayerStats(
                player_id=player.id,
                match_date=str(row.get('match_date', 'Unknown')),
                goals=int(row.get('goals', 0)),
                assists=int(row.get('assists', 0)),
                tackles=int(row.get('tackles', 0)),
                duels_won=int(row.get('duels_won', 0)),
                xg=float(row.get('xg', 0.0)),
                pass_accuracy=float(row.get('pass_accuracy', 0.0)),
                distance_covered=float(row.get('distance_covered', 0.0))
            )
            db.add(stat)
            stats_added += 1
            
    db.commit()
    
    return {
        "message": f"Successfully processed CSV! Added stats for {stats_added} players.",
        "players_processed": stats_added
    }

# --- NEW: GET STATS FOR A SPECIFIC PLAYER ---
@app.get("/stats/{player_id}", response_model=List[schemas.PlayerStatsResponse])
def get_player_stats(player_id: int, db: Session = Depends(get_db)):
    return db.query(models.PlayerStats).filter(models.PlayerStats.player_id == player_id).all()