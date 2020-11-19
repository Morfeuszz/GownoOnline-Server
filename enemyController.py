import mysql.connector
import json
import time

with open('config.json', 'r') as f:
    config = json.load(f)

mydb = mysql.connector.connect(**config["mysql"])
cursor = mydb.cursor()

enemyList = [None]
aliveList = {}


class Enemy():
    def __init__(self, ID, Name, HP, ATK):
        self.ID = ID
        self.Name = Name
        self.MaxHP = HP
        self.HP = HP
        self.ATK = ATK
    
    def position(self, x, y, z):
        posX = x
        posY = y
        posZ = z
    playerAggro = 0


def getEnemyList():
    cursor.execute("SELECT * FROM enemies;")
    row_headers=[x[0] for x in cursor.description]
    result = cursor.fetchall()
    json_data=[]
    for rv in result:
        json_data.append(dict(zip(row_headers,rv)))
    for x in result:
        json_temp = json_data[0]
        enemyList.append(Enemy(json_temp["ID"],json_temp["Name"],json_temp["HP"],json_temp["ATK"]))
getEnemyList()

def spawn(spawner):
    newEnemy = enemyList[int(spawner.enemyID)]
    newEnemy.position(spawner.x, spawner.y, spawner.z)
    toAdd = { spawner.spawnID : newEnemy}
    aliveList.update(toAdd)
    

    



    
        