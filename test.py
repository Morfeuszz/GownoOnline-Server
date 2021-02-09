import redis
import json

red = redis.Redis(host='localhost', port=6379, db=0)
pub = red.pubsub()

pub.subscribe('test')

count = 0

for new_message in pub.listen():
    try:
        message = new_message['data'].decode("utf-8")
        json_temp = json.loads(message)
        respons = {
            "target" : [json_temp["ID"]],
            "message" : message
        }
        red.publish("websocket", json.dumps(respons))
    except Exception as e:
        print(e,"error test")
