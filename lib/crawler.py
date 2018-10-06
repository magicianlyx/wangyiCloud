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


class SongSheet:
    name = ""
    musics = [MusicInfo]

    def __init__(self, name):
        self.name = name

    def AddMusics(self, musics):
        self.musics.append(musics)

    def get_play_time_author_slice(self):
        diagrams = {}
        for music in self.musics:
            if music.author in diagrams:
                diagrams[music.author] += music.play_time
            else:
                diagrams[music.author] = music.play_time
        diagrams = sorted(diagrams.items(), key=operator.itemgetter(1), reverse=True)
        return dict(diagrams)


class WangYiUser:
    url = "https://music.163.com/#"

    # music_u = "98f67da579a720f31ff2c6147ac96e03d0f2c1d6e895ac5b86fb53f95b3f20a98df3938ae24c1b7cb1417e0302d8b874b4c6e05649d650bf"
    def __init__(self, music_u):
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')
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
