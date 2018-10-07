from lib.crawler import *

fs = open("music_u.wycloud", "r")
music_u = fs.readline()
wyu = WangYiUser(music_u)

# songs = wyu.get_all_songsrank()
# list = songs.get_play_time_author_slice()
# for value in list:
#     print(value)
# songs = wyu.get_last_week_songsrank()
# list = songs.get_play_time_author_slice()
# for value in list:
#     print(value)

sheets = wyu.get_owns_songsheet()
for name, url in sheets.items():
    print(name, "   ", url)
#
# for author, count in sheets.get_play_time_author_slice().items():
#     print("author: ", author, "   count:", count)
# wyu.driver.close()
