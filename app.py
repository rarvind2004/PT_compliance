import tkinter as tk
from tkinter import messagebox, simpledialog
import threading, time, os
from movement_recorder import MovementRecorder
from persistence import save_baseline

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("PT Compliance — Day 1–2 Recorder (Sim)")
        self.geometry("520x240")
        self.resizable(False, False)

        self.recorder = MovementRecorder(target_hz=100.0, noise=0.05)
        self._ui_timer = None

        # UI
        self.start_btn = tk.Button(self, text="Start Recording", font=("Segoe UI", 12), command=self.on_start)
        self.stop_btn  = tk.Button(self, text="Stop & Save", font=("Segoe UI", 12), command=self.on_stop, state=tk.DISABLED)
        self.start_btn.pack(pady=12)
        self.stop_btn.pack(pady=4)

        self.status = tk.Label(self, text="Status: Idle", font=("Segoe UI", 10))
        self.status.pack(pady=6)

        self.stats = tk.Label(self, text="Frames: 0 | Duration: 0.00s | Measured Hz: 0.0", font=("Consolas", 10))
        self.stats.pack(pady=6)

        self.protocol("WM_DELETE_WINDOW", self.on_close)

    def on_start(self):
        if self.recorder.is_recording:
            return
        self.recorder.start()
        self.status.configure(text="Status: Recording…")
        self.start_btn.configure(state=tk.DISABLED)
        self.stop_btn.configure(state=tk.NORMAL)
        self._tick_ui() 

    def on_stop(self):
        if not self.recorder.is_recording:
            return
        self.recorder.stop()
        # Prompt for metadata
        exercise = simpledialog.askstring("Exercise", "Exercise name:", initialvalue="Arm Circles", parent=self)
        if exercise is None:
            exercise = "Arm Circles"
        skill = simpledialog.askstring("Skill Level", "Skill level (Beginner/Intermediate/Advanced):", initialvalue="Beginner", parent=self)
        if skill is None:
            skill = "Beginner"
        therapist = simpledialog.askstring("Therapist", "Therapist name:", initialvalue="Dr. Smith", parent=self)
        if therapist is None:
            therapist = "Dr. Smith"

        try:
            path = save_baseline(self.recorder.frames(), exercise, skill, therapist)
            self.status.configure(text=f"Saved: {os.path.basename(path)}")
            messagebox.showinfo("Saved", f"Baseline saved to:\n{path}")
        except Exception as e:
            messagebox.showerror("Error", str(e))
        finally:
            self.start_btn.configure(state=tk.NORMAL)
            self.stop_btn.configure(state=tk.DISABLED)

    def _tick_ui(self):
        if self.recorder.is_recording:
            frames = self.recorder.frames()
            dur = self.recorder.duration_sec()
            hz = self.recorder.measured_hz()
            self.stats.configure(text=f"Frames: {len(frames)} | Duration: {dur:0.2f}s | Measured Hz: {hz:0.1f}")
            self._ui_timer = self.after(100, self._tick_ui)  # UI refresh ~10 Hz
        else:
            self.stats.configure(text="Frames: 0 | Duration: 0.00s | Measured Hz: 0.0")

    def on_close(self):
        try:
            if self.recorder.is_recording:
                self.recorder.stop()
        finally:
            self.destroy()

if __name__ == "__main__":
    App().mainloop()
