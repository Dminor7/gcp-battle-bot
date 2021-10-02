import os
import random
from flask import Flask, request


app = Flask(__name__)
moves = ['F', 'T', 'L', 'R']


def get_bot(all_data):
    bot = all_data['_links']['self']['href']
    bot_state = all_data["arena"]["state"][bot]

    return bot_state, bot



def get_command(bot_direction, bot_x, bot_y, arena_x, arena_y, all_user_data):
    if bot_direction == "N":
        if bot_y == 0:
            return "R"
        elif is_someone_present([bot_x], [bot_y-1, bot_y-2, bot_y-3], all_user_data):
            return "T"
        else:
            return "F"

    elif bot_direction == "S":
        if bot_y == arena_y - 1:
            return "R"
        elif is_someone_present([bot_x], [bot_y+1, bot_y+2, bot_y+3], all_user_data):
            return "T"
        else:
            return "F"

    elif bot_direction == "E":
        if bot_x == arena_x - 1:
            return "R"
        elif is_someone_present([bot_x+1, bot_x+2, bot_x+3], [bot_y], all_user_data):
            return "T"
        else:
            return "F"

    elif bot_direction == "W":
        if bot_x == 0:
            return "R"
        elif is_someone_present([bot_x-1, bot_x-2, bot_x-3], [bot_y], all_user_data):
            return "T"
        else:
            return "F"
    else:
        return moves[random.randrange(len(moves))]


def is_someone_present(possible_points_x, possible_points_y, all_user_data):
    for _, user_states in all_user_data.items():
        if user_states["x"] in possible_points_x and user_states["y"] in possible_points_y:
            return True
    else:
        return False


@app.route("/", methods=['POST'])
def move():
    request.get_data()
    bot_state, _ = get_bot(request.json)
    arena_x, arena_y = request.json["arena"]["dims"]
    return get_command(bot_state['direction'], bot_state['x'], bot_state['y'], arena_x, arena_y, request.json["arena"]["state"])


if __name__ == "__main__":
    app.run(host='0.0.0.0',port=int(os.environ.get('PORT', 8080)))