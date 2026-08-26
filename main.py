import cv2
import time

from collections import deque

from hand_tracker import HandTracker
from volume_control import VolumeController


# =========================================================
# SETTINGS
# =========================================================

# Minimum thumb-index distance
MIN_DISTANCE = 0.03

# Maximum thumb-index distance
MAX_DISTANCE = 0.22

# Number of readings used for smoothing
SMOOTHING_FRAMES = 5

# Camera resolution
CAMERA_WIDTH = 1280
CAMERA_HEIGHT = 720


# =========================================================
# INITIALIZATION
# =========================================================

tracker = HandTracker(
    max_hands=2
)

volume = VolumeController()

cap = cv2.VideoCapture(0)

cap.set(
    cv2.CAP_PROP_FRAME_WIDTH,
    CAMERA_WIDTH
)

cap.set(
    cv2.CAP_PROP_FRAME_HEIGHT,
    CAMERA_HEIGHT
)


# =========================================================
# STATE
# =========================================================

# Volume starts UNLOCKED
volume_locked = False

# Prevent one palm from toggling repeatedly
palm_was_detected = False

# Smooth volume readings
volume_history = deque(
    maxlen=SMOOTHING_FRAMES
)

# Keyboard mute state
muted = volume.is_muted()

# Startup timer
startup_time = time.time()

# Startup duration
STARTUP_DURATION = 2.0


# =========================================================
# HELPER FUNCTION
# =========================================================

def map_distance_to_volume(distance):

    volume_level = (
        (distance - MIN_DISTANCE)
        / (MAX_DISTANCE - MIN_DISTANCE)
    ) * 100

    volume_level = max(
        0,
        min(
            100,
            volume_level
        )
    )

    return int(volume_level)


# =========================================================
# MAIN LOOP
# =========================================================

