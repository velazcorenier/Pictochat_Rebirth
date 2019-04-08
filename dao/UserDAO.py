from config.dbconfig import pg_config
import psycopg2

class UserDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % \
                         (pg_config['dbname'], pg_config['user'], pg_config['passwd'],
                          pg_config['port'], pg_config['host'])
        self.conn = psycopg2._connect(connection_url)


###################### Read ########################

    def getAllUsers(self):
        cursor = self.conn.cursor()
        query = "select * from users;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserInfo(self, user_id):
        cursor = self.conn.cursor()
        query = "select * from users where user_id = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result

    def getUserContactsByID(self, user_id):
        cursor = self.conn.cursor()
        query = "select C.contact_id, U.first_name, U.last_name from ContactList as C, users as U where C.user_id = %s " \
                "and U.user_id = C.contact_id"

        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result


    # Returns the users that are members of the chat with ID cid
    def getUsersByChatID(self, chat_id):
        cursor = self.conn.cursor()
        query = "select user_id, first_name, last_name from users natural join participant where chat_id = %s;"
        cursor.execute(query, (chat_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    # Returns the user that is admin of the chat with ID cid
    def getAdminByChatID(self, chat_id):
        cursor = self.conn.cursor()
        query = "select C.admin, U.first_name, U.last_name from users as U, chat as C where C.chat_id = %s and" \
                " U.user_id = C.admin;"

        cursor.execute(query, (chat_id,))
        result = cursor.fetchone()
        return result

    def getUsersWhoLikedPost(self, post_id):
        cursor = self.conn.cursor()
        query = "select user_id, first_name, last_name, react_date from users natural inner join react" \
                 " where post_id = %s AND react_type = 1;"
        cursor.execute(query, (post_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUsersWhoDislikedPost(self, post_id):
        cursor = self.conn.cursor()
        query = "select user_id, first_name, last_name, react_date from users natural inner join react" \
                " where post_id = %s AND react_type = -1;"
        cursor.execute(query, (post_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    ###################### Read Credentials########################

    def getAllCredentials(self):
        cursor = self.conn.cursor()
        query = "select * from credential;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserCredentials(self, user_id):
        cursor = self.conn.cursor()
        query = "select * from credential where user_id = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result

    ###################### Read Activity ########################

    def getAllActivity(self):
        cursor = self.conn.cursor()
        query = "select * from activity;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserActivity(self, user_id):
        cursor = self.conn.cursor()
        query = "select * from activity where user_id = %s;"
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

