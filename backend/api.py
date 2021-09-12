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
    category: str


class User(BaseModel):
    name: str


app = FastAPI()

origins = ['http://localhost:3000', 'localhost:3000']

app.add_middleware(CORSMiddleware,
                   allow_origins=origins,
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])

app.mount("/assets", StaticFiles(directory='assets'), name="static")


@app.post('/news', tags=['news'])
async def send_news(news_request: News_Request) -> dict:
    try:
        news = get_news(news_request.name,
                        news_request.size).to_json(orient='records')
        parsed = json.loads(news)
        return parsed
    except:
        return []

@app.post('/example', tags = ['homer'])
async def send_email() -> dict:

    return {"message": "it works!"}


async def connect(db="nuresearch_db"):
    conn = psycopg2.connect(host="34.150.240.215",
                            port=5432,
                            database=db,
                            user="postgres",
                            password="mcit2022")
    return conn


@app.post('/login', tags=['user'])
async def create_cookies(user: User, response: Response):
    conn = await connect()
    response.set_cookie(key="login_token", value=True, httponly=True)

    cur = conn.cursor()
    cur.execute("SELECT email FROM users;")
    query_results = cur.fetchall()

    if (user.name, ) not in query_results:
        idd = len(query_results)
        cur.execute("""INSERT INTO users (id, name, email) VALUES (%(id)s, %(name)s, %(name)s);""", \
            {'id': str(idd), 'name': user.name } )
        response.set_cookie(key='login_id', value=idd)
        cur.execute("SELECT * FROM users;")
        conn.commit()
    else:
        cur.execute("SELECT email, id FROM users WHERE email = %(name)s;",
                    {"name": user.name})
        query_results = cur.fetchall()
        print(query_results[0][1])
        response.set_cookie(key='login_id', value=query_results[0][1])

    cur.close()
    conn.close()
    return "login_token set to true"


@app.post('/category', tags=['user'])
async def add_user_category(category_request: Category_Request,
                            login_token: Optional[bool] = Cookie(None),
                            login_id: Optional[int] = Cookie(None)):
    if login_token:
        conn = await connect()
        category = category_request.category
        cur = conn.cursor()
        cur.execute(
            """SELECT id, category FROM categories WHERE id = %(idd)s; """,
            {"idd": str(login_id)})
        query_results = cur.fetchall()

        if (
                login_id,
                category_request.category,
        ) not in query_results:
            cur.execute("""INSERT INTO categories (id, category) VALUES (%(id)s, %(category)s);""", \
            {"id" : str(login_id), "category": category})

        conn.commit()
        cur.close()
        conn.close()
    else:
        return {"Message": "Not logged in"}


@app.get('/category', tags=['user'])
async def get_user_category(login_token: Optional[bool] = Cookie(None),
                            login_id: Optional[int] = Cookie(None)):
    if login_token:
        conn = await connect()
        cur = conn.cursor()
        cur.execute(
            """SELECT id, category FROM categories WHERE id = %(idd)s; """,
            {"idd": str(login_id)})
        query_results = cur.fetchall()
        query_results = [i[1] for i in query_results]
        conn.close()
        return query_results
    else:
        return {"Message": "Not logged in"}

@app.get('/channels', tags=['news'])
async def send_channels():
    return get_channels()

@app.post('/logout', tags=['user'])
async def create_cookies(response: Response):
    response.set_cookie(key="login_token", value=False, httponly=True)
    return "login_token set to false"


@app.get('/login', tags=['user'])
async def is_login(login_token: Optional[bool] = Cookie(None)):
    if login_token is None:
        return False
    return login_token


@app.get('/', tags=['root'])
async def send_hello() -> dict:
    return {'message': 'hello'}


@app.get('/catalog', tags=['news'])
async def send_catalog() -> dict:
    catalog = get_catalog().to_json(orient='records')
    parsed = json.loads(catalog)
    return parsed


@app.get('/genres', tags=['news', 'genres'])
async def send_genres() -> dict:
    catalog = get_genres()
    return catalog
