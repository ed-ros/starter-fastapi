from fastapi import FastAPI
from fastapi.responses import FileResponse

from pydantic import BaseModel

from datetime import datetime
import requests


app = FastAPI()


class Item(BaseModel):
    item_id: int


def now():
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def request_url(url):
    headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36'}

    response = requests.get(url, headers=headers)

    if response.status_code != 200:
        print("GET error", response.status_code, "- URL:", url)
    
    return response


def get_event_dates(month=4, year=2024):
    event_code = "mcXTJpXoZh8bbnvjtRmi"
    
    url = "https://services.tix.byinti.com/neofront-v3/ticket-event-dates/?"
    url += "event_code={0}&month={1}&year={2}".format(event_code, month, year)
        
    return request_url(url)
    
    
@app.get("/")
async def root():
    response = get_event_dates()
        
    return {"message": response.text}


@app.get('/favicon.ico', include_in_schema=False)
async def favicon():
    return FileResponse('favicon.ico')


@app.get("/item/{item_id}")
async def read_item(item_id: int):
    return {"item_id": item_id}


@app.get("/items/")
async def list_items():
    return [{"item_id": 1, "name": "Foo"}, {"item_id": 2, "name": "Bar"}]


@app.post("/items/")
async def create_item(item: Item):
    return item
