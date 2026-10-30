"""
Camera detector — uses your real webcam + a pretrained YOLOv8 model to detect
whether a person is in frame, and reports that to the backend.

First run will download the small YOLOv8n model weights (~6MB), so you need
internet access the first time. After that it works offline.

Run with:  python backend/camera_detector.py
(run this in its own terminal; press 'q' in the video window to quit)
"""

import os
import time

import cv2
import requests
from dotenv import load_dotenv
from ultralytics import YOLO

load_dotenv()

BACKEND_URL = os.environ.get("BACKEND_URL", "http://localhost:8000")

CONFIDENCE_THRESHOLD = 0.5   # how sure the model must be before counting it as "a person"
SEND_INTERVAL_SECONDS = 2    # only send an update this often, and only when the state changes

PERSON_CLASS_ID = 0  # in the COCO dataset YOLOv8 is trained on, class 0 is "person"


def send_occupancy(person_present: bool):
    try:
        r = requests.post(
            f"{BACKEND_URL}/occupancy",
            json={"person_present": person_present},
            timeout=3,
        )
        r.raise_for_status()
        print(f"[camera_detector] Sent person_present={person_present}")
    except requests.RequestException as e:
        print(f"[camera_detector] Failed to send occupancy: {e}")


def main():
    model = YOLO("yolov8n.pt")  # smallest/fastest YOLOv8 model — good enough for this
    cap = cv2.VideoCapture(0)   # 0 = default webcam

    if not cap.isOpened():
        print("[camera_detector] Could not open webcam. Check camera permissions / index.")
        return

    last_sent_state = None
    last_sent_time = 0

    print("[camera_detector] Running. Press 'q' in the video window to quit.")

    try:
        while True:
            ok, frame = cap.read()
            if not ok:
                print("[camera_detector] Failed to read frame from webcam.")
                break

            results = model(frame, verbose=False)[0]

            person_present = False
            for box in results.boxes:
                class_id = int(box.cls[0])
                confidence = float(box.conf[0])
                if class_id == PERSON_CLASS_ID and confidence >= CONFIDENCE_THRESHOLD:
                    person_present = True
                    break

            # Draw boxes so you can see what the model sees (handy for the demo)
            annotated = results.plot()
            cv2.imshow("Room Energy Monitor — camera feed", annotated)

            now = time.time()
            state_changed = person_present != last_sent_state
            enough_time_passed = (now - last_sent_time) >= SEND_INTERVAL_SECONDS

            if state_changed or enough_time_passed:
                send_occupancy(person_present)
                last_sent_state = person_present
                last_sent_time = now

            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    main()
