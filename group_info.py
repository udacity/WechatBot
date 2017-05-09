#-*- coding: utf-8 -*-
#encoding=utf-8

# 登录
import time 
from wxpy import *
bot = Bot(cache_path=True)
# 拿到群信息
def group_info_get(group_type):
        '''input: group_type
        return:a dictionary of group name: group members count.
        '''
        # 判断是哪些群
        if group_type == 'IPND':
                name = 'Udacity-编程入门-'

        if group_type=='DAND':
                name='Udacity-数据分析-'
        global sheetname
        sheetname=group_type
        # 获取群
        # 问题：找到的群变少了？？？？？？？
        # 解决：群必须保存到通讯录才抓得到
        my_groups=bot.groups().search(name)
        # 得到群成员数量
        group_info={group.name : len(group) for group in my_groups}
        print(group_info)
        return group_info


# 更新到google sheet

# 获取权限
t0 = time.clock()
import gspread

from oauth2client.service_account import ServiceAccountCredentials

def auth_gss_client(path, scopes):
    try:
        credentials = ServiceAccountCredentials.from_json_keyfile_name(path,scopes)
    except ConnectionResetError: 
        print('Handle Exception')                                                        
    finally:
        return gspread.authorize(credentials)

# 不同文档设置
# 1.將文档分享給剛剛的 auth.json 裡 client_email 欄位提到的 email 帳號： 460234785235-compute@developer.gserviceaccount.com，並給予編輯的權限
# 2.在文档网址的https://docs.google.com/spreadsheets/d/{key}/edit 的 {key}
#测试spreadsheet_key='1aO74sl41lGlCkQb2mdcq0SBxjkf30mQAmdthmhT0JP0'
spreadsheet_key='1KbWUhQcuKsY--ARwRTUbeAsU_qmRDXnA56E2m-EOzfk'
# 路径
auth_json_path = '/Users/apple/Downloads/auth.json'
gss_scopes = ['https://spreadsheets.google.com/feeds']

gss_client = auth_gss_client(auth_json_path, gss_scopes)
print(time.clock() - t0, "seconds to get access")
# 更新表
def update(group_info):
        t1 = time.clock()
        today = time.strftime("%c")
        # 打开表
        spreadsheet = gss_client.open_by_key(spreadsheet_key)
        # 选中worksheet
        worksheet=spreadsheet.worksheet(sheetname)
        # 插入新行在第二行
        # [0]时，时间会自己变成12/30/1899
        worksheet.insert_row([''], index=2)
        # 找到对应的名字
        for group_name in group_info:
                # 群名在表里了吗
                try:
                        group_col=worksheet.find(group_name)
                        # 填入群信息
                        worksheet.update_cell(2,group_col.col, int(group_info[group_name]))
                except:
                        print('New group needs to add manually:',group_name,':',group_info[group_name])

        # 求和
        print('本行值为：',worksheet.row_values(2))
        row_values=worksheet.row_values(2)
        total=0
        for row_value in row_values:
            if row_value!='':
                total=int(row_value)+total
        print('sum is ',total)
        worksheet.update_acell('C2',total)
        #求增减
        worksheet.update_acell('B2',(int(worksheet.acell('C2').value)-int(worksheet.acell('C3').value)))
        # 插入时间
        worksheet.update_acell('A2',today)
        # 打印
        print(sheetname, ' Update completed')
        print(time.clock() - t1, "seconds to update.")

        # answer=input('more info? Y/N')
        # if answer=='Y':
        #         get()

        # TypeError: append_row() takes 2 positional arguments but 3 were given
        # worksheet.append_row(today,group_info.values)

# 启动
def get():
        #update(group_info_get(input('group type is: ')))
        update(group_info_get('IPND'))
        update(group_info_get('DAND'))
        # 遇到问题:不能同时传递get返回的group_info 和group_type
get()


# 高级:crontab自动执行 But微信登录需要扫码 还是手动吧。。。
# API问题
# 公司网络下不行 OSError: [Errno 65] No route to host
# 小手机的热点也不行
# 4.19凌晨 宿舍[Errno 54] Connection reset by peer
# NO 原因可能是服务器上 ssl_protocols TLSv1.2 TLSv1.1 已经不支持 TLSv1 ，没有 TLSv1 的支持， MAC 里的 OpenSSL 不是最新版本就会出现这个错误。
# 解决方案：服务器开 TLSv1 支持，或者更新自己电脑的 OpenSSL 。
