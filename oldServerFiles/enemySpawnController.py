import mysql.connector
import json
import time
import enemyController

with open('config.json', 'r') as f:
    config = json.load(f)

mydb = mysql.connector.connect(**config["mysql"])
cursor = mydb.cursor()

class Spawner:
    def __init__(self, enemyID, spawnID, timeKilled, respawnTime, x, y, z):
        self.enemyID = enemyID
        self.spawnID = spawnID
        self.alive = False
        self.timeKilled = timeKilled
        self.respawnTime = respawnTime
        self.x = x
        self.y = y
        self.z = z
spawnerList = [None]

def Initialize():
    cursor.execute("SELECT * FROM enemySpawners;")
    row_headers=[x[0] for x in cursor.description]
    result = cursor.fetchall()
    json_data=[]
    for rv in result:
        json_data.append(dict(zip(row_headers,rv)))
    for x in result:
        json_temp = json_data[0]
        spawnerList.append(Spawner(json_temp["enemyID"],json_temp["ID"],0,json_temp["respawnTime"],json_temp["X"],json_temp["Y"],json_temp["Z"]))
Initialize()

def killEnemy(ID):
    enemy = spawnerList[ID]
    enemy.alive = False
    enemy.timeKilled = time.time()

def respawn():
    for spawner in spawnerList:
        if spawner == None:
            pass
        elif spawner.alive == False:
            if time.time() - spawner.timeKilled > spawner.respawnTime:
                enemyController.spawn(spawner)
                spawner.alive = True

