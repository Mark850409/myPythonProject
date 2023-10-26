#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from flask import Flask
import configparser
import pymysql
import os
app = Flask(__name__)

@app.route("/")   
def index():
    try:
        # 取得資料庫設定檔
        config = configparser.ConfigParser()
        config.read("my_config.ini")
         # 讀取資料庫變數
        username = config.get("DB", "username")
        password = config.get("DB", "password")
        db = config.get("DB", "db")
        host = config.get("DB", "host")
        ssl_disabled = config.getboolean("DB", "ssl_disabled")
        print("Name:", username, "PW:", password, "db:", db)
    except ConfigParser.NoOptionError as error:
           print(error)
    except ConfigParser.NoSectionError as error:
           print(error)
    except Exception as error:
           print(error)
    finally:
           print("沒有任何錯誤，可以進行資料庫查詢了!!!")


    # # 建立資料庫連接
    # db = pymysql.connect(**db_settings)
    
    # cursor = db.cursor()

    # # 讀取資料
    # cursor.execute("SELECT * FROM stock_all_data limit 10;")
    # rows = cursor.fetchall()
    # print("Read",cursor.rowcount,"row(s) of data.")

    # # 印出資料
    # for row in rows:
      # print(row)

    # # 釋放連線
    # db.commit()
    # cursor.close()
    # db.close()

    return "Success"
# 啟動CGI SERVER
if __name__ == "__main__":
  CGIHandler().run(app)