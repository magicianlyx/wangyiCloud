from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from bs4 import BeautifulSoup
import time

base_url = "https://music.163.com/"


def string_format(s):
    s = "".join(s.split())
    return str(s)


class MusicBase:
    name = ""  # 歌曲名
    authors = []  # type:list[str]


# 音乐信息（排行榜）
class MusicInfo(MusicBase):
    play_time = 0  # 歌曲播放次数

    def __init__(self, name: str, author, play_time: int):
        self.name = name
        self.play_time = play_time
        if type(author) == str:
            self.authors = [author]
        elif type(author) == list:
            self.authors = author
        else:
            assert "unknown type"

    def __str__(self):
        return "name:%-10s  authors:%-10s  play_time:%-10d" % (self.name, self.authors, self.play_time)


# 音乐信息（歌单）
class SongInfo(MusicBase):
    url = ""  # 歌曲链接
    album = ""  # 歌曲所属专辑

    def __init__(self, name: str, author, url: str, album: str):
        self.name = name
        self.url = url
        self.album = album
        if type(author) == str:
            self.authors = [author]
        elif type(author) == list:
            self.authors = author
        else:
            assert "unknown type"

    def __str__(self):
        return "name:%-10s  authors:%-10s  album:%-10s  url:%-10s" % (self.name, self.authors, self.album, self.url)


# 歌手信息
class AuthorInfo:
    name = ""
    type = ""
    play_time = 0
    musics = []

    def __init__(self, name: str):
        self.name = name
        self.musics = []

    def set_type(self, type):
        self.type = type

    def AddMusics(self, music_info: MusicInfo):
        self.musics.append(music_info.name)
        self.play_time += music_info.play_time
        return self

    def __str__(self):
        return "author:%-10s  play_time:%-10d  musics:[%s]" % (self.name, self.play_time, ",".join(self.musics))


# 排行榜歌单
class RankSheet:
    name = ""
    musics = []

    def __init__(self, name):
        self.name = name
        self.musics = []  # type: list[MusicInfo]

    def AddMusics(self, music: MusicInfo):
        self.musics.append(music)

    def get_play_time_author_slice(self) -> list:
        diagrams = {}
        for music in self.musics:
            for author in music.authors:
                if author in diagrams.keys():
                    diagrams[author].AddMusics(music)
                else:
                    diagrams[author] = AuthorInfo(author).AddMusics(music)
        list = diagrams.values()
        list = reversed(sorted(list, key=lambda item: item.play_time))
        return list


# 歌单
class SongSheet:
    name = ""
    play_time = 0
    musics = []
    url = ""
    created_time = time.time()

    def __init__(self, name: str, play_time: int, url: str, created_time):
        self.name = name
        self.play_time = play_time
        self.musics = []  # type: list[SongInfo]
        self.url = url
        self.created_time = created_time

    def AddMusics(self, music: SongInfo):
        self.musics.append(music)

    # 按歌手名分组 歌单内各个歌手的歌曲数
    # dict[author]=count
    def get_play_time_author_slice(self) -> dict:
        diagrams = dict()
        for music in self.musics:
            for author in music.authors:
                if author in diagrams.keys():
                    diagrams[author] += 1
                else:
                    diagrams[author] = 1
        diagrams = dict(sorted(diagrams.items(), key=lambda x: x[1], reverse=True))
        diagrams["unknown"] = diagrams[""]
        del diagrams[""]
        return diagrams


