from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api import analytics, videoes, comments, channels, user, scrap_requests

app = FastAPI()

origins = ['https://localhost:3000','*']

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=["*"],
                   allow_headers=["*"])


@app.get("/")
def read_root():
    return {""}


app.include_router(channels.router)

app.include_router(scrap_requests.router)
