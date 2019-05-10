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
        query = 'INSERT INTO Post(post_msg, post_date, user_id, chat_id) VALUES (%s, %s, %s, %s) RETURNING post_id;'
        cursor.execute(query, (post_msg, post_date, user_id, chat_id,))

        result = cursor.fetchone()['post_id']
        self.conn.commit()
        cursor.close()

        return result


    ###################### Reaction DAO ############################

    def likePost(self, user_id, post_id, react_date, react_type):
        cursor = self.conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)
        query = 'INSERT INTO React(user_id, post_id, react_date, react_type) VALUES (%s, %s, %s, %s) RETURNING post_id;'
        cursor.execute(query, (user_id, post_id, react_date, react_type,))

        result = cursor.fetchone()['post_id']
        self.conn.commit()
        cursor.close()

        return result

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

    ###################### Replies DAO ############################

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

    def getMediaByPostID(self, post_id):
        cursor = self.conn.cursor()
        query = "select * from Media;"
        cursor.execute(query, (post_id,))
        result = []

        for row in cursor:
            result.append(row)

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
