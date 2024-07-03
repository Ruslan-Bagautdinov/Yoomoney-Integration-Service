from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from app.config import DATABASE

if DATABASE == "sqlite":
    from app.database.sqlite_db import SQLiteDatabase as Database
elif DATABASE == "postgres":
    from app.database.postgre_db import PostgresDatabase as Database
else:
    raise ValueError("Unknown database type")

database = Database()


@asynccontextmanager
async def lifespan(app: FastAPI):
    await database.init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

# Import routers and use the database instance

@app.get("/")
async def root():
    return RedirectResponse(url='/docs')



