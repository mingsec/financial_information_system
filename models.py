# -*- coding: UTF-8 -*-

"""
    ORM 全称 Object Relational Mapping，中文译为对象关系映射，
    简单的说就是在数据库与业务实体对象之间建立了一种对应关系，我们可以用操作实体对象的方式来完成数据库的操作，
    ORM 封装了数据库操作，我们无需关心底层数据库是什么，也不用关心 SQL 语言，只需与数据对象交互即可
"""

import pymysql
import SQLAlchemy

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String


'''  创建数据库连接 '''
# sqlite创建数据库连接格式：
    # --以绝对路径形式创建数据库
    # --创建内存数据库（其他数据库不可以）
    # --以相对路径形式在当前目录下创建数据库
    # echo:
    # --默认为 False，表示不打印执行的 SQL 语句等较详细的执行信息;
    # --改为 Ture 表示让其打印
    # check_same_thread:
    # --sqlite 默认建立的对象只能让建立该对象的线程使用，而 sqlalchemy 是多线程的;
    # --所以我们需要指定 check_same_thread=False 来让建立的对象任意线程都可使用;
    # --否则就会报错
    # engine = create_engine('sqlite:///C:\\path\\to\\foo.db')
    # engine = create_engine('sqlite://') or engine = create_engine('sqlite:///:memory:', echo=True)
engine = create_engine('sqlite:///finance_information_system.db?check_same_thread=False', echo=Ture) 

# PostgreSQL数据库创建数据库连接格式：
# engine = create_engine('postgresql+psycopg2://scott:tiger@localhost/mydatabase')

# MySQL数据库创建数据库连接格式：
    # echo：
    # --值为 True 将执行语句打印出来，默认为 False
    # pool_size：
    # --连接池的大小，默认为 5，0 表示连接数无限制
    # pool_recycle：
    # --设置了 pool_recycle 后，SQLAlchemy 会在指定时间内回收连接，单位为秒
# engine = create_engine('mysql://root:root@localhost:3306/mysql', echo=True, pool_size=10, pool_recycle=3600)

''' 创建表 '''
# 表的创建通过映射类的方式实现,首先创建映射基类，后面的类再继承它
# 映射基类
Base = declarative_base()

# 自定义具体映射类 MdMapingAccountCodeAndAccountTitles，其继承上一步创建的 Base
class MdMapingAccountCodeAndAccountTitles(Base):
    # 指定本类映射到 md_maping_account_code_and_account_titles 表，即指定映射表名
    # 如果有多个类指向同一张表，那么在后边的类需要把 extend_existing 设为 True，表示在已有列基础上进行扩展
    # 如果表在同一个数据库服务（datebase）的不同数据库中（schema），可使用 schema 参数进一步指定数据库，或者换句话说，sqlalchemy 允许类是表的字集
    __tablename__ = 'md_maping_account_code_and_account_titles'
    # __table_args__ = {'extend_existing': True}
    # __table_args__ = {'schema': 'test_database'}
    
    # *************************************************************************
    # 各变量名一定要与表的各字段名一样，因为相同的名字是他们之间的唯一关联关系
    # 从语法上说，各变量类型和表的类型可以不完全一致，如表字段是 String(64)，但我就定义成 String(32)
    # 但为了避免造成不必要的错误，变量的类型和其对应的表的字段的类型还是要相一致
    # sqlalchemy 强制要求必须要有主键字段不然会报错，如果要映射一张已存在且没有主键的表，那么可行的做法是将所有字段都设为 primary_key=True
    # 不要看随便将一个非主键字段设为 primary_key，然后似乎就没报错就能使用了，sqlalchemy 在接收到查询结果后还会自己根据主键进行一次去重
    # *************************************************************************

    # 指定id映射到id字段; id字段为整型，为主键，自动增长（其实整型主键默认就自动增长）
    # 指定name映射到name字段; name字段为字符串类形，
    id = Column(Integer, primary_key=True, autoincrement=True)
    account_code = name = Column(String(20))               CHAR(12) NOT NULL,
  first_level_account_title   CHAR(12),
  second_level_account_title  CHAR(15),
  third_level_account_title   CHAR(12),
  fourth_level_account_title  CHAR(12),
  fifth_level_account_title   CHAR(12),
  first_level_account_code
    id = Column(Integer, primary_key=True, autoincrement=True)

    name = Column(String(20))
    fullname = Column(String(32))
    password = Column(String(32))

    # __repr__方法用于输出该类的对象被print()时输出的字符串，如果不想写可以不写
    def __repr__(self):
        return "<User(name='%s', fullname='%s', password='%s')>" % (
                   self.name, self.fullname, self.password)