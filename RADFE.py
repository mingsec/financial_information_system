'''
@Descripttion:从Excel读取财务数据，并保存至新的Excel文档或数据库 
@version: 0.0.1
@Author: Zefeng Neo Zhu
@Date: 2020-07-10 10:19:10
@LastEditors: Zefeng Neo Zhu
@LastEditTime: 2020-07-16 18:38:01
'''
# -*- coding: UTF-8 -*-


import xlwt
import xlrd
from xlutils.copy import copy;
import re 
import pymysql
#import psycopg2
from decimal import Decimal, getcontext


def get_trial_balance_data_and_change_format(filename='./OriginData/科目余额表2020.xls'):
    """转换科目余额表数据格式

    将科目余额表中的复杂表头数据转化为一维数据表
    
    参数
    ------
    filename : str
        科目余额表的存放位置及文件名，含文件格式后缀
    
    返回值
    ------
    list：
        返回转换好格式后的数据：
        list[0]为待保存的数据的表格名称；
        list[1]为待保存的数据的会计期间；
        list[2]为待保存的数据，类型为列表(list)

    """
 
    ''' 打开并读取 Excel 文件中的数据 '''
    origin_workbook = xlrd.open_workbook(filename)
    origin_sheet = origin_workbook.sheets()[-1]

    ''' 获取 Excel 的最大行、列数 '''
    max_row = origin_sheet.nrows
    max_col = origin_sheet.ncols

    ''' 获取会计期间 '''
    # 判读取得的数据是单月数据还是累计数据
    # 如果为单月数据则生成期间字段，否则提示错误
    origin_period = re.findall('\d+', origin_sheet.cell_value(5, 0)) 
    if origin_period[1] == origin_period[3]:
        period = int(origin_period[2] + origin_period[3])
    else:
        return "导入的数据有问题，请检查是否为当月数据。"

    ''' 获取其他数据 '''  
    format_data = []
    for row in range(9, max_row-4):
        # 获取会计科目
        account_code = origin_sheet.cell_value(row, 1).split('\\')[0]
        
        # 获取本期借方发生额并生成格式化数据
        if origin_sheet.cell_value(row, 4) != '':
            format_data.append([period, account_code, "本期借方","借", origin_sheet.cell_value(row, 4)])

        # 获取本期贷方发生额并生成格式化数据
        if origin_sheet.cell_value(row, 5) != '':
            format_data.append([period, account_code, "本期贷方","贷", origin_sheet.cell_value(row, 5)]) 
             
        # 获取期末余额并生成格式化数据
        if origin_sheet.cell_value(row, 9) != '':
            format_data.append([period, account_code, "期末余额",origin_sheet.cell_value(row, 8), origin_sheet.cell_value(row, 9)])
      
    print(f"{ period }期间的<科目余额表>数据转换成功！")
    
    return ("科目余额表", period, format_data)


