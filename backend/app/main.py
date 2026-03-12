from fastapi import FastAPI
from dotenv import load_dotenv

from app.api.health_routes import router as health_router
from app.api.trip_routes import router as trip_router

load_dotenv()

app = FastAPI(
    title="TripMind API",
    description="AI Agent Travel Planner",
    version="1.0.0"
)

app.include_router(health_router)
app.include_router(trip_router)


@app.get("/")
def root():
    return {"message": "TripMind API is running 🚀"}