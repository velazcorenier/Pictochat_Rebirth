from flask import jsonify, session
from dao.PostDAO import PostDAO
from handler import DictBuilder as Dict

# temporary
from dao.UserDAO import UserDAO
userDao = UserDAO()

dao = PostDAO()

###################### Main HANDLER ############################

def getAllPost():
    rows = dao.getAllPosts()
    if not rows:
        return jsonify(Error="No Message found"), 404
    result = []
    for row in rows:
        result.append(Dict.post_dict(row))
    return jsonify(Posts=result)

def getPostsByChatID(chat_id):
    chat_post_messages = dao.getPostsByChatID(chat_id)
    if not chat_post_messages:
        return jsonify(Error="No Messages Found")
    result_post_messages = []
    for row in chat_post_messages:
        result = Dict.post_msg_chat_dict_UI(row)
        result_post_messages.append(result)
    return jsonify(PostsInChat = result_post_messages)

def getPostsByChatIDForUI(chat_id):
    chat_post_messages = dao.getPostsByChatID(chat_id)
    result_post_messages = []
    for row in chat_post_messages:
        result_post_messages.append(Dict.post_msg_chat_dict_UI_2(row, getRepliesByPostIDForUI(row[1]),
                                                                 getUsersLikedByPostId(row[1]),
                                                                 getUsersDislikedByPostId(row[1])))
    return jsonify(PostsInChat = result_post_messages)

def createPost(form):
    # Assumes form contains post_msg, user_id, chat_id
    if form and len(form) == 3:
        post_msg = form['post_msg']
        post_date = 'now'
        user_id = session['user_id']
        chat_id = form['chat_id']

        if post_msg and post_date and user_id and chat_id:
            post_id = dao.createPost(post_msg, post_date, user_id, chat_id)

            result = {}
            result['post_id'] = post_id
            result['post_msg'] = post_msg
            result['post_date'] = post_date
            result['user_id'] = user_id
            result['chat_id'] = chat_id

            return jsonify(Post=result), 201
        else:
            return jsonify(Error='Malformed POST request'), 400
    else:
        return jsonify(Error='Malformed POST request'), 400


###################### Reaction HANDLER ############################

def reactPost(form):
    # Assumes form contains post_id, react_type
    if form and len(form) >= 2: # For Debugging
        # user_id = session['user_id'] //use when session is working
        user_id = form['user_id']
        post_id = form['post_id']
        react_date = 'now'
        react_type = form['react_type']

        if user_id and post_id and react_date and react_type:
            post_id = dao.reactPost(user_id, post_id, react_date, react_type)

            result = {}
            result['user_id'] = user_id
            result['post_id'] = post_id
            result['react_date'] = react_date
            result['react_type'] = react_type
            result['username'] = userDao.getUserCredentials(user_id)['username']

            return jsonify(React=result), 201
        else:
            return jsonify(Error='Malformed POST request'), 400
    else:
        return jsonify(Error='Malformed POST request'), 400


def getPostLikesCountByID(post_id):
    result = dao.getPostLikesCountByID(post_id)
    if not result:
        return jsonify(Error="No Like found"), 404
    map_result = dict()
    map_result["post_id"] = result[0][0]
    map_result["likes"] = result[0][1]
    return jsonify(PostLikes=map_result)


def getPostDislikesCountByID(post_id):
    result = dao.getPostDislikesCountByID(post_id)
    if not result:
        return jsonify(Error="No Dislike found"), 404
    map_result = dict()
    map_result["post_id"] = result[0][0]
    map_result["dislikes"] = result[0][1]
    return jsonify(PostDislikes=map_result)

def getUsersLikedByPostId(post_id):
    result = dao.getUsersLikedPostByID(post_id)
    if not result:
        return jsonify(Error="No users found"), 404
    return result
def getUsersDislikedByPostId(post_id):
    result = dao.getUsersDislikedPostByID(post_id)
    if not result:
        return jsonify(Error="No users found"), 404
    return result

###################### Reply HANDLER ############################


def getRepliesByPostID(post_id):
    replies_info = dao.getRepliesByPostID(post_id)
    if not replies_info:
        return jsonify(Error="No Replies Found"), 404
    result_replies = []
    for row in replies_info:
        result = Dict.reply_dict(row)
        result_replies.append(result)
    return jsonify(Replies=result_replies)

def getRepliesByPostIDForUI(post_id):
    replies_info = dao.getRepliesByPostID(post_id)
    result_replies = []
    for row in replies_info:
        result_replies.append(Dict.reply_dict(row))
    return result_replies

###################### Media HANDLER ############################

def insertMedia(form):
    # Assumes form contains post_id, media_type, location
    if form and len(form) == 3:
        post_id = form['post_id']
        media_type = 'now'
        location = form['location']

        if post_id and media_type and location:
            media_id = dao.insertMedia(post_id, media_type, location)

            result = {}
            result['media_id'] = media_id
            result['post_id'] = post_id
            result['media_type'] = media_type
            result['location'] = location

            return jsonify(React=result), 201
        else:
            return jsonify(Error='Malformed POST request'), 400
    else:
        return jsonify(Error='Malformed POST request'), 400

def getMediaByPostID(post_id):
    media_info = dao.getMediaByPostID(post_id)
    if not media_info:
        return jsonify(Error="No Messages Found"), 404
    result_media = []
    for row in media_info:
        result = Dict.media_dict(row)
        result_media.append(result)
    return jsonify(Media=result_media)

###################### Dashboard HANDLER ############################

def getTrendingHashtags():
    tophashtags = []
    hashtags = dao.getTrendingHashtags()
    for row in hashtags:
        result = Dict.dashboard_hashtag_dict(row)
        tophashtags.append(result)
    return jsonify(Hashtags=tophashtags)

def getPostPerDay():
    postsPerDay = dao.getPostPerDay()
    result_list = []

    for row in postsPerDay:
        result = Dict.post_per_day_dict(row)
        result_list.append(result)

    return jsonify(PostsPerDay=result_list)

def getRepliesPerDay():
    repliesPerDay = dao.getRepliesPerDay()
    return jsonify(RepliesPerDay=repliesPerDay)
