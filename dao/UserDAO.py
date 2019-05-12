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

    def getAllUsersNotSession(self, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "SELECT * FROM users WHERE user_id != %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchall()
        return result

    def getUserInfo(self, user_id):
        cursor = self.conn.cursor()
        query = "select * from users where user_id = %s;"
        cursor.execute(query, (user_id,))
        result = cursor.fetchone()
        return result

    def getUserContactsByID(self, user_id):
        cursor = self.conn.cursor()
        query = '''select C.contact_id, CD.username ,U.first_name, U.last_name 
        from ContactList as C, users as U, credential as CD where C.user_id = %s and
          U.user_id = C.contact_id and U.user_id = CD.user_id;'''

        cursor.execute(query, (user_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUsersByChatID(self, chat_id):
        cursor = self.conn.cursor()
        query = "select user_id, first_name, last_name from users natural join participant where chat_id = %s;"
        cursor.execute(query, (chat_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getAdminByChatID(self, chat_id):
        cursor = self.conn.cursor()
        query = '''select C.admin, U.first_name, U.last_name from users as U, chat as C where C.chat_id = %s and
                     U.user_id = C.admin;'''

        cursor.execute(query, (chat_id,))
        result = cursor.fetchone()
        return result

    def getUsersWhoLikedPost(self, post_id):
        cursor = self.conn.cursor()
        query = '''select user_id, username,first_name, last_name, react_date from users natural inner join react natural inner join credential where post_id = %s AND react_type = 1;'''
        cursor.execute(query, (post_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUsersWhoDislikedPost(self, post_id):
        cursor = self.conn.cursor()
        query = '''select user_id, username,first_name, last_name, react_date from users natural inner join react natural inner join credential where post_id = %s AND react_type = -1;'''
        cursor.execute(query, (post_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    ###################### Read Credentials########################

    def registerUserCredentials(self, username, password, user_id):
        cursor = self.conn.cursor()
        query = "INSERT INTO Credential(username, password, user_id) VALUES (%s, %s, %s);"
        cursor.execute(query, (username, password, user_id,))
        self.conn.commit()
        cursor.close()

    def getAllCredentials(self):
        cursor = self.conn.cursor()
        query = "select * from credential;"
        cursor.execute(query)
        result = []
        for row in cursor:
            result.append(row)
        return result

    def getUserCredentials(self, user_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
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

    def getUserByUsername(self, username):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = '''SELECT username, password, user_id 
                   FROM Credential
                   WHERE username = %s;'''
        cursor.execute(query, (username,))
        result = cursor.fetchone()

        return result

    def registerUser(self, first_name, last_name, email, phone):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'INSERT INTO Users(first_name, last_name, email, phone) VALUES (%s, %s, %s, %s) RETURNING user_id;'
        cursor.execute(query, (first_name, last_name, email, phone));
        result = cursor.fetchone()['user_id']
        self.conn.commit()
        cursor.close()

        return result

        ###################### Activity DAO ############################   

    def registerActivity(self, user_id, activity_date):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'INSERT INTO Activity(user_id, activity_date) VALUES (%s, %s) RETURNING activity_id;'
        cursor.execute(query, (user_id, activity_date,))

        result = cursor.fetchone()['activity_id']
        self.conn.commit()
        cursor.close()

        return result

    def getTopThreeActiveUsers(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = ''' select username, count(user_id) as activity
                    From (select user_id From Post 
                    UNION ALL
                    select user_id From Reply 
                    UNION ALL 
                    select user_id From React) as S natural inner join Credential as C
                    WHERE S.user_id = C.user_id
                    GROUP BY username
                    ORDER BY activity DESC
                    Limit 3'''
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def addContact(self, user_id, contact_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "INSERT INTO ContactList(user_id, contact_id) VALUES (%s, %s) RETURNING user_id;"
        cursor.execute(query, (user_id, contact_id,))

        result = cursor.fetchone()['user_id']
        self.conn.commit()

        cursor.close()
        return result
