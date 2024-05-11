import flet as ft
import numpy as np
from db_utils import *
from colors import *

def main(page: ft.Page):
    
    divider = ft.Divider(height = 10, color = 'transparent')
    mode = ft.IconButton(
        scale = 0.85, icon = ft.icons.DARK_MODE_ROUNDED, icon_color = background, on_click = lambda e: toggle_theme(e)
    )
    logo = ft.Image(src = "/images/logo.png", height = 300, width = 300)
    top_logo = ft.Image(
        src = "/images/logo.png", height = 50, width = 50
    )

    def route_change(route):
        print(f"Current Page: {page.route}")
        page.views.clear()
        
        if page.route == "/":
            loginpage()
        if page.route == "/signup":
            signuppage()
        if page.route == "/dashboard":
            dashboard()
        if page.route == "/pos":
            pos()
        if page.route == "/inventory":
            inventory()
        if page.route == "/about":
            about()
        
    def loginpage():
        print("login")
        
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
                #weight = ft.FontWeight.BOLD
            ),
        )
        
        password = ft.TextField(
            label = "Password",
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
                #weight = ft.FontWeight.BOLD
            ),
            password = True,
            can_reveal_password = True
        )
        
        loginpage = ft.Column(
            alignment = 'center',
            controls = [
                ft.Row([logo], alignment = 'center'),
                ft.Row([username], alignment = 'center'),
                ft.Row([password], alignment = 'center'),
                ft.Row([ft.TextButton("Log in", on_click = lambda e: go_login(e), width = 300, height = 50, style = ft.ButtonStyle(color = ft.colors.BLACK, bgcolor = background))], alignment = 'center'),
                ft.Row([ft.Text(spans = [
                    ft.TextSpan("No account yet? Sign up"), ft.TextSpan(" "),
                    ft.TextSpan("here", ft.TextStyle(decoration = ft.TextDecoration.UNDERLINE),
                        on_click = lambda e: go_signup(e)        
                        )], color = background)],
                    alignment = 'center'),
                ft.Divider(height = 200, color = 'transparent'),
                ft.Row([ft.Text("2024 © SDSystems Inc. All Rights Reserved.", color = background, size = 10)], alignment = 'center'),
                divider, divider
            ]
        )
        
        page.views.append(
            ft.View("/", [
                ft.SafeArea(content = ft.Column([
                    ft.Row([mode], alignment = ft.MainAxisAlignment.END),
                    loginpage
                ]))
            ], vertical_alignment = ft.MainAxisAlignment.CENTER)
        )
        page.update()
        
        def go_login(e):
            query = "SELECT * FROM credentials WHERE username = %s AND password = %s"
            data = (username.value, password.value)
            cursor.execute(query, data)
            result = cursor.fetchall()
            if (result):
                query = "SELECT role FROM credentials WHERE username = %s"
                data = (username.value,)
                cursor.execute(query, data)
                result = cursor.fetchone()
                if result[0] == 'user':
                    page.route = "/dashboard"
                    route_change(page.route)
                else:
                    page.route = "/admindash"
                    route_change(page.route)
            else:
                failed_popup = ft.AlertDialog(
                    modal = True,
                    content = ft.Text(
                        "Wrong username and/or password.",
                        color = background
                    ),
                    actions = [
                        ft.TextButton(
                            "Ok",
                            on_click = lambda e: close_dlg(e),
                            style = ft.ButtonStyle(
                                bgcolor = background,
                                color = foreground
                            )
                        )
                    ],
                    actions_alignment = ft.MainAxisAlignment.END
                )
                dialog = failed_popup
                open_dialog(dialog)
                
            def close_dlg(e):
                close_dialog(dialog)
        
        def go_signup(e):
            page.route = "/signup"
            route_change(page.route)

    def signuppage():
        print("signup")
        
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
                #weight = ft.FontWeight.BOLD
            ),
        )
        
        password = ft.TextField(
            label = "Password",
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
                #weight = ft.FontWeight.BOLD
            ),
            password = True,
            can_reveal_password = True
        )
        
        retype_password = ft.TextField(
            label = "Re-type Password",
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
                #weight = ft.FontWeight.BOLD
            ),
            password = True,
            can_reveal_password = True
        )
        
        signuppage = ft.Column(
            spacing = 0,
            alignment = 'center',
            controls = [
                ft.Row([
                    ft.Text("Create an Account", color = background, size = 30, weight = ft.FontWeight.BOLD)
                ], alignment = 'center'),
                ft.Row([
                    ft.Text(" You will use this to log in later.", color = background, size = 15)
                ], alignment = 'center'), divider, divider, divider,
                ft.Row([username], alignment = 'center'), divider,
                ft.Row([password], alignment = 'center'), divider,
                ft.Row([retype_password], alignment = 'center'), divider,
                ft.Row([ft.FilledButton("Sign up", on_click = lambda e: create_account(e), width = 300, height = 50, style = ft.ButtonStyle(color = ft.colors.BLACK, bgcolor = background))], alignment = 'center'),
                ft.Divider(height = 300, color = 'transparent')
            ]
        )
        
        page.views.append(
            ft.View("/signup", [
                ft.AppBar(
                    leading = ft.Row([ft.FilledButton("Log in", style = ft.ButtonStyle(color = background, bgcolor = 'transparent'), icon = ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,  on_click = lambda e: go_main(e))], alignment = 'left'),
                    leading_width = 150,
                    actions = [ft.Row([mode], alignment = ft.MainAxisAlignment.END)]),
                ft.SafeArea(content = ft.Column([
                    signuppage
                ]), bottom = True)
            ], vertical_alignment = ft.MainAxisAlignment.CENTER)
        )
        page.update()
        
        def create_account(e):
            special_symbols = ['_', '-', '+', '=', '!', '@', '%', '*', '&']        
            if not ((username.value == "") or (password.value == "") or (retype_password.value == "")):
                if ((password.value == retype_password.value) & (len(password.value) > 8) & (any(char.isdigit() for char in password.value)) & (any(char.isupper() for char in password.value)) & (any(char.islower() for char in password.value)) & (any(char in special_symbols for char in password.value))):
                    query = "SELECT * FROM credentials WHERE username = %s"
                    data = (username.value,)
                    cursor.execute(query, data)
                    result = cursor.fetchall()
                    
                    if result:
                        exist_popup = ft.AlertDialog(
                            modal = True, content = ft.Column([
                                ft.Text("Existing username found", size = 15, color = background, weight = ft.FontWeight.BOLD),
                                ft.Text("Username exists. Please choose another.", size = 10),
                            ], height = 50),
                            actions = [
                                ft.TextButton(
                                    "Ok",
                                    on_click = lambda e: close_dlg(e),
                                    style = ft.ButtonStyle(
                                        bgcolor = background, color = foreground
                                    )
                                )
                            ]
                        )
                        dialog = exist_popup
                        open_dialog(dialog)
                    else:
                        query = "INSERT INTO credentials (username, password, role) VALUES (%s, %s, 'user')"
                        data = (username.value, password.value)
                        cursor.execute(query, data)
                        db.commit()

                        success_popup = ft.AlertDialog(
                            modal = True, content = ft.Column([
                                ft.Text("Success", size = 15, color = background, weight = ft.FontWeight.BOLD),
                                ft.Text("Account created successfully.", size = 10),
                            ], height = 50),
                            actions = [
                                ft.TextButton(
                                    "Ok", on_click = lambda e: go_main(e),
                                    style = ft.ButtonStyle(
                                        bgcolor = background, color = foreground
                                    )
                                )
                            ]
                        )
                        
                        dialog = success_popup
                        open_dialog(dialog)
                else:
                    criteria_popup = ft.AlertDialog(
                        modal = True,
                        content = ft.Column([
                                ft.Text("Passwords don't match or password criteria not met.", size = 15, color = background, weight = ft.FontWeight.BOLD),
                                ft.Text("Password criteria:", size = 10),
                                ft.Text("- At least eight (8) characters", size = 10),
                                ft.Text("- At least one (1) uppercase letter (A - Z)", size = 10),
                                ft.Text("- At least one (1) lowercase letter (a - z)", size = 10),
                                ft.Text("- At least one (1) number (0 - 9)", size = 10),
                                ft.Text("- At least one (1) special character ('_', '-', '+', '=', '!', '@', '%', '*', '&')", size = 10),
                            ], height = 300),
                        actions = [
                            ft.TextButton(
                                "Ok",
                                on_click = lambda e: close_dlg(e),
                                style = ft.ButtonStyle(
                                    bgcolor = background,
                                    color = foreground
                                )
                            )
                        ],
                        actions_alignment = ft.MainAxisAlignment.END
                    )
                    dialog = criteria_popup
                    open_dialog(dialog)
            else:
                input_popup = ft.AlertDialog(
                    modal = True,
                    content = ft.Text(
                        "Please input all fields.",
                        color = background
                    ),
                    actions = [
                        ft.TextButton(
                            "Ok",
                            on_click = lambda e: close_dlg(e),
                            style = ft.ButtonStyle(
                                bgcolor = background,
                                color = foreground
                            )
                        )
                    ],
                    actions_alignment = ft.MainAxisAlignment.END
                )
                dialog = input_popup
                open_dialog(dialog)
            
            def close_dlg(e):
                close_dialog(dialog)
                
        def go_main(e):
            page.route = "/"
            route_change(page.route)
                            
    def admindash():
        ...
    def dashboard():
        mode = ft.IconButton(
            scale = 0.85, icon = ft.icons.DARK_MODE_ROUNDED, icon_color = background, on_click = lambda e: toggle_theme(e)
        )
        username_placeholder = ft.Row([
            ft.Text("Role:")
        ], alignment = ft.MainAxisAlignment.END)
        drawer = ft.NavigationDrawer(
            controls = [
                ft.Container(height = 12),
                ft.Row([mode], alignment = ft.MainAxisAlignment.END),
                ft.Row([
                    username_placeholder,
                    ft.OutlinedButton(
                        content = ft.Text("USER", weight = ft.FontWeight.BOLD, color = background)
                    )
                ], alignment = 'center'),
                divider, divider, divider,
                ft.Column(
                    controls = [
                        ft.FilledButton(
                            width = 200,
                            style = ft.ButtonStyle(
                                bgcolor = background
                            ),
                            content = ft.Text("Dashboard", weight = ft.FontWeight.BOLD),
                            on_click = lambda e: go_dashboard(e)
                        ),
                        ft.FilledButton(
                            width = 200,
                            style = ft.ButtonStyle(
                                bgcolor = background
                            ),
                            content = ft.Text("POS", weight = ft.FontWeight.BOLD),
                            on_click = lambda e: go_pos(e)
                        ),
                        ft.FilledButton(
                            width = 200,
                            style = ft.ButtonStyle(
                                bgcolor = background
                            ),
                            content = ft.Text("About Us", weight = ft.FontWeight.BOLD),
                            on_click = lambda e: go_about(e)
                        ),
                        ft.Divider(height = 20),
                        ft.FilledButton(
                            width = 200,
                            style = ft.ButtonStyle(
                                bgcolor = background
                            ),
                            content = ft.Text("Logout", weight = ft.FontWeight.BOLD),
                            on_click = lambda e: go_logout(e)
                        )
                    ], horizontal_alignment = ft.CrossAxisAlignment.CENTER
                )
            ]
        )
        dashboardpage = ft.Column(
            controls = [
                ft.Row([ft.Text("DASHBOARD", size = 20, weight = ft.FontWeight.BOLD, color = background)], alignment = 'center')
            ]
        )
        page.views.append(
            ft.View("/dashboard", [
                ft.AppBar(
                    leading = ft.IconButton(
                        icon = ft.icons.MENU_ROUNDED,
                        style = ft.ButtonStyle(
                            color = background
                        ),
                        on_click = lambda e: user_drawer(e)
                    ),
                    leading_width = 50,
                    title = top_logo,
                    center_title = True
                ),
                ft.SafeArea(content = ft.Column([
                    dashboardpage
                ]))
            ], drawer = drawer)
        )
        page.update()
        
        def user_drawer(e):
            drawer.open = True
            page.update()
            
        def toggle_theme(e):
            drawer.open = False
            if e.control.icon == ft.icons.LIGHT_MODE_ROUNDED:
                page.theme_mode = ft.ThemeMode.DARK
                e.control.icon = ft.icons.DARK_MODE_ROUNDED
            
            else:
                page.theme_mode = ft.ThemeMode.LIGHT
                e.control.icon = ft.icons.LIGHT_MODE_ROUNDED
                
            page.update()
            
        def go_dashboard(e):
            page.route = "/dashboard"
            route_change(page.route)
        
        def go_pos(e):
            page.route = "/pos"
            route_change(page.route)
            page.views.clear()
            
        def go_about(e):
            page.route = "/about"
            route_change(page.route)
            
        def go_logout(e):
            logout_popup = ft.AlertDialog(
                modal = True,
                content = ft.Text(
                    "Are you sure you want to logout?",
                    color = background
                ),
                actions = [
                    ft.TextButton(
                        "Yes",
                        on_click = lambda e: go_main(e),
                        style = ft.ButtonStyle(
                            bgcolor = background,
                            color = foreground
                        )
                    ),
                    ft.TextButton(
                        "No",
                        on_click = lambda e: close_dlg(e),
                        style = ft.ButtonStyle(
                            bgcolor = background,
                            color = foreground
                        )
                        
                    )
                ],
                actions_alignment = ft.MainAxisAlignment.END
            )
            dialog = logout_popup
            open_dialog(dialog)
            
            def go_main(e):
                page.route = "/"
                route_change(page.route)
                
            def close_dlg(e):
                drawer.open = False
                close_dialog(dialog)
            
    def inventory():
        ...
    def pos():
        page.views.clear()
        page.views.append(
            ft.View("/", [
                ft.SafeArea(content = ft.Column([
                    ft.Row([mode], alignment = ft.MainAxisAlignment.END),
                    loginpage
                ]))
            ], vertical_alignment = ft.MainAxisAlignment.CENTER)
        )
        page.update()
    def about():
        ...
    def toggle_theme(e):
        if e.control.icon == ft.icons.LIGHT_MODE_ROUNDED:
            page.theme_mode = ft.ThemeMode.DARK
            e.control.icon = ft.icons.DARK_MODE_ROUNDED
        
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            e.control.icon = ft.icons.LIGHT_MODE_ROUNDED
            
        page.update()
            
    def admin_drawer():
        ...
        
    def open_dialog(dialog):
        page.dialog = dialog
        dialog.open = True
        page.update()
        
    def close_dialog(dialog):
        dialog.open = False
        print(dialog)
        page.update()
        
        
    page.on_route_change = route_change
    page.go(page.route)
    
if __name__ == "__main__":
    ft.app(target = main, assets_dir = "assets")