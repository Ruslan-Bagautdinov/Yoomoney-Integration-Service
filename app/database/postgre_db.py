from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker
import asyncpg


from app.database.database_base import Database
from app.database.models import Base
from app.config import HOME_DB, WORK_DATABASE_URL, LOCAL_DATABASE_URL

# Database URL
if HOME_DB is True:
    POSTGRE_DATABASE_URL = LOCAL_DATABASE_URL
else:
    POSTGRE_DATABASE_URL = WORK_DATABASE_URL


# Create an async engine
engine = create_async_engine(POSTGRE_DATABASE_URL, echo=False)

# Create a session maker
AsyncSessionMaker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class PostgresDatabase(Database):
    async def get_session(self):
        async with AsyncSessionMaker() as session:
            yield session

    async def init_db(self):
        try:
            async with engine.begin() as conn:
                print("Creating tables...")
                await conn.run_sync(Base.metadata.create_all)
                print("Tables created successfully.")
        except Exception as e:
            print(f"Error creating tables: {e}")