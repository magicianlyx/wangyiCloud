from lib.owns import *
from lib.song import *
from lib.visualize import *
from lib.config import *
from lib.driver import driver

singer = Singer("陈百强", driver)
singer.get_top_n_songs()

# music_u = get_musci_u("魔术师LYX")
# # 获取cookie身份
# wyu = WangYiUser(music_u)
# # try:
# # 获取所有时间播放排行榜 各个歌手的歌曲播放量
# print("---------------获取所有时间播放排行榜 各个歌手的歌曲播放量-------------------")
# sheet = wyu.get_all_songsrank()
# array = sheet.get_play_time_author_slice()
# diagrams = dict()
# for item in array:
#     diagrams[item.name] = item.play_time
#
# diagrams_part = dict()
# idx = 0
# for key in diagrams.keys():
#     if idx > 20:
#         break
#     idx += 1
#     diagrams_part[key] = diagrams[key]
# # draw_histogram(diagrams_part, "所有时间各个歌手歌曲播放次数", "all_time")
# draw_pie(diagrams_part, "魔术师LYX" + " TOP20 所有时间各个歌手歌曲播放次数", "魔术师LYX" + " all_time")
#
# # 获取最近一周播放排行榜 各个歌手的歌曲播放量
# print("---------------获取最近一周播放排行榜 各个歌手的歌曲播放量-------------------")
# sheet = wyu.get_last_week_songsrank()
# rs = sheet.get_play_time_author_slice()
#
# diagrams_part = dict()
# idx = 0
# for item in rs:
#     if idx > 20:
#         break
#     diagrams_part[item.name] = item.play_time
#     idx += 1
# # draw_histogram(diagrams_part, "最近一周各个歌手歌曲播放次数", "last_week")
# draw_pie(diagrams_part, "魔术师LYX" + " TOP20 最近一周各个歌手歌曲播放次数", "魔术师LYX" + " last_week")
#
# # 获取自己创建的所有歌单
# map = wyu.get_owns_songsheet()
#
# # 获取我喜欢的歌曲歌单的所有歌曲 各个歌手的歌曲数
# print("---------------获取我喜欢的歌曲歌单的所有歌曲 TOP20 各个歌手的歌曲数-------------------")
# ss = wyu.get_songsheetinfo(list(map.values())[0])
# # ss = wyu.get_songsheetinfo("https://music.163.com/#/playlist?id=313942718")
# diagrams = ss.get_play_time_author_slice()
# print(ss.name)
# diagrams_part = dict()
# idx = 0
# for key in diagrams.keys():
#     if idx > 20:
#         break
#     idx += 1
#     diagrams_part[key] = diagrams[key]
#
# draw_pie(diagrams_part, ss.name + " TOP20 各个歌手的歌曲数", ss.name + " favourite")

# # # 获取自己收藏的所有歌单
# # sheets = wyu.get_favourite_songsheet()
# # for name, url in sheets.items():
# #     print(name, "   ", url)
# except:
#     pass
# finally:
#     wyu.driver.close()
