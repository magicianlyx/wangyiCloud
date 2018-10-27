from pymongo import MongoClient

conn = MongoClient('127.0.0.1', 27017)
db = conn.wangyiCloud  # 连接mydb数据库，没有则自动创建
si_tbl = db.SongInfo  # 使用test_set集合，没有则自动创建


# si_tbl.remove()


def close():
    conn.close()


class SongInfo:
    name = ""
    authors = []
    album = ""
    song_url = ""
    lyric = ""

    def __init__(self, name: str, authors: list, album: str, song_url: str, lyric: str):
        self.name = name
        self.authors = authors
        self.album = album
        self.song_url = song_url
        self.lyric = lyric


def insert_songinfo(name: str, authors: list, album: str, song_url: str, lyric: str, time: str):
    authors = ','.join(authors)
    si_tbl.insert({"name": name, "authors": authors, "album": album, "song_url": song_url, "lyric": lyric, "time": time})


def get_songinfos(authors) -> list:
    songs = []
    songs_name = []
    for i in si_tbl.find({}):
        # 不获取live版的歌词
        if "live" in i["name"]:
            continue
        # 只获取该歌手的歌曲
        if not authors in i["authors"]:
            continue
        if not i["name"] in songs_name:
            songs_name.append(i["name"])
            songs.append(SongInfo(i["name"], i["authors"].split(","), i["album"], i["song_url"], i["lyric"]))
    return songs
