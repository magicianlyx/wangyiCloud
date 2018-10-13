from lib.owns import *
from selenium.webdriver.chrome.webdriver import WebDriver
from bs4 import BeautifulSoup

base_url = "https://music.163.com/"


class Song:
    name = ""  # type:str
    singers = []  # type:list[str]
    album = ""  # type:str
    url = ""  # type:str

    def __init__(self, name: str, singers, url: str, album: str):
        self.name = name
        self.url = url
        self.album = album
        if type(singers) == str:
            self.singers = [singers]
        elif type(singers) == list:
            self.authors = singers
        else:
            assert "unknown type"

    # 获取歌曲歌词
    def get_songs(self):
        pass


class Singer:
    name = ""  # type: str
    driver = 0  # type: WebDriver
    owns_url = ""  # type: str
    song_search_url = ""  # type: str

    def __init__(self, name: str, driver: WebDriver):
        self.name = name
        self.driver = driver
        self.__init_args()

    # 初始化其他参数
    def __init_args(self):
        url = "https://music.163.com/#/search/m/?s=%s&type=100" % self.name
        self.driver.get(url)
        self.driver.switch_to.frame("contentFrame")
        bs = BeautifulSoup(self.driver.page_source, "html.parser")
        a = bs.find("a", attrs={"class": "nm f-thide s-fc0"})
        self.owns_url = base_url + "#" + a.attrs["href"]
        self.song_search_url = "https://music.163.com/#/search/m/?s=%s&type=1" % self.name

    # 获取热度前n首歌曲
    def get_top_n_songs(self, n=100) -> list:
        songs = []

        self.driver.get(self.song_search_url)
        self.driver.switch_to.frame("g_iframe")

        while len(songs) < n:
            next_page = self.driver.find_element_by_xpath('//a[contains(text(), "下一页")]')
            srchsongst = self.driver.find_element_by_xpath('//*[@class="srchsongst"]')
            divs1 = srchsongst.find_elements_by_xpath('//div[@class="item f-cb h-flag  "]')
            divs2 = srchsongst.find_elements_by_xpath('//div[@class="item f-cb h-flag even "]')
            song_divs = divs1 + divs2

            for div in song_divs:
                td_div = div.find_elements_by_xpath('./div')
                # name = td_div[1].find_element_by_tag_name("b").get_attribute("title")
                name = td_div[1].find_element_by_tag_name("b").text
                url = td_div[1].find_element_by_tag_name("a").get_attribute("href")
                singers_str = td_div[3].find_element_by_xpath("./div").text
                singers = singers_str.split("/")
                album = td_div[4].text
                songs.append(Song(name, url, singers,album))
            self.driver.execute_script("document.getElementById('%s').click();" % next_page.get_attribute("id"))

        return songs
