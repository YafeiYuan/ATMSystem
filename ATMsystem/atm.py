'''
自动提款机类

'''

# 导入卡类模块
from card import Card
# 导入用户类模块
from user import User
# 导入随机模块
import random
import time


# 导入界面类
# from admin import Admin
# from 银行自动提款系统 import main
# 取款机类
class ATM(object):
    # 存储所有用户的信息
    def __init__(self, allUsers):
        self.allUsers = allUsers

    # 开户
    def createUser(self):
        # 目标：向用户字典中添加一对键值对(卡号--用户)
        name = input('请输入您的姓名：')
        idCard = input('请输入您的身份证号码：')
        phone = input('请输入您的电话号码：')

        # 预存款
        prestoreMoney = int(input('请输入预存款金额：'))
        if prestoreMoney < 0:
            print('预存款输入有误！！开户失败......')
            return -1

        onePasswd = input('请设置密码：')
        # 验证密码
        if not self.checkPasswd(onePasswd):
            print('密码输入错误3次！！开户失败.....')
            return -1

        # 所有需要的信息就全了
        # 得到卡号
        cardStr = self.randomCardId()

        # 实例化Card卡类
        card = Card(cardStr, onePasswd, prestoreMoney)
        # 实例化User用户类
        user = User(name, idCard, phone, card)
        # 存到字典
        self.allUsers[cardStr] = user
        print(f'开户成功！！卡号为：{cardStr} 请牢记卡号...')

    # 查询
    def searchUserInfo(self):
        # 用户输入卡号
        cardNun = input('请输入您的卡号：')
        # 验证卡号是否存在
        user = self.allUsers.get(cardNun)  # 在存用户的字典中查找
        if not user:  # 用户不存在执行if
            print('您输入的卡号不存在！！查询失败...')
            return -1

        # 判断卡是否锁定状态
        if user.card.cardLock:  # true 为锁定状态
            print('您输入的卡号为锁定状态！！请解锁后使用...')
            return -1

        # 验证密码
        if not self.checkPasswd2(user.card.cardPasswd):
            print('密码输入错误3次！！此卡已被锁定，！！请解锁后使用...')
            # 锁卡  改变锁卡标记
            user.card.cardLock = True
            return -1
        # 密码正确打印用户对应信息
        print(f'卡号：{user.card.cardId}  余额：{user.card.cardMoney}')

    # 取款
    def getMoney(self):
        # 用户输入卡号
        cardNun = input('请输入您的卡号：')
        # 验证卡号是否存在
        user = self.allUsers.get(cardNun)  # 在存用户的字典中查找
        if not user:  # 用户不存在执行if
            print('您输入的卡号不存在！！取款失败...')
            return -1

        # 判断卡是否锁定状态
        if user.card.cardLock:  # true 为锁定状态
            print('您输入的卡号为锁定状态！！请解锁后使用...')
            return -1

        # 验证密码
        if not self.checkPasswd(user.card.cardPasswd):
            print('密码输入错误3次！！此卡已被锁定，！！请解锁后使用...')
            # 锁卡
            user.card.cardLock = True
            return -1

        # 判断余额是否不足
        money = int(input('请输入取款金额：'))
        if money > user.card.cardMoney:
            print('当前余额不足！！取款失败')
            return -1
        # 判断是否输入负数
        if money <= 0:
            print('取款金额不能为负数或零！！取款失败')
            return -1

        # 取款
        user.card.cardMoney -= money
        print(f'取款成功！！当前余额为：{user.card.cardMoney}')

    # 存款
    def saveMoney(self):
        # 用户输入卡号
        cardNun = input('请输入您的卡号：')
        # 验证卡号是否存在
        user = self.allUsers.get(cardNun)  # 在存用户的字典中查找
        if not user:  # 用户不存在执行if
            print('您输入的卡号不存在！！存款失败...')
            return -1

        # 判断卡是否锁定状态
        if user.card.cardLock:  # true 为锁定状态
            print('您输入的卡号为锁定状态！！请解锁后使用...')
            return -1

        # 验证密码
        if not self.checkPasswd(user.card.cardPasswd):
            print('密码输入错误3次！！此卡已被锁定，！！请解锁后使用...')
            # 锁卡
            user.card.cardLock = True
            return -1

        # 用户输入
        money = int(input('请输入存入金额：'))

        # 取款
        user.card.cardMoney += money
        print(f'存款成功！！当前余额为：{user.card.cardMoney}')

    # 转账
    def transferMoney(self):
        cardNunOne = input('请输入您的转出卡号：')  # 卡号一
        if self.verify(cardNunOne) == -1:
            return -1
        print()  # 换行

        cardNunTow = input('请输入您的接收卡号：')  # 卡号二
        if self.verify(cardNunTow) == -1:
            return -1
        print()

        # 开始进行转账操作
        tempMoney = int(input("请输入转账金额："))
        # 将转账卡号中的金额减去tempMoney，将接收卡号中的金额加上tempMoney
        # 获取转账卡号中的金额并减去tempMoney
        oneUser = self.allUsers.get(cardNunOne)
        oneUser.card.cardMoney -= tempMoney

        # 获取接收卡号中的金额并加上tempMoney
        towUser = self.allUsers.get(cardNunTow)
        towUser.card.cardMoney += tempMoney

        print(f"转账成功~~, 转出卡当前金额为：{oneUser.card.cardMoney}, 接收卡当前金额为：{towUser.card.cardMoney}")

    # 改密
    def changePasswd(self):
        # 用户输入卡号
        cardNun = input('请输入您的卡号：')
        # 验证卡号是否存在
        user = self.allUsers.get(cardNun)  # 在存用户的字典中查找
        if not user:  # 用户不存在执行if
            print('您输入的卡号不存在！！改密失败...')
            return -1

        # 判断卡号是否为已锁定状态
        # cardLock为True表示已锁定
        elif user.card.cardLock:
            print('您输入的卡号已被锁定！！请解锁后再使用...')
            return -1

        # 验证密码
        elif not self.checkPasswd2(user.card.cardPasswd):
            print('密码输入错误！！改密失败...')
            return -1

        # # 验证身份证
        # tempIdCard = input('请输入您的身份证号码：')
        # if tempIdCard != user.idCard:
        #     print('身份证号输入错误！！改密失败...')
        #     return -1
        #
        # # 验证手机号
        # tempPhone = input('请输入您的电话号码：')
        # if tempPhone != user.phone:
        #     print('电话号码输入错误！！改密失败...')
        #     return -1

        # 开始改密码操作
        print()
        newOnePassWD = input("请输入新的密码：")
        newTowPassWD = input("请重复输入上次密码：")
        if newOnePassWD == newTowPassWD:
            user = self.allUsers.get(cardNun)
            user.card.cardPasswd = newOnePassWD
            print(f"改密成功~ 新密码为：{newOnePassWD}, 请牢记您的密码！！")
        else:
            print("第二次输入与第一次不同！！请重新操作！！")
            return -1

    # 锁定
    def lockUser(self):
        # 用户输入卡号
        cardNun = input('请输入您的卡号：')
        # 验证卡号是否存在
        user = self.allUsers.get(cardNun)  # 在存用户的字典中查找
        if not user:  # 用户不存在执行if
            print('您输入的卡号不存在！！锁定失败...')
            return -1

        # 判断卡号是否为已锁定状态
        # cardLock为True表示已锁定
        elif user.card.cardLock:
            print('您输入的卡号已被锁定！！请解锁后再使用...')
            return -1

        # 验证密码
        elif not self.checkPasswd2(user.card.cardPasswd):
            print('密码输入错误！！锁定失败...')
            return -1

        # 锁卡
        user.card.cardLock = True
        print('锁定成功！！')

    # 解锁
    def unlockUser(self):
        # 用户输入卡号
        cardNun = input('请输入您的卡号：')
        # 验证卡号是否存在
        user = self.allUsers.get(cardNun)  # 在存用户的字典中查找
        if not user:  # 用户不存在执行if
            print('您输入的卡号不存在！！解锁失败...')
            return -1

        # cardLock为True表示已锁定
        elif not user.card.cardLock:
            print('您输入的卡号没有锁定！！无需解锁')
            return -1

        # 验证密码
        elif not self.checkPasswd2(user.card.cardPasswd):
            print('密码输入错误！！解锁失败...')
            return -1

        # 解锁
        user.card.cardLock = False
        print('解锁成功...')

    # 补卡
    def newCard(self):
        # 用户输入卡号
        cardNun = input('请输入您的卡号：')
        # 验证卡号是否存在
        user = self.allUsers.get(cardNun)  # 在存用户的字典中查找
        if not user:  # 用户不存在执行if
            print('您输入的卡号不存在！！补卡失败...')
            return -1

        # cardLock为True表示已锁定
        elif user.card.cardLock:
            print('您输入的卡号已被锁定！！请解锁后进行补卡操作~')
            return -1

        # 验证密码
        elif not self.checkPasswd2(user.card.cardPasswd):
            print('密码输入错误！！补卡失败...')
            return -1

        # 开始补卡操作  账号密码都知道，卡丢了，补一张新卡，需要生成新的卡号密码等信息。
        print("")
        print("补卡申请成功~ 请填入一些补卡需要的信息~")
        print("")
        time.sleep(0.5)
        # 目标：替换字典中的键，生成新的卡(卡号--用户)
        name = input('请输入您的姓名：')
        idCard = input('请输入您的身份证号码：')
        phone = input('请输入您的电话号码：')

        # 第一次出入的密码
        onePasswd = input('请设置密码：')
        # 验证密码 和第一次的密码对比
        if not self.checkPasswd(onePasswd):
            print('密码输入错误3次！！开户失败.....')
            return -1

        # 得到卡号
        cardStr = self.randomCardId()

        # 把遗失卡中的金额转移到新卡中
        oldUser = self.allUsers.get(cardNun)
        oldMoney = oldUser.card.cardMoney  # 老卡金额

        # 实例化Card卡类
        card = Card(cardStr, onePasswd, oldMoney)  # oldMoney 设置为遗失卡的金额

        # 实例化User用户类
        user = User(name, idCard, phone, card)
        # 存到字典  cardStr键  user值
        self.allUsers[cardStr] = user

        # 删除遗失的卡
        self.allUsers.pop(cardNun)
        # 提示信息
        print(f'补卡成功！！新的卡号为：{cardStr} 请牢记卡号...')  # 八年级上册，悦读会

    # 销户
    def killUser(self):
        # 用户输入卡号
        cardNun = input('请输入您的卡号：')
        # 验证卡号是否存在
        user = self.allUsers.get(cardNun)  # 在存用户的字典中查找
        if not user:  # 用户不存在执行if
            print('您输入的卡号不存在！！销户失败...')
            return -1

        # cardLock为True表示已锁定
        elif user.card.cardLock:
            print('您输入的卡号已被锁定！！请解锁后进行销户操作~')
            return -1

        # 验证密码
        elif not self.checkPasswd2(user.card.cardPasswd):
            print('密码输入错误！！销户失败...')
            return -1

        # 开始销户操作
        self.allUsers.pop(cardNun)
        print("销户成功~")

    # 多次用到的 验证密码
    def checkPasswd(self, realPasswd):
        # 循环输入3次密码 3次输入错误退出
        for i in range(3):
            tempPasswd = input('请输入密码：')
            if tempPasswd == realPasswd:
                return True
            else:
                print("第二次输入和第一次不同！！")
        return False

    # 多次用到的 验证密码
    def checkPasswd2(self, realPasswd):
        # 循环输入3次密码 3次输入错误退出
        for i in range(3):
            tempPasswd = input('请输入密码：')
            if tempPasswd == realPasswd:
                return True
            else:
                print("密码有误！！")
                mm = input("是否回到主界面重新操作(是/否)：")
                if mm != "是" and mm != "否":
                    print("请输入是或否！")
                    mm = input("是否回到主界面重新操作(是/否)：")
                if mm == "是":
                    main()
                    # pass
                elif mm == "否":
                    pass
        return False

    # 随机生成六位数密码
    def randomCardId(self):
        str = ''
        for i in range(6):
            # 随机生成一个数字
            ch = chr(random.randrange(ord('0'), ord('9') + 1))
            str += ch
        # 判断结果否重复
        if not self.allUsers.get(str):
            return str

    # 为转账功能专门写的。。。
    # 验证身份信息
    def verify(self, cardNum):
        # 验证卡号是否存在
        user = self.allUsers.get(cardNum)  # 在存用户的字典中查找
        if not user:  # 用户不存在执行if
            print('您输入的卡号不存在！！转账失败...')
            return -1

        # 判断卡号是否为已锁定状态
        # cardLock为True表示已锁定
        elif user.card.cardLock:
            print('您输入的卡号已被锁定！！请解锁后再使用...')
            return -1

        # 验证密码
        elif not self.checkPasswd2(user.card.cardPasswd):
            print('密码输入错误！！转账失败...')
            return -1


