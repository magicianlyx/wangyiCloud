import matplotlib.pyplot as plt
import numpy as np

font_size = 5
# 中文
font = {'family': 'SimHei',
        'weight': 'bold',
        'size': str(font_size)}
plt.rc('font', **font)
plt.rc('axes', unicode_minus=False)
plt.rcParams['figure.figsize'] = (6.0, 4.0) # 设置figure_size尺寸
plt.rcParams['savefig.dpi'] = 300  # 图片像素
# plt.rcParams['figure.dpi'] = 300


# 条形图绘制
def draw_histogram(data, title, file_name):
    singers = list(data.keys())
    time = list(data.values())


    x = np.arange(len(singers)) + 1  # 歌手
    y = np.array(time)

    plt.bar(x, time, width=0.35, align='center', color='c', alpha=0.8)

    plt.xticks(x, singers, size='small', rotation=30)
    # x、y轴标签与图形标题
    plt.xlabel('x')
    plt.ylabel('y')
    plt.title(title)
    for a, b in zip(x, y):
        plt.text(a, b + 0.05, '%.0f' % b, ha='center', va='bottom', fontsize=font_size)
    # 设置y轴的范围
    plt.ylim(0, max(time) + max(time) * 0.1)
    plt.savefig(file_name + ".png")
    plt.cla()


# 绘制饼形图
def draw_pie(data, title, file_name):
    singers = list(data.keys())
    time = list(data.values())

    label = singers

    values = time
    plt.pie(values,  labels=label, autopct='%1.1f%%')  # 绘制饼图
    plt.title(title)  # 绘制标题


    plt.legend()
    plt.savefig(file_name)  # 保存图片
    plt.cla()
