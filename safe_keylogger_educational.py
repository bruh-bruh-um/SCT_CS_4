import tkinter as tk
from tkinter import filedialog, messagebox
from datetime import datetime
import csv
import os
import time

LOGFILE = "keystrokes_log.csv"
class EducationalKeyLogger(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Educational Key Logger (Visible & Consent-based)")
        self.geometry("800x520")
        self.logging = False
        self.start_time = None
        self.total_keys = 0
        self.backspace_count = 0
        self.cumulative_chars = 0
        consent_frame = tk.Frame(self)
        consent_frame.pack(fill="x", pady=(8, 0), padx=8)
        self.consent_var = tk.IntVar(value=0)
        consent_cb = tk.Checkbutton(consent_frame, text="I have explicit consent to record keystrokes for educational/demo purposes",
                                    variable=self.consent_var, wraplength=700, justify="left")
        consent_cb.pack(side="left")
        btn_frame = tk.Frame(self)
        btn_frame.pack(fill="x", pady=8, padx=8)

        self.start_btn = tk.Button(btn_frame, text="Start Logging", command=self.start_logging, state="normal")
        self.start_btn.pack(side="left", padx=6)

        self.stop_btn = tk.Button(btn_frame, text="Stop Logging", command=self.stop_logging, state="disabled")
        self.stop_btn.pack(side="left", padx=6)

        clear_btn = tk.Button(btn_frame, text="Clear Display", command=self.clear_display)
        clear_btn.pack(side="left", padx=6)

        export_btn = tk.Button(btn_frame, text="Export Log As...", command=self.export_log)
        export_btn.pack(side="left", padx=6)
        metrics_frame = tk.Frame(self)
        metrics_frame.pack(fill="x", padx=8)
        self.metrics_var = tk.StringVar(value=self._metrics_text())
        tk.Label(metrics_frame, textvariable=self.metrics_var, anchor="w", justify="left").pack(side="left")
        self.text = tk.Text(self, wrap="word", height=20)
        self.text.pack(fill="both", expand=True, padx=8, pady=8)

        status_frame = tk.Frame(self)
        status_frame.pack(fill="x", padx=8, pady=(0, 8))
        self.status_var = tk.StringVar(value="Status: Idle")
        tk.Label(status_frame, textvariable=self.status_var).pack(side="left")
        self.bind_all("<KeyPress>", self._on_keypress)
        self._ensure_csv_header()

    def _ensure_csv_header(self):
        if not os.path.exists(LOGFILE):
            with open(LOGFILE, mode="w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerow([
                    "timestamp_utc_iso", "keysym", "char", "total_keys",
                    "backspace_count", "cumulative_chars", "elapsed_seconds", "estimated_wpm"
                ])

    def _append_csv(self, row):
        with open(LOGFILE, mode="a", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(row)

    def _metrics_text(self):
        elapsed = 0.0
        wpm = 0.0
        if self.start_time and self.total_keys > 0:
            elapsed = time.time() - self.start_time
            minutes = elapsed / 60 if elapsed > 0 else 1/60
            wpm = (self.cumulative_chars / 5) / minutes
        return (f"Total keys: {self.total_keys}    Backspaces: {self.backspace_count}    "
                f"Cumulative chars: {self.cumulative_chars}    Elapsed(s): {elapsed:.1f}    "
                f"Est. WPM: {wpm:.1f}")

    def _on_keypress(self, event):
        if not self.logging:
            return
        if self.focus_get() is None:
            return
        timestamp = datetime.utcnow().isoformat(timespec="seconds") + "Z"
        key = event.keysym
        char = event.char if event.char != "" else ""
        self.total_keys += 1
        if key in ("BackSpace",):
            self.backspace_count += 1
                self.cumulative_chars -= 1
        else:
            if len(char) > 0 and ord(char) >= 32:
                self.cumulative_chars += 1

        elapsed_seconds = 0.0
        estimated_wpm = 0.0
        if self.start_time:
            elapsed_seconds = time.time() - self.start_time
            minutes = elapsed_seconds / 60 if elapsed_seconds > 0 else 1/60
            estimated_wpm = (self.cumulative_chars / 5) / minutes
        entry = (f"{timestamp} | keysym={key} | char={repr(char)} | total_keys={self.total_keys} | "
                 f"backspace={self.backspace_count} | chars={self.cumulative_chars} | "
                 f"elapsed_s={elapsed_seconds:.1f} | wpm={estimated_wpm:.1f}")
        self.text.insert("end", entry + "\n")
        self.text.see("end")
        csv_row = [timestamp, key, char, self.total_keys, self.backspace_count,
                   self.cumulative_chars, f"{elapsed_seconds:.1f}", f"{estimated_wpm:.1f}"]
        self._append_csv(csv_row)
        self.metrics_var.set(self._metrics_text())

    def start_logging(self):
        if not self.consent_var.get():
            messagebox.showwarning("Consent required", "You must confirm you have explicit consent before logging.")
            return

        self.logging = True
        self.start_time = time.time()
        self.total_keys = 0
        self.backspace_count = 0
        self.cumulative_chars = 0
        self.start_btn.config(state="disabled")
        self.stop_btn.config(state="normal")
        self.status_var.set(f"Status: Logging (visible). Log file: {os.path.abspath(LOGFILE)}")
        header = [f"=== LOG START {datetime.utcnow().isoformat()}Z ==="]
        self.text.insert("end", header[0] + "\n")
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.write(f"\n# LOG START {datetime.utcnow().isoformat()}Z\n")

    def stop_logging(self):
        if not self.logging:
            return
        self.logging = False
        self.start_btn.config(state="normal")
        self.stop_btn.config(state="disabled")
        self.status_var.set("Status: Idle")
        footer = f"=== LOG STOP {datetime.utcnow().isoformat()}Z ===\n"
        self.text.insert("end", footer + "\n")
        with open(LOGFILE, "a", encoding="utf-8") as f:
            f.write(f"# LOG STOP {datetime.utcnow().isoformat()}Z\n")

    def clear_display(self):
        self.text.delete("1.0", "end")
        self.metrics_var.set(self._metrics_text())

    def export_log(self):
        save_path = filedialog.asksaveasfilename(defaultextension=".csv",
                                                 filetypes=[("CSV files", "*.csv"), ("All files", "*.*")],
                                                 title="Export log as...")
        if not save_path:
            return
        try:
            with open(LOGFILE, "r", encoding="utf-8") as src, open(save_path, "w", encoding="utf-8") as dst:
                dst.write(src.read())
            messagebox.showinfo("Exported", f"Log exported to:\n{save_path}")
        except Exception as e:
            messagebox.showerror("Error", f"Failed to export log: {e}")


if __name__ == "__main__":
    print("Educational Key Logger - visible and consent-based.")
    print("Use only on machines you own or with explicit permission.")
    app = EducationalKeyLogger()
    app.mainloop()
