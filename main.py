from lib.crawler import *

fs = open("music_u.wycloud","r")
music_u = fs.readline()
wyu = WangYiUser(music_u)
# songs = wyu.get_all_songsrank()
# songs = wyu.get_last_week_songsrank()
# list = songs.get_play_time_author_slice()
# for key,value in list.items():
#     print(value)

sheets = wyu.get_owns_songsheet()
sheets = wyu.get_songsheetinfo(list(sheets.values())[0])

# for music in sheets.musics:
#     print("author: ", music.author, "   name:", music.name, "   url:", music.url)
for author, count in sheets.get_play_time_author_slice().items():
    print("author: ", author, "   count:", count)
wyu.driver.close()
