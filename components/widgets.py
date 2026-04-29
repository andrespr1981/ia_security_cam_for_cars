import flet as ft
   
def alert_container(title,text,time,bg=ft.Colors.RED_100):
        return ft.Container(
            content=ft.Column(
                controls=[
                    ft.Text(value=title,weight=ft.FontWeight.BOLD),
                    ft.Text(value=text,weight=ft.FontWeight.BOLD),
                    ft.Text(value=time,weight=ft.FontWeight.BOLD)
                ]
            ),
            bgcolor=bg,
            margin=5,
            padding=10,
            border_radius=10,
            width=150,
            height=80,
        )

