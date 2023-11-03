#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from flask import Flask,  render_template
import database

app = Flask(__name__)

# 資料庫首頁
@app.route('/')
def index():
     # 取得資料庫連線
    db = database.database()
     # 讀取總表
    stock_all_datas = db.getfetchallData("""
        SELECT (@i:=@i+1) i,t.table_name,(CASE t.table_name
                WHEN 'stock_daily' THEN '每日收盤資訊' 
                WHEN 'stock_daily_3' THEN '三大法人進出' 
                WHEN 'stock_daily_mr' THEN '主力進出' 
                WHEN 'stock_daily_mt' THEN '融資融券' 
                WHEN 'stock_list' THEN '證券清冊' 
                WHEN 'stock_monthly_revenue' THEN '每月營收' 
                END) as table_desc 
                FROM information_schema.tables t ,(select @i:=0) as i
                WHERE t.table_schema = 'stock' AND t.table_type='BASE TABLE' AND t.table_name <> 'stock_all_data'
                AND t.table_name not IN('stock_daily_3_db_normalization','stock_daily_mt_all','stock_daily_mt_financing','stock_daily_mt_securities')
               """)
    # 讀取每日收盤資訊
    stock_daily_list = db.getKeyValueData(
        "SELECT * FROM stock.stock_all_data where TABLE_TYPE='每日收盤資訊'")
    # 讀取三大法人進出
    stock_daily_3_list = db.getKeyValueData(
        "SELECT * FROM stock.stock_all_data where TABLE_TYPE='三大法人進出'")
    # 讀取主力進出
    stock_daily_mr_list = db.getKeyValueData(
        "SELECT * FROM stock.stock_all_data where TABLE_TYPE='主力進出'")
    # 讀取融資融券
    stock_daily_mt_list = db.getKeyValueData(
        "SELECT * FROM stock.stock_all_data where TABLE_TYPE='融資融券'")
    # 讀取證券清冊
    stock_list_all = db.getKeyValueData(
        "SELECT * FROM stock.stock_all_data where TABLE_TYPE='證券清冊'")
    # 讀取每月營收
    stock_monthly_revenue_list = db.getKeyValueData(
        "SELECT * FROM stock.stock_all_data where TABLE_TYPE='每月營收'")

    # 字典傳遞資料
    data = {
        'stock_all_datas': stock_all_datas,
        'stock_daily_list': stock_daily_list,
        'stock_daily_3_list': stock_daily_3_list,
        'stock_daily_mr_list': stock_daily_mr_list,
        'stock_daily_mt_list': stock_daily_mt_list,
        'stock_list_all': stock_list_all,
        'stock_monthly_revenue_list': stock_monthly_revenue_list,
        'title': 'stock-資料檔案清單（DTL_Data Table List）'
    }
    # 關閉資料庫連線    
    db.close()
    # 渲染模板+資料傳送
    return render_template("index.html", **data)


# 資料庫正規化清單
@app.route('/db_normalization')
def index2():
    # 取得資料庫連線
    db = database.database()
    # 讀取總表
    stock_all_datas_normalization = db.getfetchallData("""SELECT (@i:=@i+1) i,t.table_name,(CASE t.table_name
                WHEN 'stock_daily_3_db_normalization' THEN '三大法人進出-正規化' 
                WHEN 'stock_daily_MT_All' THEN '融資融券總表-正規化' 
                WHEN 'stock_daily_MT_Financing' THEN '融資總表-正規化' 
                WHEN 'stock_daily_MT_Securities' THEN '融券總表-正規化' 
                END) as table_desc 
                FROM information_schema.tables t ,(select @i:=0) as i
                WHERE t.table_schema = 'stock' AND t.table_type='BASE TABLE' AND t.table_name <> 'stock_all_data' 
                AND t.table_name IN('stock_daily_3_db_normalization','stock_daily_mt_all','stock_daily_mt_financing','stock_daily_mt_securities');
               """)

    # 讀取三大法人進出資料
    stock_daily_3_db_normalization_list = db.getKeyValueData(
        "SELECT * FROM stock.stock_all_data where TABLE_TYPE='三大法人進出-正規化'")

    # 讀取融資融券總表-正規化資料
    stock_daily_MT_All_list = db.getKeyValueData(
        "SELECT * FROM stock.stock_all_data where TABLE_TYPE='融資融券總表-正規化'")

    # 讀取融資總表-正規化資料
    stock_daily_MT_Financing_all = db.getKeyValueData(
        "SELECT * FROM stock.stock_all_data where TABLE_TYPE='融資總表-正規化'")

    # 讀取融券總表-正規化資料
    stock_daily_MT_Securities_all = db.getKeyValueData(
        "SELECT * FROM stock.stock_all_data where TABLE_TYPE='融券總表-正規化'")

    # 字典傳遞資料
    data = {
        'stock_all_datas_normalization': stock_all_datas_normalization,
        'stock_daily_3_db_normalization_list': stock_daily_3_db_normalization_list,
        'stock_daily_MT_All_list': stock_daily_MT_All_list,
        'stock_daily_MT_Financing_all': stock_daily_MT_Financing_all,
        'stock_daily_MT_Securities_all': stock_daily_MT_Securities_all,
        'title': 'stock-資料正規化清單（db_normalization_Data Table List）'
    }
    # 關閉資料庫連線
    db.close()
    # 渲染模板+資料傳送
    return render_template("db_normalization.html", **data)


# 啟動CGI SERVER
if __name__ == "__main__":
    CGIHandler().run(app)
