from .database import engine, SessionLocal
from . import models
from .schemas import PlayerCreate
from .crud import create_player

# Ensure tables are created
models.Base.metadata.create_all(bind=engine)

db = SessionLocal()

# The Starting XI + Manager + Key Subs (2023/2024 Season)
squad = [
    {"name": "Antonin Kinsky", "position": "Goalkeeper", "number": 31, "nationality": "Czech Republic"},
    {"name": "Martin Dubravka", "position": "Goalkeeper", "number": 39, "nationality": "Slovakia"},
    {"name": "Brandon Austin", "position": "Goalkeeper", "number": 40, "nationality": "England"},
    {"name": "Ben Davies", "position": "Defender", "number": 33, "nationality": "Wales"},
    {"name": "Destiny Udogie", "position": "Defender", "number": 13, "nationality": "Italy"},
    {"name": "Marcos Senesi", "position": "Defender", "number": 5, "nationality": "Argentina"},
    {"name": "Micky van de Ven", "position": "Defender", "number": 37, "nationality": "Netherlands"},
    {"name": "Pedro Porro", "position": "Defender", "number": 23, "nationality": "Spain"},
    {"name": "Jan Paul Van Hecke", "position": "Defender", "number": 6, "nationality": "Netherlands"},
    {"name": "Andy Robertson", "position": "Defender", "number": 3, "nationality": "Scotland"},
    {"name": "Tosin Adarabioyo", "position": "Defender", "number": 4, "nationality": "England"},
    {"name": "Sandro Tonali", "position": "Midfielder", "number": 16, "nationality": "Italy"},
    {"name": "Rodrigo Bentancur", "position": "Midfielder", "number": 30, "nationality": "Uruguay"},
    {"name": "Conor Gallagher", "position": "Midfielder", "number": 8, "nationality": "England"},
    {"name": "Archie Gray", "position": "Midfielder", "number": 14, "nationality": "England"},
    {"name": "Lucas Bergvall", "position": "Midfielder", "number": 15, "nationality": "Sweden"},
    {"name": "Xavi Simons", "position": "Midfielder", "number": 7, "nationality": "Netherlands"},
    {"name": "James Maddison", "position": "Midfielder", "number": 10, "nationality": "England"},
    {"name": "Dejan Kulusevski", "position": "Midfielder", "number": 21, "nationality": "Sweden"},
    {"name": "Mateus Fernandes", "position": "Midfielder", "number": 18, "nationality": "Portugal"},
    {"name": "Mohammed Kudus", "position": "Foward", "number": 20, "nationality": "Ghana"},
    {"name": "Savinho Savio", "position": "Foward", "number": 17, "nationality": "Brazil"},
    {"name": "Wilson Odobert", "position": "Foward", "number": 28, "nationality": "France"},
    {"name": "Mathys Tel", "position": "Forward", "number": 11, "nationality": "France"},
    {"name": "Dominic Solanke", "position": "Forward", "number": 19, "nationality": "England"},
    {"name": "Omar Marmoush", "position": "Forward", "number": 22, "nationality": "Egypt"},
    {"name": "Roberto De Zerbi", "position": "Manager", "number": 0, "nationality": "Italy"},
]

print("Seeding database with Spurs squad...")
for player_data in squad:
    player = PlayerCreate(**player_data)
    create_player(db, player)

print("✅ Squad seeded successfully! COYS!")
db.close()