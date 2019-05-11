from flask import jsonify, session
from dao.PostDAO import PostDAO
from handler import DictBuilder as Dict

# For file saving
import os
from werkzeug.utils import secure_filename

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
    return jsonify(PostsInChat=result_post_messages)


def getPostsByChatIDForUI(chat_id):
    chat_post_messages = dao.getPostsByChatID(chat_id)
    result_post_messages = []
    for row in chat_post_messages:
        result_post_messages.append(Dict.post_msg_chat_dict_UI_2(row, getRepliesByPostIDForUI(row[1])))
    return jsonify(PostsInChat=result_post_messages)



def createPost(form, file, path):
    # Assumes form contains post_msg, user_id, chat_id
    if form and file and len(form) == 3:
        post_msg = form['post_msg']
        post_date = 'now'
        user_id = session['user_id']
        chat_id = form['chat_id']

        if post_msg and post_date and user_id and chat_id:
            post = dao.createPost(post_msg, post_date, user_id, chat_id)
            post_id, post_date = post['post_id'], post['post_date']

            # Register Hashtags
            insertHashtag(post_msg, post_id)

            # Upload file
            file_secure_name = secure_filename(file.filename)
            file_path = os.path.join(path, file_secure_name)
            file.save(os.path.join(os.getcwd(), file_path[1:]))

            # Register in Media table
            media = insertMedia(post_id, 'P', file_path)

            result = {}
            # result['post_id'] = post_id
            # result['post_msg'] = post_msg
            # result['post_date'] = post_date
            # result['user_id'] = user_id
            # result['chat_id'] = chat_id
            result['chatId'] = chat_id
            result['postID'] = post_id
            result['createdById'] = user_id
            result['username'] = userDao.getUserCredentials(user_id)['username']
            result['postMsg'] = post_msg
            result['postDate'] = post_date
            result['mediaId'] = media['media_id']
            result['mediaLocation'] = media['location']
            result['likes'] = dao.getPostLikesCountByID(post_id)[0][1]
            result['dislikes'] = dao.getPostDislikesCountByID(post_id)[0][1]
            result['replies'] = getRepliesByPostIDForUI(post_id)

            return jsonify(Post=result), 201
        else:
            return jsonify(Error='Malformed POST request'), 400
    else:
        return jsonify(Error='Malformed POST request'), 400


###################### Reaction HANDLER ############################

def reactPost(form):
    # Assumes form contains post_id, react_type
    if form and len(form) >= 2:  # For Debugging
        user_id = session['user_id'] #use when session is working
        #user_id = form['user_id']
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
            result['totalLikes'] = dao.getPostLikesCountByID(post_id)[0][1]
            result['totalDislikes'] = dao.getPostDislikesCountByID(post_id)[0][1]

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

# No se va a usar
def getUsersLikedByPostId(post_id):
    result = dao.getUsersLikedPostByID(post_id)
    return result

# No se va a usar
def getUsersDislikedByPostId(post_id):
    result = dao.getUsersDislikedPostByID(post_id)
    return result


###################### Reply HANDLER ############################

def reply(form):
    # Assumes form contains reply_msg, user_id, post_id
    if form and len(form) >= 3:  # For Debugging
        reply_msg = form['reply_msg']
        reply_date = 'now'
        #user_id = form['user_id']  # 
        user_id = session['user_id']
        post_id = form['post_id']

        if reply_msg and reply_date and user_id and post_id:
            reply = dao.reply(reply_msg, reply_date, user_id, post_id)
            reply_id, reply_date = reply['reply_id'], reply['reply_date']

            result = {}
            result['reply_id'] = reply_id
            result['reply_msg'] = reply_msg
            result['reply_date'] = reply_date
            result['user_id'] = user_id
            result['reply_username'] = userDao.getUserCredentials(user_id)['username']
            result['post_id'] = post_id

            return jsonify(Reply=result), 201
        else:
            return jsonify(Error='Malformed POST request'), 400
    else:
        return jsonify(Error='Malformed POST request'), 400


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

def insertMedia(post_id, media_type, location):
    # Assumes form contains post_id, media_type, location
    if post_id and media_type and location:
        media_id = dao.insertMedia(post_id, media_type, location)

        result = {}
        result['media_id'] = media_id
        result['post_id'] = post_id
        result['media_type'] = media_type
        result['location'] = location

        return result
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


###################### Hashtag HANDLER ############################

def insertHashtag(post_msg, post_id):
    # Assumes form has post_msg, post_id
    if post_msg and post_id:
        tags = [tag.strip("#") for tag in post_msg.split() if tag.startswith("#")]

        for tag in tags:
            if tag:
                tag = tag.lower()
                dao.insertHashtag(tag, post_id)


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
