"""
S.H.A.N.I.N. Mark II - Vision-Gated Personal Assistant
-------------------------------------------------------
This script acts as a face-unlock entry point.
It runs face recognition on the webcam feed. Once it positively
identifies the owner (Shanin), it closes the camera and
automatically launches the Mark I assistant.
"""

import cv2
import numpy as np
import os
import sys
import subprocess

def authenticate_face():
    """
    Runs a live face recognition loop.
    Returns True if 'Shanin' is detected with >30% confidence
    for a sustained number of frames (to avoid false positives).
    Returns False if the user manually exits (ESC).
    """
    recognizer = cv2.face.LBPHFaceRecognizer_create()

    model_path = os.path.join(os.path.dirname(__file__), 'vision_system', 'models', 'trainer.yml')
    if not os.path.exists(model_path):
        print("[ERROR] Face model not found. Please run the training scripts first:")
        print("  1. python vision_system/01_capture_faces.py")
        print("  2. python vision_system/02_train_model.py")
        return False

    recognizer.read(model_path)

    cascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    font = cv2.FONT_HERSHEY_SIMPLEX

    # Map user IDs to names
    id_names = ['None', 'Shanin']

    cam = cv2.VideoCapture(0)
    if not cam.isOpened():
        print("[ERROR] Could not access the webcam.")
        return False

    print("\n=== S.H.A.N.I.N. Mark II: Face Authentication ===")
    print("Looking for authorized user... Press 'ESC' to cancel.\n")

    # Require multiple consecutive positive frames to confirm identity
    REQUIRED_CONFIRMATIONS = 10
    confirmation_count = 0

    while True:
        ret, img = cam.read()
        if not ret:
            break

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor=1.2,
            minNeighbors=5,
            minSize=(30, 30),
        )

        identified_this_frame = False

        for (x, y, w, h) in faces:
            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            confidence_pct = round(100 - confidence)

            # Only recognize as Shanin if confidence percentage > 30%
            if confidence < 70 and id < len(id_names):
                id_text = id_names[id]
                color = (0, 255, 0)  # Green for recognized
                identified_this_frame = True
            else:
                id_text = "Unknown"
                color = (0, 0, 255)  # Red for unknown

            cv2.rectangle(img, (x, y), (x + w, y + h), color, 2)
            cv2.putText(img, id_text, (x + 5, y - 5), font, 1, (255, 255, 255), 2)
            cv2.putText(img, f"{confidence_pct}%", (x + 5, y + h - 5), font, 1, (255, 255, 0), 1)

        # Track consecutive positive identifications
        if identified_this_frame:
            confirmation_count += 1
            # Show a progress bar on screen
            progress = int((confirmation_count / REQUIRED_CONFIRMATIONS) * 200)
            cv2.rectangle(img, (10, 10), (10 + progress, 30), (0, 255, 0), -1)
            cv2.putText(img, "Authenticating...", (15, 50), font, 0.6, (0, 255, 0), 1)
        else:
            confirmation_count = 0

        cv2.imshow('S.H.A.N.I.N. - Face Authentication', img)

        # If we have enough consecutive confirmations, authenticate!
        if confirmation_count >= REQUIRED_CONFIRMATIONS:
            print("[SUCCESS] Identity confirmed: Shanin")
            cam.release()
            cv2.destroyAllWindows()
            return True

        # Press ESC to cancel
        k = cv2.waitKey(10) & 0xff
        if k == 27:
            print("[INFO] Authentication cancelled by user.")
            cam.release()
            cv2.destroyAllWindows()
            return False

    cam.release()
    cv2.destroyAllWindows()
    return False


def launch_assistant():
    """Launches the Mark I assistant script."""
    mark_one_path = os.path.join(os.path.dirname(__file__), 'mark_one.py')
    print("\n=== Launching S.H.A.N.I.N. Mark I Assistant ===\n")
    # Use subprocess.run to hand control over to mark_one.py
    # sys.executable ensures we use the same Python interpreter
    subprocess.run([sys.executable, mark_one_path])


if __name__ == "__main__":
    print("=" * 50)
    print("  S.H.A.N.I.N. Mark II - Vision System")
    print("  Face Authentication Required")
    print("=" * 50)

    authenticated = authenticate_face()

    if authenticated:
        launch_assistant()
    else:
        print("\n[ACCESS DENIED] Face not recognized. Exiting.")
