from flask import jsonify
from dao.ChatDAO import ChatDAO
from handler import DictBuilder as Dict

dao = ChatDAO()

###################### Main HANDLER ############################

def getAllChats():
    # This method will return all the chats
    chat_lists = dao.getAllChats()
    if not chat_lists:
        return jsonify(Error="No Chats Found")
    result_list = []

    for row in chat_lists:
        result = Dict.chat_dict(row)
        result_list.append(result)
    return jsonify(Chat=result_list)