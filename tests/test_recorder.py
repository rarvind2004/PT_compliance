# Optional sanity test for timing.
# Usage: python tests/test_recorder.py
import time
from movement_recorder import MovementRecorder

def main():
    rec = MovementRecorder(target_hz=100.0)
    rec.start()
    time.sleep(2.0)  # record for 2 seconds
    rec.stop()

    frames = rec.frames()
    dur = rec.duration_sec()
    hz = rec.measured_hz()

    print(f"Frames: {len(frames)}")
    print(f"Duration: {dur:.3f} s")
    print(f"Measured Hz: {hz:.1f}")
    if abs(hz - 100.0) <= 15.0:
        print("OK: Sample rate within tolerance.")
    else:
        print("WARN: Sample rate drifted. Check system load.")

if __name__ == "__main__":
    main()
