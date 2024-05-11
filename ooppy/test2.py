import flet as ft
from db_utils import *
from colors import *

def main(page: ft.Page):
    def fetch_data():
        cursor.execute("SELECT itemName, itemPrice FROM items")
        
        rows = cursor.fetchall()
        
        cursor.close()
        db.close()
        
        return rows
    
    def index():
        data = fetch_data()
        buttons = []
        
        for row in data:
            name, price = row
            buttons.append(ft.Button(text = price))
            
        return ft.Divider(*buttons)

if __name__ == "__main__":
    ft.app(target = main, assets_dir = "assets")