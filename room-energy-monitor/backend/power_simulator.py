"""
Power simulator — stands in for a real current sensor (e.g. an ACS712 + ESP32)
that you don't have hardware for. It generates a plausible wattage reading
every few seconds and POSTs it to the backend, exactly like a real sensor would.

Run with:  python backend/power_simulator.py
(run this in a separate terminal, while the backend is already running)
"""

import os
import random
import time

import requests
from dotenv import load_dotenv

load_dotenv()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

IDLE_WATTS = 10          # always-on baseline (router, standby devices, etc.)
APPLIANCE_WATTS = 20     # extra draw when "appliances" are on (lights/fan/etc.)
NOISE = 5                # random jitter so the graph doesn't look robotic

appliances_on = True     # flip this manually below, or extend with a schedule


def generate_reading():
    global appliances_on

    # Occasionally flip whether appliances are "on", to simulate real usage
    if random.random() < 0.05:
        appliances_on = not appliances_on

    base = IDLE_WATTS + (APPLIANCE_WATTS if appliances_on else 0)
    watts = max(0, base + random.uniform(-NOISE, NOISE))
    return round(watts, 1)


def is_power_cut() -> bool:
    try:
        r = requests.get(f"{BACKEND_URL}/power-state", timeout=3)
        r.raise_for_status()
        return r.json().get("power_cut", False)
    except requests.RequestException as e:
        print(f"[power_simulator] Couldn't reach backend for power-state: {e}")
        return False


def send_reading(watts: float):
    try:
        r = requests.post(f"{BACKEND_URL}/power", json={"watts": watts}, timeout=3)
        r.raise_for_status()
        print(f"[power_simulator] Sent watts={watts}")
    except requests.RequestException as e:
        print(f"[power_simulator] Failed to send reading: {e}")


if __name__ == "__main__":
    print(f"[power_simulator] Sending simulated readings to {BACKEND_URL} every 5s. Ctrl+C to stop.")
    while True:
        if is_power_cut():
            # Simulated cutoff — power draw drops to near zero
            watts = round(random.uniform(0, 2), 1)
        else:
            watts = generate_reading()

        send_reading(watts)
        time.sleep(5)
