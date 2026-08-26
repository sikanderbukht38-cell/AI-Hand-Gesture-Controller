# AI Hand Gesture Volume Controller

A real-time AI-powered volume controller that lets you control your Windows laptop's system volume using hand gestures through a webcam.

The project uses MediaPipe for hand landmark detection, OpenCV for real-time camera processing, and Pycaw to control the Windows system audio.

## Features

- Real-time hand tracking
- Gesture-based volume control
- Thumb and index finger distance controls volume
- Smooth volume adjustment
- Real Windows system volume control
- Visual volume percentage and volume bar
- Blue thumb-index distance indicator
- Two-hand gesture detection
- Open-palm gesture for volume lock/unlock
- Lock state persists when the second hand is removed
- Keyboard backup controls
- Mute and unmute support
- Volume reset functionality
- Clean on-screen interface

## How It Works

### Volume Control

The first hand controls the volume.

Move your thumb and index finger:

**Fingers close** → Lower volume

**Fingers apart** → Higher volume

The distance between the thumb and index finger is converted into a volume percentage from 0% to 100%.

A smoothing system is used to reduce sudden volume jumps caused by small hand movements.

### Lock / Unlock

The second hand is used to lock and unlock volume control.

Show an **open palm with the second hand** to toggle the lock state.

The lock remains active even after the second hand is removed.

Example:

```text
UNLOCKED
   ↓
Show second-hand palm
   ↓
LOCKED
   ↓
Remove second hand
   ↓
Still LOCKED
   ↓
Show second-hand palm again
   ↓
UNLOCKED

### Keyboard Controls

Key	Action
Q	Quit the application
M	Mute / Unmute
R	Reset volume to 50% and unlock

### Technologies

Python
OpenCV
MediaPipe
Pycaw
Windows Core Audio

### Project Structure

AI-Hand-Gesture-Controller/
│
├── main.py
├── hand_tracker.py
├── volume_control.py
├── hand_landmarker.task
├── .gitignore
└── README.md

### File Overview

main.py
Main application that connects hand tracking, gesture recognition, volume control, and the user interface.

hand_tracker.py
Handles MediaPipe hand detection, landmark tracking, open-palm detection, and thumb-index distance calculation.

volume_control.py
Controls the Windows system volume using Pycaw.

hand_landmarker.task
MediaPipe hand landmark model used for real-time hand tracking.

### Installation

1. Clone the repository
git clone https://github.com/sikanderbukht38-cell/AI-Hand-Gesture-Volume-Controller.git
2. Open the project
cd AI-Hand-Gesture-Controller
3. Create a virtual environment
python -m venv .venv
4. Activate the virtual environment

### On Windows PowerShell:

.venv\Scripts\Activate.ps1
5. Install dependencies
pip install opencv-contrib-python mediapipe pycaw comtypes
6. Run the application
python main.py

### Requirements

Windows
Python 3.10 or newer
Webcam
Speakers or headphones
Camera permissions enabled

### Volume Mapping

The thumb-index distance is mapped approximately as:

0.03 → 0% volume
0.22 → 100% volume

These values can be adjusted in main.py to change the sensitivity.

### Future Improvements

Play / pause music using gestures
Next / previous track controls
Brightness control
Application-specific volume control
Customizable gestures
Gesture-based media controls
GUI settings panel
Improved hand identification
Additional gesture recognition

### Author

Sikander Bukht

GitHub:
https://github.com/sikanderbukht38-cell

### License

This project is intended for educational and personal use.


**One correction before you paste:** in the clone command, use the actual repository URL:

```bash
git clone https://github.com/sikanderbukht38-cell/AI-Hand-Gesture-Controller.git