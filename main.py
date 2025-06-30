from typing import Union
from fastapi import FastAPI, Form, Request
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
import shortid as id
import sqlite3 as sql

# criar o banco de dados quando comecar
with sql.connect("urls.db") as conexao:
    cursor = conexao.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS url (
            originalURL TEXT NOT NULL,
            shortID CHAR(8) NOT NULL UNIQUE
        )
    """)
    conexao.commit()


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

    exists = True
    while exists:
        shortId = id.ShortId().generate() #gerando um novo código
        with sql.connect("urls.db") as conexao:
            cursor = conexao.cursor()
            cursor.execute("SELECT shortID FROM url WHERE shortID = ?", (shortId,))
            resultado = cursor.fetchone()
            if not resultado:
                exists = False


    with sql.connect("urls.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("INSERT INTO url (originalURL, shortID) VALUES (?, ?)", (originalURL, shortId))
        conexao.commit()
    shortURL = f"/{shortId}"
    display = "block"

    return templates.TemplateResponse(
        "index.html",
        {"request": request, "shortened": shortId, "display": display}
    )

@app.get("/{shortURL}", response_class=RedirectResponse, status_code=302)
def getLongURL(shortURL: str):
    with sql.connect("urls.db") as conexao:
        cursor = conexao.cursor()
        cursor.execute("SELECT originalURL FROM url WHERE shortID = ?", (shortURL,))
        resultado = cursor.fetchone()


    if resultado and resultado[0]:
        original = resultado[0]
        if not original.startswith(("http://", "https://")):
            original = "https://" + original
        return RedirectResponse(url=original)
    else:
        return RedirectResponse(url="/")

