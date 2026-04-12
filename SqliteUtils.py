# -*- coding: utf-8 -*-
"""SQLite数据库工具类 SqliteUtils.py"""

# ------------ common ------------
import os
from typing import (
    Any,
    List, 
    Dict, 
    Optional, 
    Tuple, 
    Union
)

# ------------ database ------------
import sqlite3
from sqlite3 import Connection, Cursor


class SqliteUtils:
    """SQLite 数据库工具类
    
    该类封装了 SQLite 数据库的常用操作，包括：
    1. 数据库连接管理
    2. SQL 语句执行
    3. 数据查询（单条、多条、全部）
    4. 数据插入、更新、删除
    5. 事务管理
    6. 表结构操作
    
    Attributes:
        db_path (str): 数据库文件路径
        conn (Connection): SQLite 连接对象
        cursor (Cursor): SQLite 游标对象
    """
    
    def __init__(self, db_path: str):
        """初始化 SqliteUtils 实例
        
        Args:
            db_path (str): SQLite 数据库文件路径，如果文件不存在会自动创建
            
        Example:
            >>> db = SqliteUtils('test.db')
            >>> print(db.db_path)
            >>> 'test.db'
        """
        self.db_path = db_path
        self.conn: Optional[Connection] = None
        self.cursor: Optional[Cursor] = None
        
    def connect(self) -> None:
        """连接到 SQLite 数据库
        
        如果数据库文件不存在，会自动创建。连接成功后，会设置游标对象。
        
        Raises:
            sqlite3.Error: 数据库连接失败时抛出异常
            
        Example:
            >>> db = SqliteUtils('test.db')
            >>> db.connect()
            >>> print(db.conn is not None)
            >>> True
        """
        try:
            # 确保数据库文件所在目录存在
            db_dir = os.path.dirname(self.db_path)
            if db_dir and not os.path.exists(db_dir):
                os.makedirs(db_dir)
            
            # 连接到数据库
            self.conn = sqlite3.connect(self.db_path)
            self.cursor = self.conn.cursor()
            
            # 启用外键约束
            self.cursor.execute("PRAGMA foreign_keys = ON")
            
            print(f"成功连接到数据库: {self.db_path}")
            
        except sqlite3.Error as e:
            print(f"数据库连接失败: {e}")
            raise
    
    def disconnect(self) -> None:
        """断开数据库连接
        
        关闭游标和连接，释放资源。
        
        Example:
            >>> db = SqliteUtils('test.db')
            >>> db.connect()
            >>> db.disconnect()
            >>> print(db.conn is None)
            >>> True
        """
        if self.cursor:
            self.cursor.close()
        if self.conn:
            self.conn.close()
        
        self.cursor = None
        self.conn = None
        print(f"已断开数据库连接: {self.db_path}")
    
    def execute(self, sql: str, params: Union[Tuple, Dict, None] = None) -> Cursor:
        """执行 SQL 语句
        
        执行任意 SQL 语句（查询或修改），支持参数化查询防止 SQL 注入。
        
        Args:
            sql (str): 要执行的 SQL 语句
            params (Union[Tuple, Dict, None]): SQL 参数，可以是元组或字典
            
        Returns:
            Cursor: 执行后的游标对象
            
        Raises:
            sqlite3.Error: SQL 执行失败时抛出异常
            
        Example:
            >>> db = SqliteUtils('test.db')
            >>> db.connect()
            >>> # 创建表
            >>> sql = "CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)"
            >>> db.execute(sql)
            >>> # 插入数据（参数化查询）
            >>> sql = "INSERT INTO users (name) VALUES (?)"
            >>> db.execute(sql, ('Alice',))
            >>> db.disconnect()
        """
        if not self.conn or not self.cursor:
            raise sqlite3.Error("数据库未连接，请先调用 connect() 方法")
        
        try:
            if params:
                self.cursor.execute(sql, params)
            else:
                self.cursor.execute(sql)
            
            return self.cursor
            
        except sqlite3.Error as e:
            print(f"SQL 执行失败: {e}")
            print(f"SQL: {sql}")
            print(f"参数: {params}")
            raise
    
    def execute_many(self, sql: str, params_list: List[Union[Tuple, Dict]]) -> Cursor:
        """批量执行 SQL 语句
        
        使用同一 SQL 语句，批量执行多组参数。
        
        Args:
            sql (str): 要执行的 SQL 语句
            params_list (List[Union[Tuple, Dict]]): 参数列表，每个元素是一组参数
            
        Returns:
            Cursor: 执行后的游标对象
            
        Raises:
            sqlite3.Error: SQL 执行失败时抛出异常
            
        Example:
            >>> db = SqliteUtils('test.db')
            >>> db.connect()
            >>> sql = "INSERT INTO users (name) VALUES (?)"
            >>> params_list = [('Alice',), ('Bob',), ('Charlie',)]
            >>> db.execute_many(sql, params_list)
            >>> db.disconnect()
        """
        if not self.conn or not self.cursor:
            raise sqlite3.Error("数据库未连接，请先调用 connect() 方法")
        
        try:
            self.cursor.executemany(sql, params_list)
            return self.cursor
            
        except sqlite3.Error as e:
            print(f"SQL 批量执行失败: {e}")
            print(f"SQL: {sql}")
            print(f"参数列表: {params_list}")
            raise
    
    def fetch_one(self, sql: str, params: Union[Tuple, Dict, None] = None) -> Optional[Tuple]:
        """查询单条记录
        
        执行查询语句，返回第一条记录。
        
        Args:
            sql (str): 查询 SQL 语句
            params (Union[Tuple, Dict, None]): SQL 参数
            
        Returns:
            Optional[Tuple]: 第一条记录，如果没有结果则返回 None
            
        Example:
            >>> db = SqliteUtils('test.db')
            >>> db.connect()
            >>> sql = "SELECT * FROM users WHERE id = ?"
            >>> row = db.fetch_one(sql, (1,))
            >>> print(row)
            >>> (1, 'Alice')
            >>> db.disconnect()
        """
        cursor = self.execute(sql, params)
        return cursor.fetchone()
    
    def fetch_all(self, sql: str, params: Union[Tuple, Dict, None] = None) -> List[Tuple]:
        """查询所有记录
        
        执行查询语句，返回所有记录。
        
        Args:
            sql (str): 查询 SQL 语句
            params (Union[Tuple, Dict, None]): SQL 参数
            
        Returns:
            List[Tuple]: 所有记录的列表
            
        Example:
            >>> db = SqliteUtils('test.db')
            >>> db.connect()
            >>> sql = "SELECT * FROM users"
            >>> rows = db.fetch_all(sql)
            >>> for row in rows:
            >>>     print(row)
            >>> db.disconnect()
        """
        cursor = self.execute(sql, params)
        return cursor.fetchall()
    
    def fetch_many(self, sql: str, size: int, params: Union[Tuple, Dict, None] = None) -> List[Tuple]:
        """查询多条记录
        
        执行查询语句，返回指定数量的记录。
        
        Args:
            sql (str): 查询 SQL 语句
            size (int): 要返回的记录数量
            params (Union[Tuple, Dict, None]): SQL 参数
            
        Returns:
            List[Tuple]: 指定数量的记录列表
            
        Example:
            >>> db = SqliteUtils('test.db')
            >>> db.connect()
            >>> sql = "SELECT * FROM users"
            >>> rows = db.fetch_many(sql, 5)  # 返回前5条记录
            >>> print(len(rows))
            >>> 5
            >>> db.disconnect()
        """
        cursor = self.execute(sql, params)
        return cursor.fetchmany(size)
    
    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """插入单条记录
        
        向指定表中插入一条记录。
        
        Args:
            table (str): 表名
            data (Dict[str, Any]): 要插入的数据，键为列名，值为数据
            
        Returns:
            int: 插入行的 ID（如果表有自增主键）
            
        Example:
            >>> db = SqliteUtils('test.db')
            >>> db.connect()
            >>> data = {'name': 'Alice', 'age': 25}
            >>> row_id = db.insert('users', data)
            >>> print(f"插入记录的 ID: {row_id}")
            >>> db.disconnect()
        """
        # 构建 SQL 语句
        columns = ', '.join(data.keys())
        placeholders = ', '.join(['?' for _ in data])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        # 执行插入
        self.execute(sql, tuple(data.values()))
        self.conn.commit()
        
        # 返回最后插入的 ID
        return self.cursor.lastrowid
    
    def insert_many(self, table: str, data_list: List[Dict[str, Any]]) -> None:
        """批量插入记录
        
        向指定表中批量插入多条记录。
        
        Args:
            table (str): 表名
            data_list (List[Dict[str, Any]]): 要插入的数据列表
            
        Example:
            >>> db = SqliteUtils('test.db')
            >>> db.connect()
            >>> data_list = [
            >>>     {'name': 'Alice', 'age': 25},
            >>>     {'name': 'Bob', 'age': 30},
            >>>     {'name': 'Charlie', 'age': 35}
            >>> ]
            >>> db.insert_many('users', data_list)
            >>> db.disconnect()
        """
        if not data_list:
            return
        
        # 构建 SQL 语句
        columns = ', '.join(data_list[0].keys())
        placeholders = ', '.join(['?' for _ in data_list[0]])
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        
        # 准备参数列表
        params_list = [tuple(data.values()) for data in data_list]
        
        # 批量执行
        self.executemany(sql, params_list)
        self.conn.commit()
    
    def update(self, table: str, data: Dict[str, Any], where: str, where_params: Union[Tuple, Dict, None] = None) -> int:
        """更新记录
        
        更新指定表中满足条件的记录。
        
        Args:
            table (str): 表名
            data (Dict[str, Any]): 要更新的数据，键为列名，值为新数据
            where (str): WHERE 条件语句（不包含 WHERE 关键字）
            where_params (Union[Tuple, Dict, None]): WHERE 条件参数
            
        Returns:
            int: 受影响的行数
            
        Example:
            >>> db = SqliteUtils('test.db')
            >>> db.connect()
            >>> data = {'age': 26}
            >>> affected = db.update('users', data, 'name = ?', ('Alice',))
            >>> print(f"更新了 {affected} 行")
            >>> db.disconnect()
        """
        # 构建 SET 子句
        set_clause = ', '.join([f"{col} = ?" for col in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {where}"
        
        # 合并参数
        params = tuple(data.values())
        if where_params:
            if isinstance(where_params, tuple):
                params = params + where_params
            else:
                # 如果是字典，需要特殊处理（这里简化处理）
                params = params + tuple(where_params.values())
        
        # 执行更新
        self.execute(sql, params)
        self.conn.commit()
        
        return self.cursor.rowcount
    
    def delete(self, table: str, where: str, where_params: Union[Tuple, Dict, None] = None) -> int:
        """删除记录
        
        删除指定表中满足条件的记录。
        
        Args:
            table (str): 表名
            where (str): WHERE 条件语句（不包含 WHERE 关键字）
            where_params (Union[Tuple, Dict, None]): WHERE 条件参数
            
        Returns:
            int: 受影响的行数
            
        Example:
            >>> db = SqliteUtils('test.db')
            >>> db.connect()
            >>> affected = db.delete('users', 'age > ?', (30,))
            >>> print(f"删除了 {affected} 行")
            >>> db.disconnect()
        """
        sql = f"DELETE FROM {table} WHERE {where}"
        
        self.execute(sql, where_params)
        self.conn.commit()
        
        return self.cursor.rowcount
    
    def table_exists(self, table_name: str) -> bool:
        """检查表是否存在
        
        检查数据库中是否存在指定的表。
        
        Args:
            table_name (str): 表名
            
        Returns:
            bool: 如果表存在返回 True，否则返回 False
            
        Example:
            >>> db = SqliteUtils('test.db')
            >>> db.connect()
            >>> exists = db.table_exists('users')
            >>> print(f"users 表存在: {exists}")
            >>> db.disconnect()
        """
        sql = "SELECT name FROM sqlite_master WHERE type='table' AND name=?"
        result = self.fetch_one(sql, (table_name,))
        
        return result is not None
    
    def get_table_info(self, table_name: str) -> List[Tuple]:
        """获取表结构信息
        
        获取指定表的列信息。
        
        Args:
            table_name (str): 表名
            
        Returns:
            List[Tuple]: 表的列信息列表
            
        Example:
            >>> db = SqliteUtils('test.db')
            >>> db.connect()
            >>> columns = db.get_table_info('users')
            >>> for col in columns:
            >>>     print(col)
            >>> db.disconnect()
        """
        sql = f"PRAGMA table_info({table_name})"
        return self.fetchall(sql)
    
    def begin_transaction(self) -> None:
        """开始事务
        
        开始一个数据库事务。
        
        Example:
            >>> db = SqliteUtils('test.db')
            >>> db.connect()
            >>> db.begin_transaction()
            >>> try:
            >>>     # 执行多个操作
            >>>     db.insert('users', {'name': 'Alice'})
            >>>     db.insert('users', {'name': 'Bob'})
            >>>     db.commit_transaction()
            >>> except:
            >>>     db.rollback_transaction()
            >>> db.disconnect()
        """
        if self.conn:
            self.conn.execute("BEGIN TRANSACTION")
    
    def commit_transaction(self) -> None:
        """提交事务
        
        提交当前事务，使所有更改生效。
        """
        if self.conn:
            self.conn.commit()
    
    def rollback_transaction(self) -> None:
        """回滚事务
        
        回滚当前事务，撤销所有未提交的更改。
        """
        if self.conn:
            self.conn.rollback()
    
    def __enter__(self):
        """上下文管理器入口
        
        支持 with 语句，自动连接数据库。
        
        Example:
            >>> with SqliteUtils('test.db') as db:
            >>>     db.execute("CREATE TABLE users (id INTEGER PRIMARY KEY, name TEXT)")
        """
        self.connect()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口
        
        自动提交或回滚事务，并断开数据库连接。
        """
        if exc_type:
            # 发生异常时回滚
            self.rollback_transaction()
        else:
            # 正常结束时提交
            self.commit_transaction()
        
        self.disconnect()
