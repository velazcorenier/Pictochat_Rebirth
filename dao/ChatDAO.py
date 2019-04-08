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
        return result