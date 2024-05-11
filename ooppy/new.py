import flet as ft
from db_utils import *
from colors import *
import string
import random
import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

def main(page: ft.Page):
    
    def route_change(route):
        page.views.clear()
        
        if page.route == "/":
            loginpage()
            
        if page.route == "/signup":
            signuppage()
            
        if page.route == "/dash":
            dashboardpage()
            
        if page.route == "/admindash":
            print("admindash")
            
        if page.route == "/pos":
            pospage()
            
        if page.route == "/reset":
            resetpage()
            
        if page.route == "/confirmreset":
            confirmresetpage()
      
    def loginpage():
        #ELEMENTS
        #logo = ft.Image(src = "/images/logo.png", height = 300, width = 300)
        logo = ft.Column([
            ft.Text("Aldrino's", size = 70, weight = ft.FontWeight.BOLD, italic = True, color = background),
            ft.Text("POS and Inventory Management System", size = 15, color = background)
        ], horizontal_alignment = ft.CrossAxisAlignment.CENTER, spacing = 0)
        divider = ft.Divider(height = 20, color = 'transparent')
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
        login_elements = ft.Column(
            alignment = 'center',
            controls = [
                ft.Row([logo], alignment = 'center'),
                divider,
                ft.Divider(height = 20),
                divider,
                ft.Row([username], alignment = 'center'),
                ft.Row([password], alignment = 'center'),
                ft.Row([ft.TextButton("Log in", on_click = lambda e: verify(e), width = 300, height = 50, style = ft.ButtonStyle(color = ft.colors.BLACK, bgcolor = background))], alignment = 'center'),
                divider,
                ft.Row([ft.Text(spans = [
                    ft.TextSpan("No account yet? Sign up"), ft.TextSpan(" "),
                    ft.TextSpan("here", ft.TextStyle(decoration = ft.TextDecoration.UNDERLINE),
                        on_click = lambda e: go_signup(e)        
                        )], color = background)],
                    alignment = 'center'),
                ft.Row([ft.Text(size = 10, spans = [
                    ft.TextSpan("Reset password", ft.TextStyle(decoration = ft.TextDecoration.UNDERLINE),
                        on_click = lambda e: go_resetpage(e)        
                        )], color = background)],
                    alignment = 'center'),
                ft.Divider(height = 100, color = 'transparent'),
                ft.Row([ft.Text("2024 © SDSystems Inc. All Rights Reserved.", color = background, size = 10)], alignment = 'center'),
                divider, divider
            ]
        )
        
        page.views.append(
            ft.View("/", [
                ft.SafeArea(
                    content = ft.Column([
                        ft.Row([theme()], alignment = ft.MainAxisAlignment.END),
                        login_elements
                    ])
                )
            ])
        )
        page.update()
        
        def verify(e):
            cursor.execute("SELECT role FROM credentials WHERE username = %s AND password = %s", (username.value, password.value))
            result = cursor.fetchone()
            
            if(result):
                if result[0] == 'user':
                    page.route = "/dash"
                    page.go(page.route)
                else:
                    page.route = "/admindash"
                    page.go(page.route)
            else:
                verif_failed()
                
        def verif_failed():
            dialog = ft.AlertDialog(
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
            page.dialog = dialog
            dialog.open = True
            page.update()
            
            def close_dlg(e):
                dialog.open = False
                page.update()
        
        def go_signup(e):
            page.route = "/signup"
            page.go(page.route)
            
        def go_resetpage(e):
            page.go("/reset")

    def resetpage():
        #ELEMENTS
        wrong = ft.AlertDialog(
            title = ft.Text("Wrong Credentials"),
            content = ft.Text("No username and/or email found in database. Please try again."),
            actions = [
                ft.TextButton(
                    "Ok",
                    on_click = lambda e: close(e),
                    style = ft.ButtonStyle(
                        bgcolor = background,
                        color = foreground
                    )
                )
            ],
            actions_alignment = ft.MainAxisAlignment.END
        )
        divider = ft.Divider(height = 20, color = 'transparent')
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
            suffix_text = "@gmail.com",
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
        reset = ft.Column(
            spacing = 0,
            alignment = 'center',
            controls = [
                ft.Row([
                    ft.Text("Password Reset", color = background, size = 30, weight = ft.FontWeight.BOLD)
                ], alignment = 'center'),
                ft.Row([
                    ft.Text(" Enter your username and registered email address to get your OTP.", color = background, size = 10)
                ], alignment = 'center'), divider, divider, divider,
                ft.Row([username], alignment = 'center'), divider,
                ft.Row([email], alignment = 'center'), divider,
                ft.Row([ft.FilledButton("Request OTP", on_click = lambda e: send_otp(e), width = 300, height = 50, style = ft.ButtonStyle(color = ft.colors.BLACK, bgcolor = background))], alignment = 'center'),
                ft.Divider(height = 300, color = 'transparent')
            ]
        )
        
        page.views.append(
            ft.View("/reset", [
                ft.AppBar(
                    leading = ft.Row([
                        ft.FilledButton("Log in", 
                            style = ft.ButtonStyle(
                                color = background, 
                                bgcolor = 'transparent'), 
                            icon = ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,  
                            on_click = lambda e: page.go("/"))
                    ], alignment = 'left'),
                    leading_width = 150,
                    actions = [
                        ft.Row([theme()], alignment = ft.MainAxisAlignment.END),
                    ]
                ),
                ft.SafeArea(
                    content = ft.Column([
                        reset
                    ])
                )
            ])
        )
        page.update()
        
        def send_otp(e):
            final_email = email.value + "@gmail.com"
            cursor.execute("SELECT password FROM credentials WHERE username = %s AND email = %s", (username.value, final_email))
            result = cursor.fetchone()
            
            if result:
                random_num = random.randint(1000, 9999)
                sender_email = "sdsystems52024@gmail.com"
                rec_email = str(final_email)
                password = str("cnse rube mnho hjpx")
                message = "Your OTP is " + str(random_num)

                server = smtplib.SMTP('smtp.gmail.com', 587)
                server.starttls()
                server.login(sender_email, password)
                server.sendmail(sender_email, rec_email, message)
                print("email sent to ", rec_email)
                reset_pass(str(random_num))
            else:
                page.dialog = wrong
                wrong.open = True
                page.update()
        
        def reset_pass(otpcode):
            otp = ft.TextField(
                label = "OTP",
                text_align = ft.TextAlign.CENTER,
                content_padding = ft.padding.all(10),
                border_color = background,
                border_radius = 50,
                width = 100,
                color = background,
                cursor_color = background,
                cursor_radius = 10,
                label_style = ft.TextStyle(
                    color = background,
                    #weight = ft.FontWeight.BOLD
                ),
            )
            error = ft.Text("", color = ft.colors.RED)
            otp_req = ft.AlertDialog(
                modal = True,
                title = ft.Text("Enter OTP"),
                content = ft.Column([
                    ft.Text("To reset your password, we sent an OTP to your e-mail address."),
                    ft.Divider(height = 10, color = 'transparent'),
                    ft.Row([otp], alignment = ft.MainAxisAlignment.CENTER),
                    ft.Row([error], alignment = ft.MainAxisAlignment.CENTER)
                ], height = 150),
                actions = [
                    ft.TextButton(
                        "Enter",
                        on_click = lambda e: confirm(e),
                        style = ft.ButtonStyle(
                            bgcolor = background,
                            color = foreground
                        )
                    ),
                    ft.TextButton(
                        "Cancel",
                        on_click = lambda e: close(e),
                        style = ft.ButtonStyle(
                            bgcolor = background,
                            color = foreground
                        )
                    ),
                ],
                actions_alignment = ft.MainAxisAlignment.END
            )
            
            page.dialog = otp_req
            otp_req.open = True
            page.update()
            
            def confirm(e):
                code = otp.value
                if code == otpcode:
                    otp_req.open = False
                    page.update()
                    page.views.clear()
                    confirmresetpage(username.value)
                    
                else:
                    error.value = "Invalid OTP"
                    page.update()
                
        def close(e):
            page.dialog.open = False
            page.update()
    
    def confirmresetpage(username):
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
        divider = ft.Divider(height = 20, color = 'transparent')
        error = ft.Text("", color = ft.colors.RED)
        confirmreset = ft.Column(
            spacing = 0,
            alignment = 'center',
            controls = [
                ft.Row([
                    ft.Text("Create New Password", color = background, size = 30, weight = ft.FontWeight.BOLD)
                ], alignment = 'center'),
                ft.Row([
                    ft.Text(" Create a new strong password for your account.", color = background, size = 10)
                ], alignment = 'center'), divider, divider, divider,
                ft.Row([password], alignment = 'center'), divider,
                ft.Row([retype_password], alignment = 'center'), divider, error, divider, 
                ft.Row([ft.FilledButton("Confirm New Password", on_click = lambda e: commit(e), width = 300, height = 50, style = ft.ButtonStyle(color = ft.colors.BLACK, bgcolor = background))], alignment = 'center'),
                ft.Divider(height = 300, color = 'transparent')
            ]
        )
        
        success = ft.AlertDialog(
            modal = True,
            title = ft.Text("Password Reset Successful"),
            content = ft.Text("You can now use your new password to log in."),
            actions = [
                ft.TextButton(
                    "Ok",
                    on_click = lambda e: confirm(e),
                    style = ft.ButtonStyle(
                        bgcolor = background,
                        color = foreground
                    )
                )
            ]
        )
        
        input = ft.AlertDialog(
            modal = True,
            title = ft.Text("Incomplete Fields"),
            content = ft.Text("Please input all fields."),
            actions = [
                ft.TextButton(
                    "Ok",
                    on_click = lambda e: close(e),
                    style = ft.ButtonStyle(
                        bgcolor = background,
                        color = foreground
                    )
                )
            ]
        )
        
        criteria = ft.AlertDialog(
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
                    on_click = lambda e: close(e),
                    style = ft.ButtonStyle(
                        bgcolor = background,
                        color = foreground
                    )
                )
            ],
            actions_alignment = ft.MainAxisAlignment.END
        )
        
        
        page.views.append(
            ft.View("/confirmreset", [
                ft.AppBar(
                    leading = ft.Row([
                        ft.FilledButton("Log in", 
                            style = ft.ButtonStyle(
                                color = background, 
                                bgcolor = 'transparent'), 
                            icon = ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,  
                            on_click = lambda e: page.go("/"))
                    ], alignment = 'left'),
                    leading_width = 150,
                    actions = [
                        ft.Row([theme()], alignment = ft.MainAxisAlignment.END),
                    ]
                ),
                ft.SafeArea(
                    content = ft.Column([
                        confirmreset
                    ])
                )
            ])
        )
        page.update()
        
        def commit(e):
            special_symbols = ['_', '-', '+', '=', '!', '@', '%', '*', '&']        
            if not ((password.value == "") or (retype_password.value == "")):
                if ((password.value == retype_password.value) & (len(password.value) > 8) & (any(char.isdigit() for char in password.value)) & (any(char.isupper() for char in password.value)) & (any(char.islower() for char in password.value)) & (any(char in special_symbols for char in password.value))):
                    cursor.execute("UPDATE credentials SET password = %s WHERE username = %s", (password.value, username))
                    db.commit()
                    open_success(e)
                    page.update()
                    
                else:
                    open_criteria(e)
                    
            else:
                open_input(e)
                
        def open_success(e):
            page.dialog = success
            success.open = True
            page.update()
            
        def open_criteria(e):
            page.dialog = criteria
            criteria.open = True
            page.update()
            
        def open_input(e):
            page.dialog = input
            input.open = True
            page.update()
            
        def close(e):
            page.dialog.open = False
            page.update()
            
        def confirm(e):
            success.open = False
            page.go("/")
            page.update()

    def pospage():
        
        item = ft.Column(
            height = 700,
            scroll = 'hidden',
            on_scroll_interval=0,
            alignment = 'center'
        )
        cursor.execute("SELECT itemID, itemName, itemPrice FROM items")
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
                    #on_click = lambda e = e, name = name, price = price: add_order(id, name, price)
                )
            )
        
        drawer = access_drawer()
        page.views.append(
            ft.View("/pos", [
                ft.AppBar(
                    leading = ft.IconButton(
                        icon = ft.icons.MENU_ROUNDED,
                        style = ft.ButtonStyle(
                            color = background
                        ),
                        on_click = lambda e: show_drawer(e)
                    )
                ),
                ft.SafeArea(
                    content = ft.Column([
                        ft.Row([pagetitle("Point of Sale System")]),
                        item
                    ], horizontal_alignment = 'center')
                )
            ], drawer = drawer)
        )
        page.update()
        
        def show_drawer(e):
            drawer.open = True
            page.update()
            
        def close(e):
            drawer.open = False
            page.update()

    def signuppage():
        #ELEMENTS
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
        email = ft.TextField(
            label = "Email",
            suffix_text = "@gmail.com",
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

        criteria = ft.AlertDialog(
            modal = True,
            title = ft.Text("Passwords Error"),
            content = ft.Column([
                ft.Text("Passwords don't match or password criteria not met.", size = 15, color = background, weight = ft.FontWeight.BOLD),
                ft.Text("Password criteria:", size = 10),
                ft.Text("- At least eight (8) characters", size = 10),
                ft.Text("- At least one (1) uppercase letter (A - Z)", size = 10),
                ft.Text("- At least one (1) lowercase letter (a - z)", size = 10),
                ft.Text("- At least one (1) number (0 - 9)", size = 10),
                ft.Text("- At least one (1) special character ('_', '-', '+', '=', '!', '@', '%', '*', '&')", size = 10)
            ], height = 300),
            actions = [ft.TextButton(
                "Ok",
                on_click = lambda e: close(e),
                style = ft.ButtonStyle(
                    bgcolor = background,
                    color = foreground
                )
            )]
        )
        exist = ft.AlertDialog(
            modal = True,
            title = ft.Text("Existing Username or Email"),
            content = ft.Text("Existing username or email found. Please choose another."),
            actions = [ft.TextButton(
                "Enter",
                on_click = lambda e: close(e),
                style = ft.ButtonStyle(
                    bgcolor = background,
                    color = foreground
                )
            )]
        )
        input = ft.AlertDialog(
            modal = True,
            title = ft.Text("Incomplete Fields"),
            content = ft.Text("Please input all fields."),
            actions = [ft.TextButton(
                "Ok",
                on_click = lambda e: close(e),
                style = ft.ButtonStyle(
                    bgcolor = background,
                    color = foreground
                )
            )]
        )
        
        divider = ft.Divider(height = 10, color = 'transparent')
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
                ft.Row([ft.FilledButton("Sign up", on_click = lambda e: req_otp(e), width = 300, height = 50, style = ft.ButtonStyle(color = ft.colors.BLACK, bgcolor = background))], alignment = 'center'),
                ft.Divider(height = 300, color = 'transparent')
            ]
        )
        page.views.append(
            ft.View("/signup", [
                ft.AppBar(
                    leading = ft.Row([
                        ft.FilledButton("Log in", 
                            style = ft.ButtonStyle(
                                color = background, 
                                bgcolor = 'transparent'), 
                            icon = ft.icons.ARROW_BACK_IOS_NEW_ROUNDED,  
                            on_click = lambda e: page.go("/"))
                    ], alignment = 'left'),
                    leading_width = 150,
                    actions = [
                        ft.Row([theme()], alignment = ft.MainAxisAlignment.END),
                    ]
                ),
                ft.SafeArea(
                    content = ft.Column([
                        signuppage
                    ])
                )
            ])
        )
        page.update()
        
        def req_otp(e):
            final_email = email.value + "@gmail.com"
            special_symbols = ['_', '-', '+', '=', '!', '@', '%', '*', '&']        
            if not ((username.value == "") or (password.value == "") or (retype_password.value == "")):
                if ((password.value == retype_password.value) & (len(password.value) > 8) & (any(char.isdigit() for char in password.value)) & (any(char.isupper() for char in password.value)) & (any(char.islower() for char in password.value)) & (any(char in special_symbols for char in password.value))):
                    cursor.execute("SELECT username FROM credentials WHERE username = %s OR  = %s", (username.value, final_email))
                    result = cursor.fetchall()
                    
                    if result:
                        open_exist_popup(e)
                    else:
                        user_email = email.value + "@gmail.com"
                        send_otp(user_email)
                else:
                    open_criteria_popup(e)
            else:
                open_input_popup(e)
                
        def send_otp(user_email):
            random_num = random.randint(1000, 9999)
            sender_email = "sdsystems52024@gmail.com"
            rec_email = str(user_email)
            password = str("cnse rube mnho hjpx")
            message = "Your OTP is " + str(random_num)

            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.starttls()
            server.login(sender_email, password)
            server.sendmail(sender_email, rec_email, message)
            print("email sent to ", rec_email)
            create_account(str(random_num))
                
        def open_input_popup(e):
            page.dialog = input
            input.open = True
            page.update()
        
        def open_criteria_popup(e):
            page.dialog = criteria
            criteria.open = True
            page.update()
        
        def open_exist_popup(e):
            page.dialog = exist
            exist.open = True
            page.update()
        
        def close(e):
            page.dialog.open = False
            page.update()
        
        def create_account(sent):
            otp = ft.TextField(
                label = "Enter 4-digit OTP",
                text_align = ft.TextAlign.CENTER,
                content_padding = ft.padding.all(10),
                border_color = background,
                border_radius = 50,
                width = 100,
                color = background,
                cursor_color = background,
                cursor_radius = 10,
                label_style = ft.TextStyle(
                    color = background,
                    #weight = ft.FontWeight.BOLD
                ),
            )
            success = ft.AlertDialog(
                modal = True,
                title = ft.Text("Account Creation Successful"),
                content = ft.Text("You can now use your credentials to log in."),
                actions = [
                    ft.TextButton(
                        "Ok",
                        on_click = lambda e: to_main(e),
                        style = ft.ButtonStyle(
                            bgcolor = background,
                            color = foreground
                        )
                    )
                ]
            )
            error = ft.Text("", color = ft.colors.RED)
            otp_req = ft.AlertDialog(
                modal = True,
                title = ft.Text("Enter OTP"),
                content = ft.Column([
                    ft.Text("To verify your account, we sent an OTP to your e-mail address."),
                    ft.Divider(height = 10, color = 'transparent'),
                    ft.Row([otp], alignment = ft.MainAxisAlignment.CENTER),
                    ft.Row([error], alignment = ft.MainAxisAlignment.CENTER)
                ], height = 150),
                actions = [
                    ft.TextButton(
                        "Enter",
                        on_click = lambda e: confirm(e),
                        style = ft.ButtonStyle(
                            bgcolor = background,
                            color = foreground
                        )
                    ),
                    ft.TextButton(
                        "Cancel",
                        on_click = lambda e: close(e),
                        style = ft.ButtonStyle(
                            bgcolor = background,
                            color = foreground
                        )
                    ),
                ],
                actions_alignment = ft.MainAxisAlignment.END
            )
            page.dialog = otp_req
            otp_req.open = True
            page.update()
            
            def confirm(e):
                code = otp.value
                final_email = email.value + "@gmail.com" 
                if code == sent:
                    cursor.execute("INSERT INTO credentials (username, password, email, role) VALUES (%s, %s, %s, 'user')", (username.value, password.value, final_email))
                    db.commit()
                    open_success_popup(e)
                else:
                    print("failed")
                    error.value = "Invalid OTP"
                    page.update()     
                    
            def open_success_popup(e):
                page.dialog = success
                success.open = True
                page.update()
                
            def close(e):
                page.dialog.open = False
                page.update()
                
            def to_main(e):
                success.open = False
                page.update()
                page.go("/")

    def dashboardpage():
        drawer = access_drawer()
        page.views.append(
            ft.View("/dash", [
                ft.AppBar(
                    leading = ft.IconButton(
                        icon = ft.icons.MENU_ROUNDED,
                        style = ft.ButtonStyle(
                            color = background
                        ),
                        on_click = lambda e: show_drawer(e)
                    )
                ),
                ft.SafeArea(
                    content = ft.Column([
                        ft.Row(
                            controls = [
                                pagetitle("Dashboard")
                            ]
                        )
                    ])
                ), 
            ], drawer = drawer)
        )
        page.update()
    
        def show_drawer(e):   
            drawer.open = True
            page.update()
    
    
    def access_drawer():
        divider = ft.Divider(height = 20, color = 'transparent')
        drawer = ft.NavigationDrawer(
            controls = [
                ft.Container(height = 12),
                ft.Row([theme()], alignment = ft.MainAxisAlignment.END),
                ft.Row([
                    ft.Text("Role: "),
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
                            on_click = lambda e: page.go("/dash") 
                        ),
                        ft.FilledButton(
                            width = 200,
                            style = ft.ButtonStyle(
                                bgcolor = background
                            ),
                            content = ft.Text("POS", weight = ft.FontWeight.BOLD),
                            on_click = lambda e: page.go("/pos")
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
        
        def show_logout_popup(e):
            logout_popup = ft.AlertDialog(
                modal = True,
                content = ft.Text(
                    "Are you sure you want to logout?",
                    color = background
                ),
                actions = [
                    ft.TextButton(
                        "Yes",
                        on_click = lambda e: logout_dlg(e),
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
            page.dialog = logout_popup
            logout_popup.open = True
            page.update()
            
            def logout_dlg(e):
                logout_popup.open = False
                page.update()
                page.route = "/"
                route_change(page.route)
            
            def close_dlg(e):
                logout_popup.open = False
                page.update()
        
        return(drawer)
    
    def theme():
        icon = ft.IconButton(
            scale = 0.85,
            icon = ft.icons.DARK_MODE_ROUNDED,
            icon_color = background,
            on_click = lambda e: toggle_theme(e)
        )
        
        def toggle_theme(e):
            if e.control.icon == ft.icons.LIGHT_MODE_ROUNDED:
                page.theme_mode = ft.ThemeMode.DARK
                e.control.icon = ft.icons.DARK_MODE_ROUNDED
            
            else:
                page.theme_mode = ft.ThemeMode.LIGHT
                e.control.icon = ft.icons.LIGHT_MODE_ROUNDED
                
            page.update()
        
        return icon
    
    def pagetitle(title):
        return ft.Row([ft.Text(title, size = 20, weight = ft.FontWeight.BOLD, color = background)], alignment = 'center')
    
    page.on_route_change = route_change
    page.go(page.route)
    page.update()    
    
if __name__ == "__main__":
    ft.app(target = main, assets_dir = "assets")