from flask import Flask, jsonify, request
import json
import requests
import os
import psutil
import subprocess
#import handlers.generateWeb
import handlers.getModules
app = Flask(__name__)
handlers.getModules.start()


self_generated = ''
def reload():
    handlers.getModules.start()


@app.route("/", methods=['GET', 'POST'])
def dashboard():
    self_generated = ''
    handlers.getModules.start()
    j = requests.get("http://127.0.0.1:5000/modules").json()
    def getPid(name):
        name = name + '.py'
        print(name)
        pid = None
        for p in psutil.pids():
            if name in psutil.Process(p).cmdline():
                return p
    def start(name, path):
        path = path.rstrip('/web.py') + '/' + name + '.py'
        print('start %s & %s' % (name, path))
        subprocess.run(['python3', path])
    def kill(name):
        print('kill %s' % name)
        os.system('sudo kill -9 %s' % getPid(name))
    s = len(j)
    for module in j.keys():
        name = module
        path = j[f'{name}']
        sAmount = f"Running Services: {s}<br>"
        #self_generated += f'<b>{name}: </b> Status: {status} <input type="submit" name="{name}" value="start" <input type="submit" name="{name}" value="kill"><br>'
        #self_generated += f'<form method="post" action="/"> <b>{name}: </b> Status: {status} <input type="submit" name="start" value="{name}"><br>'
        self_generated += f'<form method="post" action="/"> <b>{name}: </b> Status: Online <input type="submit" name="{name}" value="start"><input type="submit" name="{name}" value="kill"><br>'
    html_content = f"""    
    <html>
        <title>Modules</title>
        <body>
            <h1><center>
            Modules Dashboard<br>
            Available modules: {sAmount}
            </center></h1>
            <center><p1>
            {self_generated}
            </p1></center>
        </body>
    </html>
    """
    
    try:
        if request.method == 'POST':
            for k, v in request.form.items():
                if 'start' in v:
                    start(k, path)
                elif 'kill' in v:
                    kill(k)
        return html_content
    except Exception as e:
        print('err ' + str(e))

@app.route("/servers")
def web():
    j = requests.get("http://127.0.0.1:5000/servers.json").json()
    self_generated = ""
    s = len(j["serviceList"])
    print(s)
    for service in j["serviceList"]:
        name = service["name"]
        ip = service["ip"] + ":" + str(service["port"])
        status = service["status"]
        s_amount = f"Running Services: {s}<br>"
        self_generated += f"<b>{name}: </b> Status: {status} IP: {ip}<br>"
    html_content = f"""    
    <html>
        <title>Services Status</title>
        <body>
            <h1><center>
            Services Status<br>
            {s_amount}
            </center></h1>
            <center><p1>
            {self_generated}
            </p1></center>
        </body>
    </html>
    """
    return html_content

@app.route("/status")
def status():
    return jsonify ({
        "status": 200
    })

@app.route("/servers.json")
def file():
    url = "./servers.json"
    data = json.load(open(url))
    return jsonify (data)

@app.route("/modules")
def file1():
    url = "./testing.json"
    data = json.load(open(url))
    return jsonify (data)

app.run("0.0.0.0", 5000)
