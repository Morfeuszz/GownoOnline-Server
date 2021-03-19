import redis
import json
import websockets
import asyncio
import asyncio_redis
import time

red2 = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

with open('config.json', 'r') as f:
    config = json.load(f)


#pub = red.pubsub()
#pub.subscribe("websocket")

IDwebsocket = {}

red = ""

async def startRedis():
    global red
    red = await asyncio_redis.Connection.create(host='localhost',port=6379, db=0)
    pub = await red.start_subscribe()
    await pub.subscribe(["websocket"])
    await pubsub(pub)



async def auth(websocket):
    global red2
    try:
        await websocket.send('{"action" : "requestToken"}')
        message = await websocket.recv()
        print(message)
        data = json.loads(message)
        token = red2.hget(str(data["ID"]), "authToken")
        if(data["authToken"] == data["authToken"]):
            toAdd = {data["ID"] : websocket}
            IDwebsocket.update(toAdd)
            await websocket.send('{"action" : "tokenSuccess"}')
            return
        else:
            await websocket.send("wypierdalaj, zly token")
            await websocket.close()
    except Exception as e:
        print(e,"error")
        await websocket.send("nope")
        await websocket.close()



async def counter(websocket, path):
    global red
    try:
        await auth(websocket)
        async for message in websocket:
            print(message)
            data = json.loads(message)
            red2.publish(data["action"],message)
    finally:
        IDwebsocket.pop(list(IDwebsocket.keys())[list(IDwebsocket.values()).index(websocket)])

async def pubsub(pub):
    while True: 
        new_message = await pub.next_published()
        try:
            message = new_message.value
            data = json.loads(message)
            for target in data["target"]:
                print(target)
                print(IDwebsocket)
                await IDwebsocket[str(target)].send(json.dumps(data["message"]))
        except Exception as e:
            print(e,"error pubsub")






ip = config["ip"]
port = config["port"]
print("Server starting on " + ip + ":" + str(port))

start_server = websockets.serve(counter, ip, port)

asyncio.get_event_loop().run_until_complete(
     asyncio.gather(start_server,
                   startRedis())
    )
asyncio.get_event_loop().run_forever()