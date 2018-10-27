# import jieba
#
# words = "作曲 : 陈百强作词 : 郑国江愁绪挥不去苦闷散不去为何我心一片空虚感情已失去一切都失去满腔恨愁不可消除为何你的嘴里总是那一句为何我的心不会死明白到爱失去一切都不对我又为何偏偏喜欢你爱已是负累 相爱似受罪*心底如今满苦泪旧日情如醉 此际怕再追偏偏痴心想见你为何我心分秒想着过去为何你一点都不记起情义已失去恩爱都失去我却为何偏偏喜欢你爱已是负累 相爱似受罪*心底如今满苦泪旧日情如醉 此际怕再追偏偏痴心想见你为何我心分秒想着过去为何你一点都不记起情义已失去恩爱都失去我却为何偏偏喜欢你"
#
# cut = jieba.cut(words)
# print(",".join(cut))

# 单词白名单
# 数组中的单词不会纳入进行统计
wipe_words = ["周杰伦", "陈百强", "张国荣", "作曲", "作词", "你", "我", "他", "她", "它", "的", "得", "地", "-", " ", ":", ",", "都", "着", "是", "了", "这", "那", "..."]


def word_statistics(words: list) -> dict:
    map = dict()
    for word in words:
        # 不统计包含在白名单的
        if word in wipe_words:
            continue
        # 不统计1个字符的
        if len(word) == 1:
            continue
        word = word.lower()
        if word in map.keys():
            map[word] += 1
        else:
            map[word] = 1
    map = sorted(map.items(), key=lambda x: x[1], reverse=True)
    return dict(map)
