from flask import Flask, render_template
from schema import get_schema, Day

import threading
import time


app = Flask(__name__)
running = True
schema: list[Day] | None = None

UPDATE_TIME_MIN = 25

# # # # # #
#  SCHEMA #
# # # # # #
def update_schema():
    global schema
    
    last_time = time.time()
    while running:
        time.sleep(1)

        if time.time() - last_time < (UPDATE_TIME_MIN * 60):
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
    if not schema:
        schema = get_schema()
    return render_template("home/index.html", schema=schema)


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)#, debug=True)
    # app.run(host="::1", port=5000)#, debug=True)
    running = False
    thread.join()
