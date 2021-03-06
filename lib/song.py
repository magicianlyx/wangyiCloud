from lib.owns import *
from selenium.webdriver.chrome.webdriver import WebDriver
from bs4 import BeautifulSoup

base_url = "https://music.163.com/"


class Song:
    name = ""  # type:str
    singers = []  # type:list[str]
    album = ""  # type:str
    url = ""  # type:str
    time = ""  # type:str

    def __init__(self, name: str, singers, url: str, album: str, time: str, driver):
        self.name = name
        self.url = url
        self.album = album
        self.time = time
        self.driver = driver
        if type(singers) == str:
            self.singers = [singers]
        elif type(singers) == list:
            self.authors = singers
        else:
            assert "unknown type"

    # 获取歌曲歌词
    def get_lyric(self) -> str:
        self.driver.get(self.url)
        self.driver.switch_to.frame("contentFrame")
        bs = BeautifulSoup(self.driver.find_element_by_xpath('//div[@id="lyric-content"]').get_attribute("outerHTML"),
                           "html.parser")
        idx = 0
        lyric = ""
        while True:
            try:
                flag_more = bs.find("div", attrs={"id": "flag_more"}).text
                crl = bs.find("div", attrs={"class": "crl"}).text
                lyric_content = self.driver.find_element_by_xpath('//div[@id="lyric-content"]').text

                lyric = lyric_content.replace(crl, "")
                lyric = lyric.replace("\n", "")
                lyric = lyric + flag_more
                break
            except:
                if idx > 10:
                    break
                idx += 1
        return lyric


class Singer:
    name = ""  # type: str
    driver = 0  # type: WebDriver
    owns_url = ""  # type: str
    song_search_url = ""  # type: str

    def __init__(self, name: str, driver):
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

        song_count = self.driver.find_element_by_xpath('//div[@class="snote s-fc4 ztag"]').find_element_by_tag_name("em").text
        song_count = int(song_count)
        n = min(song_count, n)

        while len(songs) < n:
            next_page = self.driver.find_element_by_xpath('//a[contains(text(), "下一页")]')
            srchsongst = self.driver.find_element_by_xpath('//*[@class="srchsongst"]')
            divs1 = srchsongst.find_elements_by_xpath('//div[@class="item f-cb h-flag  "]')
            divs2 = srchsongst.find_elements_by_xpath('//div[@class="item f-cb h-flag even "]')
            divs3 = srchsongst.find_elements_by_xpath('//div[@class="item f-cb h-flag even js-dis"]')
            divs3 = srchsongst.find_elements_by_xpath('//div[@class="item f-cb h-flag  js-dis"]')
            song_divs = divs1 + divs2 + divs3

            for div in song_divs:
                td_div = div.find_elements_by_xpath('./div')
                # name = td_div[1].find_element_by_tag_name("b").get_attribute("title")
                name = td_div[1].find_element_by_tag_name("b").text
                url = td_div[1].find_element_by_tag_name("a").get_attribute("href")
                singers_str = td_div[3].find_element_by_xpath("./div").text
                singers = singers_str.split("/")
                album = td_div[4].text
                time = td_div[5].text
                songs.append(Song(name, singers, url, album, time))
            if next_page is None:
                break
            self.driver.execute_script("document.getElementById('%s').click();" % next_page.get_attribute("id"))

        return songs
