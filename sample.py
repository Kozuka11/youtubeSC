from googleapiclient.discovery import build
import datetime
import MySQLdb


API_KEY = ""
maxResults = 5

drop = "DROP TABLE IF EXISTS youtube;"

create = """CREATE TABLE sample.youtube(
                        video_id varchar(255) NOT NULL PRIMARY KEY,
                        video_title varchar(255), 
                        view_count int,
                        likes_count int,
                        comment_count int)"""
                        
insert = "INSERT INTO youtube(video_id,video_title,view_count,likes_count,comment_count) VALUES(%s,%s,%s,%s,%s)"

order = "SELECT * FROM youtube ORDER BY view_count DESC"
    
youtube = build('youtube', 'v3', developerKey = API_KEY)

def search_videos(query):
    
    search_response = youtube.search().list(
        part="id,snippet",
        q=query,
        type='video',
        maxResults=maxResults,
        order='date'
    ).execute()
    
    connection = MySQLdb.connect(
        user='root',
        passwd='iwasaki1290091',
        host='localhost',
        db='sample')
    cursor = connection.cursor()
    
    cursor.execute(drop)
    
    cursor.execute(create)
    
    for video in search_response['items']:
        id_ = video['id']['videoId']
        statistics = youtube.videos().list(part="statistics",id = id_).execute()['items'][0]['statistics']
        view = statistics['viewCount']
        come = statistics['commentCount']
        title = video['snippet']['title']
        likes = statistics['likeCount']
        #実行コード
        cursor.execute(insert,(id_,title,view,likes,come))

    #保存
    connection.commit()
    # 接続を閉じる
    connection.close()
        
if __name__ == "__main__":
    search_videos("猫")
