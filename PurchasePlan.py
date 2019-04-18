# -*- coding: UTF-8 -*-


class PurchasePlan(object):
    def __init__(self, goods, counter, quan, cuxiao):
        self.goods = goods
        self.counter = counter
        self.quan = quan
        self.cuxiao = cuxiao
        self.discount = 10 * goods.lowest_price / goods.price

    def output(self):
        outputstr = ""
        if self.quan and self.cuxiao:
            outputstr = "使用" + str(self.quan) + " 和 " + str(self.cuxiao)
            if self.quan.multiple and self.cuxiao.multiple:
                outputstr += "可翻倍下单"
        elif self.quan:
            outputstr = "使用" + str(self.quan)
            if self.quan.multiple:
                outputstr += "可翻倍下单"
        elif self.cuxiao:
            outputstr = "使用" + str(self.cuxiao)
            if self.cuxiao.multiple:
                outputstr += "可翻倍下单"
        else:
            outputstr = "没有任何优惠。。。"
        return "商品：%s \n%s\n购买数量：%s\t均价:%0.2f\t折扣：%0.2f\n%s\n" % (self.goods.pc_url, self.goods.name,
                                                                  int(self.counter), self.goods.lowest_price,
                                                                  self.discount, outputstr)