'''
卡号：988511 密码及所有信息：222  金额：9800
卡号：227962 密码及所有信息：111  金额：10200

'''
from admin import Admin
import pickle
import time
import os


def main():
    # 实例界面对象
    admin = Admin()
    # 管理员登陆页面(开机)
    # admin.printAdminView()
    # # 判断登陆密码返回值是否为-1 ,如果是-1 则结束程序
    # if admin.adminOption() == -1:
    #     return -1

    # 实例提款机ATM对象
    # 合成文件的绝对路径  os.getcwd() 获取当前文件所在的绝对路径
    filepath = os.path.join(os.getcwd(), 'allusers.txt')
    ''''''
    # 打开读入
    f = open(filepath, 'rb')
    allUsers = pickle.load(f)
    # print(allUsers)
    # 第一次读取文件中没有数据会报错！需要先创建有一个空字典存入一个或一些数据，然后再读文件。
    # allUsers = {}
    atm = ATM(allUsers)

    # 永真循环 让功能界面一直存在
    while True:
        # 系统功能界面
        admin.printSysFunctionView()
        # 等待用户的输入
        option = input('请输入您要操作的项目名称：')

        # 根据用户输入判断
        # 开户
        if option == 'open1':
            # 调用atm的开户方法
            atm.createUser()
            print('开户成功，稍后进入系统选项界面。')

        # 查询
        elif option == 'search':
            # 调用atm的查询方法
            atm.searchUserInfo()

        # 取款
        elif option == 'withdrawal':
            # 调用atm的查询方法
            atm.getMoney()

        # 存款
        elif option == 'deposit':
            print('正在打开存款界面，请稍等...')
            atm.saveMoney()

        elif option == 'transfer':
            # 转账
            atm.transferMoney()

        elif option == 'passwd':
            # 改密码
            atm.changePasswd()

        # 锁定
        elif option == 'lock':
            atm.lockUser()

        # 解锁
        elif option == 'unlock':
            atm.unlockUser()

        elif option == 'reissue':
            # 补卡
            atm.newCard()

        elif option == 'closing':
            # 销户
            atm.killUser()

        elif option == 'quit1':
            # 退出
            print('请输入管理员账号和密码！')
            # 关闭系统需要管理员操作
            # 判断管理员函数返回值  0 退出循环  -1 不退出循环
            if not admin.adminOption():
                # 将当前系统中的用户信息保存到文件中
                f = open(filepath, 'wb')
                pickle.dump(atm.allUsers, f)
                f.close()
                print("关闭成功，欢迎下次使用~")

                return -1
            else:
                print("关闭失败!! 程序会继续执行~")

        # 每次用户操作程序休眠2秒
        time.sleep(2)
