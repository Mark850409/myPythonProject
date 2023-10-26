#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from flask import Flask
import configparser
import pymysql
import os
app = Flask(__name__)

#這邊建立MYSQL連線資訊

# 取得資料庫設定檔
config = configparser.ConfigParser()
config.read("my_config.ini")
# 讀取資料庫變數
username = config.get("DB", "username")
password = config.get("DB", "password")
db = config.get("DB", "db")
host = config.get("DB", "host")
ssl_disabled = config.getint("DB", "ssl_disabled") #轉換成int型態才不會出錯
# 資料庫設定
db_settings = {
    "host": host,
    "ssl_disabled": ssl_disabled,
    "user": username,
    "password": password,
    "db": db,
    "charset": "utf8"
}

@app.route("/")   
def index():
    # 建立資料庫連接
    db = pymysql.connect(**db_settings)
    
    cursor = db.cursor()

    # 讀取資料
    cursor.execute("SELECT * FROM stock_all_data limit 10;")
    rows = cursor.fetchall()
    print("Read",cursor.rowcount,"row(s) of data.")

    # 印出資料
    for row in rows:
      print(row)

    # 釋放連線
    db.commit()
    cursor.close()
    db.close()

    return "Done"
# 啟動CGI SERVER
if __name__ == "__main__":
  CGIHandler().run(app)