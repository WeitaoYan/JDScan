# -*- coding: UTF-8 -*-


import re

from selenium import webdriver
from bs4 import BeautifulSoup


Chrome_path = "C:\Users\weitaoyx\Downloads\chromedriver_win32\chromedriver.exe"
chrome_opt = webdriver.ChromeOptions()
prefs = {"profile.managed_default_content_settings.images":2}
chrome_opt.add_experimental_option("prefs", prefs)
driver = webdriver.Chrome(executable_path=Chrome_path, chrome_options=chrome_opt)
driver.implicitly_wait(3)
url = "https://passport.jd.com/new/login.aspx?ReturnUrl=https%3A%2F%2Fwww.jd.com%2Ferror2.aspx"
driver.get(url)
soup = BeautifulSoup(driver.page_source, "html.parser")
soup.select(".login-tab-r")[0].click()
soup.select("#loginname")[0].send_keys("18691879817")
soup.select("#nloginpwd")[0].send_keys("a1985")



