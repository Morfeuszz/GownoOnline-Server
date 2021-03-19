import os
from os import listdir
import json

data = {}

excluded = ['./asd\\not', './__pycache__']
paths = []
modules = []

def start():
    for folder in ([x[0] for x in os.walk(os.getcwd()) if x[0] not in excluded]):
        for f in ([fold for fold in os.listdir(folder)]):
            if f.endswith('.py'):
                p = (folder + '/' + f)
                paths.append(p)
                modules.append(p.split('/')[-1].split('.')[0])
                #print(p.replace('\\', '/').replace('//', '/'))
    makeJSON()

def makeJSON():
    data = {}
    index = 0
    for x in modules:
        data[x] = paths[index]
        index += 1
    #print(data)
    with open('testing.json', 'w')as j:
        j.write(json.dumps(data))
    print('done!')
start()