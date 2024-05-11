from flet import *
from db_utils import *

def LoginView(page):
    nametxt = TextField(label="email")
    passwordtxt = TextField(label="password")
    
    def processlogin(e):
        cursor.execute("SELECT * FROM fletusers WHERE email = %s AND PASSWORD = %s", (nametxt.value, passwordtxt.value))
        result = cursor.fetchone()
        
        if result[0] == 1:
            
    
    return Column([
        Text("login", size= 30, weight="bold"),
        nametxt,
        passwordtxt,
        ElevatedButton("login",
            bgcolor = "green", color = "white",
            on_click = processlogin
        )
    ])