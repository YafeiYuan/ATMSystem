
# 卡类

class Card(object):
    # 为对象添加属性
    def __init__(self, cardId, cardPasswd, cardMoney):
        self.cardId = cardId
        self.cardPasswd = cardPasswd
        self.cardMoney = cardMoney
        self.cardLock = False  # 锁卡，默认开启状态
