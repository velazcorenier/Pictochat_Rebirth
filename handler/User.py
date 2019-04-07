from flask import jsonify
from dao.UserDAO import UserDAO
from handler import DictBuilder as Dict

dao = UserDAO()

###################### Main HANDLER ############################

def getUserContactList(user_id):
    result = dao.getUserContactList(user_id)
    if not result:
        return jsonify(Error="No Contacts Found")
    mapped_result = []
    for row in result:
        mapped_result.append(Dict.contacts_dict(row))
    return jsonify(UserContacts=mapped_result)

def getUsersWhoLikedPost(post_id):
    result = dao.getUsersWhoLikedPost(post_id)
    if not result:
        return jsonify(Error="No Users Found")
    mapped_result = []
    for row in result:
        mapped_result.append(Dict.reaction_user_dict(row))
    return jsonify(UsersLikedPost = mapped_result)

def getUsersWhoDislikedPost(post_id):
    result = dao.getUsersWhoDislikedPost(post_id)
    if not result:
        return jsonify(Error = "No Users Found")
    mapped_result = []
    for row in result:
        mapped_result.append(Dict.reaction_user_dict(row))
    return jsonify(UsersDislikedPost = mapped_result)