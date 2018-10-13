from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from lib.config import get_musci_u

option = webdriver.ChromeOptions()
option.add_argument('disable-infobars')  # 不出现"Chrome正在受到自动软件的控制"的提示语
# option.add_argument("headless")  # 不显示浏览器
option.add_argument('Accept-Charset="utf-8"')
driver = webdriver.Chrome(chrome_options=option)
action = ActionChains(driver)
driver.implicitly_wait(4)
driver.get("https://music.163.com")
music_u = get_musci_u("魔术师LYX")
driver.add_cookie({'name': 'MUSIC_U', 'value': music_u})
driver.refresh()
