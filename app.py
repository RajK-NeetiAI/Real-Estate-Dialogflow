import os

from flask import Flask, render_template, send_from_directory, jsonify, request

from utils import format_dialogflow_response
from action import *

app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return send_from_directory(os.path.join(app.root_path, 'static', 'images'),
                               'favicon.png', mimetype='image/png')


@app.route("/")
def home():
    return render_template("index.html")


@app.route('/dialogflow', methods=['POST'])
def dialogflow():
    body = request.get_json()
    action = body['queryResult']['action']
    response_data = {}

    if action == 'userProvidesPropertyType':
        response_data = handle_user_provides_property_type(body)
    elif action == 'userProvidesPropertyName':
        response_data = handle_user_provides_property_name(body)
    elif action == 'userAsksForFacilities':
        response_data = handle_user_asks_for_facilities(body)
    elif action == 'userSearchesByLocation':
        response_data = handle_user_searches_by_location(body)
    else:
        response_data = format_dialogflow_response([
            f'No handler is set for the action - {action}.'
        ])

    print(response_data)

    return jsonify(response_data)


if __name__ == '__main__':
    app.run(debug=True)