def get_customers_and_suppliers_balance_data_and_change_format(filename='./OriginData/客商余额表2020.xls'):
    """转换客商辅助余额表数据格式

    将客商辅助余额表中的复杂表头数据转化为一维数据表
    
    参数
    ------
    filename : str
        客商辅助余额表的存放位置及文件名，含文件格式后缀
    
    返回值
    ------
    list：
        返回转换好格式后的数据：
        list[0]为待保存的数据的表格名称；
        list[1]为待保存的数据的会计期间；
        list[2]为待保存的数据，类型为列表(list)

    """

    ''' 打开并读取 Excel 文件中的数据 '''
    origin_workbook = xlrd.open_workbook(filename)
    origin_sheet = origin_workbook.sheets()[-1]

    ''' 获取 Excel 的最大行、列数 '''
    max_row = origin_sheet.nrows
    max_col = origin_sheet.ncols

    ''' 获取会计期间 '''
    # 判读取得的数据是单月数据还是累计数据
    # 如果为单月数据则生成期间字段，否则提示错误
    origin_period = re.findall('\d+', origin_sheet.cell_value(6, 0)) 
    if origin_period[1] == origin_period[3]:
        period = int(origin_period[2] + origin_period[3])
    else:
        return "导入的数据有问题，请检查是否为当月数据。"

    ''' 获取其他数据 '''  
    format_data = []
    for row in range(10, max_row-4):
        # 获取会计科目
        account_code = origin_sheet.cell_value(row, 1).split('\\')[0]

        # 获取客户、供应商的名称
        name_of_customer_or_supplier = origin_sheet.cell_value(row, 2)
        
        # 获取本期借方发生额并生成格式化数据
        if origin_sheet.cell_value(row, 5) != '':
            format_data.append([period, account_code, name_of_customer_or_supplier, "本期借方", "借", origin_sheet.cell_value(row, 5)])

        # 获取本期贷方发生额并生成格式化数据
        if origin_sheet.cell_value(row, 6) != '':
            format_data.append([period, account_code, name_of_customer_or_supplier, "本期贷方", "贷", origin_sheet.cell_value(row, 6)]) 
             
        # 获取期末余额并生成格式化数据
        if origin_sheet.cell_value(row, 10) != '':
            format_data.append([period, account_code, name_of_customer_or_supplier, "期末余额", origin_sheet.cell_value(row, 9), origin_sheet.cell_value(row, 10)])
      
    print(f"{ period }期间的<客商辅助余额表>数据转换成功！")
    
    return ("客商辅助余额表", period, format_data)


def save_data_to_excel(data_list, filename='./FormatData/财务分析数据.xls'):
    """保存数据

    将转化为一维数据表的科目发生额及余额存至Excel文档
    
    参数
    ------
    data_list : list
        待保存的数据列表
        
    filename : str
        Excel文档的存放位置及文件名，含文件格式后缀
    
    返回值
    ------
    str
        如果保存成功则输出“数据保存成功！”，否则提示“保存失败...”

    """

    ''' 根据数据的类型选择待追加数据的 sheet '''
    if data_list[0] == 'TB':
        sheet_index = 3
    elif data_list[0] == 'DE':
        sheet_index = 2

    ''' 打开并读取原 Excel 文件中的数据 '''
    origin_data = xlrd.open_workbook(filename, formatting_info=True)
    new_data = copy(wb=origin_data)
    new_sheet = new_data.get_sheet(sheet_index)

    ''' 获取原 Excel 文档的最大行数 '''
    origin_sheet = origin_data.sheet_by_index(sheet_index)
    max_row = origin_sheet.nrows

    ''' 将数据写入 Excel 文档 '''
    for value in data_list[1]:
        for i in range(len(value)):
            new_sheet.write(max_row, i, value[i])
        max_row = max_row + 1

    new_data.save(filename)

    return "数据保存成功..."


def save_data_to_database(data_list):
    """保存数据

    将转化为一维数据表的数据存至数据库
    
    参数
    ------
    data_list : list
        待保存的数据列表
    
    返回值
    ------
    str
        如果保存成功则输出“数据保存成功！”，否则提示“保存失败...”

    """

    ''' 根据表格类型选择追加数据的 table 和 fields '''
    if data_list[0] == "科目余额表":
        table = 'ad_trial_balance'
        fields = '(account_period, account_code, type_of_amount, debit_or_credit, amount)'
        field_values = r'%s, %s, %s, %s, %s'
    elif data_list[0] == '客商辅助余额表':
        table = 'ad_customers_and_suppliers_balance'
        fields = '(account_period, account_code, name_of_customer_or_supplier, type_of_amount, debit_or_credit, amount)'
        field_values = r'%s, %s, %s, %s, %s, %s'
        
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

    ''' 查询相关数据是否已经保存到了数据库中, 如果返回结果为None，则保存数据；否则提示错误信息 '''
    # cursor.execute() 查询数据是否已在于数据库，0表示不存在
    # cursor.executemany() 用于执行写入数据的 SQL 语句，实现批量写入数据
    # FADB.commit() 提交数据库操作，保存操作结果
    # result 表示执行结果，用于函数返回值
    if cursor.execute(f'SELECT * FROM { table } WHERE account_period = { data_list[1] }') == 0:
        cursor.executemany(f'INSERT INTO { table } { fields } VALUES ( { field_values } )', data_list[2])
        FADB.commit()
        result = f"保存成功：{ data_list[1] }期间的<{ data_list[0] }>数据成功写入数据库..."
    else :
        result = f"保存失败：{ data_list[1] }期间的<{ data_list[0] }>数据已存在于数据库中，退出保存过程..."

    ''' 关闭数据库连接 '''
    FADB.close()

    return result


