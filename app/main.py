from fastapi import FastAPI
from . import models
from .database import engine

# Create the database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Spurs Fan App API",
    description="Backend API for tracking Tottenham Hotspur performance, media, and stats.",
    version="1.0.0"
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the Spurs Fan App API! COYS! ⚽🤍"}

@app.get("/players")
def get_players():
    return {"message": "Player list endpoint coming soon!"}