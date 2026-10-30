"""
Room Energy Monitor — backend

What this file does, in plain terms:
- Receives occupancy updates from the camera script  (POST /occupancy)
- Receives power readings from the power simulator    (POST /power)
- Decides whether electricity is being wasted (person absent + power draw high)
- Lets the dashboard toggle a simulated power cutoff   (POST /toggle-power)
- Tells the dashboard the current state                (GET  /status)

Run with:  uvicorn backend.main:app --reload --port 8000
(run that command from the project's root folder, not from inside backend/)
"""

import os
import time
from datetime import datetime, timezone
from typing import Literal, Optional

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPExceptnion
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from supabase import create_client, Client

# ---------------------------------------------------------------------------
# Setup
# ---------------------------------------------------------------------------

load_dotenv()

SUPABASE_URL = os.environ.get("SUPABASE_URL")
SUPABASE_KEY = os.environ.get("SUPABASE_KEY")
TARIFF_PER_KWH = float(os.environ.get("TARIFF_PER_KWH", 8.0))
IDLE_WATTS = float(os.environ.get("IDLE_WATTS", 15))
WASTE_WATTS_THRESHOLD = float(os.environ.get("WASTE_WATTS_THRESHOLD", 60))

if not SUPABASE_URL or not SUPABASE_KEY:
    raise RuntimeError(
        "SUPABASE_URL and SUPABASE_KEY must be set in your .env file. "
        "Copy .env.example to .env and fill them in."
    )

supabase: Client = create_client(SUPABASE_URL, SUPABASE_KEY)

app = FastAPI(title="Room Energy Monitor")

# Allow the dashboard (opened as a local HTML file, or served from anywhere)
# to call this API. Fine for a hackathon demo; you'd lock this down for production.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# In-memory state
# ---------------------------------------------------------------------------
# For a hackathon demo, it's fine to keep "what's happening right now" in memory
# and only write to the database for things worth persisting (readings, finished
# waste events). Restarting the backend just resets the live state, which is okay.

latest_occupancy: Optional[bool] = None
latest_power: Optional[float] = None

waste_active = False
waste_start_time: Optional[float] = None  # time.time() when waste started
waste_watts_at_start: float = 0.0


# ---------------------------------------------------------------------------
# Request/response shapes (Pydantic models)
# ---------------------------------------------------------------------------

class OccupancyIn(BaseModel):
    person_present: bool


class PowerIn(BaseModel):
    watts: float


class ToggleIn(BaseModel):
    action: Literal["cut", "restore"]


# ---------------------------------------------------------------------------
# Core waste-detection logic
# ---------------------------------------------------------------------------

def is_power_cut() -> bool:
    result = supabase.table("system_state").select("power_cut").eq("id", 1).execute()
    if not result.data:
        return False
    return bool(result.data[0]["power_cut"])


def check_waste():
    """Called after every new occupancy or power reading. Starts/stops a waste
    event depending on the current occupancy + power state."""
    global waste_active, waste_start_time, waste_watts_at_start

    if latest_occupancy is None or latest_power is None:
        return  # not enough data yet

    if is_power_cut():
        # Power has been manually (simulated) cut — never counts as waste
        if waste_active:
            _close_waste_event()
        return

    should_be_wasting = (latest_occupancy is False) and (latest_power > WASTE_WATTS_THRESHOLD)

    if should_be_wasting and not waste_active:
        waste_active = True
        waste_start_time = time.time()
        waste_watts_at_start = latest_power

    elif not should_be_wasting and waste_active:
        _close_waste_event()


def _close_waste_event():
    global waste_active, waste_start_time, waste_watts_at_start

    started_at = datetime.fromtimestamp(waste_start_time, tz=timezone.utc)
    ended_at = datetime.now(timezone.utc)
    duration_hours = (ended_at - started_at).total_seconds() / 3600.0
    kwh = (waste_watts_at_start / 1000.0) * duration_hours
    cost = kwh * TARIFF_PER_KWH

    # Only log events lasting more than a couple of seconds — avoids noise
    # from brief flickers when you're just testing.
    if duration_hours * 3600 > 2:
        supabase.table("waste_events").insert({
            "started_at": started_at.isoformat(),
            "ended_at": ended_at.isoformat(),
            "watts": waste_watts_at_start,
            "kwh": round(kwh, 4),
            "cost": round(cost, 2),
        }).execute()

    waste_active = False
    waste_start_time = None
    waste_watts_at_start = 0.0


# ---------------------------------------------------------------------------
# Endpoints
# ---------------------------------------------------------------------------

@app.post("/occupancy")
def receive_occupancy(data: OccupancyIn):
    global latest_occupancy
    latest_occupancy = data.person_present

    supabase.table("occupancy").insert({
        "person_present": data.person_present,
    }).execute()

    check_waste()
    return {"received": True, "person_present": data.person_present}


@app.post("/power")
def receive_power(data: PowerIn):
    global latest_power
    latest_power = data.watts

    supabase.table("power_readings").insert({
        "watts": data.watts,
    }).execute()

    check_waste()
    return {"received": True, "watts": data.watts}


@app.get("/power-state")
def power_state():
    """The power simulator checks this before generating each reading, so a
    'cut' triggered from the dashboard is reflected in the simulated wattage."""
    return {"power_cut": is_power_cut()}


@app.post("/toggle-power")
def toggle_power(data: ToggleIn):
    power_cut = data.action == "cut"
    supabase.table("system_state").update({"power_cut": power_cut}).eq("id", 1).execute()
    return {"power_cut": power_cut}


@app.get("/status")
def status():
    # Totals from all closed waste events
    events = supabase.table("waste_events").select("kwh, cost").execute().data or []
    total_kwh = round(sum(e["kwh"] for e in events), 3)
    total_cost = round(sum(e["cost"] for e in events), 2)

    # Recent log for the dashboard (most recent first)
    recent = (
        supabase.table("waste_events")
        .select("*")
        .order("ended_at", desc=True)
        .limit(10)
        .execute()
        .data
    )

    current_waste_seconds = 0
    if waste_active and waste_start_time is not None:
        current_waste_seconds = int(time.time() - waste_start_time)

    return {
        "person_present": latest_occupancy,
        "watts": latest_power,
        "power_cut": is_power_cut(),
        "waste_active": waste_active,
        "current_waste_seconds": current_waste_seconds,
        "total_kwh_wasted": total_kwh,
        "total_cost_wasted": total_cost,
        "event_count": len(events),
        "recent_events": recent,
    }


@app.get("/")
def root():
    return {"message": "Room Energy Monitor backend is running. See /docs for the API."}
