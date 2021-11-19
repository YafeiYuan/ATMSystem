'''
人
类名：Person
属性：姓名  身份证号  电话号  卡
方法：



卡
类名：Card
属性：开好  密码  余额
方法：



银行：
类名：Bank
属性：用户列表  提款机
方法：



提款机
类名：ATM
属性：
方法：开户  查询  取款  存款  改密码  锁定  解锁  补卡  销户  退出


管理员
类名：Admin
属性：
方法：系统登陆界面  系统功能界面 管理员验证

'''

# 导入界面类
from admin import Admin
# 导入ATM类
from atm import ATM
# 导入时间模块
import time
# 导入OS模块
import os
# 导入持久性模块
import pickle


def main():
    admin = Admin()  # 实例界面对象
    admin.printAdminView()  # 管理员登陆页面(开机
    if admin.adminOption() == -1:  # 判断登陆密码返回值是否为-1 ,如果是-1 则结束程序
        return -1

    filepath = os.path.join(os.getcwd(), 'allusers.txt')  # 合成文件的绝对路径  os.getcwd() 获取当前文件所在的绝对路径

    # 打开读入
    f = open(filepath, 'rb')
    allUsers = pickle.load(f)
    print(allUsers)  # 打印数据库中用户信息
    # 第一次读取文件中没有数据会报错！需要先创建有一个空字典存入一个或一些数据，然后再读文件。
    # allUsers = {}
    atm = ATM(allUsers)  # 实例提款机ATM对象

    while True:  # 永真循环 让功能界面一直存在
        admin.printSysFunctionView()  # 系统功能界面
        option = input('请输入您要操作的项目名称：')  # 等待用户的输入

        # 根据用户输入判断
        if option == 'open1':  # 开户
            # 调用atm的开户方法
            atm.createUser()
            print('操作成功，稍后进入系统选项界面')

        elif option == 'search':  # 调用atm的查询方法
            atm.searchUserInfo()
            print('操作成功，稍后进入系统选项界面')

        elif option == 'withdrawal':  # 取款
            atm.getMoney()
            print('操作成功，稍后进入系统选项界面')

        elif option == 'deposit':  # 存款
            atm.saveMoney()
            print('操作成功，稍后进入系统选项界面')

        elif option == 'transfer':  # 转账
            atm.transferMoney()
            print('操作成功，稍后进入系统选项界面')

        elif option == 'passwd':  # 改密码
            atm.changePasswd()
            print('操作成功，稍后进入系统选项界面')

        elif option == 'lock':  # 锁定
            atm.lockUser()
            print('操作成功，稍后进入系统选项界面')

        elif option == 'unlock':  # 解锁
            atm.unlockUser()
            print('操作成功，稍后进入系统选项界面')

        elif option == 'reissue':  # 补卡
            atm.newCard()
            print('操作成功，稍后进入系统选项界面')

        elif option == 'closing':  # 销户
            atm.killUser()
            print('操作成功，稍后进入系统选项界面')

        elif option == 'quit1':  # 退出 # 关闭系统需要管理员操作
            print('请输入管理员账号和密码!')
            if not admin.adminOption():  # 判断管理员函数返回值  0 退出循环  -1 不退出循环
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


# 程序入口，调用函数main，整个程序启动
if __name__ == '__main__':
    main()
