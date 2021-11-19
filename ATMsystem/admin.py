# 界面
import time



class Admin(object):
    # 类属性
    admin = '1'  # 管理员账号
    passwd = '1'  # 管理员密码


    # 方法
    # 管理员登陆界面
    def printAdminView(self):
        print('*************************************************')
        print('*                                               *')
        print('*                                               *')
        print('*                                               *')
        print('*                欢迎登陆暴富银行                 *')
        print('*                                               *')
        print('*                                               *')
        print('*                                               *')
        print('*************************************************')


    # 系统功能界面
    def printSysFunctionView(self):
        print('****************************************************')
        print('*--------------------------------------------------*')
        print('*                                                  *')
        print('*      开户(open1)              查询(search)         *')
        print('*      取款(withdrawal)         存款(deposit)        *')
        print('*      转账(transfer)           改密(passwd)         *')
        print('*      锁定(lock)               解锁(unlock)         *')
        print('*      补卡(reissue)            销户(closing)        *')
        print('*                                                   *')
        print('*                    退出(quit1)                    *')
        print('*                                                   *')
        print('*- - - - - - - - - - - - - - - - - - - - - - - - - -*')
        print('****************************************************')



    # 管理员账号输入
    def adminOption(self):
        # 管理员账号输入
        inputAdmin = input('请输入管理员账号：')
        # 验证管理员输入账号是否正确
        if self.admin != inputAdmin:
            print('账号输入有误！!')
            return -1  # 如果执行到return语句，程序就会结束

        # 管理员密码输入
        inputPasswd = input('请输入管理员密码：')
        # 验证管理员密码是否正确
        if self.passwd != inputPasswd:
            print('密码输入有误！!')
            return -1

        # 执行到这里说明账号密码输入正确
        print('操作成功 请稍后...')
        # 程序休眠
        time.sleep(2)
        return 0







