from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


def create_database(url: str):
    if url.startswith("postgresql://"):
        url = url.replace("postgresql://", "postgresql+psycopg://", 1)
    options = {"pool_pre_ping": True, "hide_parameters": True}
    if not url.startswith("sqlite"):
        options.update(
            pool_size=5, max_overflow=5, pool_timeout=10, connect_args={"connect_timeout": 10}
        )
    engine = create_engine(url, **options)
    return engine, sessionmaker(engine, expire_on_commit=False)
