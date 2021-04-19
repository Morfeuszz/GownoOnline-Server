import threading
from subprocess import call

init = False
threads = []
modules = [
    "dispatcher",
    "auth"
]
functions = []

for module in modules:
    def new_module(module = module):
        print("Starting" + module + "...")
        call(["python3",module + ".py"])
    functions.append(new_module)

print(functions)

init = True
for f in functions:
    try:
        module = threading.Thread(target=f)
        threads.append(module)
        module.start()
        print("OK")
    except:
        print("ERROR")

