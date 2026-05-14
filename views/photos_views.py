import os
import flet as ft
from components.navbar import Navbar
from components.info_container import clickeable_info_con

def photos_view(page: ft.Page,change_route):
    dir = 'faces/unknown'
    photos = []
    for photo in os.listdir(dir):
        photos.append(ft.Image(src=f'{dir}/{photo}',
                               height=250,
                               width=250))
    return ft.View(
        route='/photos',
        controls=[
            Navbar(page),
            clickeable_info_con(ft.Icons.LIVE_TV,'Vista en Vivo',change_route,'/',True),
            ft.Container(
                content=ft.Row(controls=photos,
                   wrap=True),
                border=ft.Border.all(0.1),
                margin=5,
                padding=10,
                border_radius=10,
            )
        ]
    )

