from flask import jsonify
from dao.PostDAO import PostDAO
from handler import DictBuilder as Dict

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
    # if not chat_post_messages:
    #     return jsonify(Error="No Messages Found")
    result_post_messages = []
    for row in chat_post_messages:
        # result = Dict.post_msg_chat_dict_UI_Test(row, getRepliesByPostIDTest(row[1]))
        result_post_messages.append(Dict.post_msg_chat_dict_UI_2(row, getRepliesByPostIDForUI(row[1])))
    return jsonify(PostsInChat = result_post_messages)

def createPost(form):
    # Assumes form contains post_msg, post_date, user_id, chat_id
    if form and len(form) == 4:
        post_msg = form['post_msg']
        post_date = form['post_date']
        user_id = form['user_id']
        chat_id = form['chat_id']

        if post_msg and post_date and user_id and chat_id:
            post_id = dao.createChat(post_msg, post_date, user_id, chat_id)

            result = {}
            result['post_id'] = post_id
            result['post_msg'] = post_msg
            result['post_date'] = post_date
            result['user_id'] = user_id
            result['chat_id'] = chat_id

            return jsonify(Post=result), 201
        else:
            return jsonify(Error='Malformed POST request')
    else:
        return jsonify(Error='Malformed POST request')


###################### Reaction HANDLER ############################


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

###################### Reply HANDLER ############################


def getRepliesByPostID(post_id):
    replies_info = dao.getRepliesByPostID(post_id)
    if not replies_info:
        return jsonify(Error="No Replies Found")
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


def getMediaByPostID(post_id):
    media_info = dao.getMediaByPostID(post_id)
    if not media_info:
        return jsonify(Error="No Messages Found")
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
