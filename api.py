from fastapi import FastAPI
from qr_utils import qr_ascii_half_block
from fastapi.responses import PlainTextResponse, JSONResponse
from contextlib import asynccontextmanager


app = FastAPI()

@app.get("/")
async def root2():
   #return {"Note":"Check the /api endpoint"}
   return PlainTextResponse(content="""
                         
  █▀▀▀▀▀█ ▄  ▀█ █▀▀▀▀▀█  
  █ ███ █  ▄▀ ▀ █ ███ █  
  █ ▀▀▀ █ ▀██ █ █ ▀▀▀ █  
  ▀▀▀▀▀▀▀ ▀▄▀▄█ ▀▀▀▀▀▀▀  
  ▀▄▀▄█ ▀ ▄ █▀  ▄▄▀▄▄█▄  
   ▀▀ ██▀▄ █  ▀ ▄▄█▀▀▀▀  
   ▀▀   ▀ ▄▀█▄▀▄▀ █ ▄█   
  █▀▀▀▀▀█  ▀██▄█▀▀▀  ▀█  
  █ ███ █ ▀▀█▀ ▀█ ▀▄▄█▀  
  █ ▀▀▀ █ ▀ ▀ ▀ ▄█▀█▀▄▀  
  ▀▀▀▀▀▀▀ ▀▀  ▀ ▀ ▀  ▀▀  
                         
         Mini Qr       

Github: https://github.com/SantiagortegaDev/mini-qr  

Discord Bot: https://discord.com/oauth2/authorize?client_id=1550911077712142336

Check the api: https://miniqr.santiagortega.dev/api
""")

@app.get("/api")
async def root():
    #return {"status": "ok","Name":"Mini Qr","Creator":"@santiagortega"}
    return PlainTextResponse(content="""
Endpoints(i think):

GET /api/v1/qr
    ?content [str] (required), text to convert in to a beautiful ascci qr code
    &invert  [bool default=False] clasic old time with the white bg
    &raw     [bool default=False] the qr in json if you don't like the plan reponse
    &long    [bool default=False] to check you are not crazy to generate a very long qr code

  Response in plaintext or json with &raw=true
  
  Errors:
  - 400 {"error": "the qr content is too long, try with &long=true"}

Example if you already didn't understand:
- GET https://miniqr.santiagortega.dev/api/v1/qr?content=hello&invert=true
""")

@app.get("/api/v1/qr")
def read_item(content: str, invert: bool = False, raw: bool = False, long: bool = False):
    if content:
     print(f"New api request:")
     print(f"Content={content}")
     print(f"Invert={invert}")
     print(f"Long={long}")
    qr=qr_ascii_half_block(content, invert, long)
    if "too long" in qr:
       print("Response= error : the qr content is tooooooo loooooong, try with &long=true, to check that you are not crazy")
       print("Code=400")
       print("i don't remember why i put this here, well, if i delete this print lines i know all the code is going to have error")
       return JSONResponse(content={"error": "the qr content is tooooooo loooooong, try with &long=true, to check that you are not crazy"}, status_code=400)
    if raw:
     return JSONResponse(content={"qr": qr})
    else:
       return PlainTextResponse(content=qr)

@app.get("/api/v1")
def v1():
     return JSONResponse(content={"Error": "you forgot /qr, wait why i made it v1 if is the only version? idk"})

@app.get("/api/v2")
def v1():
     return JSONResponse(content={"Error": "what do you mean with v2 bro? it's the first version, get out of here"})