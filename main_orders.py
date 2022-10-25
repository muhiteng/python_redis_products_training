from typing import Union

from fastapi import FastAPI
from redis-om import redis_connection,HashModel
from fastapi.middleware.cors import CORSMiddleware
from starlette.requests import Request
from fastapi.background import BackgroundTasks 
import requests,time

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_methods=['*'],
    allow_headers=['*']
    )

redis=get_redis_connection(
    host="redis-17215.c12.us-east-1-4.ec2.cloud.redislabs.com",
    port=17215,
    password="RLgCjAgK5MJ8YFJ6XQ56VZPxdUpVNNCA",
    decose_responses=true
);


##//==============================
class Order(HashModel):
    product_id:str
    price:float
    fee:float
    total:float
    quantity:int
    status:str  # pending ,completed, refunded

    class Meta:
     database=redis

@app.get("/orders/{pk}")
def get(pk:str):
     order=Order.get(pk)
     return order


@app.post("/orders")
async def create(requset:Request,background_tasks: BackgroundTasks): # will recieve id,quantity
    body=requset.json()

    req=requests.get('http://localhost:8000/prodoucts/%s'% body['id'])
    product=req.json()
    order=Order(
        product_id= body['id'],
        price=product['price'],
        fee=0.2 * product['price'],
        total=1.2 * product['price'],
        quantity=body['quantity'],
        status='pending'
    )
    order.save()
    background_tasks.add_task(order_completed,order)
    

    return order

def order_completed(order:Order):
    time.sleep(5)
    order.status='completed'
    order.save()
    redis.xadd('order_completed',order.dict(),'*')
