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
    cursor2 = db.cursor()

    # 讀取資料
    cursor.execute("""SELECT (@i:=@i+1) i,t.table_name,(CASE t.table_name
			WHEN 'stock_daily' THEN '每日收盤資訊' 
            WHEN 'stock_daily_3' THEN '每月營收' 
            WHEN 'stock_daily_mr' THEN '三大法人進出' 
            WHEN 'stock_daily_mt' THEN '主力進出' 
            WHEN 'stock_list' THEN '證券清冊' 
            WHEN 'stock_monthly_revenue' THEN '融資融券' 
			END) as table_desc 
            FROM information_schema.tables t ,(select @i:=0) as i
            WHERE t.table_schema = 'stock' AND t.table_type='BASE TABLE' AND t.table_name <> 'stock_all_data';
           """)
    rows = cursor.fetchall()



    # 讀取資料
    cursor2.execute("SELECT * FROM stock.stock_all_data;")
    rows2 = cursor2.fetchall()
    #print("Read",cursor.rowcount,"row(s) of data.")

    # 印出資料
    #for row in rows:
     # print(row)

    # 釋放連線
    db.commit()
    cursor.close()
    db.close()
    
    return render_template("index.html",rows=rows,rows2=rows2)

    
# 啟動CGI SERVER
if __name__ == "__main__":
  CGIHandler().run(app)
