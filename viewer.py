from persistence import list_baselines
import json

def main():
    baselines = list_baselines()
    if not baselines:
        print("No baselines found. Run: python app.py  and stop/save a recording.")
        return
    print("Saved baselines:")
    for i, b in enumerate(baselines, 1):
        print(f"{i:2d}. file={b['file']} | exercise={b['exercise']} | level={b['skill_level']} | frames={b['frame_count']} | duration={b['duration_sec']:.2f}s")

if __name__ == "__main__":
    main()