def get_projects_of_fs(type_of_fs, cursor, version_of_fs='202006'):
    """获取财务报表项目
    
    根据输入的财务报表版本和报表类型参数获取财务报表的项目的行次
    
    参数
    ------
    type_of_fs : int
        财务报表的类型: 1-资产负债表; 2-利润表; 3-现金流量表

    cursor : cursor()
        数据库游标
      
    version_of_fs : str
        财务报表的版本，默认为202006版
    
    返回值
    ------
    list：
        list[0]: 财务报表的类型
        list[1]: 财务报表的版本
        list[2]: 包含财务报表所有非汇总项目的行次(编号)的列表
        
    """

    ''' 确定财务报表的版本 '''
    input_version_of_fs = input("请输入财务报表的版本，默认为202006版：")
    if input_version_of_fs:
        version_of_fs = input_version_of_fs

    ''' 获取 md_project_name_of_financial_statements 表的 type_of_fs 字段的值 '''
    if type_of_fs == 1:
        field_value = "资产负债表"
    elif type_of_fs == 2:
        field_value = "利润表"
    elif type_of_fs == 3:
        field_value = "现金流量表"

    ''' 执行 SQL 查询语句，获取财务报表所有非汇总项目的行次 '''
    cursor.execute(f"SELECT DISTINCT number_of_project FROM md_project_name_of_financial_statements \
        WHERE version_of_fs='{ version_of_fs }' AND type_of_fs='{ field_value }'")
    
    ''' 将查询结果转化为 list '''
    rows = cursor.fetchall()
    number_of_projects = []
    if rows:
        for item in rows:
            number_of_projects.append(item[0])
    else:
        print("未查询到相关记录，请检查版本和报表类型数据是否正确...") 

    return [field_value, version_of_fs, number_of_projects]


def get_calculated_rules_of_project(projects, cursor, version_of_fs='202006'): 
    """获取财务报表项目的计算规则
    
    根据输入的财务报表版本和财务报表项目参数获取该项目的值的计算规则
    
    参数
    ------
   project : list
        财务报表项目的行次：前缀BS：资产负债表；前缀PL：利润表；前缀CF：现金流量表
        
    cursor : cursor()
        数据库游标
            
    version_of_fs : str
        财务报表的版本，默认为202006版
    
    返回值
    ------
    list：
        返回一个包含特定财务报表项目的值的计算规则的列表
        
    """

    ''' 执行 SQL 查询语句，获取财务报表项目的计算规则，并组合成list '''
    calculated_rules_of_projects = []
    for project in projects:
        cursor.execute(f"SELECT add_or_subtract, source_of_data, account_code, debit_or_credit, type_of_amount \
            FROM md_maping_row_of_fs_and_account_code WHERE version_of_fs='{ version_of_fs }' AND number_of_project='{ project }'")

        rules = cursor.fetchall()

        calculated_rules_of_projects.append([project, rules])

    return calculated_rules_of_projects


