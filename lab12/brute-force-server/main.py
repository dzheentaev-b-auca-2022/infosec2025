from typing import Annotated


from fastapi import FastAPI, Form

app = FastAPI()




ADMIN_USERNAME = "andrii1487"
ADMIN_PASSWORD = "22051487"




@app.post("/login")
def login(
   username: Annotated[str, Form()],
   password: Annotated[str, Form()]
):
   if username == ADMIN_USERNAME and password == ADMIN_PASSWORD:
       return "secret token"
   return "Invalid credentials"
