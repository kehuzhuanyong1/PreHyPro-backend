"""
数据库操作模块
"""

import pymysql
from pymysql import Error
from config import DB_CONFIG

def get_db_connection():
    """获取数据库连接"""
    try:
        connection = pymysql.connect(**DB_CONFIG)
        return connection
    except Error as e:
        print(f"数据库连接错误: {e}")
        return None

def close_db_connection(connection):
    """关闭数据库连接"""
    if connection:
        connection.close()

def execute_insert(sql, values):
    """执行插入操作"""
    connection = get_db_connection()
    if not connection:
        return None, "数据库连接失败"
    
    try:
        cursor = connection.cursor()
        cursor.execute(sql, values)
        connection.commit()
        record_id = cursor.lastrowid
        return record_id, None
    except Error as e:
        connection.rollback()
        return None, f"数据库操作失败: {str(e)}"
    finally:
        close_db_connection(connection) 