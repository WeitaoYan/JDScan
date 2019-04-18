# -*- coding: UTF-8 -*-
import datetime
import re
from SpecialOffers import CuXiaoMeiManJian, CuXiaoManJian, CuXiaoManZhe, CuXiaoManMian, YouHuiQuanManJian, \
    YouHuiQuanManZhe
from PurchasePlan import PurchasePlan


class GetPriceError(Exception):
    def __init__(self, value):
        self.parameter = value

    def __str__(self):
        return repr(self.parameter)


class Goods(object):
    def __init__(self, fwk, goodsid):
        self.fwk = fwk
        self.goods_id = str(goodsid)
        self.pc_url = r"https://item.jd.com/%s.html" % goodsid
        self.soup = self.get_soup()
        self.mobile_url = r"https://item.m.jd.com/product/%s.html" % goodsid
        self.plus = False
        self.fans = False
        self.name = self.get_name()
        self.youhuiquan = self.get_youhuiquan()
        self.cuxiao = self.get_cuxiao()
        self.price = self.get_price()
        self.plus_price = self.get_plus_price()
        self.fans_price = self.get_fans_price()
        self.price = self.get_lowest_price()
        self.buy_threshold = self.get_buy_threshold()
        self.purchase_plan = self.get_purchase_plan()
        self.print_purchase_plan()

    def get_purchase_plan(self):
        self.lowest_price = self.price
        result = PurchasePlan(self, 1, None, None)
        if self.youhuiquan and self.cuxiao:
            for quan in self.youhuiquan:
                for cx in self.cuxiao:
                    counter = max(quan.minCounter(self), cx.minCounter(self))
                    price = (counter * self.price - quan.allDiscount(counter, self) - cx.allDiscount(counter,
                                                                                                     self)) / counter
                    if price < self.lowest_price:
                        self.lowest_price = price
                        result = PurchasePlan(self, counter, quan, cx)
        if self.youhuiquan:
            for quan in self.youhuiquan:
                counter = quan.minCounter(self)
                price = (counter * self.price - quan.allDiscount(counter, self)) / counter
                if price < self.lowest_price:
                    self.lowest_price = price
                    result = PurchasePlan(self, counter, quan, None)
        if self.cuxiao:
            for cx in self.cuxiao:
                counter = cx.minCounter(self)
                price = (counter * self.price - cx.allDiscount(counter, self)) / counter
                if price < self.lowest_price:
                    self.lowest_price = price
                    result = PurchasePlan(self, counter, None, cx)
        return result

    def get_cuxiao(self):
        result = []
        cuxiaosoup = self.soup.select("#prom-one > div > div")
        for cuxiao in cuxiaosoup:
            cuxiaourl = None
            if cuxiao.a:
                cuxiaourl = cuxiao.a.attrs.get("href", "")
                if "https://search.jd.com/Search?activity_id=" not in cuxiaourl:
                    cuxiaourl = None
            title = cuxiao.select(".hl_red_bg")[0].text
            if title == ur"满减":
                if cuxiao.select(".hl_red"):
                    mj_type = cuxiao.select(".hl_red")[0].text
                    if re.search(ur"每满(\d+)元，可减(\d+)元现金", mj_type):
                        mj_list = cuxiao.select(".hl_red")[0].text.split("；")
                        for mj in mj_list:
                            mj_pattern = re.compile(ur"每满(\d+)元，可减(\d+)元现金")
                            mjs = mj_pattern.search(mj)
                            if mjs:
                                meimanjianobject = CuXiaoMeiManJian(mjs.group(1), mjs.group(2))
                                if cuxiaourl:
                                    meimanjianobject.setURL(cuxiaourl)
                                result.append(meimanjianobject)
                    elif re.search(ur"满(\d+)元减(\d+)元", mj_type):
                        mj_list = cuxiao.select(".hl_red")[0].text.split("，")
                        for mj in mj_list:
                            mj_pattern = re.compile(ur"满(\d+)元减(\d+)元")
                            mjs = mj_pattern.search(mj)
                            if mjs:
                                manjianobject = CuXiaoManJian(mjs.group(1), mjs.group(2))
                                if cuxiaourl:
                                    manjianobject.setURL(cuxiaourl)
                                result.append(manjianobject)
            elif title == ur"多买优惠":
                if cuxiao.select(".hl_red"):
                    mz_list = cuxiao.select(".hl_red")[0].text.split("；")
                    for mz in mz_list:
                        mz_pattern = re.compile(ur"满(\d+)件，总价打(\d+\.?\d*)折")
                        mm_pattern = re.compile(ur"满(\d+)件，立减最低(\d+)件商品价格")
                        mzs = mz_pattern.search(mz)
                        mms = mm_pattern.search(mz)
                        if mzs:
                            manzheobject = CuXiaoManZhe(mzs.group(1), mzs.group(2))
                            if cuxiaourl:
                                manzheobject.setURL(cuxiaourl)
                            result.append(manzheobject)
                        elif mms:
                            manmianobject = CuXiaoManMian(mms.group(1), mms.group(2))
                            if cuxiaourl:
                                manmianobject.setURL(cuxiaourl)
                            result.append(manmianobject)
            elif title == ur"跨自营/店铺满减":
                if cuxiao.select(".hl_red"):
                    mj_type = cuxiao.select(".hl_red")[0].text
                    if re.search(ur"满(\d+)元减(\d+)元", mj_type):
                        mj_list = cuxiao.select(".hl_red")[0].text.split("，")
                        for mj in mj_list:
                            mj_pattern = re.compile(ur"满(\d+)元减(\d+)元")
                            mjs = mj_pattern.search(mj)
                            if mjs:
                                manjianobject = CuXiaoManJian(mjs.group(1), mjs.group(2))
                                if cuxiaourl:
                                    manjianobject.setURL(cuxiaourl)
                                result.append(manjianobject)
        return result

    def get_youhuiquan(self):
        result = []
        quansoup = self.soup.select(".quan-item")
        for youhuiquan in quansoup:
            quan_title = youhuiquan.attrs.get("title", None)
            m = re.search(ur"有效期(\d+-\d+-\d+)至(\d+-\d+-\d+)", quan_title)
            if m:
                now_date = datetime.datetime.now().strftime('%Y-%m-%d')
                if now_date < str(m.group(1)) or now_date > str(m.group(2)):
                    continue
            mj_pattern = re.compile(ur"满(\d+)减(\d+)")
            mz_pattern = re.compile(ur"满(\d+)享(\d+\.?\d*)折")
            mj = mj_pattern.search(youhuiquan.text)
            mz = mz_pattern.search(youhuiquan.text)
            if mj:
                result.append(YouHuiQuanManJian(mj.group(1), mj.group(2)))
            elif mz:
                result.append(YouHuiQuanManZhe(mz.group(1), mz.group(2)))
        return result

    def get_details(self):
        self.print_purchase_plan()

    def get_buy_threshold(self):
        return 0.3 * self.price

    def print_purchase_plan(self):
        if self.lowest_price < self.buy_threshold:
            print self.purchase_plan.output()
        elif self.purchase_plan.quan and self.purchase_plan.cuxiao:
            print self.purchase_plan.output()

    def get_name(self):
        return str(self.soup.select(".sku-name")[0].text.strip())

    def get_soup(self):
        return self.fwk.get_page_soup(self.pc_url)

    def get_price(self):
        for price in self.soup.select(ur".J-p-%s" % self.goods_id):
            if price.text:
                try:
                    return float(price.text)
                except:
                    continue
        raise GetPriceError("Get price failed!")

    def get_plus_price(self):
        for price in self.soup.select(ur".J-p-p-%s" % self.goods_id):
            if price.text:
                try:
                    price = float(price.text[1:])
                    if price > 0:
                        self.plus = True
                        return price
                except:
                    continue
        return self.price

    def get_fans_price(self):
        for price in self.soup.select(ur".J-p-f-%s" % self.goods_id):
            if price.text:
                try:
                    price = float(price.text[1:])
                    if price > 0:
                        self.fans = True
                        return price
                except:
                    pass
        return self.price

    def get_lowest_price(self):
        return min(self.price, self.plus_price, self.fans_price)
