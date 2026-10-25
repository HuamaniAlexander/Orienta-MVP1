from alembic import context
from app.infrastructure.config import get_settings
from app.infrastructure.database import create_database
from sqlalchemy import text

engine, _ = create_database(get_settings().database_url)
with engine.connect() as connection:
    connection.execute(text("CREATE SCHEMA IF NOT EXISTS orienta"))
    connection.commit()
    context.configure(connection=connection, version_table_schema="orienta")
    with context.begin_transaction():
        context.run_migrations()
