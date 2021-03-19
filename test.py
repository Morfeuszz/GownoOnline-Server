import redis
import json

red = redis.Redis(host='localhost', port=6379, db=0)
pub = red.pubsub()

pub.subscribe('test2')

count = 0

for new_message in pub.listen():
    try:
        message = new_message['data'].decode("utf-8")
        json_temp = json.loads(message)
        print(json_temp)
    except Exception as e:
        print(e,"error test")
