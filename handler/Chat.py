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

def getChatByUserID(user_id):
    rows = dao.getChatByUserID(user_id)
    if not rows:
        return jsonify(Error="No Chats found"), 404
    result = []
    for row in rows:
        result.append(Dict.chat_dict(row))
    return jsonify(Chats=result)

def createChat(form):
    # Assumes form contains chat_name, admin
    if form and len(form) >= 2: # == 2
        chat_name = form['chat_name']
        admin = form['admin'] # session['user_id']

        if admin and chat_name:
            chat_id = dao.createChat(chat_name, admin)

            # Add admin to chat participants
            form = {}
            form['chat_id'] = chat_id
            form['participants'] = [admin]
            addParticipants(form)

            result = {}
            result['chat_id'] = chat_id
            result['chat_name'] = chat_name
            result['admin'] = admin

            return jsonify(Chat=result), 201
        else:
            return jsonify(Error='Malformed POST request')
    else:
        return jsonify(Error='Malformed POST request')

def getParticipants(chat_id):
    participants = dao.getParticipants(chat_id)
    if participants:
        return jsonify(Participants=participants)
    else:
        return jsonify(Error="No Participants Found"), 404

def addParticipants(form):
    # Assumes form containts chat_id, participants(list of user_ids)
    if form and len(form) >= 2:
        chat_id = form['chat_id']
        participants = form['participants']

        for participant in participants:
            chat_id = dao.addParticipant(chat_id, participant['user_id'])

        return getParticipants(chat_id)
    else:
        return jsonify(Error="No Participants Found"), 404
