import redis
import json

red = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

pub = red.pubsub()


pub.subscribe('loadCharacter')

for new_message in pub.listen():
    try:
        message = json.loads(new_message['data'])
        redis.Redis(db=1)
        characterData  = red.hgetall(message["charID"])
        redis.Redis(db=2)
        inventoryData = red.hgetall(message["charID"])

        if(message["ID"] == int(characterData["ownerID"])):
            respons = {
                "target" : [message["ID"]],
                "message" : {
                    "action" : "loadCharacter",
                    "ID" : message["ID"],
                    "characterData" : characterData,
                    "inventoryData" : inventoryData
                }
            }
            red.publish("websocket", json.dumps(respons))
        else:
            pass
        


    except Exception as e:
        print(e,"error")
        