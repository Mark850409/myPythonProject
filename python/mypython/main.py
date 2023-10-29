#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from functools import wraps
from flask import Flask, request, render_template, abort, jsonify, json
import pymysql
import os
import sys
import configparser
import traceback
import sys
from werkzeug.exceptions import HTTPException


app = Flask(__name__,template_folder='python/mypython/template')

@app.route('/')
def index():
    return render_template('mypython.html')

@app.errorhandler(500)
def error_500(exception):
    return jsonify({"error": str(exception)}), 500, {'Content-Type': 'application/json'}

@app.errorhandler(400)
def error_400(exception):
    return jsonify({"error": str(exception)}), 400, {'Content-Type': 'application/json'}

#@app.route("/")   
#def index():

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

   #  return render_template('mypython.html')
    
# 啟動CGI SERVER
if __name__ == "__main__":
  CGIHandler().run(app)
  #app.handle_http_exception = get_http_exception_handler(app)