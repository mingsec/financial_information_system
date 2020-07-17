/*
 * @Descripttion: 创建Finance_information_system的数据库，包括科目余额表、客商辅助余额表
 * @version: 0.0.1
 * @Author: Zefeng Neo Zhu
 * @Date: 2020-07-09 16:25:03
 * @LastEditors: Zefeng Neo Zhu
 * @LastEditTime: 2020-07-16 18:31:41
*/ 


-- Create finance_analysis database
CREATE DATABASE finance_information_system;


-- Create md_maping_account_code_and_account_titles table.
CREATE TABLE md_maping_account_code_and_account_titles(
  id                          INT NOT NULL AUTO_INCREMENT,
  account_code                CHAR(12) NOT NULL,
  first_level_account_title   CHAR(12),
  second_level_account_title  CHAR(15),
  third_level_account_title   CHAR(12),
  fourth_level_account_title  CHAR(12),
  fifth_level_account_title   CHAR(12),
  first_level_account_code    CHAR(4)  NOT NULL,
  PRIMARY KEY(id)
) ENGINE=InnoDB;


-- Create md_project_name_of_financial_statements table.
CREATE TABLE md_project_name_of_financial_statements(
  id                         INT NOT NULL AUTO_INCREMENT,
  version_of_fs              CHAR(6)  NOT NULL,
  type_of_fs                 CHAR(5)  NOT NULL,
  first_level_of_project     CHAR(20) NOT NULL,
  sencond_level_of_project   CHAR(25) NOT NULL,
  name_of_project            CHAR(30) NOT NULL,
  number_of_project          CHAR(6)  NOT NULL,
  PRIMARY KEY(id)
) ENGINE=InnoDB;


-- Create md_maping_row_of_fs_and_account_code table.
CREATE TABLE md_maping_row_of_fs_and_account_code(
  id                INT      NOT NULL AUTO_INCREMENT,
  version_of_fs     CHAR(6)  NOT NULL,
  number_of_project CHAR(6)  NOT NULL,
  add_or_subtract   DECIMAL(20,2) NOT NULL,
  source_of_data    CHAR(50) NOT NULL,
  account_code      CHAR(12) NOT NULL,
  debit_or_credit   CHAR(1)  NOT NULL,
  type_of_amount    CHAR(4)  NOT NULL,
  PRIMARY KEY(id)
) ENGINE=InnoDB;


-- Create ad_trial_balance table.
CREATE TABLE ad_trial_balance(
  id              INT NOT NULL AUTO_INCREMENT,
  account_period  CHAR(6)  NOT NULL,
  account_code    CHAR(12) NOT NULL,
  type_of_amount  CHAR(4)  NOT NULL,
  debit_or_credit CHAR(1)  NOT NULL,
  amount          DECIMAL(20,2) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=InnoDB;


-- Create ad_customers_and_suppliers_balance table.
CREATE TABLE ad_customers_and_suppliers_balance(
  id                                INT NOT NULL AUTO_INCREMENT,
  account_period                    CHAR(6) NOT NULL,
  account_code                      CHAR(12) NOT NULL,
  name_of_customer_or_supplier      CHAR(50) NOT NULL,
  type_of_amount                    CHAR(4)  NOT NULL,
  debit_or_credit                   CHAR(1)  NOT NULL,
  amount                            DECIMAL(20,2) NOT NULL,
  PRIMARY KEY(id)
) ENGINE=InnoDB;

