import flet as ft

def on_hover(e):
    if e.data == True:
        e.control.scale = 1.5
    else:
        e.control.scale = 1
    
    e.control.update()

def Navbar(page: ft.Page):
        return ft.Container(
                padding=10,
                border=ft.Border(bottom=ft.BorderSide(1,ft.Colors.BLACK)),
                alignment=ft.Alignment.TOP_CENTER,
                content=ft.Row(
                        alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
                        controls=[
                        ft.Row(controls=[
                                ft.Image(src='images/icon.svg',height=50),
                                ft.Column(
                                        controls=[
                                        ft.Text('DriverGuard',size=20,weight=ft.FontWeight.BOLD),
                                        ft.Text('Sistema de reconocimiento facial',size=15,weight=ft.FontWeight.BOLD)
                        ]),
                        ]),
                        ft.Row(
                                alignment=ft.MainAxisAlignment.SPACE_EVENLY,
                                controls=[
                                ft.Container(
                                     bgcolor=ft.Colors.GREY_300,
                                     padding=10,
                                     border_radius=ft.BorderRadius.all(10),
                                     content=ft.Row(
                                          controls=[
                                               ft.Container(
                                                    width=10,
                                                    height=10,
                                                    border_radius=50,
                                                    bgcolor=ft.Colors.GREEN),
                                               ft.Text('Sistema activo')])),
                                ft.Container(
                                        padding=10,
                                        on_hover=on_hover,
                                        animate_scale=ft.Animation(200, "ease"),
                                        content=ft.Image(src='images/bell.svg',))
                        ]),
                ]),
        )