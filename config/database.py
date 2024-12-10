from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

from config import settings

if settings.POSTGRESQL_DATABASE_URL:
    engine = create_engine(
        settings.POSTGRESQL_DATABASE_URL,
        connect_args={"options": "-c timezone=utc"},
    )
    SessionLocal = sessionmaker(
        autocommit=False,
        autoflush=False,
        bind=engine,
    )

Base = declarative_base()


def get_db():
    if settings.POSTGRESQL_DATABASE_URL:
        db = SessionLocal()
        try:
            yield db
        finally:
            db.close()


def create_tables():
    if settings.POSTGRESQL_DATABASE_URL:
        Base.metadata.create_all(bind=engine)
