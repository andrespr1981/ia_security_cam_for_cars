import os
import cv2
import queue
import joblib
import threading
import numpy as np
from sklearn import svm
from deepface import DeepFace

class FaceRecognition():
    def __init__(self):
        self.timer = 0
        self.pred = '.'
        self.results = []
        self.face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

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
    
    def embedding_worker(self):

        while self.running:
            if not self.frame_queue.empty():
                frame = self.frame_queue.get()

                try:
                    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

                    faces = self.face_detector.detectMultiScale(
                        gray,
                        scaleFactor=1.1,
                        minNeighbors=5,
                        minSize=(80, 80)
                    )

                    results = []

                    for (x, y, w, h) in faces:

                        face_crop = frame[y:y+h, x:x+w]

                        embedding = DeepFace.represent(
                            img_path=face_crop,
                            model_name="Facenet",
                            enforce_detection=False
                        )[0]["embedding"]

                        proba = self.svm_model.predict_proba([embedding])[0]

                        max_proba = max(proba)

                        pred_class = self.svm_model.classes_[proba.argmax()]

                        distancias = [
                            np.linalg.norm(
                                np.array(embedding) - np.array(e)
                            )
                            for e in self.embeddings
                        ]

                        min_dist = min(distancias)

                        if max_proba < 0.8 or min_dist > 10 or min_dist < 3:
                            pred = "Desconocido"
                        else:
                            pred = pred_class

                        results.append({
                            "name": pred,
                            "box": (x, y, w, h)
                        })

                    if not self.result_queue.full():
                        self.result_queue.put(results)

                except Exception as e:
                    print("Error en worker:", e)

    def findFaces(self,cap, debug=False):
        while True:

            ret, frame = cap.read()

            if not ret:
                continue

            if not self.frame_queue.full():
                self.frame_queue.put(frame.copy())

            if not self.result_queue.empty():
               self.results = self.result_queue.get()

            for result in self.results:

                x, y, w, h = result["box"]
                name = result["name"]

                cv2.rectangle(
                    frame,
                    (x, y),
                    (x + w, y + h),
                    (0, 255, 0),
                    2
                )

                cv2.putText(
                    frame,
                    name,
                    (x, y - 10),
                    cv2.FONT_HERSHEY_SIMPLEX,
                    0.9,
                    (0, 255, 0),
                    2
                )

            if debug:
                cv2.imshow("Video", frame)
            else:
                return frame

            if cv2.waitKey(1) & 0xFF == 27:
                self.running = False
                break
    
test = False

if(test):
    cap = cv2.VideoCapture(0) 
    detector = FaceRecognition()
    detector.findFaces(cap,debug=True)
