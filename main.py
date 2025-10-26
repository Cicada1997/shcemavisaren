from flask import Flask, render_template
from schema import get_schema

import threading
import time


app = Flask(__name__)
running = True
schema = None

# # # # # #
#  SCHEMA #
# # # # # #
def update_schema():
    global schema
    
    last_time = time.time()
    while running:
        time.sleep(1)

        if time.time() - last_time < (5 * 60):
            continue

        last_time = time.time()
        schema = get_schema()


thread = threading.Thread(target=update_schema)
thread.start()


# # # # # #
#  ROUTES #
# # # # # #
@app.route("/")
def home():
    global schema
    if schema is None:
        schema = get_schema()
    return render_template("home/index.html", schema=schema)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=1997) #, debug=True)
    running = False
    thread.join()
