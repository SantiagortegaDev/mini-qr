from fastapi import FastAPI
from qr_utils import qr_ascii_half_block
from fastapi.responses import PlainTextResponse, JSONResponse
import subprocess
import sys
from contextlib import asynccontextmanager


process = None
#my host only execute 1 python file soo i need to run in background the bot
@asynccontextmanager
async def lifespan(app: FastAPI):
    global process
    process = subprocess.Popen([sys.executable, "-u", "bot.py"])
    print(f"Bot started PID: {process.pid})")
    yield
    process.terminate()
    try:
        process.wait(timeout=5)
    except subprocess.TimeoutExpired:
        process.kill()
    print("Bot killed")

app = FastAPI(lifespan=lifespan)

@app.get("/api")
async def root():
    return {"status": "ok","name":"Mini Qr","creator":"@santiagortega"}


@app.get("/api/v1/qr")
def read_item(content: str, invert: bool = False, raw: bool = False, long: bool = False):
    if content:
     print(f"New api request:")
     print(f"Content={content}")
     print(f"Invert={invert}")
     print(f"Long={long}")
    qr=qr_ascii_half_block(content, invert, long)
    if "too long" in qr:
       print("Response= error : the qr content is too long, try with &long=true")
       print("Code=400")
       return JSONResponse(content={"error": "the qr content is too long, try with &long=true"}, status_code=400)
    if raw:
     return JSONResponse(content={"qr": qr})
    else:
       return PlainTextResponse(content=qr)