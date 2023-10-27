#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from flask import Flask
import pymysql
import os
import configparser
app = Flask(__name__)

# 取得資料庫設定檔
config = configparser.ConfigParser()
config.read("my_config.ini")

# 讀取資料庫變數
global username, password, db,host,ssl_disabled
username = config.get("DB", "username")
password = config.get("DB", "password")
db = config.get("DB", "db")
host = config.get("DB", "host")
ssl_disabled = 'True' 

@app.route("/")   
def index():
    # 建立資料庫連接
    db = pymysql.connect(
      host= host,
      user= username,
      password= password,
      database=db,
      ssl_disabled='True')
    
    cursor = db.cursor()

    # 讀取資料
    cursor.execute("SELECT * FROM stock_list;")
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