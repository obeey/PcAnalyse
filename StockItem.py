
class StockItem :
    def __init__(self, date, open, high, low, close, volume, transation):
        self.date       = date
        self.open       = open
        self.high       = high
        self.low        = low
        self.close      = close
        self.volume     = volume
        self.transation = transation
        self.ma5        = None

    def __repr__(self):
        return self.__get_str()

    def __str__(self):
        return self.__get_str()

    def __get_str(self):
       return " : " + repr(self.open) + "\t" + repr(self.close)