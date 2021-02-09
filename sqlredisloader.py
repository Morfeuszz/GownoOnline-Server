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
    "position" : 0,
}


for new_message in pub.listen():
    try:
        channel = new_message['channel']
        message = json.loads(new_message['data']
        if(channel == "newLogin"):
            userData["ID"] =  message["ID"]
            userData["familyName"] = message["familyName"]
            userData["authToken"] = message["authToken"]
            redis.Redis(db=0)
            red.hmset(str(userData["ID"]), userData)
            userData = {
                "ID" : 0,
                "familyName" : 0, 
                "authToken" : 0
            }
        if(channel == "loadCharacterData"):
            cursor.execute(f"SELECT ID, ownerID, Name, Level, Exp, Position FROM characters WHERE ID = '{message['charID']}'")
            result = cursor.fetchone()
            characterData["ID"] = result[0]
            characterData["ownerID"] = result[1]            
            characterData["name"] = result[2]
            characterData["level"] = result[3]
            characterData["exp"] = result[4]
            characterData["position"] = result[5]
            redis.Redis(db=1)
            red.hmset(str(characterData["ID"]), characterData)
            red.publish("loadCharacter", json.dumps(message))
            characterData = {
               "ID" : 0,
               "ownerID" : 0,
               "name" : 0,
               "level" : 0,
               "exp" : 0,
               "position" : 0,
            }

    except Exception as e:
        print(e,"error")



