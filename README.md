# AI Hand Gesture Volume Controller

AI-powered Windows volume control using real-time hand gestures and a webcam.

## Features

- Real-time hand tracking
- Gesture-based volume control
- Thumb and index finger distance controls volume
- Smooth volume adjustment
- Windows system volume control
- Live volume percentage display
- Visual volume bar
- Blue line between thumb and index finger
- Two-hand gesture detection
- Open-palm lock and unlock gesture
- Persistent volume lock
- Mute and unmute
- Volume reset
- Keyboard controls

## How It Works

### Volume Control

The first detected hand controls the system volume.

Move your thumb and index finger closer together or farther apart to change the volume.

**Fingers close = Lower volume**

**Fingers apart = Higher volume**

The distance between the thumb and index finger is converted into a volume percentage from 0% to 100%.

### Volume Lock

The second hand is used to lock and unlock the volume controller.

Show an open palm with the second hand to toggle the lock.

The lock remains active even after the second hand is removed.

**Unlocked → Show second-hand palm → Locked**

**Locked → Show second-hand palm again → Unlocked**

## Keyboard Controls

- `Q` — Quit the application
- `M` — Mute / Unmute
- `R` — Reset volume to 50% and unlock

## Technologies Used

- Python
- OpenCV
- MediaPipe
- Pycaw
- Windows Core Audio

## Project Structure

AI-Hand-Gesture-Controller/

├── main.py

├── hand_tracker.py

├── volume_control.py

├── hand_landmarker.task

├── .gitignore

└── README.md

## File Description

### main.py

The main application that connects hand tracking, gesture recognition, volume control, and the user interface.

### hand_tracker.py

Handles MediaPipe hand detection, hand landmarks, gesture recognition, and thumb-index distance calculation.

### volume_control.py

Controls the Windows system volume using Pycaw.

### hand_landmarker.task

MediaPipe's hand landmark model used for real-time hand tracking.

## Installation

### 1. Clone the Repository

git clone https://github.com/sikanderbukht38-cell/AI-Hand-Gesture-Controller.git

### 2. Open the Project

cd AI-Hand-Gesture-Controller

### 3. Create a Virtual Environment

python -m venv .venv

### 4. Activate the Virtual Environment

.venv\Scripts\Activate.ps1

### 5. Install Dependencies

pip install opencv-contrib-python mediapipe pycaw comtypes

### 6. Run the Application

python main.py

## Requirements

- Windows
- Python 3.10 or newer
- Webcam
- Speakers or headphones
- Camera permissions enabled

## Volume Mapping

The thumb-index distance is mapped approximately as:

0.03 = 0% volume

0.22 = 100% volume

These values can be adjusted in `main.py` to change the sensitivity.

## Usage

1. Start the application.
2. Allow access to your webcam.
3. Use your first hand to control the volume.
4. Move your thumb and index finger to adjust the volume.
5. Show an open palm with your second hand to lock the volume.
6. Remove the second hand. The volume remains locked.
7. Show the second-hand palm again to unlock the volume.
8. Press `Q` to exit.

## Future Improvements

- Play and pause music using gestures
- Next and previous track controls
- Brightness control
- Application-specific volume control
- Customizable gestures
- Gesture-based media controls
- GUI settings panel
- Improved hand identification
- Additional gesture recognition

## Author

**Sikander Bukht**

GitHub: https://github.com/sikanderbukht38-cell

## License

This project is intended for educational and personal use.