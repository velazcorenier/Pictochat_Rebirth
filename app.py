from flask import Flask, jsonify, request
from flask_cors import CORS
from handler import Chat
from handler import Post
from handler import User

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = True


@app.route('/Pictochat')  # OK
def homeforApp():
    return "Welcome to Pictochat"

###################### Users Routes ############################

@app.route('/Pictochat/users/post/reaction/liked/<int:post_id>', methods=['GET'])
def getUsersWhoLikedPost(post_id):
    if request.method == 'GET':
        result = User.getUsersWhoLikedPost(post_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/Pictochat/users/post/reaction/disliked/<int:post_id>', methods=['GET'])
def getUsersWhoDislikedPost(post_id):
    if request.method == 'GET':
        result = User.getUsersWhoDislikedPost(post_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

###################### Credential Routes ######################

###################### Activity Routes ########################

###################### Credential Routes ######################

###################### Chat Routes ############################

###################### Participant Routes ######################

###################### Post Routes ########################

@app.route('/Pictochat/post/messages', methods=['GET'])
def getAllPostMessages():
    if request.method == 'GET':
        result = Post.getAllPostMessages()
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

###################### Hashtag Routes ######################

###################### Reaction Routes ############################

@app.route('/Pictochat/reaction/likes/count/post/<int:post_id>', methods=['GET'])
def getPostLikesCountByID(post_id):
    if request.method == 'GET':
        result = Post.getPostLikesCountByID(post_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/Pictochat/reaction/dislikes/count/post/<int:post_id>', methods=['GET'])
def getPostDislikesCountByID(post_id):
    if request.method == 'GET':
        result = Post.getPostDislikesCountByID(post_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

###################### Media Routes ######################

###################### Reply Routes ########################


if __name__ == '__main__':
    app.run()

