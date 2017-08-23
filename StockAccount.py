class StockAccount:
    def __init__(self, money):
        self.money = (int)(money * 100)  # 放大100倍，里面全部使用定点乘除提升性能
        self.fee_rate = 20  # 默认手续费为千分之二
        self.stock_value = 0
        self.stock_num = 0  # hand stock

    def init(self):
        self.money = 50000
        self.fee_rate = 20
        self.stock_value = 0
        self.stock_num = 0

    def set_fee_rate(self, fee_rate):
        self.fee_rate = fee_rate

    def get_fee(self, value_hand):
        return (value_hand * self.fee_rate) // 10000

    # return unit is hand stock
    def get_max_num(self, value):
        multiply100 = (int)(value * 100 * 100)  # 放大100倍，然后一手是100股

        num = self.money // multiply100
        if 0 == num:
            return 0

        # total = multiply100 + (multiply100*self.fee)/10000
        #         if total > self.money: # 剩余资金不足买一手
        #             return 0

        fee = self.get_fee(num * multiply100)
        remain = self.money - num * multiply100
        if fee > remain:
            return num - 1
        else:
            return num

    # value : real stock price
    # num   : hand of stock
    def buy_stock(self, value, num):
        self.stock_value = value
        self.stock_num = num
        value = (int)(value * 100 * num * 100)
        self.money -= value + (value * self.fee_rate) // 10000

    def buy_stock_all(self, value):
        self.buy_stock(value, self.get_max_num(value))

    def sell_stock(self, value, num):
        sell_num = num
        if num > self.stock_num:
            sell_num = self.stock_num

        self.stock_num -= sell_num
        value = (int)(value * 100 * sell_num * 100)
        self.money += value - (value * self.fee_rate) // 10000 - value // 1000

    def sell_stock_all(self, value):
        self.sell_stock(value, self.stock_num)
