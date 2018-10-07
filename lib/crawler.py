from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
import operator
from bs4 import BeautifulSoup


class MusicInfo:
    name = ""
    author = ""
    play_time = 0

    def __init__(self, name, author, play_time):
        self.name = name
        self.author = author
        self.play_time = play_time

    def __str__(self):
        return "name:%-10s  author:%-10s  play_time:%-10d" % (self.name, self.author, self.play_time)


class AuthorInfo:
    name = ""
    type = ""
    play_time = 0
    musics = [str]

    def __init__(self, name):
        self.name = name
        self.musics = []

    def set_type(self, type):
        self.type = type

    def AddMusics(self, music_info):
        self.musics.append(music_info.name)
        self.play_time += music_info.play_time
        return self

    def __str__(self):
        return "author:%-10s  play_time:%-10d  musics:%s" % (self.name, self.play_time, self.musics)


class SongSheet:
    name = ""
    musics = [MusicInfo]

    def __init__(self, name):
        self.name = name
        self.musics = []

    def AddMusics(self, musics):
        self.musics.append(musics)

    def get_play_time_author_slice(self):
        diagrams = {}
        for music in self.musics:
            if music.author in diagrams:
                diagrams[music.author].AddMusics(music)
            else:
                diagrams[music.author] = AuthorInfo(music.author).AddMusics(music)
        list = diagrams.values()
        list =reversed(sorted(list, key=lambda item: item.play_time))
        return list


class WangYiUser:
    url = "https://music.163.com/#"

    def __init__(self, music_u):
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')  # 不出现"Chrome正在受到自动软件的控制"的提示语
        option.add_argument("headless")  # 不显示浏览器
        driver = webdriver.Chrome(chrome_options=option)
        action = ActionChains(driver)
        self.music_u = music_u
        self.driver = driver
        self.action = action

    # 获取最后一周的播放排行榜
    def get_last_week_songsrank(self):
        self.driver.get(self.url)
        self.driver.add_cookie({'name': 'MUSIC_U', 'value': self.music_u})
        self.driver.refresh()
        # 进入个人主页
        owns = self.driver.find_element_by_xpath('//*[@class="name f-thide f-fl f-tdn f-hide"]')
        self.driver.get(owns.get_attribute("href"))
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))

        # 进入播放排行榜
        more = self.driver.find_element_by_xpath('//*[@id="more"]')
        self.driver.get(more.get_attribute("href"))
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))

        # 获取最近一周播放排行榜
        last_week = self.driver.find_element_by_xpath('//div[@class="j-flag"]')
        timeout = 10
        l = 0
        while l < 100:
            lis = WebDriverWait(last_week, 10).until(lambda x: x.find_elements_by_tag_name("li"))
            l = len(lis)
            if len(lis) == 100:
                break
        songs = SongSheet("最后一周")
        for li in lis:
            bs = BeautifulSoup(li.get_attribute("outerHTML"), "html.parser")
            name = bs.find(name='b').text
            author = bs.find(name='a', attrs={"class": "s-fc8"}).text
            play_time = int(bs.find(name='span', attrs={"class": "times f-ff2"}).text[:-1])
            if author == "" or play_time == 0:
                continue
            songs.AddMusics(MusicInfo(name, author, play_time))
        return songs

    # 获取所有时间的播放排行榜
    def get_all_songsrank(self):
        self.driver.get(self.url)
        self.driver.add_cookie({'name': 'MUSIC_U', 'value': self.music_u})
        self.driver.refresh()
        # 进入个人主页
        owns = self.driver.find_element_by_xpath('//*[@class="name f-thide f-fl f-tdn f-hide"]')
        self.driver.get(owns.get_attribute("href"))
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # 进入播放排行榜
        more = self.driver.find_element_by_xpath('//*[@id="more"]')
        self.driver.get(more.get_attribute("href"))
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # 获取所有时间播放排行榜
        WebDriverWait(self.driver, 10).until(lambda x: x.find_element_by_xpath('//span[@id="songsall"]')).click()
        songsall = self.driver.find_element_by_xpath('//div[@class="j-flag"]')
        timeout = 10
        l = 0
        while l < 100:
            lis = WebDriverWait(songsall, 10).until(lambda x: x.find_elements_by_tag_name("li"))
            l = len(lis)
            if len(lis) == 100:
                break
        songs = SongSheet("所有时间")
        for li in lis:
            bs = BeautifulSoup(li.get_attribute("outerHTML"), "html.parser")
            name = bs.find(name='b').text
            author = bs.find(name='a', attrs={"class": "s-fc8"}).text
            play_time = int(bs.find(name='span', attrs={"class": "times f-ff2"}).text[:-1])
            if author == "" or play_time == 0:
                continue
            songs.AddMusics(MusicInfo(name, author, play_time))
        return songs

    def get_screenshot_as_file(self, filename):
        self.driver.get_screenshot_as_file(filename)
