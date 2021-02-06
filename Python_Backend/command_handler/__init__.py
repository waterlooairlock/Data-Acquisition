
from config import *
from flask import Flask, request, jsonify

# Create Flask App object
command_handler = Flask(__name__)
# Create Logger object for Flask app
api_logger = logging.get_logger("Command Handler")
command_handler.logger = logging.get_logger("Flask")


@command_handler.route("/", methods=['GET'])
def home():
    return '''<h1>Command Handler API</h1>
<p>The command handler API is running and ready for requests!</p>'''
