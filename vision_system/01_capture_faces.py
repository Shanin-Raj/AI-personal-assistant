import cv2
import os

def capture_faces():
    face_id = input("Enter user ID and press <return> (e.g. 1 for Shanin): ")
    print(f"Initializing face capture. Look at the camera and wait ...")
    
    # Initialize webcam
    cam = cv2.VideoCapture(0)
    
    # Load OpenCV's pre-trained face detector
    face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    
    count = 0
    # Create dataset dir if it doesn't exist
    if not os.path.exists("dataset"):
        os.makedirs("dataset")

    while True:
        ret, img = cam.read()
        if not ret:
            print("Failed to capture image")
            break
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        # detect faces
        faces = face_detector.detectMultiScale(gray, 1.3, 5)

        for (x,y,w,h) in faces:
            cv2.rectangle(img, (x,y), (x+w,y+h), (255,0,0), 2)     
            count += 1
            
            # Save the captured image into the dataset folder
            cv2.imwrite(f"dataset/User.{face_id}.{count}.jpg", gray[y:y+h,x:x+w])
            cv2.imshow('Image Capture', img)
            
        # Press 'ESC' to exit manually, otherwise wait to collect 100 samples
        k = cv2.waitKey(100) & 0xff
        if k == 27:
            break
        elif count >= 100: 
            break
            
    # Cleanup
    print(f"\nSuccessfully collected {count} samples for User {face_id}.")
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    capture_faces()
