# -*- coding: UTF-8 -*-


import time
import re
import Goods

# from Goods import Goods
from SpecialOffers import *
from selenium import webdriver
from bs4 import BeautifulSoup
import sys
reload(sys)
sys.setdefaultencoding('utf8')


class TestFrameworkChromePC(object):
    def __init__(self):
        Chrome_path = "C:\Users\weitaoyx\Downloads\chromedriver_win32\chromedriver.exe"
        chrome_opt = webdriver.ChromeOptions()
        prefs = {"profile.managed_default_content_settings.images":2}
        chrome_opt.add_experimental_option("prefs", prefs)
        self.driver = webdriver.Chrome(executable_path=Chrome_path, chrome_options=chrome_opt)
        self.driver.implicitly_wait(3)
        
    def get_page_soup(self, url, times=0, target=None):
        self.driver.get(url)
        finish = False
        i = 5
        if times:
            js = 'window.scrollTo(0,%s) '% (times)
            self.driver.execute_script(js)
            time.sleep(1)
        if target:
            while not finish:
                js = 'window.scrollTo(0,%s) '% (i*300)
                i += 5
                self.driver.execute_script(js)
                time.sleep(0.1)
                soup = BeautifulSoup(self.driver.page_source, "html.parser")
                tg = soup.select(target)
                if tg:
                    finish = True
        return BeautifulSoup(self.driver.page_source, "html.parser")

    def close_driver(self):
        self.driver.close()


if __name__ == "__main__":
    start_time = time.time()
    print "start..."
    fwk = TestFrameworkChromePC()
    try:
        res_list = []
        # goodsids = ["7265178", "2751756", "30026662492", "25206509193", "4333597", "1250248", "5193076", "1749283",
        #  "38252417132", "26282930680", "6988816", "7202389", "879250"]
        goodsids = [8181054]
        for goodsid in goodsids:
            try:
                goods = Goods.Goods(fwk, goodsid)
            except Goods.GetPriceError as _:
                continue
    finally:
        # fwk.close_driver()
        # del fwk
        print "end in finally"
    print "end...take %s s" % (time.time() - start_time)
