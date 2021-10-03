import os
import random
import logging
import json

from flask import Flask, request

logging.basicConfig(level=os.environ.get("LOGLEVEL", "INFO"))
logger = logging.getLogger(__name__)

app = Flask(__name__)

@app.route("/", methods=['POST'])
def move():

    stateInitial = json.loads(request.get_data(as_text=True))
    # print(stateInitial)

    state=stateInitial["arena"]["state"]

    state = dict(state)
    # print(state)

    #initialisation
    myLoc=[0,0]
    myURL=stateInitial["_links"]["self"]["href"]
    dimensions=stateInitial["arena"]["dims"]
    # print(dimensions)

    myLoc[0]=state[myURL]["x"]
    myLoc[1]=state[myURL]["y"]
    myDirection=state[myURL]["direction"]

    variable = next_move(stateInitial, state, myLoc, myDirection, myURL, dimensions)

    return variable

def next_move(stateInitial, state, myLoc, myDirection, myURL, dimensions):
    my_x = myLoc[0]
    my_y = myLoc[1]
    list_copy = state.copy()
    del list_copy[myURL]
    for i in list_copy.values():
        if(((myDirection=='N' and (my_y - i["y"] <= 3 and my_y - i["y"] > 0) and i["x"] == my_x) or \
           (myDirection=='S' and (i["y"] - my_y <= 3 and i["y"] - my_y > 0) and i["x"] == my_x) or \
           (myDirection=='W' and (my_x - i["x"] <= 3 and my_x - i["x"] > 0) and i["y"] == my_y) or \
           (myDirection=='E' and (i["x"] - my_x <= 3 and i["x"] - my_x > 0) and i["y"] == my_y))):
        
            return 'T'
        else:
            return random.choice(['F','L','R'])



if __name__ == "__main__":
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))