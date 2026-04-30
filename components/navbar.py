import flet as ft

def Navbar(page: ft.Page):
        return ft.Container(
                alignment=ft.Alignment.TOP_CENTER,
                content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                        ft.Row(controls=[
                                ft.Image(src='images/icon.svg'),
                                ft.Column(controls=[
                                    ft.Text('DriverGuard',size=20,font_family=ft.FontWeight.BOLD),
                                    ft.Text('Sistema de reconocimiento',size=15,font_family=ft.FontWeight.BOLD)
                        ]),
                        ]),
                        ft.Row(controls=[
                                ft.Container(content=ft.Text('Sistema activo')),
                                ft.Image(src='images/bell.svg')
                        ])
                ])
        )
