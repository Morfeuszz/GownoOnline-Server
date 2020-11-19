import asyncio
import json
import logging
import websockets
import datetime
import mysql.connector
import Functions
import time
import cProfile

with open('config.json', 'r') as f:
    config = json.load(f)

logging.basicConfig()

USERS = set()                               #all conntected users

posvars = {"ID": "0", "posX": "0","posY": "0", "spawnID": "0"}
message = ""
takenID = []
websocketID = Functions.idSocketConv.websocketID
IDwebsocket = Functions.idSocketConv.IDwebsocket

async def sendChatMessage(websocket,message):
    if len(USERS) > 1:
        await asyncio.wait([user.send(message) for user in USERS if user != websocket])

async def notifyConnection(websocket):
    if USERS:   
        message = '{"action" : "newPlayer", "ID" : ' + str(websocketID[websocket]) + '}'
        await asyncio.wait([user.send(message)  for user in USERS])

async def notifySelf(websocket):
    for x in takenID:
        if str(x) != websocketID[websocket]:
            await websocket.send('{"action" : "newPlayer", "ID" : ' + str(x) + '}')
            
async def notifyDisconnection(websocket):
    if USERS:
        message = '{"action" : "disconnect", "ID" : ' + str(websocketID[websocket]) + '}'
        await asyncio.wait([user.send(message) for user in USERS])

async def updatePosition(websocket,message,data):
    if len(USERS) > 0:
        idList = Functions.map_grid.usersInGrid(int(data["grid"]["x"]),int(data["grid"]["y"]))
        usersList = set()
        for x in idList:
            usersList.add(IDwebsocket[str(x)])
        if len(usersList) > 1:
            await asyncio.wait([user.send(message) for user in usersList if user != websocket])



async def register(websocket):
    await notifySelf(websocket)
    await notifyConnection(websocket)
    USERS.add(websocket)
    print(USERS)
    

async def unregister(websocket):
    await notifyDisconnection(websocket)
    removeID(websocket)
    USERS.remove(websocket)
    

async def requestID(websocket):
    await websocket.send('{"action" : "requestID"}')

       

def removeID(websocket):
    ID = websocketID[websocket]
    print(websocketID[websocket])
    Functions.map_grid.disconnectedID.add(int(ID))
    websocketID.pop(websocket)
    IDwebsocket.pop(ID)
    takenID.remove(int(ID))


async def counter(websocket, path):
    print("conntectd")
    await requestID(websocket)
    try:
        async for message in websocket:
            data = json.loads(message)
            print(message)
            if data["action"] == "playerInfo":
                await updatePosition(websocket,message,data)
            if data["action"] == "giveID":
                takenID.append(data["ID"])
                print(takenID)
                Functions.idSocketConv.addNewID(websocket,str(data["ID"]))
                if(data["ID"] in Functions.map_grid.disconnectedID):
                    Functions.map_grid.disconnectedID.remove(data["ID"])
                await register(websocket)
            if data["action"] == "chatMessage":
                await sendChatMessage(websocket,message)
            if data["action"] == "ping":
                await websocket.send('{"action" : "pong"}')
            if data["action"] == "mapGrid":
                if data["add"] == True:
                    Functions.map_grid.addToGrid(int(data["cords"]["x"]),int(data["cords"]["y"]),data["ID"])
                else:
                    Functions.map_grid.changeToGrid(int(data["cords"]["x"]),int(data["cords"]["y"]),int(data["cordsOld"]["x"]),int(data["cordsOld"]["y"]),data["ID"])
            if data["action"] == "debug":
                result = getattr(Functions.debug, data["command"])(data)
            else:
                pass      
    finally:
        if(websocket in USERS):
            await unregister(websocket)
        print("disconnected")

ip = config["ip"]
port = config["port"]
print("Server starting on " + ip + ":" + str(port))

start_server = websockets.serve(counter, ip, port)

asyncio.get_event_loop().run_until_complete(
     asyncio.gather(start_server,
                   Functions.clock.clock())
    )
asyncio.get_event_loop().run_forever()