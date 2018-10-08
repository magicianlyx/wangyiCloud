import matplotlib.pyplot as plt
import numpy as np


# 条形图绘制
def draw_histogram(data, title, file_name):
    singers = list(data.keys())
    time = list(data.values())

    # 中文
    font = {'family': 'SimHei',
            'weight': 'bold',
            'size': '7'}
    plt.rc('font', **font)
    plt.rc('axes', unicode_minus=False)

    plt.rcParams['savefig.dpi'] = 300  # 图片像素
    plt.rcParams['figure.dpi'] = 300

    x = np.arange(len(singers)) + 1  # 歌手
    y = np.array(time)

    plt.bar(x, time, width=0.35, align='center', color='c', alpha=0.8)

    plt.xticks(x, singers, size='small', rotation=30)
    # x、y轴标签与图形标题
    plt.xlabel('singer')
    plt.ylabel('play time')
    plt.title(title)
    for a, b in zip(x, y):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=7)
    # 设置y轴的范围
    plt.ylim(0, max(time) + max(time) * 0.1)
    plt.savefig(file_name + ".png")
