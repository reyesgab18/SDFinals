import flet as ft
from db_utils import *
from colors import *

def main(page: ft.Page):
    items = ft.Column(
        height = 700,
        scroll = 'hidden',
        alignment = 'center'
    )
    
    def add_order(id, name, price):
        print(name)
    
    cursor.execute("SELECT itemID, itemName, itemPrice FROM items")
    result = cursor.fetchall()
    cursor.close()
    db.close()
    
    for row in result:
        id, name, price = row
        
        items.controls.append(
            ft.Container(
                padding = 10,
                bgcolor = background,
                width = 300,
                border_radius = 10,
                content = ft.Column([ft.Text(name, color = ft.colors.BLACK, weight = ft.FontWeight.BOLD), ft.Text(price, color = ft.colors.BLACK)]),
                on_click = lambda id = id, name = name, price = price: add_order(id, name, price)
            )
        )   
        
            
    def route_change(route):
        if page.route == "/":
            page.views.append(
                ft.View("/", [
                    
                    
                    items
                    
                    
                ], vertical_alignment = ft.MainAxisAlignment.CENTER)            
            )
            page.update()
            
    page.on_route_change = route_change
    page.go(page.route)

if __name__ == "__main__":
    ft.app(target = main, assets_dir = "assets") 