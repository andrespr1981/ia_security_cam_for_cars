import os
import cv2
import queue
import joblib
import threading
import numpy as np
from sklearn import svm
from deepface import DeepFace

class FaceRecognition():
    def __init__(self,cap):
        self.cap = cap
        self.pred = '...'
        self.embeddings = []
        self.labels = []

        if os.path.exists('model/svm_model.pkl'):
            self.svm_model = joblib.load('model/svm_model.pkl')
            self.embeddings = joblib.load("model/embeddings.pkl")
            self.labels = joblib.load("model/labels.pkl")
        else:
            self.svm_model = svm.SVC(kernel='linear', probability=True)

        self.frame_queue = queue.Queue(maxsize=1)
        self.result_queue = queue.Queue(maxsize=1)
        self.running = True

        self.worker_thread = threading.Thread(target=self.embedding_worker, daemon=True)
        self.worker_thread.start()

    def create_embbedings(self):
        self.embeddings = []
        dir = 'faces'
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
        joblib.dump(self.embeddings, "model/embeddings.pkl") 
        joblib.dump(self.labels, "model/labels.pkl")

    def train_model(self):
        if len(set(self.labels)) < 2:
            print("Error: necesitas al menos 2 clases")
            return
        self.svm_model.fit(self.embeddings, self.labels)
        joblib.dump(self.svm_model, "model/svm_model.pkl")
        return
    
    def embedding_worker(self):
        while self.running:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()

                try:
                    embedding = DeepFace.represent(
                        img_path=frame,
                        model_name="Facenet",
                        enforce_detection=False
                    )[0]["embedding"]

                    proba = self.svm_model.predict_proba([embedding])[0]
                    max_proba = max(proba)
                    pred_class = self.svm_model.classes_[proba.argmax()]

                    distancias = [np.linalg.norm(np.array(embedding) - np.array(e)) for e in self.embeddings]
                    min_dist = min(distancias)

                    print('Max: ',max_proba)
                    print('Min: ',min_dist)

                    if max_proba < 0.8 or min_dist > 7:
                        self.pred = "Desconocido"
                    else:
                        self.pred = pred_class

                    if not self.result_queue.full():
                        self.result_queue.put(self.pred)

                except Exception as e:
                    print("Error en worker:", e)

    def findFaces(self,debug=False):

        while True:
            ret, frame = self.cap.read()
            if not ret:
                continue

            #frame = cv2.resize(frame, (320, 240))

            if not self.frame_queue.full():
                self.frame_queue.put(frame.copy())

            if not self.result_queue.empty():
                self.pred = self.result_queue.get()

            cv2.putText(frame, self.pred, (50, 50),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

            if(debug):
                cv2.imshow("Video", frame)
            else:
                return frame

            if cv2.waitKey(1) & 0xFF == 27:
                self.running = False
                break
    
cap = cv2.VideoCapture(0) 
detector = FaceRecognition(cap=cap)
detector.findFaces(debug=True)
#detector.create_embbedings()
#detector.train_model()
