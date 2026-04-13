import cv2
import numpy as np
import os
import platform
import threading
import time
import tkinter as tk
from tkinter import messagebox
from twilio.rest import Client
from PIL import Image, ImageTk
from detection import AccidentDetectionModel

class AccidentDetectionApp:
    def __init__(self, window, window_title, video_source="test_video.mp4"):
        self.window = window
        self.window.title(window_title)
        self.video_source = video_source
        
        # Load the mock model
        self.model = AccidentDetectionModel("model.json", "model_weights.keras")
        self.font = cv2.FONT_HERSHEY_SIMPLEX
        
        # State variables
        self.alarm_triggered = False
        self.accident_count = 0
        
        # Open video source
        self.vid = cv2.VideoCapture(self.video_source)
        if not self.vid.isOpened():
            messagebox.showerror("Error", f"Unable to open video source: {video_source}")
            self.window.destroy()
            return

        # Create UI elements
        self.canvas = tk.Canvas(window, width=self.vid.get(cv2.CAP_PROP_FRAME_WIDTH), height=self.vid.get(cv2.CAP_PROP_FRAME_HEIGHT))
        self.canvas.pack()

        # Feedback labels
        self.info_frame = tk.Frame(window)
        self.info_frame.pack(fill="x", padx=10, pady=5)
        
        self.status_label = tk.Label(self.info_frame, text="Status: Monitoring...", font=("Helvetica", 12))
        self.status_label.pack(side="left")
        
        self.btn_quit = tk.Button(window, text="Quit Application", command=self.on_closing)
        self.btn_quit.pack(side="bottom", pady=10)

        # Twilio Config (Placeholders)
        self.twilio_sid = "your_twilio_account_sid"
        self.twilio_token = "your_twilio_account_auth_token"
        self.to_num = "sender_number"
        self.from_num = "receiver_number"

        # Start the update loop
        self.delay = 15
        self.update()
        self.window.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.window.mainloop()

    def play_alert_sound(self):
        """Cross-platform alert sound."""
        if platform.system() == "Windows":
            try:
                import winsound
                winsound.Beep(2500, 1000)
            except ImportError:
                pass
        else:
            # Mac/Linux alert
            os.system('say "Accident detected. Initializing emergency protocols." &')
            os.system('printf "\a"')

    def save_accident_photo(self, frame):
        """Save a timestamped snapshot of the accident."""
        try:
            directory = "accident_photos"
            if not os.path.exists(directory):
                os.makedirs(directory)
            filename = f"{directory}/{time.strftime('%Y%m%d-%H%M%S')}.jpg"
            cv2.imwrite(filename, frame)
            print(f"Evidence saved: {filename}")
        except Exception as e:
            print(f"Snapshot error: {e}")

    def call_ambulance(self):
        """Invoke Twilio API for emergency dispatch."""
        if self.twilio_sid == "your_twilio_account_sid":
            print("Twilio credentials not configured. Skipping call.")
            return
            
        try:
            client = Client(self.twilio_sid, self.twilio_token)
            call = client.calls.create(
                url="http://demo.twilio.com/docs/voice.xml",
                to=self.to_num,
                from_=self.from_num
            )
            print(f"Emergency call initiated. SID: {call.sid}")
        except Exception as e:
            print(f"Twilio error: {e}")

    def trigger_alert_sequence(self, frame):
        """Handles the sequence when an accident is detected."""
        if self.alarm_triggered:
            return
            
        self.alarm_triggered = True
        self.accident_count += 1
        self.status_label.config(text="Status: ACCIDENT DETECTED!", fg="red")
        
        # 1. Save photo
        self.save_accident_photo(frame)
        
        # 2. Sound alarm
        self.play_alert_sound()
        
        # 3. Show GUI prompt (non-blocking)
        self.show_critical_prompt()

    def show_critical_prompt(self):
        """Ask user if the accident is critical."""
        answer = messagebox.askyesno("Critical Alert", "Accident Detected!\n\nShould we call an ambulance immediately?")
        if answer:
            self.call_ambulance()
        
        # Reset alarm after prompt is handled
        self.alarm_triggered = False
        self.status_label.config(text="Status: Monitoring...", fg="black")

    def update(self):
        """The main loop that processes frames and updates the UI."""
        ret, frame = self.vid.read()
        if ret:
            # Process frame for AI
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
            roi = cv2.resize(rgb_frame, (250, 250))
            
            # AI Inference
            pred, prob = self.model.predict_accident(roi[np.newaxis, :, :])
            risk_percent = round(prob[0][0] * 100, 2)
            
            if pred == "Accident" and risk_percent > 99 and not self.alarm_triggered:
                self.trigger_alert_sequence(frame)

            # Overlay info on frame for UI
            cv2.rectangle(frame, (10, 10), (250, 70), (0, 0, 0), -1)
            cv2.putText(frame, f"Risk: {risk_percent}%", (20, 35), self.font, 0.7, (0, 255, 255), 2)
            cv2.putText(frame, f"Count: {self.accident_count}", (20, 60), self.font, 0.7, (0, 255, 255), 2)

            # Display frame in Tkinter
            self.photo = ImageTk.PhotoImage(image=Image.fromarray(cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)))
            self.canvas.create_image(0, 0, image=self.photo, anchor=tk.NW)
            
        else:
            # Loop video or stop
            self.vid.set(cv2.CAP_PROP_POS_FRAMES, 0)
            
        self.window.after(self.delay, self.update)

    def on_closing(self):
        self.vid.release()
        self.window.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = AccidentDetectionApp(root, "Road Accident Detection System")
