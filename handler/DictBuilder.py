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


# Dict used for demo
def contacts_dict(userContact):
    # contact_id, first_name, last_name
    contacts = {}
    contacts["user_id"] = userContact[0]
    contacts["username"] = userContact[1]
    contacts["first_name"] = userContact[2]
    contacts["last_name"] = userContact[3]
    return contacts


def chat_dict(chatInfo):
    # chat_id, chat_name, admin
    chat = {}
    chat["chat_id"] = chatInfo[0]
    chat["chat_name"] = chatInfo[1]
    chat["admin"] = chatInfo[2]
    return chat


def chatUI_dict(chatInfo):
    # chat_id, chat_name, admin
    chat = {}
    chat["chat_id"] = chatInfo[0]
    chat["chat_name"] = chatInfo[1]
    chat["admin"] = chatInfo[2]
    chat["first_name"] = chatInfo[3]
    chat["last_name"] = chatInfo[4]
    return chat


# Dict use for demo
def post_msg_chat_dict(postChatInfo):
    # chat_id, chat_name, admin
    post_chat = {}
    post_chat["post_id"] = postChatInfo[0]
    post_chat["post_msg"] = postChatInfo[1]
    post_chat["user_id"] = postChatInfo[2]
    post_chat["first_name"] = postChatInfo[3]
    post_chat["last_name"] = postChatInfo[4]
    return post_chat


# Dict use for UI
def post_msg_chat_dict_UI(postChatInfo):
    # chat_id, chat_name, admin
    post_chat_UI = {}
    post_chat_UI["chatId"] = postChatInfo[0]
    post_chat_UI["postId"] = postChatInfo[1]
    post_chat_UI["createdById"] = postChatInfo[2]
    post_chat_UI["username"] = postChatInfo[3]
    post_chat_UI["postMsg"] = postChatInfo[4]
    post_chat_UI["postDate"] = postChatInfo[5]
    post_chat_UI["mediaId"] = postChatInfo[6]
    post_chat_UI["mediaLocation"] = postChatInfo[7]
    post_chat_UI["likes"] = postChatInfo[8]
    post_chat_UI["dislikes"] = postChatInfo[9]
    return post_chat_UI


def post_msg_chat_dict_UI_2(postChatInfo, replies):
    # chat_id, chat_name, admin
    post_chat_UI = {}
    post_chat_UI["chatId"] = postChatInfo[0]
    post_chat_UI["postId"] = postChatInfo[1]
    post_chat_UI["createdById"] = postChatInfo[2]
    post_chat_UI["username"] = postChatInfo[3]
    post_chat_UI["postMsg"] = postChatInfo[4]
    post_chat_UI["postDate"] = postChatInfo[5]
    post_chat_UI["mediaId"] = postChatInfo[6]
    post_chat_UI["mediaLocation"] = postChatInfo[7]
    post_chat_UI["likes"] = postChatInfo[8]
    post_chat_UI["dislikes"] = postChatInfo[9]
    post_chat_UI["replies"] = replies

    return post_chat_UI


def participants_dict(chatParticipant):
    # chat_id, user_id
    participant = {}
    participant["chat_id"] = chatParticipant[0]
    participant["user_id"] = chatParticipant[1]
    return participant


# Dict used for demo
def chat_participants_dict(chatParticipant):
    # chat_id, user_id
    chat_participants = {}
    chat_participants["user_id"] = chatParticipant[0]
    chat_participants["first_name"] = chatParticipant[1]
    chat_participants["last_name"] = chatParticipant[2]
    return chat_participants


# Dict used for demo
def chat_admin_dict(chatAdmin):
    # chat_id, user_id
    admin = {}
    admin["admin"] = chatAdmin[0]
    admin["first_name"] = chatAdmin[1]
    admin["last_name"] = chatAdmin[2]
    return admin


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


# Dict used for demo
def reaction_user_dict(joinReaction):
    # user_id, first_name, last_name, react_date
    reaction_user = {}
    reaction_user["user_id"] = joinReaction[0]
    reaction_user["username"] = joinReaction[1]
    reaction_user["first_name"] = joinReaction[2]
    reaction_user["last_name"] = joinReaction[3]
    reaction_user["react_date"] = joinReaction[4]
    return reaction_user


def hashtag_dict(postHashtag):
    # hashtag_id, hashtag_text, post_id
    hashtag = {}
    hashtag["hashtag_id"] = postHashtag[0]
    hashtag["hashtag_text"] = postHashtag[1]
    hashtag["post_id"] = postHashtag[2]
    return hashtag


def dashboard_hashtag_dict(postHashtag):
    # hashtag_text
    hashtag = {}
    hashtag["hashtag_text"] = postHashtag[0]
    hashtag["Total"] = postHashtag[1]
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
    reply["reply_username"] = postReply[3]
    return reply


def post_per_day_dict(post):
    # reply_id, reply_msg, reply_date, reply_time, user_id, post_id
    postPerDay = {}
    postPerDay["day"] = post[0]
    postPerDay["total"] = post[1]
    return postPerDay
