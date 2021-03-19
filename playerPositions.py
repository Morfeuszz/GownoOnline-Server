import asyncio
import redis
import asyncio_redis
import json
import time
import math
from itertools import product
import random

tickrate = 50
grid_size = 50 
map_size = 1000
grid = [ [ set() for y in range(int(map_size/grid_size)) ] for x in range(int(map_size/grid_size))]

newPositions = {}
doneID = set()

red = ""

red2 = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)

async def startRedis():
    global red
    red = await asyncio_redis.Connection.create(host='localhost',port=6379, db=1)
    pub = await red.start_subscribe()
    await pub.subscribe(["position"])
    await pubsub(pub)

async def clock():
    startTime = time.time()
    while True:
        #if(time.time() - startTime >= 1/tickrate):
        await asyncio.sleep(1/tickrate)
        #print(time.time()-startTime)
        startTime = time.time()
            
        #await test()
        
        await sendPositions()
 
            
            

async def sendPositions():
    global grid, newPositions
    for y in range(int(map_size/grid_size)):
        for x in range(int(map_size/grid_size)):
            if(len(grid[y][x]) > 0):
                target = set()
                for id in grid[y][x]:
                    target.add(id)
                for cords in list(neighbours((y,x))):
                    temp = grid[cords[0]][cords[1]]
                    if(len(temp) > 0):
                        for id in temp:
                            target.add(id)
                posMessageID = [position for position in newPositions if position in target]
                posMessage = [newPositions[message] for message in posMessageID]
                if(posMessage):
                    respons = {
                        "target" : list(target),
                        "message" : {
                            "action" : "updatePositions",
                            "positions" : posMessage 
                            }
                    }
                    red2.publish("websocket", json.dumps(respons))
                       
    newPositions = {}                    
    #grid = [ [ set() for y in range(int(map_size/grid_size)) ] for x in range(int(map_size/grid_size))]

async def pubsub(pub):
    while True: 
            new_message = await pub.next_published()
            try:
                message = new_message.value
                data = json.loads(message)
                grid[math.floor(data["position"]["x"]/grid_size)][math.floor(data["position"]["z"]/grid_size)].add(data["ID"])
                tempData = {
                    "ID" : data["ID"],
                    "position" : data["position"],
                    "rotation" : data["rotation"],
                    "velocity" : data["velocity"]

                }
                newPositions[data["ID"]] = json.dumps(tempData)
                #print(newPositions)
                #print(grid)
            except Exception as e:
                print(e,"error pubsub")



def neighbours(cell):
    for c in product(*(range(n-1, n+2) for n in cell)):
        if c != cell and all(0 <= n < len(grid) for n in c):
            yield c


asyncio.get_event_loop().run_until_complete(
     asyncio.gather(clock(),
                   startRedis())
    )
asyncio.get_event_loop().run_forever()





async def test():
    for y in range(int(map_size/grid_size)):
        for x in range(int(map_size/grid_size)):
            grid[y][x].add(random.random())
            grid[y][x].add(random.random())
            grid[y][x].add(random.random())
            grid[y][x].add(random.random())
            grid[y][x].add(random.random())
            grid[y][x].add(random.random())
            grid[y][x].add(random.random())
            grid[y][x].add(random.random())
            grid[y][x].add(random.random())
            grid[y][x].add(random.random())