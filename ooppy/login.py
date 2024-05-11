import flet as ft
from db_utils import *
from colors import *

username = ft.TextField(
    label = "Username",
    content_padding = ft.padding.all(10),
    border_color = background,
    border_radius = 50,
    width = 300,
    color = background,
    cursor_color = background,
    text_align = 'left',
    cursor_radius = 10,
    label_style = ft.TextStyle(
        color = background,
        weight = ft.FontWeight.BOLD
    )
)

from main import go_login

loginpage = ft.Column(
    alignment = 'center',
    controls = [
        ft.Row([username], alignment = 'center'),
        ft.Row([ft.TextButton("Log in", on_click = lambda e: go_login(e))], alignment = 'center')
    ]
)