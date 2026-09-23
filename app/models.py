from sqlalchemy import Column, Integer, String
from .database import Base

class Player(Base):
    __tablename__ = "players"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    position = Column(String)
    number = Column(Integer)
    nationality = Column(String)
    photo_url = Column(String, nullable=True)  # Optional field for player photo URL