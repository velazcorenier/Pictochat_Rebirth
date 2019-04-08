from flask import jsonify
from dao.UserDAO import UserDAO
from handler import DictBuilder as Dict

dao = UserDAO()

###################### Main HANDLER ############################

def getUserContactsByID(user_id):
    result = dao.getUserContactsByID(user_id)
    if not result:
        return jsonify(Error="No Contacts Found")
    mapped_result = []
    for row in result:
        mapped_result.append(Dict.contacts_dict(row))
    return jsonify(UserContacts=mapped_result)

def getUsersByChatID(chat_id):
    result = dao.getUsersByChatID(chat_id)
    if not result:
        return jsonify(Error = "No Users Found")
    mapped_result = []
    for row in result:
        mapped_result.append(Dict.chat_participants_dict(row))
    return jsonify(Users = mapped_result)

def getAdminByChatID(chat_id):
    result = dao.getAdminByChatID(chat_id)
    if not result:
        return jsonify(Error="No Admin Found")
    mapped_result = Dict.chat_admin_dict(result)
    return jsonify(Admin=mapped_result)

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