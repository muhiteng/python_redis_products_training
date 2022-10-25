from main import redis,Product
import time

key='order_completed'
group= 'products_group'

try:
    redis.xgroupcreate(key,group)
except:
    print('group already exists')

while True:
    try:
        results=redis.xreadgroup(group,key,{key:'>'},None)
        if results != []:
            for result in results:
                obj=result[1][0][1]
                product=Product.get(obj['product_id'])
                try:
                    product.quantity=product.quantity - int(obj['quantity'])
                    product.save()
                except:
                    redis.xadd('refund_order',obj,'*')
    except Exception as e:
        print(str(e))

    time.sleep(1)