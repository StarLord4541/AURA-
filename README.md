# 🚨 Road Accident Detection & Alert System

![Accident Detection Demo](https://github.com/user-attachments/assets/69ecddbf-3db9-43bb-9c0e-81497fb50600)

## 📖 Overview
The **Road Accident Detection & Alert System** is a computer-vision powered application designed to identify vehicle accidents on roads in real-time, trigger automated alerts, capture accident details, and enable rapid emergency response. By analyzing CCTV or video feeds, it utilizes predictive AI models and communication technologies to vastly improve emergency response times.

## ✨ Features
* **Accident Detection:** Employs trained computer vision (Keras/TensorFlow) and OpenCV algorithms to detect accident events based on visual cues.
* **Audio Alerts:** Instantly triggers an audible alarm upon detecting an accident to alert local monitoring operators.
* **Screenshot Capture:** Automatically captures and saves a timestamped snapshot of the accident scene for documentation and evidence.
* **Emergency Response:** Features a graphical user interface (Tkinter) that allows authorized personnel to quickly request emergency medical services via the Twilio API.
* **Live Risk Telemetry:** Displays persistent screen telemetry indicating live risk percentages and the total daily accident count.

## 🛠️ Technologies Used
* **Computer Vision & AI:** OpenCV, Keras, TensorFlow, NumPy.
* **Audio & UI Interfaces:** Tkinter, Python Winsound.
* **Telecommunications:** Twilio API for automated SMS/Voice response.
* **Image Processing:** OpenCV, Pillow (PIL).

## 🚀 Getting Started

To install and use the Road Accident Detection & Alert System locally:

1. **Clone the repository:**
   ```bash
   git clone <your-repository-url>
   cd Road-Accident-Detection-Alert-System
   ```

2. **Install Dependencies:**
   Install python dependencies required for computer vision and telecommunications:
   ```bash
   pip install opencv-python numpy pillow twilio tensorflow
   ```

3. **Configure API Settings:**
   * Create a Twilio account and obtain your authentication keys.
   * Insert your Twilio SID, Auth Token, and verified phone numbers into `camera.py`.

4. **Run the System:**
   Execute the main python script to begin frame-by-frame monitoring:
   ```bash
   python main.py
   ```

## 🎯 Usage
The system is optimized for use in live surveillance environments, traffic management intersections, and city monitoring rooms where rapid detection is crucial. In the event of an accident, an emergency prompt will cleanly display and allow operators to authorize a direct call to the authorities.


