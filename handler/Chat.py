from flask import jsonify
from dao.ChatDAO import ChatDAO
from handler import DictBuilder as Dict

dao = ChatDAO()

###################### Main HANDLER ############################