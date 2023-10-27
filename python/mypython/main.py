#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from flask import Flask
import configparser
import pymysql
import os
import sys
from MySQLdb import Error
app = Flask(__name__)

@app.route("/")   
def index():
    # 宣告全域變數
    global result, connection, cursor
       
     # 取得資料庫設定檔
    config = configparser.ConfigParser()
    config.read("my_config.ini")

    try:
        # 連接 MySQL/MariaDB 資料庫
          # 建立資料庫連接
        db = pymysql.connect(
          host= config.get("DB", "host"),
          user= config.get("DB", "username"),
          password= config.get("DB", "password"),
          database= config.get("DB", "db"),
          ssl_disabled='True')
          
        if db.open:
           print("資料庫連接成功!!!")
        
        cursor = db.cursor()

        # 讀取資料
        cursor.execute("SELECT * FROM stock_list;")
        rows = cursor.fetchall()
        print("Read",cursor.rowcount,"row(s) of data.")

        # 印出資料
        for row in rows:
          print(row)
          
        db.commit()

    except Error as e:
           print("資料庫連接失敗!!!", e)
    finally:
        if db.open:
           cursor.close()
           db.close()

    return "Success"
# 啟動CGI SERVER
if __name__ == "__main__":
  CGIHandler().run(app)