from config.dbconfig import pg_config
import psycopg2

class UserDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % \
                         (pg_config['dbname'], pg_config['user'], pg_config['passwd'],
                          pg_config['port'], pg_config['host'])
        self.conn = psycopg2._connect(connection_url)


###################### Read ########################

    def getUserContactList(self, user_id):
        cursor = self.conn.cursor()
        query = "select contact_id, first_name, last_name from ContactList natural inner join where user_id = %s;"
        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUsersWhoLikedPost(self, post_id):
        cursor = self.conn.cursor()
        query = "select user_id, first_name, last_name, react_date from users natural inner join react" \
                 "where post_id = %s AND react_type = 1;"
        cursor.execute(query, (post_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUsersWhoDislikedPost(self, post_id):
        cursor = self.conn.cursor()
        query = "select user_id, first_name, last_name, react_date from users natural inner join react" \
                "where post_id = %s AND react_type = -1;"
        cursor.execute(query, (post_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result