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
    # 取得資料庫設定檔
    config = configparser.ConfigParser()
    config.read("my_config.ini")

    # 宣告全域變數
    global result, connection, cursor
    # 讀取資料庫變數
    username = config.get("DB", "username")
    password = config.get("DB", "password")
    db = config.get("DB", "db")
    host = config.get("DB", "host")
    port = config.getint("DB", "port") #轉換成int型態才不會出錯
    # 資料庫設定
    db_settings = {
        "host": host,
        "port": port,
        "user": username,
        "password": password,
        "db": db,
        "charset": "utf8"
    }

    try:
        # 連接 MySQL/MariaDB 資料庫
        connection = pymysql.connect(**db_settings)  # 密碼
        cursor = connection.cursor()
        if connection.open:
           print("資料庫連接成功!!!")
    except Error as e:
           print("資料庫連接失敗!!!", e)
    finally:
        if connection.open:
           cursor.close()
           connection.close()

    return "Success"
# 啟動CGI SERVER
if __name__ == "__main__":
  CGIHandler().run(app)