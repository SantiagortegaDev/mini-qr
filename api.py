from fastapi import FastAPI
from qr_utils import qr_ascii_half_block
from fastapi.responses import PlainTextResponse, JSONResponse
app = FastAPI()


@app.get("/api")
async def root():
    return {"status": "ok","name":"Mini Qr","creator":"@santiagortega"}


@app.get("/api/v1/qr")
def read_item(content: str, invert: bool = False, raw: bool = False, long: bool = False):

    qr=qr_ascii_half_block(content, invert, long)
    if "too long" in qr:
       return JSONResponse(content={"error": "the qr content is too long, try with &long=true"})
    if raw:
     return JSONResponse(content={"qr": qr})
    else:
       return PlainTextResponse(content=qr)