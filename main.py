from lib.crawler import *

fs = open("music_u.wycloud", "r")
music_u = fs.readline()
wyu = WangYiUser(music_u)

sheet = wyu.get_all_songsrank()
array = sheet.get_play_time_author_slice()
for value in array:
    print(value)

sheet = wyu.get_last_week_songsrank()
rs = sheet.get_play_time_author_slice()
for value in rs:
    print(value)

map = wyu.get_owns_songsheet()
for name, url in map.items():
    print(name, "   ", url)

ss = wyu.get_songsheetinfo(list(map.values())[0])

array = ss.get_play_time_author_slice()
for name, count in array.items():
    print(name, "   ", count)

sheets = wyu.get_favourite_songsheet()
for name, url in sheets.items():
    print(name, "   ", url)
