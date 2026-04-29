import cv2
import time
import base64
import threading
import flet as ft
from components.handleCSV import *
from components.widgets import *
#from FaceRecognition import FaceRecognition

cap = cv2.VideoCapture(0)

def main(page: ft.Page):
    page.title = 'SecureCar IA'
    page.theme_mode = ft.ThemeMode.SYSTEM
    page.window_maximized = True
    page.window_full_screen = True
    page.window_resizable = True
    page.padding = 20

    is_cam_activated = True
    ia_activated = False
    ia_is_loading = False
    alerts = read_csv()
    alerts_list = []
    live = ft.Image(src='')
    #live = ft.Image(src='images/test.jpg',fit=ft.ImageFit.CONTAIN,border_radius=20)
    live_container = ft.Container(content=live,alignment=ft.alignment.topCenter,width=800)

    def toggle(value):
        nonlocal ia_activated
        if value == None:
            return
        if value == 'ia_deteccion':
            ia_activated = not ia_activated
            if ia_activated:
                ia_text_ref.current.value = 'Activa'
                ia_text_ref.current.color = ft.Colors.GREEN
            else:
                ia_text_ref.current.value = 'Desactivada'
                ia_text_ref.current.color = ft.Colors.RED
            page.update()
        if value == 'recording':
            return

    def container(top_text,bottom_text,value=None,ref=None,top_color=ft.Colors.BLACK,bottom_color=ft.Colors.BLACK):
            return ft.Container(
                content=ft.Column(
                    controls=[
                        ft.Text(value=top_text,color=top_color,weight=ft.FontWeight.BOLD),
                        ft.Text(ref=ref,value=bottom_text,color=bottom_color,weight=ft.FontWeight.BOLD)
                    ]
                ),
                on_click= lambda x: toggle(value),
                bgcolor=ft.Colors.GREY_200,
                margin=5,
                padding=10,
                border_radius=10,
                width=150,
                height=80,
            )

    ia_text_ref = ft.Ref[ft.Text]()
    ia_deteccion = container('Detección IA','Desactivada',ref=ia_text_ref,bottom_color=ft.Colors.RED,value='ia_deteccion')
    recording = container('Grabación','Activa',bottom_color=ft.Colors.GREEN,value='recording')
    today_alerts = container('Alertas hoy','4')
    storage = container('Almacenamiento','73% usado')

    if alerts:
        for alert in alerts:
            print(alert)
            alerts_list.append(alert_container(alert['title'],alert['text'],alert['time']))
    else:
        alerts_list.append(alert_container('No hay','No existe',''))
    
    page.add(
        ft.Column([
            ft.Container(
                content=ft.Row(
                    alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                    controls=[
                    ft.Row(
                        [
                        ft.Image(src='images/icon.svg',width=50,height=50),
                        ft.Text('SecureCar IA',size=28,weight=ft.FontWeight.BOLD,)
                        ]),
                    ft.Row(
                        [
                        ft.Container(content=ft.Text('Sistema activo',weight=ft.FontWeight.BOLD),bgcolor=ft.Colors.GREY_200,margin=5,padding=10,border_radius=10),
                        ft.IconButton(content=ft.Image(src='images/bell.svg'))
                        ])
                            ]
                
                       )
                         ),

            ft.Container(content=ft.Row(
                controls=[
                    ft.ElevatedButton(content=ft.Text('En vivo')),
                    ft.ElevatedButton(content=ft.Text('Grabaciones'))
                        ]
                            )
                    ),
            ft.Row(
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                vertical_alignment=ft.CrossAxisAlignment.START,
                controls=[
                ft.Container(width=800,content=ft.Row(controls=[
                ft.Column(controls=[
                    live_container,
                    ft.Container(padding=10,width=800,content=ft.Column(controls=[ft.Text('Estado',size=18,weight=ft.FontWeight.BOLD,),
                                                             ft.Row(alignment=ft.MainAxisAlignment.CENTER,controls=[ia_deteccion,recording,today_alerts,storage]),
                                                             ]),
                                                             border_radius=10,
                                                             border=ft.border.all(width=2,color=ft.Colors.GREY_200)),
                ]),
            ])),
            ft.Container(padding=10,height=450,content=ft.Column(controls=[ft.Text('Alertas recientes',size=18,weight=ft.FontWeight.BOLD,),
                                                             ft.Column(alignment=ft.MainAxisAlignment.CENTER,controls=alerts_list),
                                                             ]),
                                                             border_radius=10,
                                                             border=ft.border.all(width=2,color=ft.Colors.GREY_200)),
            ])

            
            
                ])
    )

    def video_loop():
        nonlocal ia_is_loading,live_container
        frame = None
        while is_cam_activated:
            if ia_activated:
                live_container.content = live
                #frame = detector.findObjets()
            else:
                ret,frame = cap.read()
                if not ret:
                    continue
            if frame is not None:
                    _, buffer = cv2.imencode('.jpg', frame)
                    img_base64 = base64.b64encode(buffer).decode()

                    live.src_base64 = img_base64
                    page.update()
            else:
                ia_is_loading = True
                live_container.content = ft.ProgressRing()
                page.update()
            time.sleep(0.03)
    
    threading.Thread(target=video_loop, daemon=True).start()
                

ft.run(main)