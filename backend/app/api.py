from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from .rss import *
from aiofiles import *
from pydantic import BaseModel
import json
from pathlib import Path


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

app.mount("/assets", StaticFiles(directory=Path(BASE_DIR, '/assets')), name="static")

class News_Request(BaseModel):
    name: str
    size: int

@app.get('/', tags = ['root'])
async def send_hello() -> dict:
    return {'message': 'hello'}
    
@app.get('/catalog', tags = ['news'])
async def send_catalog() -> dict:
    catalog = get_catalog().to_json(orient='records')     
    parsed = json.loads(catalog)
    return parsed

@app.get('/genres', tags = ['news', 'genres'])
async def send_genres():
    catalog = get_genres().to_json(orient='records')     
    parsed = json.loads(catalog)
    return parsed

@app.post('/news', tags = ['news'])
async def send_news(news_request: News_Request) -> dict:
    news = get_news(news_request.name, news_request.size).to_json(orient='records')
    parsed = json.loads(news)
    return parsed
