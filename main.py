from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

# Own import
from app.routers import token_request as token_request
from app.routers import token_receive as token_receive

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(token_request.router)
app.include_router(token_receive.router)


@app.get("/")
async def root():
    return RedirectResponse(url='/docs')
