from fastapi import FastAPI
from qr_utils import qr_ascii_half_block
from fastapi.responses import PlainTextResponse, JSONResponse
app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/api/v1/qr", response_class=PlainTextResponse)
async def read_item(content: str, invert: bool | None = False, raw: bool | None = False):
    qr=qr_ascii_half_block(content, invert)
    if raw:
     return JSONResponse(content={"qr": qr})
    else:
       return PlainTextResponse(content=qr)