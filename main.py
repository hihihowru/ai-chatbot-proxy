from fastapi import FastAPI
from routes import answer

app = FastAPI()
app.include_router(answer.router) 