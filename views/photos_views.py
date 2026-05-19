import os
import flet as ft
from components.navbar import Navbar
from components.info_container import clickeable_info_con

def photos_view(page: ft.Page, change_route):
    dir = "faces/unknown"
    photos_column = ft.Row(wrap=True)

    def refresh_photos():
        photos_column.controls.clear()
        for photo in os.listdir(dir):
            photos_column.controls.append(
                ft.Container(content=ft.Column(
                    alignment=ft.MainAxisAlignment.CENTER,
                    horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                    controls=[
                        ft.Image(
                            src=f"{dir}/{photo}",
                            height=250,
                            width=250
                        ),
                        ft.IconButton(
                            icon=ft.Icons.DELETE,
                            icon_color=ft.Colors.RED,
                            on_click=lambda e, p=photo: (
                                os.remove(f"{dir}/{p}"),
                                refresh_photos()
                            )
                        )
                    ]
                ),
                border=ft.Border.all(0.1),
                margin=5,
                padding=10,
                border_radius=10,)
            )
        page.update()

    refresh_photos()

    return ft.View(
        route="/photos",
        controls=[
            Navbar(page),
            clickeable_info_con(
                ft.Icons.LIVE_TV,
                "Vista en Vivo",
                change_route,
                "/",
                True
            ),
            ft.Container(
                content=photos_column,
                border=ft.Border.all(0.1),
                height=600,
                width=1500,
                margin=5,
                padding=10,
                border_radius=10,
            )
        ]
    )
