from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, DeclarativeBase
from .config import settings

connect_args = {"check_same_thread": False} if settings.database_url.startswith("sqlite") else {}
engine_options = {"pool_pre_ping": True}
if not settings.database_url.startswith("sqlite"):
    engine_options.update({"pool_recycle": 1800, "pool_size": 5, "max_overflow": 10})
engine = create_engine(settings.database_url, connect_args=connect_args, **engine_options)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

class Base(DeclarativeBase):
    pass

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
