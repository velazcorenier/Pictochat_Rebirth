from flask import jsonify
from dao.ChatDAO import ChatDAO
from handler import DictBuilder as Dict

dao = ChatDAO()

###################### Main HANDLER ############################

def getAllChats():
    chat_lists = dao.getAllChats()
    if not chat_lists:
        return jsonify(Error="No Chats Found")
    result_list = []

    for row in chat_lists:
        result = Dict.chat_dict(row)
        result_list.append(result)
    return jsonify(Chats=result_list)

def getChatByID(chat_id):
    chat = dao.getChatByID(chat_id)
    if not chat:
        return jsonify(Error=" Chat not found"), 404
    chat = Dict.chatUI_dict(chat)
    return jsonify(Chat=chat)