import cv2
import base64
import asyncio
import flet as ft
from components.navbar import Navbar
from components.info_container import info_container
from components.alert_container import alert_container
#from FaceRecognition import FaceRecognition
from utils.csv_handler import read_csv,write_csv



#cap = cv2.VideoCapture(0)
#detector = FaceRecognition(cap=cap)

def main(page: ft.Page):
    page.title = 'Driver Guard'
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window_maximized = True
    page.window_full_screen = True
    page.window_resizable = True

    ia_activated = True
    recording_activated = False
    today_alerts = 90
    storage = 90

    alerts = read_csv()

    video = ft.Image(src='images/test.jpg',gapless_playback=True,border_radius=ft.BorderRadius.all(20))
    video_container = ft.Container(content=video,alignment=ft.Alignment.CENTER,width=800,border=ft.BorderRadius.all(10))

    page.add(
        Navbar(page),
        ft.SafeArea(
           content=ft.Row(
               controls=[
                   ft.Column(
               controls=[
                   video_container,
                    ft.Container(
                       content=ft.Row(controls=[
                           info_container(ia_activated,recording_activated,today_alerts,storage),
                       ])
                    ),
                   
               ]
            ),
            alert_container(alerts)
               ]
           )
        )
    )

    async def video_loop():
        nonlocal video, video_container
        frame = None

        while cap.isOpened():

            if ia_activated:
                video_container.content = video
                frame = detector.findFaces()
            else:
                ret, frame = cap.read()
                if not ret:
                    continue

            if frame is not None:
                _, buffer = cv2.imencode('.jpg', frame)
                img_base64 = base64.b64encode(buffer).decode("utf-8")

                video.src = img_base64
            else:
                video_container.content = ft.ProgressRing()

            page.update()
            await asyncio.sleep(0.03)
          

    #page.run_task(video_loop)
                

ft.run(main)