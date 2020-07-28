<!--
 * @Descripttion: 项目的版本修改内容记录
 * @version: 0.0.1
 * @Author: Zefeng Neo Zhu
 * @Date: 2020-07-13 10:43:59
 * @LastEditors: Zefeng Neo Zhu
 * @LastEditTime: 2020-07-27 15:58:46
--> 
# Finance Information System


20200713 version0.0.1
1. 从REFD项目中导入数据，并将项目升级成为FIS，保存所有财务数据用于后续的分析

20200713 version0.0.2
1. 调整get_trial_balance_data_and_change_format()函数输出的数据列表(data_list[2])的格式，去除1~5级会计科目字段
2. 调整get_trial_balance_data_and_change_format()函数输出的内容，增加“期间”元素(datalist[1])
3. 修改代码格式及bug修复

20200715 version0.0.3
1. 增加创建如下数据表的SQL语句：
        md_maping_account_code_and_account_titles
        md_project_name_of_finance_report
        md_maping_row_of_fr_and_account_code
        ad_customers_and_suppliers_balance
2. 增加get_customers_and_suppliers_balance_data_and_change_format()函数
3. 修改文字描述错误

20200718 version0.0.4
1. 调整项目架构，models存在数据库相关信息；views存储相关函数；main为主程序入口
2. 增加open_database()函数，用于打开数据库进行后续操作

20200727 version0.0.5
1. 计算项目值函数calculate_value_of_project()输出内容增加一列“项目名称”
2. 调整计算项目值函数calculate_value_of_project()数据的数据值格式为保留2位小数