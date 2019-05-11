from flask import Flask, jsonify, request, session, flash
from flask_cors import CORS
from functools import wraps
from handler import Chat
from handler import Post
from handler import User
from dao.PostDAO import PostDAO
from dao.UserDAO import UserDAO

postDao = PostDAO()
userDao = UserDAO()

app = Flask(__name__)
CORS(app)

app.config['DEBUG'] = True
app.config['SECRET_KEY'] = 'pictochat'


# Check if user is logged in
def is_logged_in(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash('Unauthorized, please log in.', 'danger')
            return jsonify(Error="Unauthorized, please log in."), 404

    return wrap


@app.route('/Pictochat')  # OK
def homeforApp():
    return "Welcome to Pictochat"


###################### Users Routes ############################

@app.route('/Pictochat/users/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        return User.register(request.json)
    return jsonify(Error="Method not allowed."), 405


# Login
@app.route('/Pictochat/users/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        result = User.login(request.json)
        return result
    return jsonify(Error="Method not allowed."), 405


# Logout
@app.route('/Pictochat/users/logout')
# @is_logged_in
def logout():
    session.clear()
    flash("You are now logged out.", "success")
    return jsonify(LoggedOut='Logged out')


@app.route('/Pictochat/users/all', methods=['GET'])
def getAllUsers():
    if request.method == 'GET':
        result = User.getAllUsers()
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/users/logged', methods=['GET'])
def getAllUsersNotSession():
    if request.method == 'GET':
        result = User.getAllUsersNotSession()
        return result
    else:
        return jsonify(Error="Method not allowed"), 405

@app.route('/Pictochat/users/<int:user_id>', methods=['GET'])
def getUserByID(user_id):
    if request.method == 'GET':
        result = User.getUserInfo(user_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/users/username/<string:username>', methods=['GET'])
def getUserByUsername(username):
    if request.method == 'GET':
        result = User.getUserByUsername(username)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/post/<int:post_id>/likes', methods=['GET'])
def getUsersWhoLikedPost(post_id):
    if request.method == 'GET':
        result = User.getUsersWhoLikedPost(post_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/post/<int:post_id>/dislikes', methods=['GET'])
def getUsersWhoDislikedPost(post_id):
    if request.method == 'GET':
        result = User.getUsersWhoDislikedPost(post_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/chat/<int:chat_id>/users', methods=['GET'])
def getUsersByChatID(chat_id):
    if request.method == 'GET':
        result = User.getUsersByChatID(chat_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/chat/<int:chat_id>/admin', methods=['GET'])
def getAdminByChatID(chat_id):
    if request.method == 'GET':
        result = User.getAdminByChatID(chat_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


###################### Credential Routes ######################

@app.route('/Pictochat/credentials/all', methods=['GET'])
def getCredentials():
    if request.method == 'GET':
        result = User.getAllCredentials()
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/credentials/user/<int:user_id>', methods=['GET'])
def getUserCredentialByID(user_id):
    if request.method == 'GET':
        result = User.getUserCredentials(user_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


###################### Activity Routes ########################

@app.route('/Pictochat/activity/all', methods=['GET'])
def getAllActivities():
    if request.method == 'GET':
        result = User.getAllActivity()
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/activity/user/<int:user_id>', methods=['GET'])
def getUserActivityByID(user_id):
    if request.method == 'GET':
        result = User.getUserActivity(user_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


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
        return jsonify(Error="Method not allowed"), 405


###################### Chat Routes ############################

@app.route('/Pictochat/chats/new', methods=['GET', 'POST'])
# @is_logged_in
def createChat():
    if request.method == 'POST':
        User.registerActivity()
        return Chat.createChat(request.json)
    return jsonify(Error="Method not allowed."), 405


@app.route('/Pictochat/chats/all', methods=['GET', 'POST'])
def getAllChats():
    if request.method == 'GET':
        result = Chat.getAllChats()
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/chat/<int:chat_id>', methods=['GET'])
def getChatByID(chat_id):
    if request.method == 'GET':
        result = Chat.getChatByID(chat_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/chats/<int:user_id>', methods=['GET'])
def getChatByUserID(user_id):
    if request.method == 'GET':
        result = Chat.getChatByUserID(user_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/chat/<int:chat_id>/posts', methods=['GET', 'POST'])
def getPostsByChatID(chat_id):
    if request.method == 'GET':
        result = Post.getPostsByChatIDForUI(chat_id)
        return result
    elif request.method == 'POST':
        result = Post.insertMessage(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


###################### Post Routes ########################

@app.route('/Pictochat/post/new', methods=['GET', 'POST'])
# @is_logged_in
def createPost():
    if request.method == 'POST':
        # User.registerActivity()
        return Post.createPost(request.json)
    return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/posts/all', methods=['GET'])
def getAllPosts():
    if request.method == 'GET':
        result = Post.getAllPost()
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


###################### Hashtag Routes ######################


###################### Reaction Routes ############################

@app.route('/Pictochat/post/react', methods=['GET', 'POST'])
# @is_logged_in
def reactPost():
    if request.method == 'POST':
        # User.registerActivity()
        result = Post.reactPost(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/post/<int:post_id>/count/likes', methods=['GET'])
def getPostLikesCountByID(post_id):
    if request.method == 'GET':
        result = Post.getPostLikesCountByID(post_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/post/<int:post_id>/count/dislikes', methods=['GET'])
def getPostDislikesCountByID(post_id):
    if request.method == 'GET':
        result = Post.getPostDislikesCountByID(post_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405

###################### Participant Routes ######################

@app.route('/Pictochat/chat/addparticipants', methods=['GET', 'POST'])
@is_logged_in
def addParticipants():
    if request.method == 'POST':
        result = Chat.addParticipants(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405

###################### Media Routes ######################

@app.route('/Pictochat/post/insertmedia', methods=['GET', 'POST'])
@is_logged_in
def insertMedia():
    if request.method == 'POST':
        result = Post.insertMedia(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405

@app.route('/Pictochat/post/<int:post_id>/media', methods=['GET', 'POST'])
def getMediaByPostID(post_id):
    if request.method == 'GET':
        result = Post.getMediaByPostID(post_id)
        return result
    elif request.method == 'POST':
        result = Post.insertMedia(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


###################### Reply Routes ########################

@app.route('/Pictochat/post/reply', methods=['GET', 'POST'])
# @is_logged_in
def reply():
    if request.method == 'POST':
        # User.registerActivity()
        result = Post.reply(request.json)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405

@app.route('/Pictochat/post/<int:post_id>/replies', methods=['GET'])
def getRepliesByPostID(post_id):
    if request.method == 'GET':
        result = Post.getRepliesByPostID(post_id)
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


###################### Dashboard Routes ########################


@app.route('/Pictochat/dashboard/hashtags', methods=['GET'])
def getTrendingHashtags():
    if request.method == 'GET':
        result = Post.getTrendingHashtags()
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/dashboard/posts', methods=['GET'])
def getPostPerDay():
    if request.method == 'GET':
        result = Post.getPostPerDay()
        return result
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/dashboard/replies', methods=['GET'])
def getRepliesPerDay():
    if request.method == 'GET':
        result = postDao.getRepliesPerDay()
        return jsonify(RepliesPerDay=result)
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/dashboard/likes', methods=['GET'])
def getLikesPerDay():
    if request.method == 'GET':
        result = postDao.getLikesPerDay()
        return jsonify(LikesPerDay=result)
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/dashboard/dislikes', methods=['GET'])
def getDislikesPerDay():
    if request.method == 'GET':
        result = postDao.getDislikesPerDay()
        return jsonify(DislikesPerDay=result)
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/dashboard/post/replies', methods=['GET'])
def getRepliesPerPost():
    if request.method == 'GET':
        result = postDao.getRepliesPerPost()
        return jsonify(RepliesPerPost=result)
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/dashboard/post/likes', methods=['GET'])
def getLikesPerPost():
    if request.method == 'GET':
        result = postDao.getLikesPerPost()
        return jsonify(LikesPerPost=result)
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/dashboard/post/dislikes', methods=['GET'])
def getDislikesPerPost():
    if request.method == 'GET':
        result = postDao.getDislikesPerPost()
        return jsonify(DislikesPerPost=result)
    else:
        return jsonify(Error="Method not allowed"), 405


@app.route('/Pictochat/dashboard/user/active', methods=['GET'])
def getTopThreeActiveUsers():
    if request.method == 'GET':
        result = userDao.getTopThreeActiveUsers()
        return jsonify(TopThreeActiveUsers=result)
    else:
        return jsonify(Error="Method not allowed"), 405


if __name__ == '__main__':
    app.run('localhost')
