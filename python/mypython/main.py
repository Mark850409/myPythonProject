#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from flask import Flask
import pymysql
import os
import sys
import configparser
app = Flask(__name__)



@app.route("/")   
def index():

    auth_ticket = sys.argv[1]
    print(auth_ticket)
     # # 取得資料庫設定檔
    # config = configparser.ConfigParser()
    # config.read("my_config.ini")
    # config.add_section('section_b')
    # config.set('section_b', 'meal_val', 'spam')
    # config.set('section_b', 'not_found_val', '404')

    # # save to a file
    # with open('my_config.ini', 'w') as configfile:
        # config.write(configfile)
    # print(configfile)
    
    # meal_val = config.get("section_b", "meal_val")
    # not_found_val = config.get("section_b", "not_found_val")
    # print(meal_val)
    # print(not_found_val)
    # # 建立資料庫連接
    # db = pymysql.connect(
      # host= config.get("DB", "host"),
      # user= config.get("DB", "username"),
      # password= config.get("DB", "password"),
      # database=config.get("DB", "db"),
      # ssl_disabled='True')
    
    # cursor = db.cursor()

    # # 讀取資料
    # cursor.execute("SELECT * FROM stock_list;")
    # rows = cursor.fetchall()
    # print("Read",cursor.rowcount,"row(s) of data.")

    # # 印出資料
    # for row in rows:
      # print(row)

    # # 釋放連線
    # db.commit()
    # cursor.close()
    # db.close()

    return "Done"
# 啟動CGI SERVER
if __name__ == "__main__":
  CGIHandler().run(app)