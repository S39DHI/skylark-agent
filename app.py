from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel
from agent import handle_message

# Create FastAPI app
app = FastAPI()

# Set up templates
templates = Jinja2Templates(directory="templates")


# Request model for chat
class ChatRequest(BaseModel):
    message: str


# Home route (chat interface)
@app.get("/", response_class=HTMLResponse)
def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})


# Chat endpoint
@app.post("/chat")
def chat(req: ChatRequest):
    response = handle_message(req.message)
    return {"response": response}
