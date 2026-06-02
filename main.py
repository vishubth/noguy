from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

from src.database.database import init_database
from src.api.routes.investor_routes import router as investor_router
from src.api.routes.admin_routes import router as admin_router


app = FastAPI(
    title="Digital Asset Fundraising Operations Platform",
    version="1.0.0",
)


@app.on_event("startup")
def startup():
    init_database()


app.mount(
    "/static",
    StaticFiles(directory="static"),
    name="static",
)

app.include_router(investor_router)
app.include_router(admin_router)


@app.get("/health")
def health():
    return {
        "status": "healthy",
        "service": "digital-asset-fundraising-platform",
    }
