from pathlib import Path

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker, declarative_base
from .config import conf
from urllib.parse import quote_plus

SQLITE_DATABASE_URL = f"sqlite:///{Path(__file__).resolve().parents[2] / 'app.db'}"
MYSQL_DATABASE_URL = (
    f"mysql+pymysql://{conf.db_user}:{quote_plus(conf.db_password)}"
    f"@{conf.db_host}:{conf.db_port}/{conf.db_name}?charset=utf8mb4"
)


def _build_engine():
    try:
        mysql_engine = create_engine(MYSQL_DATABASE_URL, pool_pre_ping=True)
        with mysql_engine.connect() as connection:
            connection.execute(text("SELECT 1"))
        return mysql_engine
    except Exception:
        return create_engine(
            SQLITE_DATABASE_URL,
            connect_args={"check_same_thread": False},
        )


engine = _build_engine()
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
