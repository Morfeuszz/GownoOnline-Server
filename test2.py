import redis
import json


red = redis.Redis(host='localhost', port=6379, db=0)



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


red.publish('test2', '2')

data = red.hgetall('55')

red.hmset('testhash', userData)
data = red.hgetall('54')
print(data["ID"])