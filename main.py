from lib.owns import *



# 获取cookie身份
fs = open("music_u.wycloud", "r")
music_u = fs.readline()
wyu = WangYiUser(music_u)

# 获取所有时间播放排行榜 各个歌手的歌曲播放量
print("---------------获取所有时间播放排行榜 各个歌手的歌曲播放量-------------------")
sheet = wyu.get_all_songsrank()
array = sheet.get_play_time_author_slice()
for value in array:
    print(value)

# 获取最近一周播放排行榜 各个歌手的歌曲播放量
print("---------------获取最近一周播放排行榜 各个歌手的歌曲播放量-------------------")
sheet = wyu.get_last_week_songsrank()
rs = sheet.get_play_time_author_slice()
for value in rs:
    print(value)

# 获取自己创建的所有歌单
map = wyu.get_owns_songsheet()
# for name, url in map.items():
#     print(name, "   ", url)

# 获取我喜欢的歌曲歌单的所有歌曲 各个歌手的歌曲数
print("---------------获取我喜欢的歌曲歌单的所有歌曲 各个歌手的歌曲数-------------------")
ss = wyu.get_songsheetinfo(list(map.values())[0])
array = ss.get_play_time_author_slice()
for name, count in array.items():
    print(name, "   ", count)

# # 获取自己收藏的所有歌单
# sheets = wyu.get_favourite_songsheet()
# for name, url in sheets.items():
#     print(name, "   ", url)
