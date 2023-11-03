import pymysql
import configparser
import collections

class database :
    conn = ""
    cursor = ""

    def __init__(self):
            # 讀取ini設定檔
            config = configparser.ConfigParser()
            config.read('my_config.ini')
            username = config['DB']['username']
            db = config['DB']['db']
            host = config['DB']['host']
            pw = config['DB']['password']
            port = config['DB'].getint('port')

            # 傳入資料庫連線參數
            self.conn = pymysql.connect(
                    host= host,
                    user= username,
                    password= pw,
                    database= db,
                    port=port,
                    ssl_disabled = True,
            )

            # 檢查資料庫連線
            try:
                if self.conn.open:
                    self.cursor = self.conn.cursor() 
                else:
                    print("please trying to reconnect")
            except Exception as e:
                 print(e)
         
    # 取得所有資料                     
    def getfetchallData(self, query):

        try:
            self.cursor.execute(query)
            result = self.cursor.fetchall()
        except pymysql.Error as e:
            print("Error",e)
            return False
        return result
    
     # 取得含有key、value的資料
    def getKeyValueData(self, query):

        try:
            self.cursor.execute(query)
            result=self.cursor.fetchall()
            data_list = []
            for row in result :
                d = collections.OrderedDict()
                d['COLUMN_NAMES']  = row[0] #COLUMN_NAMES
                d['DATA_TYPE']   = row[1] #DATA_TYPE
                d['IS_NULLABLE']      = row[2] #IS_NULLABLE
                d['COLUMN_KEY']      = row[3] #COLUMN_KEY
                d['DESCS']      = row[4] #DESCS
                d['TABLE_TYPE']      = row[5] #TABLE_TYPE
                data_list.append(d)
        except pymysql.Error as e:
            print("your mysql error is：",e)
        return data_list
    
    # 關閉資料庫連線
    def close(self):
        self.conn.close()
        self.cursor.close()

