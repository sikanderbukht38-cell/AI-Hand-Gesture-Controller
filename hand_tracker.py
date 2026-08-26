import cv2
import mediapipe as mp
import math


class HandTracker:

    def __init__(
        self,
        max_hands=2,
        detection_confidence=0.7,
        tracking_confidence=0.7
    ):
        self.base_options = mp.tasks.BaseOptions(
            model_asset_path="hand_landmarker.task"
        )

        self.options = mp.tasks.vision.HandLandmarkerOptions(
            base_options=self.base_options,
            running_mode=mp.tasks.vision.RunningMode.VIDEO,
            num_hands=max_hands,
            min_hand_detection_confidence=detection_confidence,
            min_hand_presence_confidence=detection_confidence,
            min_tracking_confidence=tracking_confidence
        )

        self.detector = (
            mp.tasks.vision.HandLandmarker.create_from_options(
                self.options
            )
        )

        self.timestamp = 0

    def find_hands(self, frame):

        rgb_frame = cv2.cvtColor(
            frame,
            cv2.COLOR_BGR2RGB
        )

        mp_image = mp.Image(
            image_format=mp.ImageFormat.SRGB,
            data=rgb_frame
        )

        self.timestamp += 1

        results = self.detector.detect_for_video(
            mp_image,
            self.timestamp
        )

        if results.hand_landmarks:

            h, w, _ = frame.shape

            connections = [
                (0, 1), (1, 2), (2, 3), (3, 4),
                (0, 5), (5, 6), (6, 7), (7, 8),
                (5, 9), (9, 10), (10, 11), (11, 12),
                (9, 13), (13, 14), (14, 15), (15, 16),
                (13, 17), (17, 18), (18, 19), (19, 20),
                (0, 17)
            ]

            for landmarks in results.hand_landmarks:

                # -------------------------------
                # Draw hand connections
                # -------------------------------

                for connection in connections:

                    x1 = int(
                        landmarks[connection[0]].x * w
                    )
                    y1 = int(
                        landmarks[connection[0]].y * h
                    )

                    x2 = int(
                        landmarks[connection[1]].x * w
                    )
                    y2 = int(
                        landmarks[connection[1]].y * h
                    )

                    cv2.line(
                        frame,
                        (x1, y1),
                        (x2, y2),
                        (0, 255, 0),
                        2
                    )

                # -------------------------------
                # Draw landmarks
                # -------------------------------

                for landmark in landmarks:

                    x = int(landmark.x * w)
                    y = int(landmark.y * h)

                    cv2.circle(
                        frame,
                        (x, y),
                        5,
                        (0, 0, 255),
                        -1
                    )

                # -------------------------------
                # Blue thumb-index line
                # -------------------------------

                thumb_x = int(
                    landmarks[4].x * w
                )
                thumb_y = int(
                    landmarks[4].y * h
                )

                index_x = int(
                    landmarks[8].x * w
                )
                index_y = int(
                    landmarks[8].y * h
                )

                cv2.line(
                    frame,
                    (thumb_x, thumb_y),
                    (index_x, index_y),
                    (255, 0, 0),
                    3
                )

        return frame, results

    def get_thumb_index_distance(
        self,
        results,
        hand_index=0
    ):

        if not results.hand_landmarks:
            return None

        if len(results.hand_landmarks) <= hand_index:
            return None

        landmarks = results.hand_landmarks[hand_index]

        thumb = landmarks[4]
        index = landmarks[8]

        distance = math.sqrt(
            (thumb.x - index.x) ** 2 +
            (thumb.y - index.y) ** 2
        )

        return distance

    def is_open_palm(
        self,
        results,
        hand_index=0
    ):

        if not results.hand_landmarks:
            return False

        if len(results.hand_landmarks) <= hand_index:
            return False

        landmarks = results.hand_landmarks[hand_index]

        # Finger tips
        index_tip = landmarks[8]
        middle_tip = landmarks[12]
        ring_tip = landmarks[16]
        pinky_tip = landmarks[20]

        # PIP joints
        index_pip = landmarks[6]
        middle_pip = landmarks[10]
        ring_pip = landmarks[14]
        pinky_pip = landmarks[18]

        # Check whether fingers are extended
        index_open = index_tip.y < index_pip.y
        middle_open = middle_tip.y < middle_pip.y
        ring_open = ring_tip.y < ring_pip.y
        pinky_open = pinky_tip.y < pinky_pip.y

        return (
            index_open
            and middle_open
            and ring_open
            and pinky_open
        )

    def get_hand_count(self, results):

        if not results.hand_landmarks:
            return 0

        return len(results.hand_landmarks)