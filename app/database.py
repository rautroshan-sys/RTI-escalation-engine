from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Using a local SQLite file for the hackathon MVP
SQLALCHEMY_DATABASE_URL = "sqlite:///./rti_audit.db"

# check_same_thread=False is required for SQLite + FastAPI concurrency
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    """Dependency injection for FastAPI route handlers."""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()