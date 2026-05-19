import os
import cv2
import time
import base64
import asyncio
import flet as ft
from components.navbar import Navbar
from views.photos_views import photos_view
from FaceRecognition import FaceRecognition
from utils.csv_handler import insert_row, read_csv
from components.info_container import info_container
from components.alert_container import alert_container, mini_alert_container

cap = cv2.VideoCapture(0)

def main(page: ft.Page):
    page.title = 'Driver Guard'
    page.theme_mode = ft.ThemeMode.LIGHT
    page.window_maximized = True
    page.window_full_screen = True
    page.window_resizable = True
    
    def load_alerts():
        alert_container_widget.content.controls.clear()
        alerts = read_csv() 
        for alert in alerts:

            alert_container_widget.content.controls.append(
                mini_alert_container(
                    alert['id'],
                    alert['title'],
                    alert['text'],
                    alert['time'],
                    alert['level'],
                    load_alerts
                )
            )

        page.update()

    recording_activated = {'state':True}

    def create_alert(reason,frame):
        if recording_activated['state']:
            timestamp = time.strftime("%Y%m%d_%H%M%S")
            cv2.imwrite(f'faces/unknown/{timestamp}.jpg', frame)
        insert_row(reason)
        load_alerts()
        
    detector = FaceRecognition(on_alert=create_alert)
    dir = 'faces/unknown'
    photos = 0
    for _ in os.listdir(dir):
        photos += 1
    ia_activated = {'state':True}
    storage = photos
    alerts = read_csv()
    today_alerts = len(alerts)

    video = ft.Image(src='images/test.jpg',gapless_playback=True,border_radius=ft.BorderRadius.all(20))
    video_container = ft.Container(content=video,alignment=ft.Alignment.CENTER,width=800,border=ft.BorderRadius.all(10))

    alert_container_widget = None
    alert_container_widget = alert_container(alerts,load_alerts)

    info_section = ft.Container()

    def refresh_info():
        info_section.content = info_container(
            ia_activated['state'],
            recording_activated['state'],
            today_alerts,
            storage,
            change_route,
            change_ia_state,
            change_recording_state
        )
    
    def change_route(route):
        asyncio.create_task(
            page.push_route(route)
        ),
    
    def change_ia_state(e):
        ia_activated['state'] = not ia_activated['state']
        refresh_info()
        page.update()

    def change_recording_state(e):
        recording_activated['state'] = not recording_activated['state']
        refresh_info()
        page.update()

    refresh_info()
    
    def home_view(page: ft.Page):
        return ft.View(
            route='/',
            controls=[
                Navbar(page),
                ft.SafeArea(
           content=ft.Row(
               controls=[
                   ft.Column(
               controls=[
                   video_container,
                    ft.Container(
                       content=ft.Row(
                           controls=[
                            info_section,          
                       ])
                    ),
               ]
            ),
            alert_container_widget
               ]
           )
        )
            ]
        )

    def route_change():
        page.views.clear()
        page.views.append(
            home_view(page)
        )
        if page.route == '/photos':
            page.views.append(photos_view(page,change_route))
        page.update()

    async def view_pop(e):
        if e.view is not None:
            page.views.remove(e.view)
            top_view = page.views[-1]
            await page.push_route(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop

    route_change()

    async def video_loop():
        nonlocal video, video_container
        frame = None

        while cap.isOpened():

            if ia_activated['state']:
                video_container.content = video
                frame = detector.findFaces(cap=cap)
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
          
    page.run_task(video_loop)
                

ft.run(main)