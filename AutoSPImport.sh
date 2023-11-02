#!/bin/bash
# ====================================================================
# bash script Name     : procCreateTableSchema
# Function    : CreateStockTable
# Author      : Mark
# Create Date : 2023-10-26
# Parameter   : 
# Modify His  : 
# ===================================================================
#參數定義
USER=markhsu
PASSWORD=Mypython_850409
HOST=mysqlforpython1102.mysql.database.azure.com
DB=stock
SQL_NAME=procCreateTableSchema.sql
#如果資料庫不存在就建立一個新的
mysql -h $HOST -u $USER -p$PASSWORD -e "source $SQL_NAME;" -e "use $DB;"  && \
mysql -h $HOST -u $USER -p$PASSWORD -e "use $DB;" -e 'call procExportTableSchemaAndInsertTable("stock");' 