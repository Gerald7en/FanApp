from sqlalchemy import Column, Integer, String
from .database import Base

class Player(Base):
    __tablename__ = "players"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    position = Column(String)
    number = Column(Integer)
    nationality = Column(String)
    photo_url = Column(String, nullable=True)

# --- NEW MEDIA MODEL ---
class Media(Base):
    __tablename__ = "media"
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, index=True)
    description = Column(String, nullable=True) # e.g., "Matchday vs Arsenal"
    media_type = Column(String) # "photo" or "video"