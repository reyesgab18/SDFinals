from db_utils import *


query = "SELECT * FROM items"
cursor.execute(query,)
result = cursor.fetchall()
items = []
for x in result:
    items.append(x[1])
