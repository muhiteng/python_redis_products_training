from typing import Union

from fastapi import FastAPI
from redis-om import redis_connection,HashModel
from fastapi.middleware.cors import CORSMiddleware
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
class Product(HashModel):
    name:str
    price:float
    quantity:int
    class Meta:
     database=redis

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/products")
def all():
    return [format(pk) for pk in Product.pks()];

def format(pk:str):
    product= Product.get(pk);
    return {
        'id':product.pk,
        'name':product.name,
         'price':product.price,
         'quantity':product.quantity,
    }
       
    
@app.post("/product")
def create(product:Product):
    return product.save();

@app.get("/products/{pk}")
def get(pk:str):
    return product.get(pk);

@app.delete("/products/{pk}")
def get(pk:str):
    return product.delete(pk);
