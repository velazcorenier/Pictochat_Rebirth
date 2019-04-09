from config.dbconfig import pg_config
import psycopg2


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

    # def getPostMessagesByChatID(self, chat_id):
    #     cursor = self.conn.cursor()
    #     query = "select post_id, post_msg, user_id from Post natural inner join users where chat_id = %s;"
    #     cursor.execute(query, (chat_id,))
    #     result = []
    #     for row in cursor:
    #         result.append(row)
    #     return result

    def getChatPostsForUI(self, chat_id):
        cursor = self.conn.cursor()
        query = '''SELECT post_id, post_msg, post_date, user_id, username, L.post_likes, D.post_dislikes, location, media_id
                    FROM Post natural inner join Credential natural inner join Media natural inner join
                        (SELECT post_id, count(react_type) as post_likes
                         FROM React
                         WHERE react_type = 1
                         GROUP BY post_id) as L
                         natural inner join
                        (SELECT post_id, count(react_type) as post_dislikes
                         FROM React
                         WHERE react_type = -1
                         GROUP BY post_id) as D'''
        cursor.execute(query, (chat_id,))
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

    ###################### Replies DAO ############################


    def getRepliesByPostID(self, post_id):
        cursor = self.conn.cursor()
        query = "select reply_id, reply_msg, reply_date from Reply;"
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
