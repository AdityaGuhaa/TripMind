# TripMind 

**TripMind** is an AI‑powered travel planning backend that generates intelligent multi‑day itineraries using real‑time data and a Large Language Model. It combines live place discovery, weather information, and LLM reasoning to build context‑aware travel plans.

This project was built as a modular AI‑agent style system using **FastAPI**, **Google Gemini**, **Google Places API**, and **Open‑Meteo weather data**.

---

# Project Overview

TripMind acts as an **AI Travel Planner Agent** that:

1. Accepts user trip parameters
2. Fetches real places from Google Maps
3. Retrieves live weather conditions
4. Sends structured context to Gemini
5. Generates a realistic itinerary
6. Returns clean JSON for frontend consumption

Example request:

```
POST /plan-trip

{
  "destination": "Goa",
  "days": 3,
  "interests": ["beaches", "cafes", "nightlife"]
}
```

Example response:

```
{
  "destination": "Goa",
  "weather": {
    "temperature": 28.9,
    "windspeed": 11.8,
    "condition": "Mainly clear"
  },
  "itinerary": {
    "days": [
      {
        "day": 1,
        "morning": "Baga Beach",
        "afternoon": "Fort Aguada",
        "evening": "Dinner at Thalassa"
      }
    ]
  }
}
```

---

# Core Features

## AI‑Generated Travel Itineraries

TripMind uses **Gemini 2.5 Flash** to generate structured itineraries based on:

* Destination
* Trip duration
* User interests
* Weather conditions
* Real places from Google Maps

## Real‑Time Place Discovery

Places are fetched using the **Google Places API** including:

* Cafes
* Restaurants
* Beaches
* Bars / Nightlife
* Tourist Attractions

The system dynamically selects categories based on **user interests**.

## Weather Awareness

TripMind integrates **Open‑Meteo API** to adjust recommendations depending on weather.

Examples:

Sunny → Beaches and outdoor places

Rainy → Cafes, restaurants, indoor attractions

## Modular AI Agent Architecture

The backend is structured like a lightweight AI agent system.

```
User Request
     ↓
FastAPI API
     ↓
TravelAgent
     ↓
Tools
  ├── PlaceFinder
  └── WeatherTool
     ↓
Services
  ├── Google Places API
  └── Open‑Meteo Weather API
     ↓
Gemini Reasoning
     ↓
Structured Itinerary
```

This modular design allows new tools to be added easily.

---

# Project Structure

```
TripMind
│
├── backend
│   ├── app
│   │   ├── agents
│   │   │   └── travel_agent.py
│   │   │
│   │   ├── api
│   │   │   └── trip_routes.py
│   │   │
│   │   ├── config
│   │   │   └── settings.py
│   │   │
│   │   ├── services
│   │   │   ├── places_service.py
│   │   │   └── weather_service.py
│   │   │
│   │   ├── tools
│   │   │   ├── place_finder.py
│   │   │   └── weather_tool.py
│   │   │
│   │   └── main.py
│   │
│   └── requirements.txt
│
├── frontend
│
├── docs
│   ├── architecture.md
│   └── api_design.md
│
└── README.md
```

---

# Technologies Used

Backend

* Python
* FastAPI
* Uvicorn

AI

* Google Gemini 2.5 Flash

APIs

* Google Places API
* Open‑Meteo Weather API

Other

* Requests
* Python Dotenv

---

# Installation

Clone the repository

```
git clone https://github.com/yourusername/tripmind.git
cd tripmind
```

Create environment

```
conda create -n tripmind python=3.11
conda activate tripmind
```

Install dependencies

```
pip install -r requirements.txt (inside backend folder)
```

---

# Environment Variables

Create a `.env` file in the backend directory.

```
GEMINI_API_KEY=your_gemini_api_key
GOOGLE_PLACES_API_KEY=your_google_places_api_key
```

---

# Running the Server

```
cd backend
uvicorn app.main:app --reload
```

Swagger API documentation will be available at:

```
http://127.0.0.1:8000/docs
```

---

# Current Capabilities

TripMind currently supports:

* Multi‑day itinerary generation
* Weather‑aware recommendations
* Real places from Google Maps
* Dynamic categories based on interests
* Structured JSON responses
* FastAPI REST API

---

# Example Request

```
{
  "destination": "Goa",
  "days": 3,
  "interests": ["beaches", "nightlife", "cafes"]
}
```

---

# Future Improvements

Planned upgrades for TripMind:

## Adaptive AI Agent

Allow the LLM to dynamically decide which tools to use.

```
LLM
  ↓
Tool Selection
  ↓
Weather Tool
Places Tool
Route Tool
Hotel Tool
```

## User Location Awareness

Use browser geolocation to:

* detect user location
* show nearby trips
* calculate travel distance

## Route Optimization

Add:

* travel time
* route optimization
* transportation suggestions

## Hotel & Accommodation Discovery

Integrate hotel APIs to recommend:

* hotels
* hostels
* Airbnb

## Budget Planning

Estimate travel costs for:

* food
* accommodation
* activities

---

# Goal of the Project

TripMind aims to demonstrate how **LLMs can be combined with real APIs to create intelligent AI agents** capable of reasoning over structured data.

The project serves as a foundation for building **next‑generation AI travel assistants**.

---

# Author

Aditya Guha

AI & ML Enthusiast

Computer Science Engineering

---

# Support

If you found this project useful, consider starring the repository.
