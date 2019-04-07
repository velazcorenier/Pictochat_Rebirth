def user_dict(userInfo):
    # user_id, first_name, last_name, email, phone
    user = {}
    user["user_id"] = userInfo[0]
    user["first_name"] = userInfo[1]
    user["last_name"] = userInfo[2]
    user["email"] = userInfo[3]
    user["phone"] = userInfo[4]
    return user

def credential_dict(userCredential):
    # username, password, user_id
    credential = {}
    credential["username"] = userCredential[0]
    credential["password"] = userCredential[1]
    credential["user_id"] = userCredential[2]
    return credential

def activity_dict(userActivity):
    # activity_id, user_id, activity_date, activity_time
    activity = {}
    activity["activity_id"] = userActivity[0]
    activity["user_id"] = userActivity[1]
    activity["activity_date"] = userActivity[2]
    return activity

def contactList_dict(userContactList):
    # user_id, contact_id
    contactList = {}
    contactList["user_id"] = userContactList[0]
    contactList["contact_id"] = userContactList[1]
    return contactList

#Dict use for demo
def contacts_dict(userContact):
    # contact_id, first_name, last_name
    contacts = {}
    contacts["contact_id"] = userContact[0]
    contacts["first_name"] = userContact[1]
    contacts["last_name"] = userContact[2]
    return contacts

def chat_dict(chatInfo):
    # chat_id, chat_name, admin
    chat = {}
    chat["chat_id"] = chatInfo[0]
    chat["chat_name"] = chatInfo[1]
    chat["admin"] = chatInfo[2]
    return chat

def participants_dict(chatParticipant):
    # chat_id, user_id
    participant = {}
    participant["chat_id"] = chatParticipant[0]
    participant["user_id"] = chatParticipant[1]
    return participant

def post_dict(chatPost):
    # post_id, post_msg, post_date, post_time, user_id, chat_id
    post = {}
    post["post_id"] = chatPost[0]
    post["post_msg"] = chatPost[1]
    post["post_date"] = chatPost[2]
    post["user_id"] = chatPost[3]
    post["chat_id"] = chatPost[4]
    return post


def reaction_dict(postReaction):
    # user_id, post_id, react_date, react_time, react_type
    reaction = {}
    reaction["user_id"] = postReaction[0]
    reaction["post_id"] = postReaction[1]
    reaction["react_date"] = postReaction[1]
    reaction["react_type"] = postReaction[2]
    return reaction

#Dict use for demo
def reaction_user_dict(joinReaction):
    # user_id, first_name, last_name, react_date
    reaction_user = {}
    reaction_user["user_id"] = joinReaction[0]
    reaction_user["first_name"] = joinReaction[1]
    reaction_user["last_name"] = joinReaction[2]
    reaction_user["react_date"] = joinReaction[3]
    return reaction_user

def hashtag_dict(postHashtag):
    # hashtag_id, hashtag_text, post_id
    hashtag = {}
    hashtag["hashtag_id"] = postHashtag[0]
    hashtag["hashtag_text"] = postHashtag[1]
    hashtag["post_id"] = postHashtag[2]
    return hashtag

def media_dict(postMedia):
    # media_id, post_id, media_type, location
    media = {}
    media["media_id"] = postMedia[0]
    media["post_id"] = postMedia[1]
    media["media_type"] = postMedia[2]
    media["location"] = postMedia[3]
    return media

def reply_dict(postReply):
    # reply_id, reply_msg, reply_date, reply_time, user_id, post_id
    reply = {}
    reply["reply_id"] = postReply[0]
    reply["reply_msg"] = postReply[1]
    reply["reply_date"] = postReply[2]
    reply["user_id"] = postReply[3]
    reply["post_id"] = postReply[4]
    return reply
