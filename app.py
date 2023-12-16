from typing import Dict

from fastapi import Depends, FastAPI
from routes.candidates import candidate_router
from routes.users import user_router
from views.users import verify_user

app = FastAPI(
    title="Elevatus Technical Assignment",
    version="1.0.0",
    openapi_url="/openapi.json",
    docs_url="/docs",
    redoc_url="/redoc",
)


@app.get("/ping", tags=["Health Check"])
async def health_check() -> Dict:
    """
    Health Check Endpoint.

    Returns:
        Dict
    """
    return {"message": "pong"}


app.include_router(user_router)
app.include_router(candidate_router, dependencies=[Depends(verify_user)])
