import redis
import json

red = redis.Redis(host='localhost', port=6379, db=2, decode_responses=True)

pub = red.pubsub()
red.publish("loadAllItems", "")

pub.subscribe('loadInventory')

for new_message in pub.listen():
    try:
        message = json.loads(new_message['data'])
                
    except Exception as e:
        print(e,"error")
        
