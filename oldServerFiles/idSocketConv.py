websocketID = {}
IDwebsocket = {}


def addNewID(websocket,ID):
    toAdd = {websocket : ID}
    websocketID.update(toAdd)
    toAdd = {ID : websocket}
    IDwebsocket.update(toAdd)
