import redis
import json

red = redis.Redis(host='localhost', port=6379, db=2, decode_responses=True)

pub = red.pubsub()


#pub.subscribe('loadInventory')

for new_message in pub.listen():
    try:
        message = json.loads(new_message['data'])
        else:
            pass
        
    except Exception as e:
        print(e,"error")
        

def addItem():
    pass

def removeItem():
    pass



