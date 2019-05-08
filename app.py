from flask import Flask, jsonify, request
from flask_cors import CORS
from handler import Chat
from handler import Post
from handler import User
from dao.PostDAO import PostDAO

postDao = PostDAO()


app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = True


@app.route('/Pictochat')  # OK
def homeforApp():
    return "Welcome to Pictochat"

###################### Users Routes ############################

@app.route('/Pictochat/users/register', methods=['GET, POST'])
def register():
    if request.method == 'POST':
        return User.registerUser(request.form)
    return jsonify(Error="Method not allowed."), 405

@app.route('/Pictochat/users/all', methods=['GET', 'POST'])
def getAllUsers():
    if request.method == 'GET':
        result = User.getAllUsers()
        return result
    elif request.method == 'POST':
        result = User.addUser(request.json)
        return result
    else:
         return jsonify(Error="Method not allowed"), 404

@app.route('/Pictochat/users/<int:user_id>', methods=['GET'])
def getUserByID(user_id):
    if request.method == 'GET':
        result = User.getUserInfo(user_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

@app.route('/Pictochat/users/username/<string:username>', methods=['GET'])
def getUserByUsername(username):
    if request.method == 'GET':
        result = User.getUserByUsername(username)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

@app.route('/Pictochat/post/<int:post_id>/likes', methods=['GET'])
def getUsersWhoLikedPost(post_id):
    if request.method == 'GET':
        result = User.getUsersWhoLikedPost(post_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/Pictochat/post/<int:post_id>/dislikes', methods=['GET'])
def getUsersWhoDislikedPost(post_id):
    if request.method == 'GET':
        result = User.getUsersWhoDislikedPost(post_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/Pictochat/chat/<int:chat_id>/users', methods=['GET'])
def getUsersByChatID(chat_id):
    if request.method == 'GET':
        result = User.getUsersByChatID(chat_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/Pictochat/chat/<int:chat_id>/admin', methods=['GET'])
def getAdminByChatID(chat_id):
    if request.method == 'GET':
        result = User.getAdminByChatID(chat_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

###################### Credential Routes ######################

@app.route('/Pictochat/credentials/all', methods=['GET'])
def getCredentials():
    if request.method == 'GET':
        result = User.getAllCredentials()
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/Pictochat/credentials/user/<int:user_id>', methods=['GET'])
def getUserCredentialByID(user_id):
    if request.method == 'GET':
        result = User.getUserCredentials(user_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

###################### Activity Routes ########################

@app.route('/Pictochat/activity/all', methods=['GET'])
def getAllActivities():
    if request.method == 'GET':
        result = User.getAllActivity()
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/Pictochat/activity/user/<int:user_id>', methods=['GET'])
def getUserActivityByID(user_id):
    if request.method == 'GET':
        result = User.getUserActivity(user_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

###################### Contacts Routes ######################

@app.route('/Pictochat/user/<int:user_id>/contacts', methods=['GET', 'POST'])
def getUserContactsByID(user_id):
    if request.method == 'GET':
        result = User.getUserContactsByID(user_id)
        return result
    elif request.method == 'POST':
        result = User.addContact(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

###################### Chat Routes ############################

@app.route('/Pictochat/chats/all', methods=['GET', 'POST'])
def getAllChats():
    if request.method == 'GET':
        result = Chat.getAllChats()
        return result
    elif request.method == 'POST':
        print('working')
        return Chat.insertChat(request.json)
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/Pictochat/chat/<int:chat_id>', methods=['GET'])
def getChatByID(chat_id):
    if request.method == 'GET':
        result = Chat.getChatByID(chat_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

@app.route('/Pictochat/chats/<int:user_id>', methods=['GET'])
def getChatByUserID(user_id):
    if request.method == 'GET':
        result = Chat.getChatByUserID(user_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/Pictochat/chat/<int:chat_id>/posts', methods=['GET', 'POST'])
def getPostsByChatID(chat_id):
    if request.method == 'GET':
        result = Post.getPostsByChatIDForUI(chat_id)
        return result
    elif request.method == 'POST':
        result = Post.insertMessage(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

###################### Post Routes ########################

@app.route('/Pictochat/posts/all', methods=['GET'])
def getAllPosts():
    if request.method == 'GET':
        result = Post.getAllPost()
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


###################### Hashtag Routes ######################



###################### Reaction Routes ############################

@app.route('/Pictochat/post/<int:post_id>/count/likes', methods=['GET'])
def getPostLikesCountByID(post_id):
    if request.method == 'GET':
        result = Post.getPostLikesCountByID(post_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/Pictochat/post/<int:post_id>/count/dislikes', methods=['GET'])
def getPostDislikesCountByID(post_id):
    if request.method == 'GET':
        result = Post.getPostDislikesCountByID(post_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

###################### Media Routes ######################

@app.route('/Pictochat/post/<int:post_id>/media', methods=['GET', 'POST'])
def getMediaByPostID(post_id):
    if request.method == 'GET':
        result = Post.getMediaByPostID(post_id)
        return result
    elif request.method == 'POST':
        result = Post.insertMedia(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

###################### Reply Routes ########################

@app.route('/Pictochat/post/<int:post_id>/replies', methods=['GET'])
def getRepliesByPostID(post_id):
    if request.method == 'GET':
        result = Post.getRepliesByPostID(post_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

###################### Dashboard Routes ########################


@app.route('/Pictochat/dashboard/hashtags', methods=['GET'])
def getTrendingHashtags():
    if request.method == 'GET':
        result = Post.getTrendingHashtags()
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

@app.route('/Pictochat/dashboard/posts', methods=['GET'])
def getPostPerDay():
    if request.method == 'GET':
        result = Post.getPostPerDay()
        return result
    else:
        return jsonify(Error="Method not allowed"), 404

@app.route('/Pictochat/dashboard/replies', methods=['GET'])
def getRepliesPerDay():
    if request.method == 'GET':
        result = postDao.getRepliesPerDay()
        return jsonify(RepliesPerDay=result)
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/Pictochat/dashboard/likes', methods=['GET'])
def getLikesPerDay():
    if request.method == 'GET':
        result = postDao.getLikesPerDay()
        return jsonify(LikesPerDay=result)
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/Pictochat/dashboard/dislikes', methods=['GET'])
def getDislikesPerDay():
    if request.method == 'GET':
        result = postDao.getDislikesPerDay()
        return jsonify(DislikesPerDay=result)
    else:
        return jsonify(Error="Method not allowed"), 404

@app.route('/Pictochat/dashboard/post/replies', methods=['GET'])
def getRepliesPerPost():
    if request.method == 'GET':
        result = postDao.getRepliesPerPost()
        return jsonify(RepliesPerPost=result)
    else:
        return jsonify(Error="Method not allowed"), 404

@app.route('/Pictochat/dashboard/post/likes', methods=['GET'])
def getLikesPerPost():
    if request.method == 'GET':
        result = postDao.getLikesPerPost()
        return jsonify(LikesPerPost=result)
    else:
        return jsonify(Error="Method not allowed"), 404


@app.route('/Pictochat/dashboard/post/dislikes', methods=['GET'])
def getDislikesPerPost():
    if request.method == 'GET':
        result = postDao.getDislikesPerPost()
        return jsonify(DislikesPerPost=result)
    else:
        return jsonify(Error="Method not allowed"), 404






if __name__ == '__main__':
    app.run()