while True:

    success, frame = cap.read()

    if not success:

        print(
            "Failed to read from camera."
        )

        break

    # Mirror camera
    frame = cv2.flip(
        frame,
        1
    )

    # =====================================================
    # HAND TRACKING
    # =====================================================

    frame, results = tracker.find_hands(
        frame
    )

    hand_count = tracker.get_hand_count(
        results
    )

    # =====================================================
    # SECOND HAND PALM LOCK / UNLOCK
    # =====================================================

    second_palm = False

    if hand_count >= 2:

        second_palm = tracker.is_open_palm(
            results,
            hand_index=1
        )

    # -----------------------------------------------------
    # Palm appeared
    # -----------------------------------------------------

    if second_palm and not palm_was_detected:

        volume_locked = not volume_locked

        if volume_locked:

            print(
                "VOLUME LOCKED"
            )

        else:

            print(
                "VOLUME UNLOCKED"
            )

    # Remember palm state
    palm_was_detected = second_palm

    # =====================================================
    # VOLUME CONTROL
    # =====================================================

    volume_level = volume.get_volume()

    if (
        hand_count >= 1
        and not volume_locked
        and not muted
    ):

        distance = tracker.get_thumb_index_distance(
            results,
            hand_index=0
        )

        if distance is not None:

            raw_volume = map_distance_to_volume(
                distance
            )

            # Add reading to smoothing buffer
            volume_history.append(
                raw_volume
            )

            # Calculate smooth volume
            volume_level = int(
                sum(volume_history)
                / len(volume_history)
            )

            volume.set_volume(
                volume_level
            )

    # =====================================================
    # STARTUP SCREEN
    # =====================================================

    elapsed_time = (
        time.time() - startup_time
    )

    if elapsed_time < STARTUP_DURATION:

        overlay = frame.copy()

        cv2.rectangle(
            overlay,
            (0, 0),
            (
                frame.shape[1],
                frame.shape[0]
            ),
            (0, 0, 0),
            -1
        )

        cv2.addWeighted(
            overlay,
            0.75,
            frame,
            0.25,
            0,
            frame
        )

        cv2.putText(
            frame,
            "AI HAND GESTURE",
            (
                50,
                250
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.5,
            (255, 255, 255),
            3
        )

        cv2.putText(
            frame,
            "VOLUME CONTROLLER",
            (
                50,
                310
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            1.2,
            (255, 255, 255),
            2
        )

        cv2.putText(
            frame,
            "Initializing...",
            (
                50,
                380
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.8,
            (200, 200, 200),
            2
        )

        cv2.imshow(
            "AI Hand Gesture Volume Controller",
            frame
        )

        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

        continue

    # =====================================================
    # UI HEADER
    # =====================================================

    cv2.rectangle(
        frame,
        (0, 0),
        (
            frame.shape[1],
            70
        ),
        (25, 25, 25),
        -1
    )

    cv2.putText(
        frame,
        "AI HAND GESTURE VOLUME CONTROLLER",
        (
            25,
            45
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.85,
        (255, 255, 255),
        2
    )

    # =====================================================
    # VOLUME DISPLAY
    # =====================================================

    cv2.putText(
        frame,
        f"{volume_level}%",
        (
            30,
            125
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        1.3,
        (255, 255, 255),
        3
    )

    # =====================================================
    # VOLUME BAR
    # =====================================================

    bar_x = 30
    bar_y = 150

    bar_width = 400
    bar_height = 35

    # Background
    cv2.rectangle(
        frame,
        (
            bar_x,
            bar_y
        ),
        (
            bar_x + bar_width,
            bar_y + bar_height
        ),
        (70, 70, 70),
        -1
    )

    # Filled section
    filled_width = int(
        bar_width
        * volume_level
        / 100
    )

    cv2.rectangle(
        frame,
        (
            bar_x,
            bar_y
        ),
        (
            bar_x + filled_width,
            bar_y + bar_height
        ),
        (0, 255, 0),
        -1
    )

    # Border
    cv2.rectangle(
        frame,
        (
            bar_x,
            bar_y
        ),
        (
            bar_x + bar_width,
            bar_y + bar_height
        ),
        (255, 255, 255),
        2
    )

    # LOCK STATUS

    if volume_locked:

        status_text = "LOCKED"

        status_color = (
            0,
            0,
            255
        )

    else:

        status_text = "UNLOCKED"

        status_color = (
            0,
            255,
            0
        )

    cv2.putText(
        frame,
        f"STATUS: {status_text}",
        (
            30,
            230
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.9,
        status_color,
        2
    )

    # HAND COUNT

    cv2.putText(
        frame,
        f"Hands detected: {hand_count}",
        (
            30,
            270
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.65,
        (255, 255, 255),
        2
    )

    # INSTRUCTIONS PANEL

    panel_x = 30
    panel_y = 310
    panel_width = 500
    panel_height = 175

    cv2.rectangle(
        frame,
        (
            panel_x,
            panel_y
        ),
        (
            panel_x + panel_width,
            panel_y + panel_height
        ),
        (30, 30, 30),
        -1
    )

    cv2.rectangle(
        frame,
        (
            panel_x,
            panel_y
        ),
        (
            panel_x + panel_width,
            panel_y + panel_height
        ),
        (100, 100, 100),
        2
    )

    cv2.putText(
        frame,
        "CONTROLS",
        (
            panel_x + 20,
            panel_y + 35
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.75,
        (255, 255, 255),
        2
    )

    cv2.putText(
        frame,
        "1 Hand: Thumb + Index = Volume",
        (
            panel_x + 20,
            panel_y + 75
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (220, 220, 220),
        1
    )

    cv2.putText(
        frame,
        "2nd Open Palm = Lock / Unlock",
        (
            panel_x + 20,
            panel_y + 105
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (220, 220, 220),
        1
    )

    cv2.putText(
        frame,
        "Palm disappears = State stays",
        (
            panel_x + 20,
            panel_y + 135
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.55,
        (220, 220, 220),
        1
    )

    # KEYBOARD CONTROLS
    keyboard_text = (
        "Q: Quit   M: Mute/Unmute   R: Reset"
    )

    cv2.putText(
        frame,
        keyboard_text,
        (
            30,
            frame.shape[0] - 25
        ),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.6,
        (255, 255, 255),
        2
    )


    # MUTE STATUS


    if muted:

        cv2.putText(
            frame,
            "MUTED",
            (
                470,
                125
            ),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.9,
            (0, 0, 255),
            2
        )

    # 
    # SHOW CAMERA
    # 

    cv2.imshow(
        "AI Hand Gesture Volume Controller",
        frame
    )


    # KEYBOARD CONTROLS

    key = cv2.waitKey(1) & 0xFF

    # Q = Quit

    if key == ord("q"):

        break

    # M = Mute / Unmute

    elif key == ord("m"):

        if volume.is_muted():

            volume.unmute()

            muted = False

            print(
                "UNMUTED"
            )

        else:

            volume.mute()

            muted = True

            print(
                "MUTED"
            )

    # R = Reset volume to 50%

    elif key == ord("r"):

        volume.unmute()

        muted = False

        volume_locked = False

        volume_history.clear()

        volume.set_volume(
            50
        )

        volume_level = 50

        print(
            "RESET: Volume 50%, Unlocked"
        )

# CLEANUP

cap.release()

cv2.destroyAllWindows()