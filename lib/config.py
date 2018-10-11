import json

config_path = "config.txt"


def get_musci_u(user_name: str):
    fp = open(config_path, "r")
    json_str = json.load(fp)
    users = json_str["list"]
    return users[user_name]


def add_music_u(name: str, music_u: str):
    try:
        with open(config_path, 'r', encoding='utf-8') as load_f:
            load_dict = json.load(load_f)
        load_dict['list'][name] = music_u
    except:
        load_dict = dict()
        load_dict['list']  = dict()
        load_dict['list'][name] = music_u
    with open(config_path, "w", encoding='utf-8') as dump_f:
        json.dump(load_dict, dump_f,indent=4)

