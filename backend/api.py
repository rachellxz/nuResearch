from os import name
from typing import List, Optional
from fastapi import FastAPI, Response, Cookie
from fastapi.middleware.cors import CORSMiddleware
from starlette.staticfiles import StaticFiles
from rss import *
from aiofiles import *
from pydantic import BaseModel
import json
import psycopg2

class News_Request(BaseModel):
    name: str
    size: int

class Category_Request(BaseModel):
    name: str

class User(BaseModel):
    name: str

app = FastAPI()

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

async def connect():
    conn = psycopg2.connect(host="34.150.240.215", port = 5432, database="nuresearch_db", user="postgres", password="mcit2022")
    return conn

@app.post('/login', tags = ['login_status'])
async def create_cookies(user: User, response: Response):
    conn = await connect()
    response.set_cookie(key = "login_token", value = True, httponly = True)
    

    cur = conn.cursor()
    cur.execute("SELECT email FROM users;")
    query_results = cur.fetchall()

    if (user.name, ) not in query_results:
        print(user.name)
        cur.execute("""INSERT INTO users (id, name, email) VALUES (%(id)s, %(name)s, %(name)s);""", \
            {'id': str(len(query_results)), 'name': user.name } )
        cur.execute("SELECT * FROM users;")
        conn.commit()

    cur.close()
    conn.close()
    return "login_token set to true"

@app.post('/category', tags = ['news'])
async def add_user_category(category_request: Category_Request, login_token: Optional[bool] = Cookie(None)):
    if login_token:
        conn = await connect()
        category = category_request.name

        """TODO ADD SQL: Check if category associated with user. If not add category"""
        # Example of how to do sql query
        #cur = conn.cursor()
        #cur.execute("""SELECT * FROM vendors""")
        #query_results = cur.fetchall()
        #print(query_results)    
        #curr.close()
        # return query_results
        conn.close()
    else:
        return {"Message": "Not logged in"}

@app.get('/category', tags = ['news'])
async def add_user_category(category_request: Category_Request, login_token: Optional[bool] = Cookie(None)):
    if login_token:
        conn = await connect()
        category = category_request.name

        """TODO ADD SQL: Return  all categories associated with the user"""
        # Example of how to do sql query
        #cur = conn.cursor()
        #cur.execute("""SELECT * FROM vendors""")
        #query_results = cur.fetchall()
        #print(query_results)    
        #curr.close()
        conn.close()
    else:
        return {"Message": "Not logged in"}

@app.post('/logout', tags = ['login_status'])
async def create_cookies(response: Response):
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

