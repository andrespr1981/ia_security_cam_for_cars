import os
import cv2
import joblib
from sklearn import svm
from deepface import DeepFace

class FaceRecognition():
    def __init__(self):
        self.embeddings = []
        self.labels = []

        if os.path.exists('svm_model.pkl'):
            self.svm_model = joblib.load('svm_model.pkl')
            self.embeddings = joblib.load("embeddings.pkl")
            self.labels = joblib.load("labels.pkl")
        else:
            self.svm_model = svm.SVC(kernel='linear', probability=True)

    def create_embbedings(self):
        self.embeddings = []
        dir = 'fotos'
        for person in os.listdir(dir):
            face_dir = os.path.join(dir, person)

            for file in os.listdir(face_dir):
                path = os.path.join(face_dir, file)

                try:
                    embedding = DeepFace.represent(
                        img_path=path,
                        model_name="Facenet",
                        enforce_detection=False
                    )[0]["embedding"]

                    self.embeddings.append(embedding)
                    self.labels.append(person)  

                    print(f"Procesado: {file}")

                except Exception as e:
                    print(f"Error en {file}: {e}")  
        joblib.dump(self.embeddings, "embeddings.pkl") 
        joblib.dump(self.labels, "labels.pkl")

    def train_model(self):
        if len(set(self.labels)) < 2:
            print("Error: necesitas al menos 2 clases")
            return
        self.svm_model.fit(self.embeddings, self.labels)
        joblib.dump(self.svm_model, "svm_model.pkl")
        return

    def findFaces(self,cap):
        ret, frame = cap.read()

        if not ret:
            return

        try:
            embedding = DeepFace.represent(
                img_path=frame,
                model_name="Facenet",
                enforce_detection=False
            )[0]["embedding"]

            pred = self.svm_model.predict([embedding])[0]

            cv2.putText(frame, pred, (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

        except Exception as e:
            print("Error:", e)

        return frame