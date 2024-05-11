import flet as ft
import numpy as np
from db_utils import *
from colors import *
        
def main(page: ft.Page):
    total = 0
    
    mode = ft.IconButton(
        scale = 0.85, icon = ft.icons.DARK_MODE_ROUNDED, icon_color = background, on_click = lambda e: toggle_theme(e)
    )

    ###LOGIN AND SIGNUP
    divider = ft.Divider(height = 10, color = 'transparent')
    logo = ft.Image(src = "/images/logo.png", height = 300, width = 300)
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
    email = ft.TextField(
        label = "Email",
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
    loginpage = ft.Column(
        alignment = 'center',
        controls = [
            ft.Row([logo], alignment = 'center'),
            ft.Row([username], alignment = 'center'),
            ft.Row([password], alignment = 'center'),
            ft.Row([ft.TextButton("Log in", on_click = lambda e: go_login(e), width = 300, height = 50, style = ft.ButtonStyle(color = ft.colors.BLACK, bgcolor = background))], alignment = 'center'),
            divider,
            ft.Row([ft.Text(spans = [
                ft.TextSpan("No account yet? Sign up"), ft.TextSpan(" "),
                ft.TextSpan("here", ft.TextStyle(decoration = ft.TextDecoration.UNDERLINE),
                    on_click = lambda e: go_signup(e)        
                    )], color = background)],
                alignment = 'center'),
            ft.Row([ft.Text(size = 10, spans = [
                ft.TextSpan("Reset password", ft.TextStyle(decoration = ft.TextDecoration.UNDERLINE),
                    on_click = lambda e: resetpage(e)        
                    )], color = background)],
                alignment = 'center'),
            ft.Divider(height = 100, color = 'transparent'),
            ft.Row([ft.Text("2024 © SDSystems Inc. All Rights Reserved.", color = background, size = 10)], alignment = 'center'),
            divider, divider
        ]
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
            ft.Row([email], alignment = 'center'), divider,
            ft.Row([password], alignment = 'center'), divider,
            ft.Row([retype_password], alignment = 'center'), divider,
            ft.Row([ft.FilledButton("Sign up", on_click = lambda e: create_account(e), width = 300, height = 50, style = ft.ButtonStyle(color = ft.colors.BLACK, bgcolor = background))], alignment = 'center'),
            ft.Divider(height = 300, color = 'transparent')
        ]
    )
    forgotpage = ft.Column(
        spacing = 0,
        alignment = 'center',
        controls = [
            ft.Row([ft.Text("Reset Password", color = background, size = 30, weight = ft.FontWeight.BOLD)], alignment = 'center'),
            ft.Row([ft.Text(" Input your username and associated e-mail address.", color = background, size = 15)], alignment = 'center'), divider, divider, divider,
            ft.Row([username], alignment = 'center'), divider,
            ft.Row([email], alignment = 'center'), divider,
            ft.Row([
                ft.FilledButton("Reset Password", on_click = lambda e: reset(e), width = 300, height = 50,
                    style = ft.ButtonStyle(
                        color = ft.colors.BLACK, bgcolor = background
                    )
                )
            ], alignment = 'center')
        ]
    )
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
    success_popup = ft.AlertDialog(
        modal = True, content = ft.Column([
            ft.Text("Success", size = 15, color = background, weight = ft.FontWeight.BOLD),
            ft.Text("Account created successfully.", size = 10),
        ], height = 50),
        actions = [
            ft.TextButton(
                "Ok", on_click = lambda e: close_dlg(e),
                style = ft.ButtonStyle(
                    bgcolor = background, color = foreground
                )
            )
        ]
    )
    ###ADMINDASH
    admindash = ft.Column(                  
        controls = [
            ft.Row([ft.Text("ADMIN DASHBOARD", size = 20, weight = ft.FontWeight.BOLD, color = background)], alignment = 'center')
        ]
    )
    
    ###DASHBOARD
    top_logo = ft.Image(
        src = "/images/logo.png", height = 50, width = 50
    )
    dashboard = ft.Column(
        controls = [
            ft.Row([ft.Text("DASHBOARD", size = 20, weight = ft.FontWeight.BOLD, color = background)], alignment = 'center')
        ]
    )
    pos = ft.Column(
        controls = [
            ft.Row([ft.Text("POS", size = 20, weight = ft.FontWeight.BOLD, color = background)], alignment = 'flet center')
        ]
    )
    
    ###POS
    item = ft.Column(
        height = 700,
        scroll = 'hidden',
        on_scroll_interval=0,
        alignment = 'center'
    )
    cursor.execute("SELECT SQL_NO_CACHE itemID, itemName, itemPrice FROM items")
    result = cursor.fetchall()
    
    for row in result:
        e, name, price = row
        
        item.controls.append(
            ft.Container(
                padding = 10,
                bgcolor = background,
                width = 300,
                border_radius = 10,
                content = ft.Row([ft.Text(name, color = ft.colors.BLACK, weight = ft.FontWeight.BOLD), ft.Column(expand = True), ft.Row([ft.Text(f"Php {price}", color = ft.colors.BLACK)], alignment = 'left', width = 50)]),
                on_click = lambda e = e, name = name, price = price: add_order(id, name, price)
            )
        )

    del result

    ##DRAWERS
    username_placeholder = ft.Row([
        ft.Text("Role:")
    ], alignment = ft.MainAxisAlignment.END)
    admin_drawer = ft.NavigationDrawer(
        controls = [
            ft.Container(height = 12),
            ft.Row([mode], alignment = ft.MainAxisAlignment.END),
            ft.Row([
                username_placeholder,
                ft.OutlinedButton(
                    content = ft.Text("ADMIN", weight = ft.FontWeight.BOLD, color = background)
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
                        content = ft.Text("Admin Dashboard", weight = ft.FontWeight.BOLD),
                        on_click = lambda e: go_admindash(e)
                    ),
                    ft.FilledButton(
                        width = 200,
                        style = ft.ButtonStyle(
                            bgcolor = background
                        ),
                        content = ft.Text("Inventory", weight = ft.FontWeight.BOLD),
                        on_click = lambda e: go_inventory(e)
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
                        on_click = lambda e: show_logout_popup(e)
                    )
                ], horizontal_alignment = ft.CrossAxisAlignment.CENTER
            )
        ]
    )
    user_drawer = ft.NavigationDrawer(
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
                        on_click = lambda e: go_user_about(e)
                    ),
                    ft.Divider(height = 20),
                    ft.FilledButton(
                        width = 200,
                        style = ft.ButtonStyle(
                            bgcolor = background
                        ),
                        content = ft.Text("Logout", weight = ft.FontWeight.BOLD),
                        on_click = lambda e: show_logout_popup(e)
                    )
                ], horizontal_alignment = ft.CrossAxisAlignment.CENTER
            )
        ]
    )
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

    def route_change(args):
        print(f"current page: {page.route}")
        page.views.clear()
        page.horizontal_alignment = 'center'
        page.vertical_alignment = 'center'
    
        if page.route == "/":
            page.views.append(
                ft.View("/", [
                    ft.SafeArea(content = ft.Column([
                        ft.Row([mode], alignment = ft.MainAxisAlignment.END),
                        loginpage
                    ]))
                ], vertical_alignment = ft.MainAxisAlignment.CENTER)
            )
            
        if page.route == "/signup":
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
            
        if page.route == "/forgot":
            page.views.append(
                ft.View("/forgot", [
                    ft.AppBar(
                        leading = ft.Row([ft.FilledButton("Log in", style = ft.ButtonStyle(color = background, bgcolor = 'transparent'), icon = ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,  on_click = lambda e: go_main(e))], alignment = 'left'),
                        leading_width = 150,
                        actions = [ft.Row([mode], alignment = ft.MainAxisAlignment.END)]),
                    ft.SafeArea(content = ft.Column([
                        forgotpage
                    ]), bottom = True)
                ], vertical_alignment = ft.MainAxisAlignment.CENTER)
            )
            
        if page.route == "/admindash":
            page.views.append(
                ft.View("/admindash", [
                    ft.AppBar(
                        leading = ft.IconButton(
                            icon = ft.icons.MENU_ROUNDED,
                            style = ft.ButtonStyle(
                                color = background
                            ),
                            on_click = lambda e: show_admin_drawer(e)
                        ),
                        leading_width = 50,
                        title = top_logo,
                        center_title = True
                    ),
                    ft.SafeArea(content = ft.Column([
                        admindash,
                    ]))
                ], drawer = admin_drawer)
            )
            
        if page.route == "/dashboard":
            page.views.append(
                ft.View("/dashboard", [
                    ft.AppBar(
                        leading = ft.IconButton(
                            icon = ft.icons.MENU_ROUNDED,
                            style = ft.ButtonStyle(
                                color = background
                            ),
                            on_click = lambda e: show_user_drawer(e)
                        ),
                        leading_width = 50,
                        title = top_logo,
                        center_title = True
                    ),
                    ft.SafeArea(content = ft.Column([
                        dashboard
                    ]))
                ], drawer = user_drawer)
            )
        if page.route == "/inventory":
            page.views.append(
                ft.View("/inventory", [
                    ft.AppBar(
                        leading = ft.IconButton(
                            icon = ft.icons.MENU_ROUNDED,
                            style = ft.ButtonStyle(
                                color = background
                            ),
                            on_click = lambda e: show_admin_drawer(e)
                        ),
                        leading_width = 50,
                        title = top_logo,
                        center_title = True
                    ),
                    ft.SafeArea(content = ft.Column([
                        ft.Row([ft.Text("INVENTORY", color = background, size = 20, weight = ft.FontWeight.BOLD)], alignment = 'center'),
                    ]))
                ], drawer = admin_drawer)
            )
        if page.route == "/pos":
            if type(args) is int:
                ...
            else:
                total = 0
                cursor.execute("SELECT SQL_NO_CACHE itemPrice, itemQuantity FROM order_temp")
                result1 = cursor.fetchall()
                
                for i in result1:
                    total += int(i[0] * i[1])
                args = total
            
            
            bottomappbar = ft.Column([
                ft.Row([
                    ft.Text("Total Amount: ", color = ft.colors.BLACK, weight = ft.FontWeight.W_800)
                ])
            ], horizontal_alignment = ft.CrossAxisAlignment.CENTER)
            
            page.views.append(ft.View("/pos", [
                ft.AppBar(
                    leading = ft.IconButton(
                        icon = ft.icons.MENU_ROUNDED,
                        style = ft.ButtonStyle(
                            color = background
                        ),
                        on_click = lambda e: show_user_drawer(e)
                    ),
                    leading_width = 50,
                    title = top_logo,
                    center_title = True
                ),
                ft.BottomAppBar(
                    bgcolor = background,
                    content = ft.Column([
                        ft.Row([
                            bottomappbar,
                            ft.Container(expand = True),
                            ft.Card(
                                width = 100,
                                color = foreground,
                                content = ft.Column([
                                    ft.IconButton(
                                        icon = ft.icons.SHOPPING_CART_ROUNDED,
                                        icon_size = 40,
                                        icon_color = background,
                                        on_click = lambda e: order_cart(e)
                                    ),
                                    ft.Text("Order Cart", color = background)
                                ], horizontal_alignment = ft.CrossAxisAlignment.CENTER, spacing = 0)
                            )
                        ], )
                    ])
                ),
                ft.SafeArea(
                    content = ft.Column([
                        ft.Row([pos], alignment = 'center'),
                        item
                    ], horizontal_alignment = 'center')
                )
            ], drawer = user_drawer))
            
            bottomappbar.controls.append(
                ft.Row([
                    ft.Text("Php", size = 15, color = ft.colors.BLACK),
                    ft.Text(args, size = 30, color = ft.colors.BLACK, weight = ft.FontWeight.BOLD)
                ])
            )
            
        if page.route != "/pos":
            print("truncated!")
            cursor.execute("TRUNCATE TABLE order_temp")
            db.commit() 
            
        if page.route == "/about":
            page.views.append(
                ft.View("/about", [
                    ft.AppBar(
                        leading = ft.IconButton(
                            icon = ft.icons.MENU_ROUNDED,
                            style = ft.ButtonStyle(
                                color = background
                            ),
                            on_click = lambda e: show_admin_drawer(e)
                        ),
                        leading_width = 50,
                        title = top_logo,
                        center_title = True
                    ),
                    ft.SafeArea(content = ft.Column([
                        ft.Row([ft.Text("ABOUT US", color = background, size = 20, weight = ft.FontWeight.BOLD)], alignment = 'center'),
                        ft.Text("    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
                    ]))
                ], drawer = admin_drawer)
            )
        if page.route == "/user_about":
            page.views.append(
                ft.View("/user_about", [
                    ft.AppBar(
                        leading = ft.IconButton(
                            icon = ft.icons.MENU_ROUNDED,
                            style = ft.ButtonStyle(
                                color = background
                            ),
                            on_click = lambda e: show_user_drawer(e)
                        ),
                        leading_width = 50,
                        title = top_logo,
                        center_title = True
                    ),
                    ft.SafeArea(content = ft.Column([
                        ft.Row([ft.Text("ABOUT US", color = background, size = 20, weight = ft.FontWeight.BOLD)], alignment = 'center'),
                        ft.Text("    Lorem Ipsum is simply dummy text of the printing and typesetting industry. Lorem Ipsum has been the industry's standard dummy text ever since the 1500s, when an unknown printer took a galley of type and scrambled it to make a type specimen book. It has survived not only five centuries, but also the leap into electronic typesetting, remaining essentially unchanged. It was popularised in the 1960s with the release of Letraset sheets containing Lorem Ipsum passages, and more recently with desktop publishing software like Aldus PageMaker including versions of Lorem Ipsum.")
                    ]))
                ], drawer = user_drawer)
            )
        
        page.update()  
    
    def resetpage(e):
        page.route = "/forgot"
        route_change(page.route)
        
    def reset(e):
        ...  
        
    def show_user_drawer(e):
        user_drawer.open = True
        page.update()
        
    def show_admin_drawer(e):
        admin_drawer.open = True
        page.update()
        
    def toggle_theme(e):
        admin_drawer.open = False
        user_drawer.open = False
        if e.control.icon == ft.icons.LIGHT_MODE_ROUNDED:
            page.theme_mode = ft.ThemeMode.DARK
            e.control.icon = ft.icons.DARK_MODE_ROUNDED
        
        else:
            page.theme_mode = ft.ThemeMode.LIGHT
            e.control.icon = ft.icons.LIGHT_MODE_ROUNDED
            
        page.update()
        
    def order_cart(e):
        orders = ft.Column(
            expand = True,
            scroll = 'hidden',
            alignment = ft.MainAxisAlignment.START,
            spacing = 0,
            height = 500
        )
        cursor.execute("SELECT SQL_NO_CACHE itemName, itemPrice, itemQuantity FROM order_temp")
        result = cursor.fetchall()
        
        for row in result:
            itemName, itemPrice, itemQuantity = row
            orders.controls.append(
                ft.Row([
                    ft.Container(
                        padding = 10,
                        bgcolor = background,
                        expand = True,
                        border_radius = 10,
                        content = ft.Row([
                            ft.Row([ft.Text(row[0], color = ft.colors.BLACK)], width = 70),
                            ft.Row([ft.Text(row[1], color = ft.colors.BLACK)], width = 30),
                            ft.Row([ft.Text(f"x{row[2]}", color = ft.colors.BLACK)], width = 30)    
                        ]),
                    ),
                    ft.IconButton(
                        icon = ft.icons.DELETE_ROUNDED,
                        icon_color = background,
                        icon_size = 15,
                        on_click = lambda e = e, itemName = itemName, itemQuantity = itemQuantity: delete_row(e, itemName, itemQuantity)
                    )
                ], alignment = ft.MainAxisAlignment.CENTER)
            )
        
        del result
        
        total = 0
        cursor.execute("SELECT SQL_NO_CACHE itemPrice, itemQuantity FROM order_temp")
        result = cursor.fetchall()
        
        for i in result:
            total += int(i[0] * i[1])
        
        order_cart_popup = ft.AlertDialog(
            modal = True,
            content = ft.Column([
                ft.Text("Order Summary", size = 20, color = background),
                ft.Divider(height = 20),
                ft.Row([
                    ft.Row([ft.Text("Name", color = background)], width = 60, alignment = ft.MainAxisAlignment.CENTER),
                    ft.Row([ft.Text("Price", color = background)], width = 50, alignment = ft.MainAxisAlignment.CENTER),
                    ft.Row([ft.Text("Qty", color = background)], width = 30, alignment = ft.MainAxisAlignment.CENTER)
                ]), 
                ft.Divider(height = 10, color = 'transparent'),
                orders,
                ft.Divider(height = 20),
                ft.Row([
                    ft.Text("Amount: ", size = 15, color = background), ft.Text(total, size = 25, color = background)
                ])
            ], height = 400, spacing = 0, horizontal_alignment = ft.CrossAxisAlignment.CENTER),
             
            actions = [
                ft.TextButton(
                    "Confirm",
                    on_click = lambda e: confirm_order(e),
                    style = ft.ButtonStyle(
                        bgcolor = background,
                        color = foreground
                    )
                ),
                ft.TextButton(
                    "Cancel",
                    on_click = lambda e: close_order_cart(e),
                    style = ft.ButtonStyle(
                        bgcolor = background,
                        color = foreground
                    )
                ),
                ft.TextButton(
                    "Delete",
                    on_click = lambda e: confirm_delete(e),
                    style = ft.ButtonStyle(
                        bgcolor = ft.colors.RED,
                        color = foreground
                    )
                )
            ],
            actions_alignment = ft.MainAxisAlignment.END
        )
        page.dialog = order_cart_popup
        order_cart_popup.open = True
        del result
        page.update()
        
        def confirm_order(e):
            confirm_popup = ft.AlertDialog(
                modal = True,
                content = ft.Column([
                    ft.Text("Confirm order?", size = 20, color = background, weight = ft.FontWeight.BOLD),
                    ft.Row([ft.Text("This action cannot be undone.", size = 15, color = background)])    
                ], height = 100),
                actions = [
                    ft.TextButton(
                        "Yes",
                        on_click = lambda e: confirm(e),
                        style = ft.ButtonStyle(
                            bgcolor = background,
                            color = foreground
                        )
                    ),
                    ft.TextButton(
                        "No",
                        on_click = lambda e: close_confirm(e),
                        style = ft.ButtonStyle(
                            bgcolor = background,
                            color = foreground
                        )
                    ),
                ]
            )
            page.dialog = confirm_popup
            confirm_popup.open = True
            page.update()
            
            def confirm(e):
                confirm_popup.open = False
                page.update()
                cursor.execute("SELECT SQL_NO_CACHE itemName, itemQuantity FROM order_temp")
                result = cursor.fetchall()

                for i in result:
                    order_name = i[0]
                    order_qty = i[1]
                    
                    cursor.execute("SELECT SQL_NO_CACHE itemName, itemQuantity FROM items WHERE itemName = %s", (order_name,))
                    result = cursor.fetchone()
                    item_name = result[0]
                    item_qty = result[1]
                    
                    updated_qty = item_qty - order_qty
                    
                    cursor.execute("UPDATE items SET itemQuantity = %s WHERE itemName = %s", (updated_qty ,item_name))
                    db.commit()
                
                div = ft.Divider(height = 20, color = 'transparent')
                overlay_sheet = ft.BottomSheet(
                    open = True,
                    on_dismiss = lambda e: close_overlay(e),
                    content = ft.Container(
                        content = ft.Column(
                            [
                                div,
                                ft.Text("Order Confirmed!", size = 20, weight = ft.FontWeight.BOLD, color = background),
                                ft.Row([ft.Text("Total Amount: ", size = 15), ft.Text(f"Php {total}", size = 25)], alignment = ft.MainAxisAlignment.CENTER),
                                div,
                                ft.TextButton(
                                    "Close",
                                    on_click = lambda e: close_overlay(e),
                                    style = ft.ButtonStyle(
                                        bgcolor = background,
                                        color = foreground
                                    )
                                )
                            ],
                            width = 500,
                            height = 200,
                            horizontal_alignment = ft.CrossAxisAlignment.CENTER
                        ),
                        padding = 10,    
                    ),
                )
                
                del result
                page.overlay.append(overlay_sheet)
                page.update()
                
                def close_overlay(e):
                    overlay_sheet.open = False,
                    overlay_sheet.update()
                    cursor.execute("TRUNCATE TABLE order_temp")
                    db.commit()
                    route_change(page.route)
            
            def close_confirm(e):
                confirm_popup.open = False
                page.update()
        
        def delete_row(e, itemName, itemQuantity):
            cursor.execute("DELETE SQL_NO_CACHE FROM order_temp WHERE itemName = %s AND itemQuantity = %s", (itemName, itemQuantity))
            db.commit()
            order_cart_popup.open = False
            page.update()
            route_change(page.route)
            
        def confirm_delete(e):
            confirm_popup = ft.AlertDialog(
                modal = True,
                content = ft.Column([
                    ft.Text("Confirm delete?", size = 20, color = background, weight = ft.FontWeight.BOLD),
                    ft.Row([ft.Text("This action cannot be undone.", size = 15, color = background)])    
                ], height = 100),
                actions = [
                    ft.TextButton(
                        "Yes",
                        on_click = lambda e: delete_cart(e),
                        style = ft.ButtonStyle(
                            bgcolor = background,
                            color = foreground
                        )
                    ),
                    ft.TextButton(
                        "No",
                        on_click = lambda e: close_confirm(e),
                        style = ft.ButtonStyle(
                            bgcolor = background,
                            color = foreground
                        )
                    ),
                ]
            )
            page.dialog = confirm_popup
            confirm_popup.open = True
            page.update()
            
            def delete_cart(e):
                confirm_popup.open = False
                cursor.execute("TRUNCATE TABLE order_temp")
                db.commit()
                route_change(page.route)
            
            def close_confirm(e):
                confirm_popup.open = False
                page.update()
        
        def close_order_cart(e):
            order_cart_popup.open = False
            page.update()

    def add_order(e, name, price):
        
        quantity_field = ft.TextField(
            value = 1,
            width = 50,
            height = 30,
            text_align = ft.TextAlign.CENTER,
            text_vertical_align = -0.5,
            border_color = background
        )
        add_order_popup = ft.AlertDialog(
            modal = True,
            content = ft.Column([
                ft.Text("Add to order?", size = 20, color = background, weight = ft.FontWeight.BOLD),
                ft.Text(name, size = 20),
                ft.Text(f"Php {price}", size = 15),
                ft.Divider(height = 20),
                ft.Row([
                    ft.Text("Amount", size = 15), ft.IconButton(ft.icons.REMOVE, icon_color = background, on_click = lambda e: minus_click(e)), quantity_field, ft.IconButton(ft.icons.ADD, icon_color = background, on_click = lambda e: plus_click(e)),
                ], alignment = ft.MainAxisAlignment.CENTER)
            ], height = 120, spacing = 0, horizontal_alignment = ft.CrossAxisAlignment.CENTER), 
            actions = [
                ft.TextButton(
                    "Yes",
                    on_click = lambda e, name = name, price = price: add_to_total(e, name, price),
                    style = ft.ButtonStyle(
                        bgcolor = background,
                        color = foreground
                    )
                ),
                ft.TextButton(
                    "No",
                    on_click = lambda e: close_add_order(e),
                    style = ft.ButtonStyle(
                        bgcolor = background,
                        color = foreground
                    )
                    
                )
            ],
            actions_alignment = ft.MainAxisAlignment.END
        )
        page.dialog = add_order_popup
        add_order_popup.open = True
        page.update()
        
        def minus_click(e):
            if quantity_field.value > str(1):
                quantity_field.value = str(int(quantity_field.value) - 1)
            else:
                ...
            page.update()
                
        def plus_click(e):
            quantity_field.value = str(int(quantity_field.value) + 1)
            page.update()
        
        def close_add_order(e):
            add_order_popup.open = False
            page.update()
            
        def add_to_total(e, name, price):
            itemName = name
            itemPrice = price
            
            cursor.execute("SELECT SQL_NO_CACHE itemQuantity FROM order_temp WHERE itemName = %s", (itemName,))
            result = cursor.fetchone()
            if (result):
                print("found existing")
                itemQuantity = int(result[0])
            else:
                print("no existing")
                itemQuantity = quantity_field.value
            
            cursor.execute("SELECT SQL_NO_CACHE itemQuantity FROM items WHERE itemName = %s", (itemName,))
            result = cursor.fetchone()
            inventory_qty = result[0]
            
            if (int(itemQuantity) > inventory_qty):
                div = ft.Divider(height = 20, color = 'transparent')
                overlay_sheet = ft.BottomSheet(
                    open = True,
                    content = ft.Container(
                        content = ft.Column(
                            [
                                div,
                                ft.Text("Insufficient Supply", size = 20, weight = ft.FontWeight.BOLD, color = background),
                                ft.Row([ft.Text(f"Remaining supply for {itemName}:", size = 15), ft.Text(inventory_qty, size = 25)], alignment = ft.MainAxisAlignment.CENTER),
                                div,
                                ft.TextButton(
                                    "Close",
                                    on_click = lambda e: close_overlay(e),
                                    style = ft.ButtonStyle(
                                        bgcolor = background,
                                        color = foreground
                                    )
                                )
                            ],
                            width = 500,
                            height = 200,
                            horizontal_alignment = ft.CrossAxisAlignment.CENTER
                        ),
                        padding = 10,    
                    ),
                )
                
                page.overlay.append(overlay_sheet)
                page.update()
            else:
                print("sufficient... continuing...")
                cursor.execute("SELECT SQL_NO_CACHE itemQuantity FROM order_temp WHERE itemName = %s", (itemName,))
                result = cursor.fetchone()
                #if wala pang data
                if not (result):
                    print("no existing, adding order...")
                    cursor.execute("INSERT INTO order_temp (itemName, itemPrice, itemQuantity) VALUES (%s, %s, %s)", (itemName, itemPrice, itemQuantity))
                    db.commit()
                
                #if meron, update column
                else:
                    if(itemQuantity + int(quantity_field.value) > inventory_qty):
                        print("insufficient")
                        div = ft.Divider(height = 20, color = 'transparent')
                        overlay_sheet = ft.BottomSheet(
                            open = True,
                            content = ft.Container(
                                content = ft.Column(
                                    [
                                        div,
                                        ft.Text("Insufficient Supply", size = 20, weight = ft.FontWeight.BOLD, color = background),
                                        ft.Row([ft.Text(f"Remaining supply for {itemName}:", size = 15), ft.Text(inventory_qty, size = 25)], alignment = ft.MainAxisAlignment.CENTER),
                                        div,
                                        ft.TextButton(
                                            "Close",
                                            on_click = lambda e: close_overlay(e),
                                            style = ft.ButtonStyle(
                                                bgcolor = background,
                                                color = foreground
                                            )
                                        )
                                    ],
                                    width = 500,
                                    height = 200,
                                    horizontal_alignment = ft.CrossAxisAlignment.CENTER
                                ),
                                padding = 10,    
                            ),
                        )
                        page.overlay.append(overlay_sheet)
                        
                    else:
                        print(f"existing, adding {quantity_field.value}...")
                        updated = itemQuantity + int(quantity_field.value)
                        print(f"updated: {updated}")
                        cursor.execute("UPDATE order_temp SET itemQuantity = %s WHERE itemName = %s", (updated, itemName))
                        db.commit()
                
                add_order_popup.open = False
                page.update()
                
                total = 0
                cursor.execute("SELECT SQL_NO_CACHE itemPrice, itemQuantity FROM order_temp")
                result = cursor.fetchall()
                
                for i in result:
                    total += int(i[0] * i[1])
                
                route_change(total)
                
            def close_overlay(e):
                overlay_sheet.open = False
                page.update()

    def show_logout_popup(e):
        admin_drawer.open = False
        user_drawer.open = False
        page.dialog = logout_popup
        logout_popup.open = True
        page.update()
    
    def open_input_popup(e):
        page.dialog = input_popup
        input_popup.open = True
        page.update() 
        
    def open_criteria_popup(e):
        page.dialog = criteria_popup
        criteria_popup.open = True
        page.update()
    
    def open_success_popup(e):
        page.dialog = success_popup
        success_popup.open = True
        page.update()
        go_main(e)
        
    def open_exist_popup(e):
        page.dialog = exist_popup
        exist_popup.open = True
        page.update()
        
    def open_failed_popup(e):
        page.dialog = failed_popup
        failed_popup.open = True
        page.update()
        
    def close_dlg(e):
        print("closing...")
        input_popup.open = False
        criteria_popup.open = False
        exist_popup.open = False
        success_popup.open = False
        logout_popup.open = False
        failed_popup.open = False
        
        page.update()
    
    def create_account(e):
        special_symbols = ['_', '-', '+', '=', '!', '@', '%', '*', '&']        
        if not ((username.value == "") or (password.value == "") or (retype_password.value == "")):
            if ((password.value == retype_password.value) & (len(password.value) > 8) & (any(char.isdigit() for char in password.value)) & (any(char.isupper() for char in password.value)) & (any(char.islower() for char in password.value)) & (any(char in special_symbols for char in password.value))):
                query = "SELECT SQL_NO_CACHE * FROM credentials WHERE username = %s"
                data = (username.value,)
                cursor.execute(query, data)
                result = cursor.fetchall()
                
                if result:
                    open_exist_popup(e)
                else:
                    query = "INSERT INTO credentials (username, password, role) VALUES (%s, %s, 'user')"
                    data = (username.value, password.value)
                    cursor.execute(query, data)
                    db.commit()
                    open_success_popup(e)
            else:
                open_criteria_popup(e)
        else:
            open_input_popup(e)
        
    def go_signup(e):
        page.route = "/signup"
        page.go(page.route)
        
    def go_login(e):
        query = "SELECT SQL_NO_CACHE * FROM credentials WHERE username = %s AND password = %s"
        data = (username.value, password.value)
        cursor.execute(query, data)
        result = cursor.fetchall()
        if (result):
            query = "SELECT SQL_NO_CACHE role FROM credentials WHERE username = %s"
            data = (username.value,)
            cursor.execute(query, data)
            result = cursor.fetchone()
            if result[0] == 'user':
                page.route = "/dashboard"
                page.go(page.route)
            else:
                page.route = "/admindash"
                page.go(page.route)
        else:
            open_failed_popup(e)

    def go_main(e):
        page.route = "/"
        page.go(page.route)
        
    def go_admindash(e):
        page.route = "/admindash"
        page.go(page.route)
    
    def go_dashboard(e):
        page.route = "/dashboard"
        page.go(page.route)

    def go_pos(e):
        page.route = "/pos"
        page.go(page.route)
        
    def go_inventory(e):
        admin_drawer.open = False
        page.route = "/inventory"
        page.go(page.route)
        
    def go_user_about(e):
        user_drawer.open = False
        page.route = "/user_about"
        page.go(page.route)
        
    def go_about(e):
        admin_drawer.open = False
        page.route = "/about"
        page.go(page.route)
    
    page.on_route_change = route_change
    page.go(page.route)
    page.update()
    print("engk")

if __name__ == "__main__":
    ft.app(target = main, assets_dir = "assets")