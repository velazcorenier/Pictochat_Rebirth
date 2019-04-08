from config.dbconfig import pg_config
import psycopg2

class PostDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % \
                         (pg_config['dbname'], pg_config['user'], pg_config['passwd'],
                          pg_config['port'], pg_config['host'])
        self.conn = psycopg2._connect(connection_url)


###################### Main DAO ########################

    def getAllPostMessages(self):
        cursor = self.conn.cursor()
        query = "select * from Post;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getPostMessagesByChatID(self, chat_id):
        cursor = self.conn.cursor()
        query = "select post_id, post_msg, user_id from Post natural inner join users where chat_id = %s;"
        cursor.execute(query,(chat_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    ###################### Reaction DAO ############################

    def getPostLikesCountByID(self, post_id):
        cursor = self.conn.cursor()
        query = "select post_id, count(*) from React where post_id = %s and react_type = 1 group by post_id;"
        cursor.execute(query, (post_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result


    def getPostDislikesCountByID(self, post_id):
        cursor = self.conn.cursor()
        query = "select post_id, count(*) from React where post_id = %s and react_type = -1 group by post_id;"
        cursor.execute(query, (post_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result