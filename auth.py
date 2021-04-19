from cryptography.fernet import Fernet
import asyncio
import json
import websockets
import mysql.connector
import redis
from uuid import uuid4



USERS = set()
with open('config.json', 'r') as f:
    config = json.load(f)
mydb = mysql.connector.connect(**config["mysql"])
cursor = mydb.cursor()
ip = config["ip"]
port = config["portAuth"]
key = config["encryptKey"]

red = redis.Redis(host='localhost', port=6379, db=0)

class methods:
    async def encrypt(password):
        password = password.encode()
        return Fernet(key).encrypt(password).decode()

    async def decrypt(password):
        password = password.encode()
        return Fernet(key).decrypt(password).decode()

    async def login(data,websocket):
        cursor.execute(f"SELECT id, username, password, familyName FROM users WHERE username = '{data['username']}'")
        result = cursor.fetchone()
        if(result):
            if(data["password"] == await methods.decrypt(result[2])):
                rand_token = uuid4()
                red.publish('newLogin', '{"ID" : "%s", "familyName" : "%s", "authToken" : "%s"}' % (result[0], result[3], rand_token))
                await websocket.send('{"action" : "login", "status" : "success", "ID" : "%s", "familyName" : "%s", "authToken" : "%s"}' % (result[0], result[3], rand_token))
            else:
                await websocket.send('{"action" : "login", "status" : "failed"}')
        else:
            await websocket.send('{"action" : "login", "status" : "failed"}')

    async def register(data,websocket):
        cursor.execute(f"SELECT id FROM users WHERE username = '{data['username']}'")
        result = cursor.fetchone()
        if(result == None):
            temp = await methods.encrypt(data['password'])
            cursor.execute(f'INSERT INTO users (Username, Password, mail) VALUES ("{data["username"]}", "{temp}", "{data["mail"]}")')
            mydb.commit()
            cursor.execute(f"SELECT id, familyName FROM users WHERE username = '{data['username']}'")
            result = cursor.fetchone()
            rand_token = uuid4()
            red.publish('newLogin', '{"ID" : "%s", "familyName" : "%s", "authToken" : "%s"}' % (result[0], result[1], rand_token))
            await websocket.send('{"action" : "register", "status" : "success", "ID" : "%s", "familyName" : "%s", "authToken" : "%s"}' % (result[0], result[1], rand_token))
        else:
            await websocket.send('{"action" : "register", "status" : "taken"}')
    
    async def getCharacters(data,websocket):
        cursor.execute(f"SELECT * FROM characters WHERE ownerID = '{data['ID']}'")
        result = cursor.fetchall()
        charactersList = []
        for characterData in result:
            character = {
                "ID" : characterData[0],
                "ownerID" : characterData[1],
                "Name" : characterData[2],
                "Level" : characterData[3],
                "Exp" : characterData[4],
                "Position" : characterData[5],
                "Appearance" : characterData[6]
            }
            charactersList.append(character)
        
        respons = {
            "action" : "getCharacters",
            "data" : charactersList
        }
        await websocket.send(json.dumps(respons))

    async def loadCharacterData(data,websocket):
        red.publish('loadCharacterData', json.dumps(data))

    async def createCharacter(data,websocket):
        cursor.execute(f"SELECT * FROM characters WHERE Name= '{data['Name']}'")
        result = cursor.fetchone()
        if(result):
            respons = {
                "action" : "createCharacter",
                "status" : "usernameTaken"
            }
            await websocket.send(json.dumps(respons))
        else:
            cursor.execute(f"INSERT INTO characters (Name, ownerID, Appearance) VALUES ('{data['Name']}','{data['ownerID']}','{data['Appearance']}')")
            mydb.commit()
            respons = {
                "action" : "createCharacter",
                "status" : "success"
            }
            await websocket.send(json.dumps(respons))


    
        

class auth:
    async def counter(websocket, path):
        USERS.add(websocket)
        try:
            async for message in websocket:
                try:
                    data = json.loads(message)
                    method = getattr(methods,data["action"])
                    await method(data,websocket)
                except KeyboardInterrupt:
                    await websocket.send('nope')
        finally:
            USERS.remove(websocket)


    start_server = websockets.serve(counter, ip, port)

    asyncio.get_event_loop().run_until_complete(start_server)
    asyncio.get_event_loop().run_forever()

