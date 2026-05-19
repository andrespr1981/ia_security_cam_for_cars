import os
import cv2
import time
import queue
import joblib
import threading
import numpy as np
from utils.sound import play_sound
from sklearn import svm
from deepface import DeepFace
from utils.send_email import send_email

class FaceRecognition():
    def __init__(self,on_alert=None):
        self.unknown_start_time = None
        self.sent_alert = False
        self.on_alert = on_alert
        self.time_end = 0
        self.motion_start_time = None
        self.last_motion_alert_time = 0
        self.motion_cooldown = 30
        self.pred = '.'
        self.results = []
        self.face_detector = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
        self.motion_detector = cv2.createBackgroundSubtractorMOG2(history=100,varThreshold=40,detectShadows=True)

        if os.path.exists('model/svm_model.pkl'):
            self.svm_model = joblib.load('model/svm_model.pkl')
            self.embeddings = joblib.load("model/embeddings.pkl")
            self.labels = joblib.load("model/labels.pkl")
        else:
            self.svm_model = svm.SVC(kernel='linear', probability=True)

        self.frame_queue = queue.Queue(maxsize=1)
        self.result_queue = queue.Queue(maxsize=1)
        self.motion_queue = queue.Queue(maxsize=1)
        self.motion_result_queue = queue.Queue(maxsize=1)
        self.running = True

        self.worker_thread = threading.Thread(target=self.embedding_worker, daemon=True)
        self.worker_thread.start()
        #self.motion_thread = threading.Thread(target=self.motion_worker,daemon=True)
        #self.motion_thread.start()
    
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
                            detector_backend='skip',
                            enforce_detection=False,
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

                        if max_proba < 0.8 or min_dist > 10:
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
                    print("Error:", e)

    def motion_worker(self):

        while self.running:

            if not self.motion_queue.empty():

                frame = self.motion_queue.get()

                motion_mask = self.motion_detector.apply(frame)

                _, motion_mask = cv2.threshold(
                    motion_mask,
                    200,
                    255,
                    cv2.THRESH_BINARY
                )

                contours, _ = cv2.findContours(
                    motion_mask,
                    cv2.RETR_EXTERNAL,
                    cv2.CHAIN_APPROX_SIMPLE
                )

                motion_boxes = []

                for contour in contours:

                    area = cv2.contourArea(contour)

                    if area > 3000:

                        x, y, w, h = cv2.boundingRect(contour)

                        motion_boxes.append(
                            (x, y, w, h)
                        )

                if not self.motion_result_queue.full():

                    self.motion_result_queue.put(
                        motion_boxes
                    )

    def findFaces(self,cap, debug=False):

        ret, frame = cap.read()
        if not ret:
            return

        if not self.frame_queue.full():
            self.frame_queue.put(frame.copy())

        if not self.motion_queue.full():
            self.motion_queue.put(frame.copy())

        if not self.result_queue.empty():
            self.results = self.result_queue.get()

        motion_results = []

        if not self.motion_result_queue.empty():
            motion_results = self.motion_result_queue.get()


        motion_detected = len(motion_results) > 0
        for (x, y, w, h) in motion_results:

            cv2.rectangle(
                frame,
                (x, y),
                (x+w, y+h),
                (255, 0, 0),
                2
            )

        current_time = time.perf_counter()

        unknown_face = False
        known_face = False
        face_detected = len(self.results) > 0

        for result in self.results:
                
            if result['name'] == 'Desconocido':
                unknown_face = True
            else:
                known_face = True

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

        if unknown_face and not known_face:

            if self.unknown_start_time is None:
                self.unknown_start_time = current_time

            elapsed = current_time - self.unknown_start_time

            if elapsed >= 10 and not self.sent_alert:

                self.on_alert('Cara desconocida',frame)
                threading.Thread(
                    target=send_email,
                    args=(
                        'al22760571@ite.edu.mx',
                        'Cara desconocida'
                    ),
                    daemon=True
                ).start()
                threading.Thread(
                    target=play_sound,
                    daemon=True
                ).start()

                self.sent_alert = True
                self.unknown_start_time = None
        else:

            self.unknown_start_time = None
            self.sent_alert = False

        if motion_detected and not face_detected:

            if self.motion_start_time is None:
                self.motion_start_time = current_time

            elapsed_motion = current_time - self.motion_start_time

            cooldown_elapsed = (
                current_time - self.last_motion_alert_time
            )

            if (
                elapsed_motion >= 10
                and cooldown_elapsed >= self.motion_cooldown
            ):

                self.on_alert(
                    'Movimiento sospechoso detectado',
                    frame
                )

                threading.Thread(
                    target=send_email,
                    args=(
                        'al22760571@ite.edu.mx',
                        'Movimiento sospechoso detectado'
                    ),
                    daemon=True
                ).start()

                threading.Thread(
                    target=play_sound,
                    daemon=True
                ).start()

                self.last_motion_alert_time = current_time

        else:

            self.motion_start_time = None

        if debug:
            cv2.imshow("Video", frame)
        else:
            return frame

        if cv2.waitKey(1) & 0xFF == 27:
            self.running = False
            

test = False

if(test):
    cap = cv2.VideoCapture(0) 
    detector = FaceRecognition()
    detector.findFaces(cap,debug=True)
