from fastapi import APIRouter
from app.agents.travel_agent import TravelAgent

router = APIRouter()

agent = TravelAgent()

@router.post("/plan-trip")
def plan_trip(data: dict):

    destination = data.get("destination")
    days = data.get("days")
    interests = data.get("interests")

    result = agent.generate_itinerary(destination, days, interests)

    return {"itinerary": result}