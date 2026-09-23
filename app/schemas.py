from pydantic import BaseModel
from typing import Optional

# Base schema (what a player looks like)
class PlayerBase(BaseModel):
    name: str
    position: str
    number: int
    nationality: str
    photo_url: Optional[str] = None # We will add photos later!

# Schema for creating a player (what the user sends)
class PlayerCreate(PlayerBase):
    pass

# Schema for returning a player (what the API sends back)
class PlayerResponse(PlayerBase):
    id: int

    class Config:
        from_attributes = True # Tells Pydantic to read data from SQLAlchemy models