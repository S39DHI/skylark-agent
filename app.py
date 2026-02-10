from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from agent import handle_query

app = FastAPI()
templates = Jinja2Templates(directory="templates")


class ChatRequest(BaseModel):
    message: str


@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


@app.post("/chat")
def chat(req: ChatRequest):
    reply = handle_query(req.message)
    return {"response": reply}