def calculate_value_of_project(rules, account_period, cursor):
    """计算财务报表项目的值
    
    根据财务报表项目的计算规则获取数据计算出该项目的值
    
    参数
    ------
    rules : list
        list[0]: 财务报表项目的行次（编号）
        list[1]: 财务报表项目的计算规则，为一个元组；当某个项目有多条计算规则时可以嵌套：
            tuple[0]：加或减去该规则的计算结果
            tuple[1]：数据来自何表
            tuple[2]：会计科目
            tuple[3]：借贷方向，主要是针对期末余额
            tuple[4]：金额类型，是本期借方发生额、贷方发生额还是期末余额
    
    account_period : str
        待计算数值的财务报表项目的会计期间
    
    cursor : cursor()
        数据库游标

    返回值
    ------
    list：
        list[0]: 财务报表项目的行次（编号）
        list[1]: 该财务报表项目的值，保留两位小数
        
    """

    ''' 设置计算数值的精度和返回值的类型 '''
    getcontext().prec = 22

    ''' 执行 SQL 查询语句，计算财务报表项目的值 '''
    # 按顺序执行各个项目的计算规则
    # 如果该项目的计算规则为空则跳过；
    # 否则按顺序执行各项目的计算规则，
    # 并对这些项目的值进行求和
    project_and_his_value = []
    for rule in rules:
        if rule[1]:
            value =  Decimal('0')
            for line in rule[1]:
                cursor.execute(f"SELECT SUM(amount) FROM { line[1] } \
                    WHERE account_period='{ account_period }' AND account_code = '{ line[2] }' \
                    AND debit_or_credit='{ line[3] }' AND type_of_amount='{ line[4] }'")
                values = cursor.fetchone()
                if values[0]:
                    value = value + values[0]*line[0]

            project_and_his_value.append([rule[0], value])
            
    return project_and_his_value


def generate_financial_statements(type_of_fs, account_period):
    """生成财务报表

    根据数据库中的数据自动生成财务报表
    
    参数
    ------
    type_of_fs : int
        待生成的财务报表类型：1-资产负债表；2-利润表；3-现金流量表
    
    account_period : int
        待计算的财务报表的会计期间
    
    返回值
    ------
    list：
        返回财务报表数据：
        list[0]为所计算的财务报表的名称；
        list[1]为所计算的财务报表的会计期间；
        list[2]为计算出的财务报表数据，类型为列表(list)

    """

    ''' 使用 pymysql 创建 MySQL 数据库连接 '''
    FADB = pymysql.connect(
        host='127.0.0.1',
        port=3306,
        db='finance_information_system',
        user='root', 
        password='330715', 
    )

    ''' 创建数据库游标 '''
    cursor = FADB.cursor()

    ''' 获取财务报表的项目 '''
    projects = get_projects_of_fs(type_of_fs, cursor)

    ''' 获取财务报表项目的计算规则 '''
    rules = get_calculated_rules_of_project(projects[2], cursor, projects[1])

    ''' 计算财务报表项目的值 '''
    values = calculate_value_of_project(rules, account_period, cursor)


    if type_of_fs == 1:
        table = "资产负债表"
    elif type_of_fs == 2:
        table = "利润表"
    elif type_of_fs == 3:
        table = "现金流量表"

    return [table, account_period, values]

    
if __name__ == "__main__":
    ''' 向数据库写入科目余额表数据 '''
    #print(save_data_to_database(get_trial_balance_data_and_change_format()))

    ''' 向数据库写入客商辅助余额表数据 '''
    #print(save_data_to_database(get_customers_and_suppliers_balance_data_and_change_format()))
    
    ''' 生成财务报表 '''
    type_of_fs = int(input("可生成财务报表：\n 1  资产负债表\n 2  利润表\n 3  现金流量表\n请输入待生成的财务报表的类型："))
    account_period = int(input("请输入会计期间："))

    data_of_fs = generate_financial_statements(type_of_fs, account_period)

    print(f"{ data_of_fs[1] }期间的<{ data_of_fs[0] }>的数据如下:")
    for item in data_of_fs[2]:
        print(f"{ item[0] } : { item[1] }")