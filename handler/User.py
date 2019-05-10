from flask import jsonify, flash, session
from dao.UserDAO import UserDAO
from handler import DictBuilder as Dict

dao = UserDAO()

###################### Main HANDLER ############################

def register(form):
    # Assumes form contains username, password, first_name, last_name, email, phone
    if form and len(form) == 6:
        username = form['username']
        password = form['password']
        first_name = form['first_name']
        last_name = form['last_name']
        email = form['email']
        phone = form['phone']

        if username and password and first_name and last_name and email and phone:
            user_id = dao.registerUser(first_name, last_name, email, phone)
            dao.registerUserCredentials(username, password, user_id)

            result = {}
            result['user_id'] = user_id
            result['username'] = username
            result['first_name'] = first_name
            result['last_name'] = last_name
            result['email'] = email
            result['phone'] = [phone]

            return jsonify(User=result), 201
        else:
            return jsonify(Error='Malformed POST request'), 400
    else:
        return jsonify(Error='Malformed POST request'), 400

def login(form):
    if form and len(form) == 2:
        username = form['username']
        password_candidate = form['password']

        user = dao.getUserByUsername(username)

        if user:
            password = user['password']

            if password == password_candidate:
                # Passed
                session['logged_in'] = True
                session['username'] = username
                session['user_id'] = user['user_id']

                flash('You are now logged in.', 'success')
                return jsonify(User=user), 201
            else:
                flash('Invalid login.', 'danger')
            return jsonify(Error='Invalid login.'), 404
        else:
            return jsonify(Error='Username Not Found.'), 404
    else:
        return jsonify(Error='Malformed POST request'), 400

def getAllUsers():
    result = dao.getAllUsers()
    if not result:
        return jsonify(Error ="No Users Found"), 404
    mapped_result = []
    for row in result:
        mapped_result.append(Dict.user_dict(row))
    return jsonify(Users = mapped_result)

def getUserInfo(user_id):
    result = dao.getUserInfo(user_id)
    if not result:
        return jsonify(Error ="No User Found"), 404
    result = Dict.user_dict(result)
    return jsonify(UserInfo = result)

def getUserContactsByID(user_id):
    result = dao.getUserContactsByID(user_id)
    if not result:
        return jsonify(Error="No Contacts Found"), 404
    mapped_result = []
    for row in result:
        mapped_result.append(Dict.contacts_dict(row))
    return jsonify(UserContacts=mapped_result)

def getUsersByChatID(chat_id):
    result = dao.getUsersByChatID(chat_id)
    if not result:
        return jsonify(Error = "No Users Found"), 404
    mapped_result = []
    for row in result:
        mapped_result.append(Dict.chat_participants_dict(row))
    return jsonify(Users = mapped_result)

def getAdminByChatID(chat_id):
    result = dao.getAdminByChatID(chat_id)
    if not result:
        return jsonify(Error="No Admin Found"), 404
    mapped_result = Dict.chat_admin_dict(result)
    return jsonify(Admin=mapped_result)

def getUsersWhoLikedPost(post_id):
    result = dao.getUsersWhoLikedPost(post_id)
    if not result:
        return jsonify(Error="No Users Found"), 404
    mapped_result = []
    for row in result:
        mapped_result.append(Dict.reaction_user_dict(row))
    return jsonify(UsersLikedPost = mapped_result)

def getUsersWhoDislikedPost(post_id):
    result = dao.getUsersWhoDislikedPost(post_id)
    if not result:
        return jsonify(Error = "No Users Found"), 404
    mapped_result = []
    for row in result:
        mapped_result.append(Dict.reaction_user_dict(row))
    return jsonify(UsersDislikedPost = mapped_result)

###################### Credential HANDLER ############################

def getAllCredentials():
    result = dao.getAllCredentials()
    if not result:
        return jsonify(Error ="No Credentials Found"), 404
    mapped_result = []
    for row in result:
        mapped_result.append(Dict.credential_dict(row))
    return jsonify(Credentials=mapped_result)


def getUserCredentials(user_id):
    result = dao.getUserCredentials(user_id)
    if not result:
        return jsonify(Error = "No Credentials Found"), 404
    return jsonify(UserCredentials = result)



###################### Activity HANDLER ############################

def getAllActivity():
    result = dao.getAllActivity()
    if not result:
        return jsonify(Error="No Activity Found"), 404
    mapped_result = []
    for row in result:
        mapped_result.append(Dict.activity_dict(row))
    return jsonify(Activity=mapped_result)

def getUserActivity(user_id):
    result = dao.getUserActivity(user_id)
    if not result:
        return jsonify(Error = "No Activity Found"), 404
    mapped_result = []
    for row in result:
        mapped_result.append(Dict.activity_dict(row))
    return jsonify(UserActivity = result)

def getUserByUsername(username):
    user = dao.getUserByUsername(username)

    if not user:
        return jsonify(Error="No User Found"), 404
    return jsonify(User=user)
