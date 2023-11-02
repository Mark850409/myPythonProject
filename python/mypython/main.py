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
import collections

app = Flask(__name__)

# 資料庫首頁
@app.route('/')
def index():
    # 讀取ini設定檔
    config = configparser.ConfigParser()
    config.read('my_config.ini')
    username = config['DB']['username']
    db = config['DB']['db']
    host = config['DB']['host']
    pw = config['DB']['password']
    port = config['DB'].getint('port')
    
    # 建立資料庫連接
    db = pymysql.connect(
      host= host,
      user= username,
      password= pw,
      database= db,
      port=port,
      ssl_disabled = True)

     # 建立cursor
    cursor = db.cursor()

    # 讀取總表
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
    stock_all_datas = cursor.fetchall()



    # 讀取每日收盤資訊資料
    cursor.execute("SELECT * FROM stock.stock_all_data where TABLE_TYPE='每日收盤資訊'")
    stock_daily = cursor.fetchall()
    stock_daily_list = []
    for row in stock_daily :
        d = collections.OrderedDict()
        d['COLUMN_NAMES']  = row[0] #name
        d['DATA_TYPE']   = row[1] #lname
        d['IS_NULLABLE']      = row[2] #email
        d['COLUMN_KEY']      = row[3] #email
        d['DESCS']      = row[4] #email
        d['TABLE_TYPE']      = row[5] #email
        stock_daily_list.append(d)


    # 讀取每月營收資料
    cursor.execute("SELECT * FROM stock.stock_all_data where TABLE_TYPE='每月營收'")
    stock_daily_3 = cursor.fetchall()
    stock_daily_3_list = []
    for row in stock_daily_3 :
        d = collections.OrderedDict()
        d['COLUMN_NAMES']  = row[0] #name
        d['DATA_TYPE']   = row[1] #lname
        d['IS_NULLABLE']      = row[2] #email
        d['COLUMN_KEY']      = row[3] #email
        d['DESCS']      = row[4] #email
        d['TABLE_TYPE']      = row[5] #email
        stock_daily_3_list.append(d)


    #讀取三大法人進出資料
    cursor.execute("SELECT * FROM stock.stock_all_data where TABLE_TYPE='三大法人進出'")
    stock_daily_mr = cursor.fetchall()
    stock_daily_mr_list = []
    for row in stock_daily_mr :
        d = collections.OrderedDict()
        d['COLUMN_NAMES']  = row[0] #name
        d['DATA_TYPE']   = row[1] #lname
        d['IS_NULLABLE']      = row[2] #email
        d['COLUMN_KEY']      = row[3] #email
        d['DESCS']      = row[4] #email
        d['TABLE_TYPE']      = row[5] #email
        stock_daily_mr_list.append(d)


    # 讀取主力進出資料
    cursor.execute("SELECT * FROM stock.stock_all_data where TABLE_TYPE='主力進出'")
    stock_daily_mt = cursor.fetchall()
    stock_daily_mt_list = []
    for row in stock_daily_mt :
        d = collections.OrderedDict()
        d['COLUMN_NAMES']  = row[0] #name
        d['DATA_TYPE']   = row[1] #lname
        d['IS_NULLABLE']      = row[2] #email
        d['COLUMN_KEY']      = row[3] #email
        d['DESCS']      = row[4] #email
        d['TABLE_TYPE']      = row[5] #email
        stock_daily_mt_list.append(d)


    # 讀取證券清冊資料
    cursor.execute("SELECT * FROM stock.stock_all_data where TABLE_TYPE='證券清冊'")
    stock_list = cursor.fetchall()
    stock_list_all = []
    for row in stock_list :
        d = collections.OrderedDict()
        d['COLUMN_NAMES']  = row[0] #name
        d['DATA_TYPE']   = row[1] #lname
        d['IS_NULLABLE']      = row[2] #email
        d['COLUMN_KEY']      = row[3] #email
        d['DESCS']      = row[4] #email
        d['TABLE_TYPE']      = row[5] #email
        stock_list_all.append(d)


    # 讀取融資融券資料
    cursor.execute("SELECT * FROM stock.stock_all_data where TABLE_TYPE='融資融券'")
    stock_monthly_revenue = cursor.fetchall()
    stock_monthly_revenue_list = []
    for row in stock_monthly_revenue :
        d = collections.OrderedDict()
        d['COLUMN_NAMES']  = row[0] #name
        d['DATA_TYPE']   = row[1] #lname
        d['IS_NULLABLE']      = row[2] #email
        d['COLUMN_KEY']      = row[3] #email
        d['DESCS']      = row[4] #email
        d['TABLE_TYPE']      = row[5] #email
        stock_monthly_revenue_list.append(d)
    
    #字典傳遞資料
    data = { 
        'stock_all_datas': stock_all_datas,
        'stock_daily_list':stock_daily_list,
        'stock_daily_3_list':stock_daily_3_list,
        'stock_daily_mr_list':stock_daily_mr_list,
        'stock_daily_mt_list':stock_daily_mt_list,
        'stock_list_all':stock_list_all,
        'stock_monthly_revenue_list':stock_monthly_revenue_list,
        'title':'stock-資料檔案清單（DTL_Data Table List）'
    }

    db.commit()
    
    # 釋放連線
    cursor.close()
    db.close()
    
    # 渲染模板+資料傳送
    return render_template("index.html",**data)
    
    
# 資料庫正規化清單
@app.route('/db_normalization')
def index2():
    return render_template("db_normalization.html",title='stock-資料正規化清單（db_normalization_Data Table List）')

# 啟動CGI SERVER
if __name__ == "__main__":
  CGIHandler().run(app)