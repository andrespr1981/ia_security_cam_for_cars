import cv2
import time
import base64
import threading
import flet as ft
from components.navbar import Navbar
from utils.csv_handler import *
#from FaceRecognition import FaceRecognition

cap = cv2.VideoCapture(0)
#detector = FaceRecognition(cap=cap)

def main(page: ft.Page):
    page.title = 'SecureCar IA'
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window_maximized = True
    page.window_full_screen = True
    page.window_resizable = True
    page.padding = 20

    ia_activated = True

    video = ft.Image(src='images/test.jpg')
    video_container = ft.Container(content=video,alignment=ft.Alignment.CENTER,width=800)

    page.add(
        Navbar(page),
        ft.SafeArea(content=video_container)
    )

    def video_loop():
        frame = None
        while cap.isOpened():

            if ia_activated:
                video_container.content = video
                frame = detector.findFaces()
            else:
                ret,frame = cap.read()
                if not ret:
                    continue

            if frame is not None:
                    _, buffer = cv2.imencode('.jpg', frame)
                    img_base64 = base64.b64encode(buffer).decode()

                    video.src_base64 = img_base64
                    page.update()
            else:
                video_container.content = ft.ProgressRing()
                page.update()
            time.sleep(0.03)

    #threading.Thread(target=video_loop, daemon=True).start()
                

ft.run(main)