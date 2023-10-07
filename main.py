from flask import Flask, request, jsonify
from waitress import serve
import json
import logging
import getmsg
import notification
import argparse


app = Flask(__name__)


@app.route(args.path, methods=['POST', 'GET'])
def process_endpoint():
    # Try to get data from JSON body
    data = request.get_json(silent=True) or {}

    # If roomNumber is not in JSON body, get it from query parameters
    roomNumber = data.get('roomNumber') or request.args.get('roomNumber')

    if not roomNumber:
        return jsonify({"error": "roomNumbers required."}), 400

     # If bark is not in JSON body, get it from query parameters
    bark = data.get('bark') or request.args.get(
        'bark', default=False, type=bool)

    result = getmsg.get_msg(roomNumber)

    if bark:
        notification.send_bark(result)

    return jsonify({"roomNumber": roomNumber, "bark": bark, "result": result})


if __name__ == '__main__':
    # Read configuration from config.json
    with open('config.json', 'r') as config_file:
        config = json.load(config_file)

    parser = argparse.ArgumentParser(
        description="Start the backend on a given port.")
    parser.add_argument('--port', '-P', type=int, default=config.get('port',
                        5000), help="Port to run the backend on.")
    parser.add_argument('--host', '-H', type=str,
                        default=config.get('host', '127.0.0.1'), help="Binding IP.")
    parser.add_argument('--debug', '-D', action="store_true",
                        default=config.get('debug', False), help="Run in debug mode.")
    parser.add_argument('--path', '-p', type=str,
                        default=config.get('path', '/'), help="Path to run the backend on.")
    args = parser.parse_args()

    if args.debug:
        logging.basicConfig(level=logging.DEBUG)  # Set logging level
        app.run(debug=True, port=args.port, host=args.host)
    else:
        logging.basicConfig(level=logging.INFO)  # Set logging level
        serve(app, host=args.host, port=args.port)
