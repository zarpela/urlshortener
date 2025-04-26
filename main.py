from typing import Union
from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import shortid as id
import mysql.connector as mysql

banco = mysql.connect(
    host="localhost",
    user="root",
    password="zarpela123",
    database="URLShortener"
)
cursor = banco.cursor()
app = FastAPI()
app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")
templates = Jinja2Templates(directory="frontend")


@app.get("/", response_class=HTMLResponse)
async def home(request: Request, shortened: str = None, display: str = "none"):
    return templates.TemplateResponse(
        request=request, name="index.html", context={"shortened": shortened, "display": display}
    )


@app.post("/create")
async def convertLongToShort(request: Request, originalURL: str = Form(...)):
    shortId = id.ShortId().generate()
    cursor.execute(f"insert into url values ('{originalURL}', '{shortId}')")
    banco.commit()

    shortURL = f"/{shortId}"
    display = "block"

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "shortened": shortId, "display": display}  
    )

@app.get("/{shortURL}", response_class=RedirectResponse, status_code=302)
def getLongURL(shortURL: str):
    cursor.execute(f"select originalURL from url where shortID = '{shortURL}'")
    resultado = cursor.fetchone()
    if resultado and resultado[0]:
        original = resultado[0]
        if not original.startswith(("http://", "https://")):
            original = "https://" + original
        return RedirectResponse(url=original)
    else:
        return RedirectResponse(url="/")
    
