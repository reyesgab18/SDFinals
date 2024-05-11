from flet import *

def main(page:Page):
    
    def route_change(route):
        page.views.clear()
        page.views.append(
            View(
                "/login", [
                    Text("TEST LOGIN")
                ]
            )
        )
        page.update()
        
    page.on_route_change = route_change
    page.go(page.route)
        
app(target = main)