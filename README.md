STEP 2 — Paste this entire content
# AI Hand Gesture Volume Controller

An AI-powered hand gesture system that allows you to control your laptop's system volume using hand movements through your webcam.

The project uses MediaPipe hand landmark detection and OpenCV for real-time hand tracking, while Pycaw controls the Windows system volume.

---

## Features

- Real-time hand tracking using MediaPipe
- Thumb-index finger distance controls volume
- Smooth volume adjustment
- Real Windows system volume control
- Visual volume percentage and volume bar
- Blue line showing thumb-index distance
- Two-hand gesture detection
- Open-palm gesture to lock/unlock volume control
- Lock state remains active even after the second hand disappears
- Keyboard backup controls
- Mute/unmute support
- Volume reset function
- Startup screen
- Real-time gesture instructions

---

## How It Works

### Volume Control

The first detected hand controls the volume.

Move your thumb and index finger:

```text
Fingers close
     ↓
Low volume

Fingers apart
     ↓
High volume

The distance between the thumb and index finger is converted into a volume percentage from 0% to 100%.

A smoothing system is used to prevent sudden jumps caused by small hand movements.

Lock / Unlock

The second hand is used only for locking and unlocking the volume controller.

Show an open palm with the second hand:

Open Palm
    ↓
Toggle Lock

The lock state remains unchanged when the second hand disappears.

Example:

UNLOCKED
   ↓
Second hand shows palm
   ↓
LOCKED
   ↓
Second hand disappears
   ↓
Still LOCKED
   ↓
Second hand shows palm again
   ↓
UNLOCKED

This prevents accidental volume changes when you don't want the volume to move.

Keyboard Controls
Key	Action
Q	Quit application
M	Mute / Unmute
R	Reset volume to 50% and unlock

Keyboard controls are provided as a backup to the gesture controls.

Technologies Used
Python
OpenCV
MediaPipe
Pycaw
Windows Core Audio
Project Structure
AI-Hand-Gesture-Controller/
│
├── hand_landmarker.task
├── hand_tracker.py
├── volume_control.py
├── main.py
├── .gitignore
└── README.md
File Description

main.py

Main application that connects hand tracking, volume control, gestures and the user interface.

hand_tracker.py

Handles MediaPipe hand detection, landmark tracking, gesture detection and thumb-index distance calculation.

volume_control.py

Controls the Windows system audio volume using Pycaw.

hand_landmarker.task

MediaPipe hand landmark model used for real-time hand detection.

Installation
1. Clone the repository
git clone https://github.com/sikanderbukht38-cell/AI-Hand-Gesture-Controller.git
2. Open the project
cd AI-Hand-Gesture-Controller
3. Create a virtual environment
python -m venv .venv
4. Activate the virtual environment

Windows PowerShell:

.venv\Scripts\Activate.ps1
5. Install dependencies
pip install opencv-contrib-python mediapipe pycaw comtypes
6. Run the application
python main.py
Requirements
Windows
Python 3.10+
Webcam
Working microphone/camera permissions
Speakers or headphones
Usage

After starting the application:

Show one hand to the camera.
Move your thumb and index finger closer or farther apart.
The system volume changes accordingly.
Show an open palm with your second hand to lock the volume.
Show the second-hand palm again to unlock it.
Press Q to exit.
Volume Range

The controller maps thumb-index distance approximately as follows:

0.03 → 0%

0.22 → 100%

The range can be adjusted in main.py if needed.

Future Improvements

Possible future additions include:

Custom gesture profiles
Music playback controls
Play / pause gestures
Next / previous track gestures
Brightness control
Application-specific volume control
Gesture customization
Improved hand identification
GUI settings panel
Machine-learning based gesture classification
Author

Sikander Bukht

GitHub:
https://github.com/sikanderbukht38-cell

License

This project is available for educational and personal use.


## STEP 3 — Save it

Make sure the file is actually named:

```text
README.md