from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from .config import settings

# Default to sqlite for tests if postgres not available, but production uses postgres
# Using settings.DATABASE_URL, fallback to sqlite memory for import safety
DATABASE_URL = settings.DATABASE_URL

# For SQLite, need check_same_thread False
connect_args = {}
if DATABASE_URL.startswith("sqlite"):
    connect_args = {"check_same_thread": False}

engine = create_engine(DATABASE_URL, connect_args=connect_args, future=True)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine, future=True)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
