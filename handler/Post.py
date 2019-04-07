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
        result.append(Dict.user_dict(row))
    return jsonify(Post_Messages=result)

###################### Reaction HANDLER ############################


def getPostLikesCountByID(post_id):
    result = dao.getPostLikesCountByID(post_id)
    if not result:
        return jsonify(Error="No Like found"), 404
    map_result = dict()
    map_result["likes"] = result[0][0]
    return jsonify(PostLikes=map_result)


def getPostDislikesCountByID(post_id):
    result = dao.getPostDislikesCountByID(post_id)
    if not result:
        return jsonify(Error="No Dislike found"), 404
    map_result = dict()
    map_result["dislikes"] = result[0][0]
    return jsonify(PostDislikes=map_result)


