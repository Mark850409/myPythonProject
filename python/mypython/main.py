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
from werkzeug.exceptions import HTTPException, default_exceptions

app = Flask(__name__)

@app.route('/')
def index():
    config = configparser.ConfigParser()
    config.read('my_config.ini')
    username = config['DB']['username']
    db = config['DB']['db']
    host = config['DB']['host']
    pw = config['DB']['password']
    # print("user:",username,"db:",db,"host:",host)
    
     # 建立資料庫連接
    db = pymysql.connect(
      host= host,
      user= username,
      password= pw,
      database= db,
      ssl_disabled='True')
    
    cursor = db.cursor()

    # 讀取資料
    cursor.execute("SELECT * FROM stock_list limit 5;")
    rows = cursor.fetchall()
    #print("Read",cursor.rowcount,"row(s) of data.")

    # 印出資料
    #for row in rows:
     # print(row)

    # 釋放連線
    db.commit()
    cursor.close()
    db.close()
    
    return render_template("index.html",rows=rows)

    
# 啟動CGI SERVER
if __name__ == "__main__":
  CGIHandler().run(app)
