#!/usr/bin/python3
from wsgiref.handlers import CGIHandler
from flask import Flask
import pymysql
import os
app = Flask(__name__)

#這邊建立MYSQL連線資訊

@app.route("/")   
def index():
    return "Hello World 20231026"
# 啟動CGI SERVER
if __name__ == "__main__":
  CGIHandler().run(app)