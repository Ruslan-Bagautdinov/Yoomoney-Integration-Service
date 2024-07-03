from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker




from app.database.database_base import Database
from app.database.models import Base

# Database URL
DATABASE_URL = "sqlite+aiosqlite:///./test.db"

# Create an async engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Create a session maker
AsyncSessionMaker = sessionmaker(bind=engine, class_=AsyncSession, expire_on_commit=False)

class SQLiteDatabase(Database):
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
