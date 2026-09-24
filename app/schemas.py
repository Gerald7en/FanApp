from pydantic import BaseModel
from typing import Optional

# --- PLAYER SCHEMAS ---
class PlayerBase(BaseModel):
    name: str
    position: str
    number: int
    nationality: str
    photo_url: Optional[str] = None 

class PlayerCreate(PlayerBase):
    pass

class PlayerResponse(PlayerBase):
    id: int

    class Config:
        from_attributes = True

# --- MEDIA SCHEMAS ---
class MediaBase(BaseModel):
    description: Optional[str] = None
    media_type: str

class MediaCreate(MediaBase):
    pass

class MediaResponse(MediaBase):
    id: int
    filename: str

    class Config:
        from_attributes = True

# --- PLAYER STATS SCHEMAS ---
class PlayerStatsBase(BaseModel):
    player_id: int
    match_date: str
    goals: int = 0
    assists: int = 0
    tackles: int = 0
    duels_won: int = 0
    xg: float = 0.0
    pass_accuracy: float = 0.0
    distance_covered: float = 0.0

class PlayerStatsResponse(PlayerStatsBase):
    id: int

    class Config:
        from_attributes = True