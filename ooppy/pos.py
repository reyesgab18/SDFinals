import flet as ft
from db_utils import *
from colors import *

item = ft.Column(
    height = 700,
    scroll = 'hidden',
    on_scroll_interval=0,
    alignment = 'center',
    controls = [
        ft.Row([ft.Text('sample'), ft.Text('sample')]
        )
    ]
)

query = "SELECT * FROM items"
cursor.execute(query,)
result = cursor.fetchall()

for row in result:
    item.controls.append(
        ft.Card(
            elevation = 20,
            content=ft.Container(
                content=ft.Column(
                    [
                        ft.Row([
                            ft.Image(src = "/images/bibingka.jpg", height = 75),
                            ft.Column([
                                ft.Text(row[1]),
                                ft.Text(f"Php {row[2]}"),
                                ft.Row([ft.IconButton(ft.icons.REMOVE), 
                                        ft.IconButton(ft.icons.ADD),
                                        ft.TextButton("Add")],
                                    alignment = ft.MainAxisAlignment.END)
                            ], spacing = 2, expand = True)
                        ])
                    ]
                ),
                width = 400,
                padding = 5
            )
        ),
    )
    
