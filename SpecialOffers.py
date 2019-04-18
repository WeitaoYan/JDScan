# -*- coding: UTF-8 -*-
import math


class YouHuiQuanBase(object):
    def __init__(self, threshold, discount):
        self.id = None
        self.multiple = False
        self.threshold = float(threshold)
        self.discount = float(discount)

    def setID(self, quanid):
        self.id = quanid
        self.url = r"https://search.jd.com/Search?coupon_batch=%s" % self.id

    def setURL(self, url):
        self.url = url
        self.id = url[42:]


class CuXiaoBase(object):
    def __init__(self, threshold, discount):
        self.multiple = False
        self.threshold = float(threshold)
        self.discount = float(discount)

    def setID(self, quanid):
        self.id = quanid
        self.url = r"https://search.jd.com/Search?activity_id=%s" % self.id

    def setURL(self, url):
        self.url = url
        self.id = url[41:]


class YouHuiQuanManJian(YouHuiQuanBase):
    def __str__(self):
        return r"优惠券满%s减%s" % (self.threshold, self.discount)

    def minCounter(self, goods):
        return math.ceil(self.threshold / goods.price)

    def allDiscount(self, counter, goods):
        return self.discount


class YouHuiQuanManZhe(YouHuiQuanBase):
    def __init__(self, threshold, discount):
        super(YouHuiQuanManZhe, self).__init__(threshold, discount)
        self.multiple = True

    def __str__(self):
        return r"优惠券满%s享%s折" % (self.threshold, self.discount)

    def minCounter(self, goods):
        return self.threshold

    def allDiscount(self, counter, goods):
        return (1 - self.discount * 0.1) * goods.price * counter


class CuXiaoManJian(CuXiaoBase):
    def __str__(self):
        return r"促销满%s元减%s元" % (self.threshold, self.discount)

    def minCounter(self, goods):
        return math.ceil(self.threshold / goods.price)

    def allDiscount(self, counter, goods):
        return self.discount


class CuXiaoMeiManJian(CuXiaoBase):
    def __init__(self, threshold, discount):
        super(CuXiaoMeiManJian, self).__init__(threshold, discount)
        self.multiple = True

    def __str__(self):
        return r"促销每满%s元，可减%s元现金" % (self.threshold, self.discount)

    def minCounter(self, goods):
        return math.ceil(self.threshold / goods.price)

    def allDiscount(self, counter, goods):
        return int(goods.price * counter / self.threshold) * self.discount


class CuXiaoManZhe(CuXiaoBase):
    def __init__(self, threshold, discount):
        super(CuXiaoManZhe, self).__init__(threshold, discount)
        self.multiple = True

    def __str__(self):
        return r"促销满%s件，总价打%s折" % (self.threshold, self.discount)

    def minCounter(self, goods):
        return self.threshold

    def allDiscount(self, counter, goods):
        return (1 - self.discount * 0.1) * goods.price * counter


class CuXiaoManMian(CuXiaoBase):
    def __init__(self, threshold, discount):
        super(CuXiaoManMian, self).__init__(threshold, discount)
        self.multiple = True

    def __str__(self):
        return r"促销满%s件，立减最低%s件商品价格" % (self.threshold, self.discount)

    def minCounter(self, goods):
        return self.threshold

    def allDiscount(self, counter, goods):
        return goods.price * self.discount
