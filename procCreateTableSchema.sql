-- ====================================================================
-- SP Name     : procExportTableSchemaAndInsertTable
-- Function    : 批次將各資料表匯出table schema，並複製一份到總表進行管理
-- Author      : Mark
-- Create Date : 2023-10-26
-- Parameter   : DBName
-- Modify His  : 
-- (1) 2023-10-26 : Mark    : CREATE 
-- ===================================================================

-- 如果stock資料庫不存在就建立一個新的
CREATE DATABASE IF NOT EXISTS stock DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
-- 使用stock資料庫
USE stock;
DELIMITER $$
-- 如果PROCEDURE存在就先移除                                                                                                                                                                   
DROP PROCEDURE IF EXISTS procExportTableSchemaAndInsertTable $$       
-- 建立PROCEDURE(傳入資料庫名稱參數)                                                                                                                           
CREATE PROCEDURE procExportTableSchemaAndInsertTable(DBName varchar(255))    
BEGIN   
		-- 變數宣告
			-- 1. 資料表集合名稱
			-- 2. 取得最後一張資料表
			-- 3. 時間戳記
        DECLARE table_name VARCHAR(255);                                                                                                                                        
        DECLARE end_of_tables INT DEFAULT 0;
        DECLARE mylocaltimestamp DATETIME;
		
        -- 利用SQL取出指定資料庫裡面所有資料表的list，直到最後一張資料表為止
        DECLARE cur CURSOR FOR                                                                                                                                                  
            SELECT t.table_name                                                                                                                                                 
            FROM information_schema.tables t                                                                                                                                    
            WHERE t.table_schema = DBName AND t.table_type='BASE TABLE' AND t.table_name <> 'stock_all_data';                                                                                                 
        DECLARE CONTINUE HANDLER FOR NOT FOUND SET end_of_tables = 1;   
        
		-- 開始建立6張資料表
		DROP TABLE IF EXISTS stock_daily;
		CREATE TABLE IF NOT EXISTS stock_daily
		(
			sdate varchar(10),
			id varchar(10),
			sname varchar(255),
			trs_qty decimal(18, 0),
			trs_count decimal(18, 0),
			trs_amt decimal(18, 0),
			open_price decimal(18, 2),
			h_price decimal(18, 2),
			l_price decimal(18, 2),
			close_price decimal(18, 2),
			s_status varchar(255),
			dec_price decimal(18, 2),
			lb_price decimal(18, 2),
			lb_amt decimal(18, 2),
			ls_price decimal(18, 2),
			ls_amt decimal(18, 2),
			PE decimal(18, 2)
		);
        
		DROP TABLE IF EXISTS stock_list;
		CREATE TABLE IF NOT EXISTS stock_list
		(
			id varchar(10),
			sname varchar(255),
			stock_attr varchar(255),
			industry varchar(255),
			CONSTRAINT PK_stock_list
				PRIMARY KEY (id)
		);

		DROP TABLE IF EXISTS stock_monthly_revenue;
		CREATE TABLE IF NOT EXISTS stock_monthly_revenue
		(
			yyyymm varchar(6),
			id varchar(10),
			sname varchar(255),
			month_amt decimal(18, 0),
			pre_m_amt decimal(18, 0),
			pre_y_amt decimal(18, 0),
			pre_m_percent decimal(18, 2),
			pre_y_percent decimal(18, 2),
			sum_amt decimal(18, 0),
			per_sum_amt decimal(18, 0),
			sum_percent decimal(18, 2),
			memo_str varchar(255),
			CONSTRAINT PK_stock_monthly_revenue
				PRIMARY KEY
				(
					id,
					yyyymm
				)
		);

		DROP TABLE IF EXISTS stock_daily_3;
		CREATE TABLE IF NOT EXISTS stock_daily_3
		(
			sdate varchar(10),
			id varchar(10),
			f_qty decimal(18, 0),
			i_qty decimal(18, 0),
			s_qty decimal(18, 0),
			t_qty decimal(18, 0),
			est_f_qty decimal(18, 0),
			est_i_qty decimal(18, 0),
			est_s_qty decimal(18, 0),
			est_t_qty decimal(18, 0),
			trs_f_percent decimal(18, 2),
			trs_3_percent decimal(18, 2),
			CONSTRAINT PK_stock_daily_3
				PRIMARY KEY
				(
					id,
					sdate
				)
		);

		DROP TABLE IF EXISTS stock_daily_MT;
		CREATE TABLE IF NOT EXISTS stock_daily_MT
		(
			sdate varchar(10),
			id varchar(10),
			mt_b_qty decimal(18, 0),
			mt_s_qty decimal(18, 0),
			mt_r_qty decimal(18, 0),
			mt_qty decimal(18, 0),
			mt_dec_qty decimal(18, 0),
			mt_limit_qty decimal(18, 0),
			mt_use_percent decimal(18, 2),
			ss_b_qty decimal(18, 0),
			ss_s_qt decimal(18, 0),
			ss_r_qty decimal(18, 0),
			ss_qty decimal(18, 0),
			ss_dec_qty decimal(18, 0),
			ms_percent decimal(18, 2),
			ms_dec_qty decimal(18, 0),
			CONSTRAINT PK_stock_daily_MT
				PRIMARY KEY
				(
					id,
					sdate
				)
		);

		DROP TABLE IF EXISTS stock_daily_MR;
		CREATE TABLE IF NOT EXISTS stock_daily_MR
		(
			sdate varchar(10),
			id varchar(50),
			id_sub varchar(50),
			id_mr varchar(50),
			mrname varchar(255),
			b_qty decimal(18, 0),
			s_qty decimal(18, 0),
			dec_qty decimal(18, 0),
			dstatus int,
			trs_percent decimal(18, 2),
			CONSTRAINT PK_stock_daily_MR
				PRIMARY KEY
				(
					id,
					sdate
				)
		);
		
	   -- 如果總表存在先行移除，避免資料重複
	   SET @drop_table=CONCAT("DROP TABLE IF EXISTS stock_all_data");
       PREPARE stmt2 FROM @drop_table;                                                                                                                                               
	   EXECUTE stmt2; 
        
        OPEN cur;                                                                                                                                                               
		
        -- 迴圈開始
        tables_loop: LOOP                   
            	
			-- 將資料集透過迴圈取出，最後一張表時強制離開迴圈
            FETCH cur INTO table_name;             			
            IF end_of_tables = 1 THEN                                                                                                                                           
                LEAVE tables_loop;                                                                                                                                              
            END IF;                                                                                                                                                             
			
            -- 使用CONCAT串接SQL語法(這一段是查看SQL結果，可以拿掉不執行)
             -- SET @show_schema = CONCAT("desc"," ",DBName,".",table_name);
            -- 建立PREPARE STATEMENT，並執行
            --  PREPARE stmt FROM @show_schema;                                                                                                                                               
            -- EXECUTE stmt;     
     
            -- 判斷不同的資料表，給予不同的中文欄位名稱
			CASE table_name
			WHEN 'stock_list' THEN
			   SET @table_type='證券清冊';
			   SET @caseSQL = CONCAT("(
						CASE 
							WHEN COLUMN_NAME='id' THEN '證券代號'
                            WHEN COLUMN_NAME='sname' THEN '證券名稱' 
                            WHEN COLUMN_NAME='stock_attr' THEN '上市上櫃類別'
                            WHEN COLUMN_NAME='industry' THEN '產業分類'
						ELSE 'null'
						END)  as descs"
						);
                        
			WHEN  'stock_daily' THEN
			   SET @table_type='每日收盤資訊';
			   SET @caseSQL=CONCAT("(
						CASE 
							WHEN COLUMN_NAME='sdate' THEN '交易日期' 
							WHEN COLUMN_NAME='id' THEN '證券代號'
                            WHEN COLUMN_NAME='sname' THEN '證券名稱'
                            WHEN COLUMN_NAME='trs_qty' THEN '成交股數'
                            WHEN COLUMN_NAME='trs_count' THEN '成交筆數'
                            WHEN COLUMN_NAME='trs_amt' THEN '成交金額'
                            WHEN COLUMN_NAME='open_price' THEN '開盤價'
                            WHEN COLUMN_NAME='h_price' THEN '最高價'
                            WHEN COLUMN_NAME='l_price' THEN '最低價'
                            WHEN COLUMN_NAME='close_price' THEN '收盤價'
                            WHEN COLUMN_NAME='s_status' THEN '漲跌(+/-)'
                            WHEN COLUMN_NAME='dec_price' THEN '漲跌價差'
                            WHEN COLUMN_NAME='lb_price' THEN '最後揭示買價'
                            WHEN COLUMN_NAME='lb_amt' THEN '最後揭示買量'
                            WHEN COLUMN_NAME='ls_price' THEN '最後揭示賣價'
                            WHEN COLUMN_NAME='ls_amt' THEN '最後揭示賣量'
                            WHEN COLUMN_NAME='PE' THEN '本益比'
						ELSE 'null'
						END)  as descs"
						);
                        
			   WHEN 'stock_monthly_revenue' THEN
			    SET @table_type='每月營收';
			   SET @caseSQL = CONCAT("(
						CASE 
							WHEN COLUMN_NAME='yyyymm' THEN '營收年月' 
							WHEN COLUMN_NAME='id' THEN '證券代號'
                            WHEN COLUMN_NAME='sname' THEN '證券名稱'
                            WHEN COLUMN_NAME='month_amt' THEN '當月營收'
                            WHEN COLUMN_NAME='pre_m_amt' THEN '上月營收'
                            WHEN COLUMN_NAME='pre_y_amt' THEN '去年當月營收'
                            WHEN COLUMN_NAME='pre_m_percent' THEN '上月比較增減(%)'
                            WHEN COLUMN_NAME='pre_y_percent' THEN '去年同月增減(%)'
                            WHEN COLUMN_NAME='sum_amt' THEN '當月累計營收'
                            WHEN COLUMN_NAME='per_sum_amt' THEN '去年累計營收'
                            WHEN COLUMN_NAME='sum_percent' THEN '前期比較增減(%)'
                            WHEN COLUMN_NAME='memo_str' THEN '備註'
						ELSE 'null'
						END)  as descs"
						);
                        
			WHEN 'stock_daily_3' THEN
               SET @table_type='三大法人進出';
			   SET @caseSQL = CONCAT("(
						CASE 
							WHEN COLUMN_NAME='sdate' THEN '交易日期' 
							WHEN COLUMN_NAME='id' THEN '證券代號'
                            WHEN COLUMN_NAME='f_qty' THEN '外資'
                            WHEN COLUMN_NAME='i_qty' THEN '投信'
                            WHEN COLUMN_NAME='s_qty' THEN '自營商'
                            WHEN COLUMN_NAME='t_qty' THEN '單日合計'
                            WHEN COLUMN_NAME='est_f_qty' THEN '估計外資持股'
                            WHEN COLUMN_NAME='est_i_qty' THEN '估計投信持股'
                            WHEN COLUMN_NAME='est_s_qty' THEN '估計自營商持股'
                            WHEN COLUMN_NAME='est_t_qty' THEN '合計'
                            WHEN COLUMN_NAME='trs_f_percent' THEN '外資比例'
                            WHEN COLUMN_NAME='trs_3_percent' THEN '三大法人比例'
						ELSE 'null'
						END) as descs"
						);
			WHEN 'stock_daily_mr' THEN
               SET @table_type='主力進出';
			   SET @caseSQL = CONCAT("(
						CASE 
							WHEN COLUMN_NAME='sdate' THEN '日期' 
							WHEN COLUMN_NAME='id' THEN '股票代號'
                            WHEN COLUMN_NAME='id_sub' THEN '券商代號'
                            WHEN COLUMN_NAME='id_mr' THEN '券商主代號'
                            WHEN COLUMN_NAME='mrname' THEN '券商名稱'
                            WHEN COLUMN_NAME='b_qty' THEN '買進'
                            WHEN COLUMN_NAME='s_qty' THEN '賣出'
                            WHEN COLUMN_NAME='dec_qty' THEN '買超'
                            WHEN COLUMN_NAME='dstatus' THEN '買or賣'
                            WHEN COLUMN_NAME='trs_percent' THEN '佔成交比重'
						ELSE 'null'
						END)  as descs"
						);
			WHEN 'stock_daily_mt' THEN
               SET @table_type='融資融券';
			   SET @caseSQL = CONCAT("(
						CASE 
							WHEN COLUMN_NAME='sdate' THEN '交易日期' 
							WHEN COLUMN_NAME='id' THEN '證券代號'
                            WHEN COLUMN_NAME='mt_b_qty' THEN '融資買進'
                            WHEN COLUMN_NAME='mt_s_qty' THEN '融資賣出'
                            WHEN COLUMN_NAME='mt_r_qty' THEN '融資現償'
                            WHEN COLUMN_NAME='mt_qty' THEN '融資餘額'
                            WHEN COLUMN_NAME='mt_dec_qty' THEN '融資增減'
                            WHEN COLUMN_NAME='mt_limit_qty' THEN '融資限額'
                            WHEN COLUMN_NAME='mt_use_percent' THEN '融資使用率'
                            WHEN COLUMN_NAME='ss_b_qty' THEN '融券賣出'
                            WHEN COLUMN_NAME='ss_s_qt' THEN '融券買進'
                            WHEN COLUMN_NAME='ss_r_qty' THEN '融券券償'
                            WHEN COLUMN_NAME='ss_qty' THEN '融券餘額'
                            WHEN COLUMN_NAME='ss_dec_qty' THEN '融券增減'
                            WHEN COLUMN_NAME='ms_percent' THEN '券資比'
                            WHEN COLUMN_NAME='ms_dec_qty' THEN '資券相抵'
						ELSE 'null'
						END)  as descs"
						);	

				ELSE BEGIN END;  
			END CASE;
            
				-- 建立總表資料表
				SET @create_table = CONCAT("CREATE TABLE IF NOT EXISTS stock_all_data(COLUMN_NAMES varchar(255),DATA_TYPE varchar(255),IS_NULLABLE varchar(255),COLUMN_KEY varchar(255),DESCS varchar(255),TABLE_TYPE varchar(255))");
                PREPARE stmt3 FROM @create_table;                                                                                                                                               
   			    EXECUTE stmt3; 
                
                -- 總表的資料來源是透過原先串好並取得的資料複製一份到stock_all_data
                SET @Insert_table = CONCAT("INSERT INTO stock_all_data (COLUMN_NAMES,DATA_TYPE,IS_NULLABLE,COLUMN_KEY,DESCS,TABLE_TYPE)");
				SET @join_table = CONCAT(@Insert_table,"select COLUMN_NAME,DATA_TYPE,IS_NULLABLE,COLUMN_KEY,",@caseSQL,",","'",@table_type,"'",' as TABLE_TYPE'" FROM information_schema.columns 
				where table_schema = '",DBName,"' AND table_name='",table_name,"'",";");  
                PREPARE stmt4 FROM @join_table;                                                                                                                                               
   			    EXECUTE stmt4; 
            
            -- 這一段供測試用
			-- SELECT @join_table;
         
         -- 迴圈結束
        END LOOP;                                                                                                                                                               
        CLOSE cur;                                                                                                                                                              
    END $$                                                                                                                                                                      
DELIMITER ;