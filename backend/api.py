from typing import List, Optional
from fastapi import FastAPI, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from rss import *
from aiofiles import *
from pydantic import BaseModel
import json
from pathlib import Path

class News_Request(BaseModel):
    name: str
    size: int

app = FastAPI()
BASE_DIR = Path(__file__).resolve().parent

origins = [
    'http://localhost:3000',
    'localhost:3000'
]


app.add_middleware(
        CORSMiddleware,
        allow_origins=origins,
        allow_credentials=True,
        allow_methods=['*'],
        allow_headers=['*']
)

app.mount("/assets", StaticFiles(directory='assets'), name="static")

@app.post('/news', tags = ['news'])
async def send_news(news_request: News_Request) -> dict:
    news = get_news(news_request.name, news_request.size).to_json(orient='records')
    parsed = json.loads(news)
    return parsed

@app.post('/login', tags = ['login_status'])
def create_cookies(response: Response):
    response.set_cookie(key = "login_token", value = True, httponly = True)
    return "login_token set to true"

@app.post('/logout', tags = ['login_status'])
def create_cookies(response: Response):
    response.set_cookie(key = "login_token", value = False, httponly = True)
    return "login_token set to false"

@app.get('/login', tags = ['login_status'])
async def is_login(login_token: Optional[bool] = Cookie(None)):
    return login_token

@app.get('/', tags = ['root'])
async def send_hello() -> dict:
    return {'message': 'hello'}
    
@app.get('/catalog', tags = ['news'])
async def send_catalog() -> dict:
    catalog = get_catalog().to_json(orient='records')     
    parsed = json.loads(catalog)
    return parsed

@app.get('/genres', tags = ['news', 'genres'])
async def send_genres() -> dict:
    catalog = get_genres()     
    return json.dumps(catalog)

