from flask import Flask, jsonify, request
from flask_cors import CORS
from handler import Chat
from handler import Post
from handler import User

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = True


@app.route('/')  # OK
def home():
    return "Welcome to Pictochat!"


@app.route('/Pictochat/')  # OK
def homeforApp():
    return "Welcome to Pictochat"

###################### User Routes ############################

###################### Credential Routes ######################

###################### Activity Routes ########################

###################### Credential Routes ######################

###################### Chat Routes ############################

###################### Participant Routes ######################

###################### Post Routes ########################

###################### Hashtag Routes ######################

###################### React Routes ############################

###################### Media Routes ######################

###################### Reply Routes ########################


if __name__ == '__main__':
    app.run()