# 网易云用户
class WangYiUser:
    url = "https://music.163.com/#"

    def __init__(self, music_u):
        option = webdriver.ChromeOptions()
        option.add_argument('disable-infobars')  # 不出现"Chrome正在受到自动软件的控制"的提示语
        # option.add_argument("headless")  # 不显示浏览器
        option.add_argument('Accept-Charset="utf-8"')
        driver = webdriver.Chrome(chrome_options=option)
        action = ActionChains(driver)
        self.music_u = music_u
        self.driver = driver
        self.action = action

    # 获取最后一周的播放排行榜
    def get_last_week_songsrank(self) -> RankSheet:
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
            lis = WebDriverWait(last_week, timeout).until(lambda x: x.find_elements_by_tag_name("li"))
            l = len(lis)
            if len(lis) == 100:
                break
        rs = RankSheet("最近一周")
        for li in lis:
            bs = BeautifulSoup(li.get_attribute("outerHTML"), "html.parser")
            name = bs.find(name='b').text
            author = bs.find(name='a', attrs={"class": "s-fc8"}).parent.attrs["title"]
            play_time = int(bs.find(name='span', attrs={"class": "times f-ff2"}).text[:-1])
            if author == "" or play_time == 0:
                continue
            if "/" in author:
                song = MusicInfo(name, string_format(author).split("/"), play_time)
            else:
                song = MusicInfo(name, string_format(author), play_time)
            rs.AddMusics(song)
        return rs

    # 获取所有时间的播放排行榜
    def get_all_songsrank(self) -> RankSheet:
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
            lis = WebDriverWait(songsall, timeout).until(lambda x: x.find_elements_by_tag_name("li"))
            l = len(lis)
            if len(lis) == 100:
                break
        rs = RankSheet("所有时间")
        for li in lis:
            bs = BeautifulSoup(li.get_attribute("outerHTML"), "html.parser")
            name = bs.find(name='b').text
            author = bs.find(name='a', attrs={"class": "s-fc8"}).parent.attrs["title"]
            play_time = int(bs.find(name='span', attrs={"class": "times f-ff2"}).text[:-1])
            if author == "" or play_time == 0:
                continue
            if "/" in author:
                song = MusicInfo(name, string_format(author).split("/"), play_time)
            else:
                song = MusicInfo(name, string_format(author), play_time)
            rs.AddMusics(song)
        return rs

    # 获取所有我自己创建的歌单
    # 返回的dict[name]=url
    def get_owns_songsheet(self):
        self.driver.get(self.url)
        self.driver.add_cookie({'name': 'MUSIC_U', 'value': self.music_u})
        self.driver.refresh()
        # 进入个人主页
        owns = self.driver.find_element_by_xpath('//*[@class="name f-thide f-fl f-tdn f-hide"]')
        self.driver.get(owns.get_attribute("href"))
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # 滚动到最下
        c_box = self.driver.find_element_by_id("cBox")
        try:
            WebDriverWait(self.driver, 3).until(
                lambda x: x.execute_script("window.scrollBy(0,%d)" % (c_box.rect["height"] + c_box.rect["y"])))
        except:
            pass
        # 获取个人歌单
        c_box = self.driver.find_element_by_id("cBox")
        bs = BeautifulSoup(c_box.get_attribute("outerHTML"), "html.parser")
        alinks = bs.find_all("a", attrs={"class": "tit f-thide s-fc0"})
        sheets = dict()
        for alink in alinks:
            sheets[string_format(alink.text)] = base_url + alink.attrs["href"]
        return sheets

    # 获取我收藏的歌单
    # 返回的dict[name]=url
    def get_favourite_songsheet(self):
        self.driver.get(self.url)
        self.driver.add_cookie({'name': 'MUSIC_U', 'value': self.music_u})
        self.driver.refresh()
        # 进入个人主页
        owns = self.driver.find_element_by_xpath('//*[@class="name f-thide f-fl f-tdn f-hide"]')
        self.driver.get(owns.get_attribute("href"))
        self.driver.switch_to.frame(self.driver.find_element_by_tag_name("iframe"))
        # 滚动到最下
        c_box = self.driver.find_element_by_id("cBox")
        try:
            WebDriverWait(self.driver, 3).until(
                lambda x: x.execute_script("window.scrollBy(0,%d)" % (c_box.rect["height"] + c_box.rect["y"])))
        except:
            pass
        # 获取收藏的歌单
        c_box = self.driver.find_element_by_id("sBox")
        bs = BeautifulSoup(c_box.get_attribute("outerHTML"), "html.parser")
        alinks = bs.find_all("a", attrs={"class": "tit f-thide s-fc0"})
        sheets = dict()
        for alink in alinks:
            sheets[string_format(alink.text)] = base_url + alink.attrs["href"]
        return sheets

    # 获取指定名歌单的信息
    def get_songsheetinfo(self, url) -> SongSheet:
        self.driver.get(url)
        self.driver.switch_to.frame("contentFrame")
        m_playlist = self.driver.find_element_by_id("m-playlist")

        bs = BeautifulSoup(m_playlist.get_attribute("outerHTML"), "html.parser")
        name = bs.find("h2", attrs={"class": "f-ff2 f-brk"}).text  # 获取歌单名
        play_time = bs.find("strong", attrs={"id": "play-count"}).text  # 获取歌单播放次数
        created_time = bs.find("span", attrs={"class": "time s-fc4"}).text.split(" ")[0]  # 获取歌单创建时间
        ss = SongSheet(name, play_time, url, created_time)

        tbody = self.driver.find_element_by_tag_name("tbody")
        bs = BeautifulSoup(tbody.get_attribute("outerHTML"), "html.parser")
        hshows = bs.find_all(name="tr")
        for tr in hshows:
            tds = tr.find_all("td")
            name = tds[1].find("b").attrs["title"]  # 歌曲名
            url = base_url + tds[1].find("a").attrs["href"]  # 歌曲url
            author = tds[3].find("div", attrs={"class": "text"}).attrs["title"]  # 歌手名
            album = tds[4].find("div", attrs={"class": "text"}).find("a").attrs["title"]  # 专辑名
            if string_format(author).find("/") != -1:
                song = SongInfo(name, string_format(author).split("/"), url, album)
            else:
                song = SongInfo(name, string_format(author), url, album)
            ss.AddMusics(song)
        return ss

    def get_screenshot_as_file(self, filename):
        self.driver.get_screenshot_as_file(filename)
