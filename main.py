'''
@Descripttion: 
@version: 
@Author: Zefeng Neo Zhu
@Date: 2020-07-18 10:27:04
@LastEditors: Zefeng Neo Zhu
@LastEditTime: 2020-07-27 15:51:02
'''


import pymysql

from views import *


if __name__ == "__main__":
    ''' 使用 pymysql 创建 MySQL 数据库连接 '''
    FADB = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        db='finance_information_system',
        user='root', 
        password='330715', 
    )

    ''' 使用 psycopg2 创建 PostgreSQL 数据库连接 '''
    #FADB = psycopg2.connect(
    #    host='',
    #    port='5432',
    #    database='finance_analysis',
    #    user='postgres',
    #    password='330715'
    #)

    ''' 创建数据库游标 '''
    cursor = FADB.cursor()

    ''' 主要操作 '''
    type_of_operation = input("可执行的操作：\n  1 保存科目余额表数据\n  2 保存客商辅助余额表数据\n  3 生成财务报表\n请输入操作内容：")
    # 向数据库写入科目余额表数据
    if type_of_operation == '1':
        print(save_data_to_database(get_trial_balance_data_and_change_format(), cursor))
    # 向数据库写入客商辅助余额表数据
    elif type_of_operation == '2':        
        print(save_data_to_database(get_customers_and_suppliers_balance_data_and_change_format(), cursor))
    # 生成财务报表 
    elif type_of_operation == '3':        
        type_of_fs = int(input("可生成财务报表：\n  1 资产负债表\n  2 利润表\n  3 现金流量表\n请输入待生成的财务报表的类型："))
        account_period = int(input("请输入会计期间："))

        data_of_fs = generate_financial_statements(type_of_fs, account_period, cursor)

        print(f"{ data_of_fs[1] }期间的<{ data_of_fs[0] }>的数据如下:")
        for item in data_of_fs[2]:
            print(f"{ item[0] } { item[1] } : { item[2] }")
    else: 
        print("不支持的操作！")

    ''' 提交数据库操作 '''
    FADB.commit()

    ''' 关闭数据库连接 '''
    FADB.close()