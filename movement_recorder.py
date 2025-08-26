import threading
import time
import math
import random
from dataclasses import dataclass, asdict
from typing import List, Callable, Optional

@dataclass
class MovementFrame:
    t: float   # seconds since start
    ax: float  # m/s^2 (simulated)
    ay: float
    az: float

class MovementRecorder:
    """Simulates IMU frames at ~100 Hz in a background thread.
    Call start(), then stop() to get frames and timing stats.
    """
    def __init__(self, target_hz: float = 100.0, noise: float = 0.05):
        self.target_hz = target_hz
        self.noise = noise
        self._frames: List[MovementFrame] = []
        self._thread: Optional[threading.Thread] = None
        self._stop_flag = threading.Event()
        self._lock = threading.Lock()
        self._t0: Optional[float] = None
        self._t_end: Optional[float] = None

    def start(self) -> None:
        if self.is_recording:
            return
        self._frames.clear()
        self._stop_flag.clear()
        self._t0 = time.perf_counter()
        self._t_end = None
        self._thread = threading.Thread(target=self._loop, daemon=True)
        self._thread.start()

    def stop(self) -> None:
        if not self.is_recording:
            return
        self._stop_flag.set()
        if self._thread:
            self._thread.join(timeout=2.0)
        self._t_end = time.perf_counter()

    @property
    def is_recording(self) -> bool:
        return self._thread is not None and self._thread.is_alive()

    def _loop(self):
        # Simulate an exercise-like motion (combined sinusoids) + noise
        # Keep loop timing tight for ~100 Hz
        next_time = time.perf_counter()
        period = 1.0 / max(1e-6, self.target_hz)
        while not self._stop_flag.is_set():
            now = time.perf_counter()
            if now < next_time:
                time.sleep(max(0.0, next_time - now))
                continue
            t = now - (self._t0 or now)
            # simulate motion signals (e.g., arm circles)
            ax = math.sin(2 * math.pi * 0.7 * t) + 0.2 * math.sin(2 * math.pi * 1.3 * t)
            ay = math.cos(2 * math.pi * 0.7 * t) + 0.2 * math.cos(2 * math.pi * 1.1 * t)
            az = 0.5 * math.sin(2 * math.pi * 0.35 * t)
            # add small random noise
            ax += random.uniform(-self.noise, self.noise)
            ay += random.uniform(-self.noise, self.noise)
            az += random.uniform(-self.noise, self.noise)
            frame = MovementFrame(t=t, ax=ax, ay=ay, az=az)
            with self._lock:
                self._frames.append(frame)
            next_time += period

    def frames(self) -> List[MovementFrame]:
        with self._lock:
            return list(self._frames)

    def duration_sec(self) -> float:
        if self._t0 is None:
            return 0.0
        end = self._t_end if self._t_end is not None else time.perf_counter()
        return max(0.0, end - self._t0)

    def measured_hz(self) -> float:
        dur = self.duration_sec()
        if dur <= 0:
            return 0.0
        return len(self.frames()) / dur
