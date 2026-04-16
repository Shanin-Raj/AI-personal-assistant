import cv2
import numpy as np
import os
from PIL import Image

def get_images_and_labels(path, detector):
    image_paths = [os.path.join(path, f) for f in os.listdir(path) if f.endswith('.jpg')]     
    face_samples = []
    ids = []
    
    for imagePath in image_paths:
        # Convert image to grayscale using PIL
        pil_image = Image.open(imagePath).convert('L')
        # Convert PIL image to numpy array
        img_numpy = np.array(pil_image, 'uint8')
        
        # The filename is like "User.1.45.jpg", so splitting by "." gets the ID
        id = int(os.path.split(imagePath)[-1].split(".")[1])
        
        # Extract the face from the training image
        faces = detector.detectMultiScale(img_numpy)
        for (x, y, w, h) in faces:
            face_samples.append(img_numpy[y:y+h, x:x+w])
            ids.append(id)
            
    return face_samples, ids

def train_model():
    path = 'dataset'
    
    if not os.path.exists(path) or len(os.listdir(path)) == 0:
        print(f"Error: No images found in {path}. Run 01_capture_faces.py first.")
        return

    print("\nTraining faces. This will take a few seconds. Wait ...")
    
    recognizer = cv2.face.LBPHFaceRecognizer_create()
    detector = cv2.CascadeClassifier(cv2.data.haarcascades + "haarcascade_frontalface_default.xml")
    
    # Get faces and IDs
    faces, ids = get_images_and_labels(path, detector)
    
    # Train the recognizer
    recognizer.train(faces, np.array(ids))
    
    # Save the model
    if not os.path.exists('models'):
        os.makedirs('models')
        
    recognizer.write('models/trainer.yml') 
    
    print(f"\n[INFO] {len(np.unique(ids))} face(s) trained. Model saved to models/trainer.yml.")

if __name__ == "__main__":
    train_model()
