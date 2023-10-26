-- ====================================================================
-- SP Name     : procCreateTableSchema
-- Function    : 批次建立 stock table
-- Author      : Mark
-- Create Date : 2023-10-22
-- Parameter   : DBName
-- Modify His  : 
-- (1) 2023-10-22 : Mark    : CREATE 
-- (2) 2023-10-23 : Mark    : Modify SP describe 
-- ===================================================================

-- 如果stock資料庫不存在就建立一個新的
CREATE DATABASE IF NOT EXISTS stock DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_general_ci;
-- 使用stock資料庫
USE stock;
-- 如果PROCEDURE存在就先移除
DROP PROCEDURE IF EXISTS stock.CreateStockTable; 
DELIMITER //
-- 建立PROCEDURE
CREATE PROCEDURE CreateStockTable()
BEGIN
       
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
        INSERT INTO stock_list VALUES('1','mark','hello','world');
        select * from stock_list;

END //
DELIMITER ;