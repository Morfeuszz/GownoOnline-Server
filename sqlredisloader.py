import redis
import json
import sys
import mysql.connector


with open('config.json', 'r') as f:
    config = json.load(f)

mydb = mysql.connector.connect(**config["mysql"])
cursor = mydb.cursor()


red = redis.Redis(host='localhost', port=6379, db=0, decode_responses=True)
pub = red.pubsub()

pub.subscribe('newLogin')
pub.subscribe('loadCharacterData')
pub.subscribe('getInventoryData')
pub.subscribe('loadAllItems')

userData = {
    "ID" : 0,
    "familyName" : 0, 
    "authToken" : 0
}
characterData = {
    "ID" : 0,
    "ownerID" : 0,
    "name" : 0,
    "level" : 0,
    "exp" : 0,
    "position" : 0
}
inventoryData = {
    "ID" : 0,
    "slots" : 0,
    "money" : 0,
    "weight" : 0,
    "maxWeight" : 0,
    "data" : 0
}


for new_message in pub.listen():
    try:
        print(new_message)
        channel = new_message['channel']
        message = json.loads(new_message['data'])
        if(channel == "newLogin"):
            redis.Redis(db=0)
            if(not red.exists(message["ID"])):
                userData["ID"] =  message["ID"]
                userData["familyName"] = message["familyName"]
                userData["authToken"] = message["authToken"]
                red.hmset(str(userData["ID"]), userData)
                userData = {
                    "ID" : 0,
                    "familyName" : 0, 
                    "authToken" : 0
                }
        if(channel == "loadCharacterData"):
            redis.Redis(db=1)
            if(not red.exists(message["ID"])):
                cursor.execute(f"SELECT ID, ownerID, Name, Level, Exp, Position FROM characters WHERE ID = '{message['charID']}'")
                result = cursor.fetchone()
                characterData["ID"] = result[0]
                characterData["ownerID"] = result[1]            
                characterData["name"] = result[2]
                characterData["level"] = result[3]
                characterData["exp"] = result[4]
                characterData["position"] = result[5]
                red.hmset(str(characterData["ID"]), characterData)
                characterData = {
                   "ID" : 0,
                   "ownerID" : 0,
                   "name" : 0,
                   "level" : 0,
                   "exp" : 0,
                   "position" : 0
                }
                redis.Redis(db=2)            
                if(not red.exists(message["charID"])):
                    cursor.execute(f"SELECT characterID, slots, money, weight, maxWeight, data FROM inventory WHERE characterID = '{message['charID']}'")
                    inventoryData["ID"] = result[0]
                    inventoryData["slots"] = result[1]
                    inventoryData["data"] = result[2]
                    red.hmset(str(inventoryData["ID"]), inventoryData )
                    inventoryData = {
                        "ID" : 0,
                        "slots" : 0,
                        "money" : 0,
                        "weight" : 0,
                        "maxWeight" : 0,
                        "data" : 0
                    }
                    red.publish("loadCharacter", json.dumps(message))
                    
            if(channel == "loadAllItems"):
                redis.Redis(db=9)
                cursor.execute(f"SELECT * FROM items;")
                result = cursor.fetchall()
                for item in result:
                    itemsData["ID"] = item[0]
                    itemsData["Name"] = item[1]
                    itemsData["Stats"] = item[2]
                    itemsData["Weight"] = item[3]
                    red.hmset(str(itemsData["ID"]), itemsData)
                    itemsData = {
                        "ID" : 0,
                        "Name" : 0,
                        "Stats" : 0,
                        "Weight" : 0
                    }
    except Exception as e:
        print(e,"error")



