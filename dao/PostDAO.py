from config.dbconfig import pg_config
import psycopg2
import psycopg2.extras


class PostDAO:

    def __init__(self):
        connection_url = "dbname=%s user=%s password=%s port=%s host=%s" % \
                         (pg_config['dbname'], pg_config['user'], pg_config['passwd'],
                          pg_config['port'], pg_config['host'])
        self.conn = psycopg2._connect(connection_url)

    ###################### Main DAO ########################

    def getAllPosts(self):
        cursor = self.conn.cursor()
        query = "select * from Post;"
        cursor.execute(query)
        result = []

        for row in cursor:
            result.append(row)
        return result

    def getPostsByChatID(self, chat_id):
        cursor = self.conn.cursor()
        query = '''select chat_id, Post.post_id, user_id as created_by,username, post_msg, post_date, media_id,location,
                  COALESCE(L.post_likes,'0') as post_likes, COALESCE(D.post_dislikes,'0') as post_dislikes
                   from Credential natural inner join Post left outer join Media on Post.post_id = Media.post_id
                   left outer join (SELECT post_id, count(react_type) as post_likes 
                   from React where react_type = 1 group by post_id) as L on Post.post_id = L.post_id
                   left outer join (SELECT post_id, count(react_type) as post_dislikes 
                   from React where react_type = -1 group by post_id) as D on Post.post_id = D.post_id
                   where chat_id = %s;'''
        cursor.execute(query, (chat_id,))
        result = []

        for row in cursor:
            result.append(row)

        return result

    def createPost(self, post_msg, post_date, user_id, chat_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'INSERT INTO Post(post_msg, post_date, user_id, chat_id) VALUES (%s, %s, %s, %s) RETURNING post_id, post_date;'
        cursor.execute(query, (post_msg, post_date, user_id, chat_id,))

        result = cursor.fetchone()
        self.conn.commit()
        cursor.close()

        return result

    ###################### Reaction DAO ############################

    def reactPost(self, user_id, post_id, react_date, react_type):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'SELECT * FROM React WHERE user_id = %s and post_id = %s'
        cursor.execute(query, (user_id, post_id))
        result = cursor.fetchone()

        if result:
            # Reaction already in table
            if result['react_type'] == int(react_type):
                # If reaction is the same, remove
                query = 'DELETE FROM React WHERE user_id = %s and post_id = %s RETURNING post_id;'
                cursor.execute(query, (user_id, post_id))
                result = cursor.fetchone()['post_id']
            elif result['react_type'] != int(react_type):
                # If it's a dislike, change to like
                query = 'UPDATE React SET react_type=%s WHERE user_id = %s and post_id =%s RETURNING post_id;'
                cursor.execute(query, (react_type, user_id, post_id))
                result = cursor.fetchone()['post_id']
        else:
            # Reaction not in table
            query = 'INSERT INTO React(user_id, post_id, react_date, react_type) VALUES (%s, %s, %s, %s) RETURNING post_id;'
            cursor.execute(query, (user_id, post_id, react_date, react_type,))
            result = cursor.fetchone()['post_id']

        self.conn.commit()
        cursor.close()

        return result

    # TODO: Convert to dictionary
    def getPostLikesCountByID(self, post_id):
        cursor = self.conn.cursor()
        query = "select post_id, count(*) as likes from React where post_id = %s and react_type = 1 group by post_id;"
        cursor.execute(query, (post_id,))
        result = []

        for row in cursor:
            result.append(row)

        return result

    # TODO: Convert to dictionary
    def getPostDislikesCountByID(self, post_id):
        cursor = self.conn.cursor()
        query = "select post_id, count(*) as dislikes from React where post_id = %s and react_type = -1 group by post_id;"
        cursor.execute(query, (post_id,))
        result = []

        for row in cursor:
            result.append(row)

        return result

    def getUsersLikedPostByID(self, post_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "select user_id as userId, username as username from React natural inner join credential where post_id = %s and react_type = 1;"
        cursor.execute(query, (post_id,))
        result = []

        for row in cursor:
            result.append(row)

        return result

    def getUsersDislikedPostByID(self, post_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = "select user_id as userId, username as username from React natural inner join credential where post_id = %s and react_type = -1;"
        cursor.execute(query, (post_id,))
        result = []

        for row in cursor:
            result.append(row)

        return result

    ###################### Replies DAO ############################

    def reply(self, reply_msg, reply_date, user_id, post_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'INSERT INTO Reply(reply_msg, reply_date, user_id, post_id) VALUES (%s, %s, %s, %s) RETURNING reply_id, reply_date;'
        cursor.execute(query, (reply_msg, reply_date, user_id, post_id,))

        result = cursor.fetchone()
        self.conn.commit()
        cursor.close()

        return result

    def getRepliesByPostID(self, post_id):
        cursor = self.conn.cursor()
        query = '''select reply_id, reply_msg, reply_date, username 
                    from Reply natural inner join credential where post_id = %s; '''
        cursor.execute(query, (post_id,))
        result = []
        for row in cursor:
            result.append(row)
        return result

    ###################### Media DAO ############################

    def insertMedia(self, post_id, media_type, location):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'INSERT INTO Media(post_id, media_type, location) VALUES (%s, %s, %s) RETURNING media_id;'
        cursor.execute(query, (post_id, media_type, location,))

        result = cursor.fetchone()['media_id']
        self.conn.commit()
        cursor.close()

        return result

    def getMediaByPostID(self, post_id):
        cursor = self.conn.cursor()
        query = "select * from Media;"
        cursor.execute(query, (post_id,))
        result = []

        for row in cursor:
            result.append(row)

        return result

    ###################### Hashtag DAO ############################

    def insertHashtag(self, hashtag_text, post_id):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'INSERT INTO Hashtag(hashtag_text, post_id) VALUES (%s, %s) RETURNING hashtag_id;'
        cursor.execute(query, (hashtag_text, post_id,))

        result = cursor.fetchone()['hashtag_id']
        self.conn.commit()
        cursor.close()

        return result

    ###################### Dashboard DAO ############################

    def getTrendingHashtags(self):
        cursor = self.conn.cursor()
        query = "select hashtag_text, count(*)  as Total from hashtag group by hashtag_text order by Total desc;"
        cursor.execute(query)
        result = []

        for row in cursor:
            result.append(row)
            print(row)

        return result

    def getPostPerDay(self):
        cursor = self.conn.cursor()
        query = '''SELECT DATE(post_date), count(*)
                   FROM Post
                   GROUP BY DATE(post_date)'''
        cursor.execute(query)
        result = []

        for row in cursor:
            result.append(row)

        return result

    def getRepliesPerDay(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = '''SELECT DATE(reply_date), count(*)
                   FROM Reply
                   GROUP BY DATE(reply_date)'''
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getLikesPerDay(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = '''SELECT DATE(react_date), count(*)
                           FROM React
                           WHERE react_type = 1
                           GROUP BY DATE(react_date)'''
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getDislikesPerDay(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = '''SELECT DATE(react_date), count(*)
                   FROM React
                   WHERE react_type = -1
                   GROUP BY DATE(react_date)'''
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getRepliesPerPost(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = '''select  post_msg as Post, count(post_msg) as Replies
                    from (select Reply.post_id, Post.post_msg
                    from Reply inner join Post
                    on Reply.post_id = Post.post_id) as A
                    GROUP BY post_msg'''
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getLikesPerPost(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = '''select  post_msg as Post, count(post_msg) as likes
                    from(select React.react_type, React.post_id, Post.post_msg
                    from React  inner join Post 
                    on React.post_id = Post.post_id
                    where React.react_type = 1) as A
                    GROUP BY post_msg'''
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result

    def getDislikesPerPost(self):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = '''select  post_msg as Post, count(post_msg) as Dislikes
                   from (select React.react_type, React.post_id, Post.post_msg
                   from React inner join Post 
                   on React.post_id = Post.post_id
                   where React.react_type = -1) as A
                   GROUP BY post_msg'''
        cursor.execute(query)
        result = cursor.fetchall()
        cursor.close()
        return result
