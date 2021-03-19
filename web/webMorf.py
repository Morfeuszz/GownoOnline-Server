from flask import Flask, jsonify, request, render_template
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
    return render_template('admin.html')

app.run("0.0.0.0", 5000)
