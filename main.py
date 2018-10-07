from lib.crawler import *

music_u = "98f67da579a720f31ff2c61asdfac96e0318f806752a1aa67fa73cd84c4dddec5bbcc46fc6a96b64497d502eb74a7de49fb4c6e05649d650bf"
wyu = WangYiUser(music_u)
# songs = wyu.get_all_songsrank()
songs = wyu.get_last_week_songsrank()
list = songs.get_play_time_author_slice()
for value in list:
    print("歌手:%-30s " % value)
