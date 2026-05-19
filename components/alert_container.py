import flet as ft
from utils.csv_handler import delete_row

def mini_alert_container(alert_id,title,text,time,level,refresh):

    def delete():
        delete_row(alert_id)
        refresh()

    color = ft.Colors.BLUE
    if level == '1':
        color = ft.Colors.YELLOW
    if level == '2':
        color = ft.Colors.RED
    return ft.Row(
        controls=[
            ft.Container(
        content=ft.Row(
            controls=[
                ft.Column(
                controls=[
                ft.Row(
                    controls=[
                    ft.Container(
                        width=10,
                        height=10,
                        border_radius=50,
                        bgcolor=color),
                    ft.Text(value=title)
                ]),
                ft.Text(
    value=text,
    width=500,              # ancho máximo
    selectable=True,        # permite copiar
    overflow="visible",     # o "clip", "ellipsis"
    max_lines=None,         # sin límite de líneas
),

                ft.Text(value=time)
                ],
            ),
            ]
        ),
        bgcolor=ft.Colors.with_opacity(0.2, color),
        margin=5,
        padding=10,
        border_radius=10,
        width=500
    ),
    ft.IconButton(icon=ft.Icons.DELETE,on_click=delete)
        ]
    )

def alert_container(data,refresh):
    alerts = []
    for alert in data:
        alerts.append(mini_alert_container(alert['id'],alert['title'],alert['text'],alert['time'],alert['level'],refresh))
    return ft.Container(
        content=ft.Column(
            controls=alerts if alerts else [ft.Text(value='No hay alertas')],
            expand=True,
            scroll='always'
        ),
        border=ft.Border.all(0.1),
        padding=10,
        border_radius=10,
        width=600,
        height=600
    )


