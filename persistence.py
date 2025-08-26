import os, json, time
from typing import List, Dict, Any
from movement_recorder import MovementFrame

BASE_DIR = os.path.abspath(os.path.dirname(__file__))
BASELINE_DIR = os.path.join(BASE_DIR, "baselines")
os.makedirs(BASELINE_DIR, exist_ok=True)
INDEX_PATH = os.path.join(BASELINE_DIR, "index.json")

def _load_index() -> Dict[str, Any]:
    if not os.path.exists(INDEX_PATH):
        return {"baselines": []}
    with open(INDEX_PATH, "r", encoding="utf-8") as f:
        return json.load(f)

def _save_index(idx: Dict[str, Any]) -> None:
    with open(INDEX_PATH, "w", encoding="utf-8") as f:
        json.dump(idx, f, indent=2)

def save_baseline(frames: List[MovementFrame], exercise: str = "Arm Circles",
                  skill_level: str = "Beginner", therapist: str = "Dr. Smith") -> str:
    ts = time.strftime("%Y%m%d_%H%M%S")
    safe_ex = "".join(c for c in exercise if c.isalnum() or c in (" ", "_", "-")).strip().replace(" ", "_")
    fname = f"{ts}_{safe_ex}_{skill_level}.json"
    fpath = os.path.join(BASELINE_DIR, fname)
    if not frames:
        raise ValueError("No frames to save.")
    t0 = frames[0].t
    tN = frames[-1].t
    duration = max(0.0, tN - t0) if tN >= t0 else 0.0

    payload = {
        "meta": {
            "timestamp": ts,
            "exercise": exercise,
            "skill_level": skill_level,
            "therapist": therapist,
            "frame_count": len(frames),
            "duration_sec": duration
        },
        "frames": [frame.__dict__ for frame in frames]
    }
    with open(fpath, "w", encoding="utf-8") as f:
        json.dump(payload, f, indent=2)

    # update index
    idx = _load_index()
    idx["baselines"].append({
        "file": fname,
        "exercise": exercise,
        "skill_level": skill_level,
        "therapist": therapist,
        "frame_count": len(frames),
        "duration_sec": duration
    })
    _save_index(idx)
    return fpath

def list_baselines():
    idx = _load_index()
    return idx.get("baselines", [])
