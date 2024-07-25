from fastapi import FastAPI
from fastapi.responses import RedirectResponse
from starlette.middleware.cors import CORSMiddleware

from app.routers import payment_check as payment_check
from app.routers import payment_create as payment_create
from app.routers import register_end as register_end
from app.routers import register_start as register_start
from app.routers import token_receive as token_receive
# Own import
from app.routers import token_request as token_request

app = FastAPI(
    title="Yoomoney Integration Service",
    description="""
    A FastAPI service to automate the process of registering Yoomoney applications for users and integrating these apps into the payment system.
    """,
    version="1.0.0"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"]
)

app.include_router(token_request.router)
app.include_router(token_receive.router)
app.include_router(payment_create.router)
app.include_router(payment_check.router)
app.include_router(register_end.router)
app.include_router(register_start.router)


@app.get("/")
async def root():
    """
    Redirect to the API documentation.
    """
    return RedirectResponse(url='/docs')
