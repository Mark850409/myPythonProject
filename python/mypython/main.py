#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from flask import Flask
import pymysql
import os
app = Flask(__name__)

#這邊建立MYSQL連線資訊

@app.route("/")   
def index():
    # 建立資料庫連接
    db = pymysql.connect(
      host='mysqlforpython.mysql.database.azure.com',
      user='markhsu',
      password='Mypython_850409',
      database='stock',
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