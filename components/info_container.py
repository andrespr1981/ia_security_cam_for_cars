import flet as ft
   
def bolean_info_con(title,state):
    return ft.Container(
        content=ft.Column(
              controls=[
                ft.Text(value=title,),
                ft.Text(value='Activada' if state else 'Desactivada',color=ft.Colors.GREEN if state else ft.Colors.RED)
              ]
        ),
        bgcolor=ft.Colors.GREY_300,
        padding=10,
        border_radius=10,
        width=200,
        height=70
    )

def mini_info_con(title,value):
    return ft.Container(
        content=ft.Column(
              controls=[
                ft.Text(value=title),
                ft.Text(value=value)
              ]
        ),
        bgcolor=ft.Colors.GREY_300,
        padding=10,
        border_radius=10,
        width=200,
        height=70
    )

def clickeable_info_con(icon,title):
    def on_click(e):
        pass

    return ft.Container(
         content=ft.Row(
              controls=[
                   ft.Icon(icon=icon,color=ft.Colors.WHITE),
                   ft.Text(value=title,color=ft.Colors.WHITE )

              ],
         ),
        bgcolor=ft.Colors.BLACK,
        padding=10,
        border_radius=10,
        width=200,
        on_click=on_click,
        height=70
    )

def info_container(ia_activated,recording_activated,today_alerts,storage):
        return ft.Container(
            content=ft.Column(
                controls=[
                   ft.Text('Estado del Sistema'),
                   ft.Container(content=ft.Column(controls=[
                        ft.Row(controls=[
                        bolean_info_con('Deteccion IA',ia_activated),
                        bolean_info_con('Grabacion',recording_activated),
                        clickeable_info_con(ft.Icons.LIVE_TV,'Vista en Vivo')
                   ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER),
                        ft.Row(controls=[
                            mini_info_con('Alertas hoy',today_alerts),
                            mini_info_con('Fotos guardadas',storage),
                            clickeable_info_con(ft.Icons.CAMERA,'Fotos Tomadas')
                   ],
                    expand=True,
                    alignment=ft.MainAxisAlignment.CENTER)    
                   ]))
                ],
                expand=True,
                horizontal_alignment=ft.MainAxisAlignment.CENTER
            ),
            border=ft.Border.all(0.1),
            margin=5,
            padding=10,
            border_radius=10,
            width=800,
            height=200,
        )


