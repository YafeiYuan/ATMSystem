
# 用户类

class User(object):
    # 为对象添加属性
    def __init__(self, name, idCard, phone, card):
        self.name = name
        self.idCard = idCard
        self.phone = phone
        self.card = card
