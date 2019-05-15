from config.dbconfig import pg_config
import psycopg2

class ChatDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % \
                         (pg_config['dbname'], pg_config['user'], pg_config['passwd'],
                          pg_config['port'], pg_config['host'])
        self.conn = psycopg2._connect(connection_url)


###################### Main DAO ########################

    def getAllChats(self):
        cursor = self.conn.cursor()
        query = "select * from chat;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)

        cursor.close()    
        return result

    def getChatByID(self, chat_id):
        cursor = self.conn.cursor()
        query = "select C.chat_id, C.chat_name, C.admin, U.first_name, U.last_name from users as U, chat as C where C.chat_id = %s and" \
                " U.user_id = C.admin;"
        cursor.execute(query, (chat_id,))
        result = cursor.fetchone()

        cursor.close()
        return result

    def getChatByUserID(self, user_id):
        cursor = self.conn.cursor()
        query = "select chat_id, chat_name, admin from Chat natural inner join Participant where user_id = %s;"
        cursor.execute(query, (user_id,))
        result = []

        for row in cursor:
            result.append(row)

        cursor.close()
        return result

    def createChat(self, chat_name, admin):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO Chat(chat_name, admin) VALUES (%s, %s) RETURNING chat_id;"
        cursor.execute(query, (chat_name, admin,))

        result = cursor.fetchone()['chat_id']
        self.conn.commit()

        cursor.close()
        return result

    def getParticipants(self, chat_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT P.user_id, U.first_name, U.last_name FROM Participant as P, Users as U WHERE P.user_id=U.user_id and chat_id=%s;"
        cursor.execute(query, (chat_id,))
        result = cursor.fetchall()

        cursor.close()
        return result

    def addParticipant(self, chat_id, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO Participant(chat_id, user_id) VALUES (%s, %s) RETURNING chat_id;"
        cursor.execute(query, (chat_id, user_id,))

        result = cursor.fetchone()['chat_id']
        self.conn.commit()

        cursor.close()
        return result
