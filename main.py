from lib.owns import *
from lib.visualize import *

fs =open("music_u.wycloud","r")
music_u = fs.readline()
print(music_u)

# 获取cookie身份
wyu = WangYiUser(music_u)


# 获取所有时间播放排行榜 各个歌手的歌曲播放量
print("---------------获取所有时间播放排行榜 各个歌手的歌曲播放量-------------------")
sheet = wyu.get_all_songsrank()
array = sheet.get_play_time_author_slice()
diagrams = dict()
for item in array:
    diagrams[item.name] = item.play_time

diagrams_part = dict()
idx = 0
for key in diagrams.keys():
    if idx > 20:
        break
    idx += 1
    diagrams_part[key] = diagrams[key]
draw_histogram(diagrams_part, "所有时间各个歌手歌曲播放次数", "all_time")

# 获取最近一周播放排行榜 各个歌手的歌曲播放量
print("---------------获取最近一周播放排行榜 各个歌手的歌曲播放量-------------------")
sheet = wyu.get_last_week_songsrank()
rs = sheet.get_play_time_author_slice()

diagrams_part = dict()
idx = 0
for item in rs:
    if idx > 20:
        break
    diagrams_part[item.name] = item.play_time
    idx += 1
draw_histogram(diagrams_part, "最近一周各个歌手歌曲播放次数", "last_week")

# 获取自己创建的所有歌单
map = wyu.get_owns_songsheet()

# 获取我喜欢的歌曲歌单的所有歌曲 各个歌手的歌曲数
print("---------------获取我喜欢的歌曲歌单的所有歌曲 各个歌手的歌曲数-------------------")
ss = wyu.get_songsheetinfo(list(map.values())[0])
diagrams = ss.get_play_time_author_slice()

diagrams_part = dict()
idx = 0
for key in diagrams.keys():
    if idx > 10:
        break
    idx += 1
    diagrams_part[key] = diagrams[key]

draw_pie(diagrams_part,"我喜欢的歌曲歌单 各个歌手的歌曲数","favourite")


# # # 获取自己收藏的所有歌单
# # sheets = wyu.get_favourite_songsheet()
# # for name, url in sheets.items():
# #     print(name, "   ", url)
