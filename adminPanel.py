from flask import Flask, jsonify
import json
import requests

j = requests.get("http://127.0.0.1/file.json").json()
app = Flask(__name__)
@app.route("/")
def web():
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

app.run("0.0.0.0", 5000)