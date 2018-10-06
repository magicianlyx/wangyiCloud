from lib.crawler import *

music_u = "98f67da579a720f31ff2c6147ac96e03d0f2c1d6e895ac5b86fb53f95b3f20a98df3938ae24c1b7cb1417e0302d8b874b4c6e05649dasdbf"
wyu = WangYiUser(music_u)
# songs = wyu.get_last_week_songsrank()
# for item in songs.musics:
#     print(item)
songs = wyu.get_all_songsrank()
# for item in songs.musics:
#     print(item)
map = songs.get_play_time_author_slice()
for key, value in map.items():
    print("author:%-30s  play time:%-10d" % ("\t{:^20}\t".format(key), value))
# wyu.get_all_songsrank()
