#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from flask import Flask
from flask import render_template
import pymysql
import os
import sys
import configparser
import traceback
import sys
from werkzeug.exceptions import HTTPException




app = Flask(__name__,template_folder='python/mypython/template')


@app.errorhandler(Exception)
def handle_exception(e):
    # pass through HTTP errors
    if isinstance(e, HTTPException):
        return e

    # now you're handling non-HTTP exceptions only
    return render_template("500_generic.html", e=e), 500



@app.route("/")   
def index():

#  # 建立資料庫連接
#     db = pymysql.connect(
#       host='mysqlforpython.mysql.database.azure.com',
#       user='markhsu',
#       password='Mypython_850409',
#       database='stock',
#       ssl_disabled='True')
    
#     cursor = db.cursor()

#     # 讀取資料
#     cursor.execute("SELECT * FROM stock_list limit 5;")
#     rows = cursor.fetchall()
#     print("Read",cursor.rowcount,"row(s) of data.")

#     # 印出資料
#     for row in rows:
#       print(row)

#     # 釋放連線
#     db.commit()
#     cursor.close()
#     db.close()

     return render_template('mypython.html')
    
# 啟動CGI SERVER
if __name__ == "__main__":
  #CGIHandler().run(app)
  app.run()