# import MySQLdb
# import json
# import urllib.parse
#
# conn = MySQLdb.connect(host='localhost', port=3306, db='wangyiCloud', user='root', passwd='root', charset='utf8')
# cs1 = conn.cursor()
# # 如果数据表已经存在使用 execute() 方法删除表。
# cs1.execute("DROP TABLE IF EXISTS songinfo")
#
# # 创建数据表SQL语句
# sql = """CREATE TABLE songinfo (
#          `name`  VARCHAR(1000)  NOT NULL,
#          `authors`  VARCHAR(1000),
#          `album`  VARCHAR(1000),
#          `song_url`  VARCHAR(1000),
#          `lyric`  TEXT)"""
#
# cs1.execute(sql)
#
#
# def close():
#     conn.close()
#
#
# class SongInfo:
#     name = ""
#     authors = []
#     album = ""
#     song_url = ""
#     lyric = ""
#
#     def __init__(self, name: str, authors: list, album: str, song_url: str, lyric: str):
#         self.name = name
#         self.authors = authors
#         self.album = album
#         self.song_url = song_url
#         self.lyric = lyric
#
#
# def insert_songinfo(name: str, authors: list, album: str, song_url: str, lyric: str):
#     csl = conn.cursor()
#     authors = ','.join(authors)
#     # name = urllib.parse.quote(name)
#     # authors = urllib.parse.quote(','.join(authors))
#     # album = urllib.parse.quote(album)
#     # song_url = urllib.parse.quote(song_url)
#     # lyric = urllib.parse.quote(lyric)
#     sql = "insert into songinfo (name,authors,album,song_url,lyric)values('%s','%s','%s','%s','%s')" % (name, authors, album, song_url, lyric)
#     csl.execute(sql)
#     conn.commit()
#     cs1.close()
#
#
# def get_songinfos() -> list:
#     csl = conn.cursor()
#     songs = []
#     # SQL 查询语句
#     sql = "SELECT name,authors,album,song_url,lyric FROM songinfo"
#     try:
#         # 执行SQL语句
#         csl.execute(sql)
#         # 获取所有记录列表
#         results = csl.fetchall()
#         for row in results:
#             name = row[0]
#             authors = row[1].split(",")
#             album = row[2]
#             song_url = row[3]
#             lyric = row[4]
#             # name = urllib.parse.unquote(row[0])
#             # authors = urllib.parse.unquote(row[1]).split(",")
#             # album = urllib.parse.unquote(row[2])
#             # song_url = urllib.parse.unquote(row[3])
#             # lyric = urllib.parse.unquote(row[4])
#             songs.append(SongInfo(name, authors, album, song_url, lyric))
#     except:
#         pass
#     cs1.close()
#     return songs
#
#
#
# insert_songinfo("陈百强",["陈百强"],"陈百强","陈百强","陈百强")