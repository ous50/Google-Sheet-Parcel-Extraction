from flask import Flask, request, jsonify
from waitress import serve
import json
import logging
import getmsg
import notification
import argparse

# Read configuration from config.json
with open('config.json', 'r') as config_file:
    config = json.load(config_file)


parser = argparse.ArgumentParser(
    description="Start the backend on a given port.")
parser.add_argument('--port', '-P', type=int, default=config.get('port',
                    5000), help="Port to run the backend on.")
parser.add_argument('--host', '-H', type=str,
                    default=config.get('host', '0.0.0.0'), help="Binding IP.")
parser.add_argument('--debug', '-D', type=bool,
                    default=config.get('debug', False), help="Run in debug mode.")
args = parser.parse_args()


app = Flask(__name__)


@app.route('/', methods=['POST', 'GET'])
def process_endpoint():
    data = request.get_json()
    roomNumber = data.get('roomNumber')
    if not roomNumber:
        return jsonify({"error": "roomNumbers required."}), 400
    bark = data.get('bark') or False

    result = getmsg.get_msg(roomNumber)

    if bark:
        notification.send_bark(result)

    return jsonify({"roomNumber": roomNumber, "bark": bark, "result": result})


if __name__ == '__main__':
    if args.debug:
        logging.basicConfig(level=logging.DEBUG)  # Set logging level
        app.run(debug=True, port=args.port, host=args.host)
    else:
        logging.basicConfig(level=logging.INFO)  # Set logging level
        serve(app, host=args.host, port=args.port)
