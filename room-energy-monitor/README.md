# Room Energy Monitor

Detects whether a room is occupied (real webcam + AI) and cross-checks that
against power draw (simulated, since there's no physical sensor) to flag
electricity being wasted.

## Project layout

```
room-energy-monitor/
├── backend/
│   ├── main.py              # FastAPI app — the "brain"
│   ├── camera_detector.py   # Real webcam + YOLOv8 person detection
│   └── power_simulator.py   # Fakes a power/current sensor
├── database/
│   └── schema.sql           # Run this in Supabase's SQL editor
├── frontend/
│   └── index.html           # Live dashboard — just open it in a browser
├── requirements.txt
└── .env.example
```

## 1. Set up Supabase (one-time)

1. Go to https://supabase.com, sign up/log in, and create a new project.
2. Once it's ready, open **SQL Editor** (left sidebar) → **New query**.
3. Paste in the entire contents of `database/schema.sql` and run it. This
   creates the four tables the backend needs.
4. Go to **Project Settings → API**. Copy the **Project URL** and the
   **anon public key** — you'll need both next.

## 2. Configure your environment

```bash
cd room-energy-monitor
cp .env.example .env
```

Open `.env` and paste in your Supabase URL and key from step 1. The other
values (tariff rate, thresholds) have sensible defaults — tweak them later
if you want.

## 3. Install dependencies

Using a virtual environment is recommended so this doesn't clash with
anything else on your machine:

```bash
python -m venv venv
source venv/bin/activate        # on Windows: venv\Scripts\activate
pip install -r requirements.txt
```

Note: `ultralytics` (for the camera script) will download a small model file
(~6MB) the first time it runs, so you'll need internet access at least once.

## 4. Run everything

You'll run three things simultaneously, each in its own terminal (all from
the `room-energy-monitor/` folder, with the virtual environment activated):

**Terminal 1 — the backend:**
```bash
uvicorn backend.main:app --reload --port 8000
```
Visit `http://localhost:8000/docs` to confirm it's running — you should see
the interactive API docs.

**Terminal 2 — the power simulator:**
```bash
python backend/power_simulator.py
```
This starts sending fake wattage readings to the backend every 5 seconds.

**Terminal 3 — the camera detector:**
```bash
python backend/camera_detector.py
```
This opens your webcam and starts sending real occupancy detections. A
window will pop up showing what the camera sees with detection boxes drawn
on it — press `q` in that window to stop it.

**The dashboard:**
Just open `frontend/index.html` directly in your browser (double-click it,
or right-click → Open With → your browser). It polls the backend every 3
seconds and updates live. No server needed for this part.

## Demoing waste detection

To see the whole thing work end-to-end: step out of the camera's view (or
cover the lens) while the power simulator's "appliances_on" happens to be
true. After a few seconds, the dashboard should show the waste banner and
start accumulating cost. Walk back into frame and it should clear.

You can also click **"Cut power (simulate)"** on the dashboard at any time
to simulate an automatic cutoff — the power simulator will drop its
readings to near-zero on its next cycle.

## Troubleshooting

- **Dashboard shows no data / console errors about CORS or fetch failing:**
  Make sure the backend (`uvicorn`) is actually running first, and that
  `API` at the top of `index.html`'s `<script>` matches where it's running
  (default `http://localhost:8000`).
- **Camera script says it can't open the webcam:** another app might be
  using it, or you may need to change `cv2.VideoCapture(0)` to `1` in
  `camera_detector.py` if you have multiple cameras.
- **"SUPABASE_URL and SUPABASE_KEY must be set" error on backend startup:**
  double check `.env` exists (not just `.env.example`) and is in the
  project's root folder, not inside `backend/`.
