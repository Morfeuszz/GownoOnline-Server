import redis
import json


red = redis.Redis(host='localhost', port=6379, db=1)



userData = {
    "ID" : 1,
    "charID" : 1,
    "familyName" : "Morfeusz", 
    "name" : "Morfeusz232",
    "level" : 10,
    "exp" : 420,
    "position" : "0.3,0,1.5",
    "authToken" : "asfgfoiewuyfeui32if"
}



newPositions = { 34 : "sdsdsdsdd", 66 : "4545454",35 : "sdsdsdsdd", 68 : "4545454"}
target = set()
target.add(34)
target.add(68)

posMessageID = [position for position in newPositions if position in target]
posMessage = [newPositions[message] for message in posMessageID]
print(posMessage)


#red.publish('test', '2')

