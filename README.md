<<<<<<< HEAD
# PT Compliance — Day 1–2 Windows Prototype (No Mac Needed)

This is a Windows-friendly prototype that mirrors **Day 1–2** of the project:
- A `MovementRecorder` collects **simulated IMU frames** at ~100 Hz.
- A tiny desktop app lets you **Start/Stop** recording and **Save as Baseline**.
- Baselines are saved as JSON with counts, duration, and metadata.
- A simple CLI viewer lists what you recorded.

## 1) Prereqs (Windows)
- Install **Python 3.10+** (recommended 3.11). Check with:
  ```powershell
  python --version
  ```
- (Optional) Create and activate a virtualenv:
  ```powershell
  python -m venv .venv
  .\.venv\Scripts\Activate.ps1
  ```
- Tkinter ships with most Windows Python installers. If `tkinter` import fails,
  reinstall Python using the official Windows installer from python.org.

## 2) Run the UI (Start/Stop Recording)
From this folder:
```powershell
python app.py
```
- Click **Start Recording** to begin a ~100 Hz capture (simulated).
- Click **Stop & Save** to store frames as a JSON baseline. You'll be prompted
  for Exercise name, Skill level, and Therapist (pre-filled defaults are OK).
- The bottom status shows **frames**, **duration**, and **measured sample rate**.

**Where saved?** In `baselines/` with a timestamped file. We also keep an `index.json`
with quick summaries.

## 3) List your saved baselines
```powershell
python viewer.py
```

## 4) Acceptance Checks (mapped to Day 1–2 goals)
- Start a recording for ≥ 10 seconds.
- Stop & Save → a new JSON appears in `baselines/`.
- Run `python viewer.py` and confirm:
  - `frame_count` is non-zero (typically ~1000 for 10s).
  - `duration_sec` ≈ wall time (within ±0.3s).
  - `measured_hz` is ~100 (±10%).
- File size should be a few hundred KB → confirms dense frames.

## 5) Project structure
```text
app.py               # Tkinter UI, start/stop/save baseline
movement_recorder.py # ~100 Hz recorder (simulated IMU frames)
persistence.py       # Save/list baselines (JSON)
viewer.py            # CLI listing of saved baselines
baselines/           # Saved JSON baselines + index.json
tests/test_recorder.py  # Optional sanity test (timing)
```

## 6) Optional quick test
```powershell
python tests/test_recorder.py
```

## Notes
- This prototype **simulates** IMU signals so you can build and test logic on Windows.
- The JSON format mirrors what you'd store on iOS/watchOS later (timestamps + ax/ay/az).
- When you move to devices, swap the simulator with real sensor reads—everything else
  (persistence, lists, later comparison logic) can stay the same.
=======
#drop in readme contents
# PT Compliance Platform (cross platform starter)

A proof of concept system that lets physical therapists (PTs) record **baseline movements** and lets patients **compare** their own movements in real time using only commodity apple devices.

##Core idea
* PT records “gold standard” set of reps.
* Patient app streams accelerometer /gyro data.
* Backend scores similarity and returns instant feedback.

##Tech stack
| Layer | Tech |
| Mobile / Wear OS | **Flutter** (`sensors_plus`, `sqflite`) |
| Backend API | **FastAPI** + Pydantic |
| Web dashboard | **Next.js** + Chakra UI |
| CI / CD | GitHub Actions → debug APK + Docker image |
| Storage | SQLite local, Postgres cloud (via SQLAlchemy) |
>>>>>>> 4c4e8fc82b1a71f8d20238eb4f0f79a709677ff9
