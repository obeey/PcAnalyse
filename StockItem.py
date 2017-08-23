
class StockItem :
    def __init__(self, date, open, high, low, close, volume, transation):
        self.date       = date
        self.open       = (int)(open*100)
        self.high       = (int)(high*100)
        self.low        = (int)(low*100)
        self.close      = (int)(close*100)
        self.volume     = (int)(volume)
        self.transation = (int)(transation)
        self.ma5        = None

    def __repr__(self):
        return self.__get_str()

    def __str__(self):
        return self.__get_str()

    def __get_str(self):
       return " : " + repr(self.open) + "\t" + repr(self.close)