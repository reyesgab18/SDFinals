#modules
import os
import mysql.connector
from dotenv import load_dotenv

#load .env file containing database credentials
load_dotenv()

#loads .env data into python file
host = os.getenv("host")
user = os.getenv("user")
password = os.getenv("password")
name = os.getenv("name")
port = os.getenv("port")

#initialize database     
db = mysql.connector.connect(
    host = host, 
    user = user, 
    password = password, 
    database = name, 
    port = int(port)
)

#get cursor
cursor = db.cursor()
    
