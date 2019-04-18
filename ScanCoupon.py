# -*- coding: UTF-8 -*-
import time
import re

from SpecialOffers import YouHuiQuanManJian, YouHuiQuanManZhe
from TestFramework import TestFrameworkChromePC
from JDPage import JDGoodListPage


def get_youhuiquan_from_center(soup):
    if r"折" in soup.text:
        m = re.search(ur"(\d(\.\d+)?)折满(\d+)可用", soup.text)
        if m:
            # print soup.text + "mz"
            return YouHuiQuanManZhe(m.group(2), m.group(1))
    elif r"¥" in soup.text:
        mj = re.search(ur"¥(\d+)满(\d+)可用", soup.text) #¥20满199可用
        if mj:
            # print soup.text + "mj"
            return YouHuiQuanManJian(mj.group(2), mj.group(1))
        m = re.search(ur"¥(\d+)", soup.text)
        if m:
            # print soup.text + "m"
            return YouHuiQuanManJian(0, m.group(1))
    return None


class CouponCenterPage(object):
    def __init__(self, fwk, cate_item):
        self.fwk = fwk
        self.item_map = {"计生情趣": 2, "服饰内衣": 10, "电脑办公": 11, "个护化妆": 12, "运动户外": 13, "母婴用品": 14, "食品饮料": 15,
                    "家用电器": 16, "鞋靴箱包": 17, "海囤全球": 18, "手机数码": 19, "家居家纺": 20, "宠物园艺": 77, "支付白条": 80,
                    "PLUS专区": 81, "珠宝钟表": 82, "汽车用品": 84, "图书音像": 87, "生活旅行": 88, "医药保健": 95, "生鲜": 105, "发现好店": 115}
        self.url = "https://a.jd.com/?cateId=%d" % self.item_map[cate_item]
        self.goods_list = []

    def get_coupons(self):
        self.soup = self.fwk.get_page_soup(self.url, target=".cate-end")
        couponssoup = self.soup.select(".quan-item")
        result = []
        for coupon in couponssoup:
            details = coupon.select(".q-type")[0]
            price_soup = details.select(".q-price ")[0]
            # coupon_range = coupon.select(".q-range")[0].text
            progress = details.select(".q-progress")[0].text
            if progress != ur"今日已抢光":   # and ur"自营" in coupon_range:
                cpid = coupon.select(".q-ops-jump .q-opbtns > a")[0]
                url = "https:" + cpid.get("href")
                if r"//search.jd.com/Search?coupon_batch=" in url:
                    cp = get_youhuiquan_from_center(price_soup)
                    cp.setURL(url)
                    result.append(cp)
        return result


if __name__ == "__main__":
    start_time = time.time()
    print "start..."
    fwk = TestFrameworkChromePC()
    try:
        page = JDGoodListPage(fwk)
        for shop_class in ["运动户外", "母婴用品", "食品饮料", "服饰内衣", "电脑办公", "个护化妆"]:
            cop = CouponCenterPage(fwk, shop_class)
            cops = cop.get_coupons()
            for cp in cops:
                url = cp.url
                while url:
                    page.setUrl(url)
                    goods = page.get_all_goods(cop.goods_list)
                    for gd in goods:
                        cop.goods_list.append(gd.goods_id)
                    url = page.get_next_page_url()
    finally:
        # fwk.close_driver()
        print "end in finally"
    print "end"
