from flask import jsonify
from dao.PostDAO import PostDAO
from handler import DictBuilder as Dict

dao = PostDAO()

###################### Main HANDLER ############################

def getAllPostMessages():
    rows = dao.getAllPostMessages()
    if not rows:
        return jsonify(Error="No Message found"), 404
    result = []
    for row in rows:
        result.append(Dict.post_dict(row))
    return jsonify(Post_Messages=result)

def getPostMessagesByChatID(chat_id):
    # This method will return the messages in a determined  chat
    chat_post_messages = dao.getPostMessagesByChatID(chat_id)
    if not chat_post_messages:
        return jsonify(Error="No Messages Found")
    result_post_messages = []
    for row in chat_post_messages:
        result = Dict.post_msg_chat_dict(row)
        result_post_messages.append(result)
    return jsonify(PostMessages = result_post_messages)

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


###################### Dashboard HANDLER ############################

def getTrendingHashtags():
    tophashtags = []
    hashtags = dao.getTrendingHashtags()
    for row in hashtags:
        result = Dict.hashtag_dict(row)
        print(result)
        tophashtags.append(result)
    return jsonify(Topics=tophashtags)
