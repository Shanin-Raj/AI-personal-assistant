import cv2
import numpy as np
import os 

def start_recognition():
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    
    # Load the trained model
    if not os.path.exists('models/trainer.yml'):
        print("Error: Could not find 'models/trainer.yml'. Please run 01_capture_faces.py and 02_train_model.py first.")
        return
        
    recognizer.read('models/trainer.yml')
    
    cascadePath = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
    faceCascade = cv2.CascadeClassifier(cascadePath)
    
    font = cv2.FONT_HERSHEY_SIMPLEX
    
    # Map ID to name. Since we instructed the user to use ID 1 for Shanin:
    id_names = ['None', 'Shanin'] 
    
    cam = cv2.VideoCapture(0)
    print("\nStarting Face Recognition. Press 'ESC' to exit.")
    
    while True:
        ret, img = cam.read()
        if not ret:
            break
            
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        faces = faceCascade.detectMultiScale(
            gray,
            scaleFactor = 1.2,
            minNeighbors = 5,
            minSize = (30, 30),
        )
        
        for(x, y, w, h) in faces:
            cv2.rectangle(img, (x,y), (x+w, y+h), (0, 255, 0), 2)
            
            # Predict the face
            id, confidence = recognizer.predict(gray[y:y+h, x:x+w])
            
            # Only recognize as Shanin if confidence percentage (100 - distance) > 30%
            # i.e. the raw distance must be < 70
            if confidence < 70:
                id_text = id_names[id] if id < len(id_names) else f"User {id}"
            else:
                id_text = "Unknown"
            
            # Display properties
            cv2.putText(img, str(id_text), (x+5, y-5), font, 1, (255, 255, 255), 2)
            # Display confidence (Lower distance value means higher confidence)
            cv2.putText(img, f"{round(100 - confidence)}%", (x+5, y+h-5), font, 1, (255, 255, 0), 1)  
        
        cv2.imshow('S.H.A.N.I.N - Visual Identification Matrix (Mark II)', img) 
        
        k = cv2.waitKey(10) & 0xff 
        if k == 27: # Press 'ESC' for exiting video
            break
            
    print("\nExiting Program")
    cam.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    start_recognition()
