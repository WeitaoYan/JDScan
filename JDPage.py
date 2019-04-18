# -*- coding: UTF-8 -*-
import time
import re
import Goods, TestFramework


class JDGoodListPage(object):
    def __init__(self, fwk):
        self.fwk = fwk
        self.soup = None

    def get_next_page_url(self):
        lastpage = int(self.soup.select(".fp-text")[0].i.text)
        m = re.search(".+&page=(\d+)", self.url)
        if m:
            current_page = (int(m.group(1)) + 1) / 2
            if current_page == lastpage:
                return None
            next_page_number = 2 * current_page + 1
            return self.url[0:len(self.url) - len(m.group(1))] + str(next_page_number)
        else:
            if lastpage in [0, 1]:
                return None
            return self.url + "&page=3"

    def setUrl(self, url):
        self.url = url

    def get_all_goods(self, known_list=None):
        self.soup = self.fwk.get_page_soup(self.url, times=3000)
        self.goods_list_soup = self.soup.select(".gl-item")
        result = []
        for eachgoods in self.goods_list_soup:
            goods_id = eachgoods.attrs["data-sku"]
            if goods_id in known_list:
                continue
            zi_ying = eachgoods.select(".goods-icons")
            if zi_ying and zi_ying[0].text == u"自营":
                try:
                    goods = Goods.Goods(self.fwk, goods_id)
                    result.append(goods)
                except Goods.GetPriceError as _:
                    print "get price fail, skip it. https://item.jd.com/%s.html" % goods_id
                    continue
        return result


if __name__ == "__main__":
    start_time = time.time()
    print "start..."
    fwk = TestFramework.TestFrameworkChromePC()
        # url = r"https://search.jd.com/Search?coupon_batch=188009002"
        # url = r"https://search.jd.com/Search?coupon_batch=186230186"
        # url = r'https://search.jd.com/Search?coupon_batch=192212958'
        # url = r"https://search.jd.com/Search?coupon_batch=192345094"
        # url = "https://search.jd.com/Search?activity_id=50004472496"
        # url = r"https://search.jd.com/Search?keyword=%E9%A1%BA%E6%B8%85%E6%9F%94&enc=utf-8&wq=%E9%A1%BA%E6%B8%85%E6%9F%94&pvid=0c7f160a1398460ca39c545eaa84c4fc"
        # url = 'https://search.jd.com/Search?activity_id=50002588090'  # cuxiao
        # url = 'https://search.jd.com/Search?coupon_batch=192334598'
    try:
        url = 'https://search.jd.com/Search?coupon_batch=200465062'
        # wtype=1 京东物流  stock=1 仅显示有货
        while url:
            page = JDGoodListPage(fwk)
            # print "start capture %s" % url
            page.setUrl(url)
            goods = page.get_all_goods()
            url = page.get_next_page_url()
    finally:
        # fwk.close_driver()
        print "end in finally"
    print "end"
