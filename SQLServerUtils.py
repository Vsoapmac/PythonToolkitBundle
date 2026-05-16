# -*- coding: utf-8 -*-
# SQL Server 数据库操作工具类, 提供连接管理、CRUD、事务、批量操作等功能
# ------------ common ------------
from typing import (
    Any,
    Dict,
    List,
    Optional,
    Tuple,
    Union
)

# ------------ database ------------
import pymssql


class SQLServerUtils:
    """SQL Server 数据库操作工具类

    提供连接管理、增删改查、批量操作和事务支持。
    基于 pymssql 实现。

    Usage:
        >>> db = SQLServerUtils(host="localhost", user="sa", password="xxx", database="test")
        >>> results = db.select("SELECT * FROM users WHERE age > %d", params=[18])
        >>> db.close()
    """
    _conn = None  # 数据库连接
    _host = ""  # 主机地址
    _port = 0  # 端口
    _user = ""  # 用户名
    _password = ""  # 密码
    _database = ""  # 数据库名
    _config = {}  # 额外配置

    def __init__(self, host: str = "localhost", port: int = 1433,
                 user: str = "sa", password: str = "",
                 database: str = "", charset: str = "utf8",
                 autocommit: bool = True, **kwargs):
        """初始化 SQL Server 连接

        Args:
            host (str): 数据库主机地址, 默认为 localhost
            port (int): 端口号, 默认为 1433
            user (str): 数据库用户名, 默认为 sa
            password (str): 数据库密码
            database (str): 数据库名
            charset (str): 字符集, 默认为 utf8
            autocommit (bool): 是否自动提交, 默认为 True
            **kwargs: 传递给 pymssql.connect 的其他参数

        Example:
            >>> db = SQLServerUtils(host="localhost", user="sa", password="123456", database="test")
            >>> db._conn is not None
            True
            >>> db.close()
        """
        self._host = host
        self._port = port
        self._user = user
        self._password = password
        self._database = database
        self._config = kwargs
        self._conn = pymssql.connect(
            server=host,
            port=port,
            user=user,
            password=password,
            database=database,
            charset=charset,
            autocommit=autocommit,
            **kwargs
        )

    # region ---------------------------- 连接管理 ----------------------------

    def get_connection(self):
        """获取当前数据库连接

        Returns:
            Connection: pymssql 连接对象
        """
        try:
            self._conn.ping()
        except Exception:
            self._conn = pymssql.connect(
                server=self._host, port=self._port,
                user=self._user, password=self._password,
                database=self._database, **self._config
            )
        return self._conn

    def close(self):
        """关闭数据库连接"""
        if self._conn:
            self._conn.close()
            self._conn = None

    def __enter__(self) -> "SQLServerUtils":
        """进入上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器, 自动关闭连接"""
        self.close()

    # endregion ---------------------------- 连接管理 ----------------------------

    # region ---------------------------- 查询操作 ----------------------------

    def select(self, sql: str, params: Optional[Union[List, Tuple, Dict]] = None,
               size: int = -1, as_dict: bool = True) -> List[Union[Dict[str, Any], Tuple]]:
        """执行查询语句, 返回结果列表

        Args:
            sql (str): SQL 查询语句, 使用 %d 或 %s 作为占位符
            params (Optional[Union[List, Tuple, Dict]]): 查询参数
            size (int): 返回行数, -1 表示返回全部, 默认为 -1
            as_dict (bool): 是否以字典形式返回, 默认为 True

        Returns:
            List[Union[Dict[str, Any], Tuple]]: 查询结果

        Example:
            >>> db = SQLServerUtils(host="localhost", user="sa", password="123456", database="test")
            >>> results = db.select("SELECT * FROM users WHERE age > %d", params=[18])
            >>> isinstance(results, list)
            True
            >>> db.close()
        """
        conn = self.get_connection()
        with conn.cursor(as_dict=as_dict) as cursor:
            cursor.execute(sql, params)
            if size == -1:
                return cursor.fetchall()
            return cursor.fetchmany(size)

    def select_one(self, sql: str, params: Optional[Union[List, Tuple, Dict]] = None,
                   as_dict: bool = True) -> Optional[Union[Dict[str, Any], Tuple]]:
        """查询单条记录

        Args:
            sql (str): SQL 查询语句
            params (Optional[Union[List, Tuple, Dict]]): 查询参数
            as_dict (bool): 是否以字典形式返回, 默认为 True

        Returns:
            Optional[Union[Dict[str, Any], Tuple]]: 单条记录, 无结果时返回 None

        Example:
            >>> db = SQLServerUtils(host="localhost", user="sa", password="123456", database="test")
            >>> user = db.select_one("SELECT * FROM users WHERE id = %d", params=[1])
            >>> db.close()
        """
        conn = self.get_connection()
        with conn.cursor(as_dict=as_dict) as cursor:
            cursor.execute(sql, params)
            return cursor.fetchone()

    # endregion ---------------------------- 查询操作 ----------------------------

    # region ---------------------------- 写入操作 ----------------------------

    def execute(self, sql: str, params: Optional[Union[List, Tuple, Dict]] = None) -> int:
        """执行单条 SQL(INSERT/UPDATE/DELETE)

        Args:
            sql (str): SQL 语句
            params (Optional[Union[List, Tuple, Dict]]): 参数

        Returns:
            int: 影响的行数

        Example:
            >>> db = SQLServerUtils(host="localhost", user="sa", password="123456", database="test")
            >>> affected = db.execute("UPDATE users SET name = %s WHERE id = %d", params=["new_name", 1])
            >>> db.close()
        """
        conn = self.get_connection()
        with conn.cursor() as cursor:
            cursor.execute(sql, params)
            conn.commit()
            return cursor.rowcount

    def execute_many(self, sql: str, params_list: List[Union[List, Tuple, Dict]]) -> int:
        """批量执行 SQL

        Args:
            sql (str): SQL 语句
            params_list (List[Union[List, Tuple, Dict]]): 参数列表

        Returns:
            int: 影响的总行数

        Example:
            >>> db = SQLServerUtils(host="localhost", user="sa", password="123456", database="test")
            >>> affected = db.execute_many(
            ...     "INSERT INTO users(name, age) VALUES(%s, %d)",
            ...     [["Alice", 20], ["Bob", 25]]
            ... )
            >>> db.close()
        """
        conn = self.get_connection()
        total = 0
        with conn.cursor() as cursor:
            for params in params_list:
                cursor.execute(sql, params)
                total += cursor.rowcount
            conn.commit()
        return total

    def insert(self, table: str, data: Dict[str, Any]) -> Optional[int]:
        """插入单条记录, 返回自增 ID(如有)

        Args:
            table (str): 表名
            data (Dict[str, Any]): 字段名到值的字典

        Returns:
            Optional[int]: 自增 ID, 如果没有自增 ID 则返回 None

        Example:
            >>> db = SQLServerUtils(host="localhost", user="sa", password="123456", database="test")
            >>> new_id = db.insert("users", {"name": "Alice", "age": 20})
            >>> db.close()
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}); SELECT SCOPE_IDENTITY()"

        conn = self.get_connection()
        with conn.cursor() as cursor:
            cursor.execute(sql, list(data.values()))
            conn.commit()
            identity = cursor.fetchone()
            return int(identity[0]) if identity and identity[0] else None

    def insert_batch(self, table: str, data_list: List[Dict[str, Any]]) -> int:
        """批量插入多条记录

        Args:
            table (str): 表名
            data_list (List[Dict[str, Any]]): 数据字典列表

        Returns:
            int: 影响的行数

        Example:
            >>> db = SQLServerUtils(host="localhost", user="sa", password="123456", database="test")
            >>> affected = db.insert_batch("users", [
            ...     {"name": "Alice", "age": 20},
            ...     {"name": "Bob", "age": 25}
            ... ])
            >>> db.close()
        """
        if not data_list:
            return 0
        columns = list(data_list[0].keys())
        col_str = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(columns))
        sql = f"INSERT INTO {table} ({col_str}) VALUES ({placeholders})"

        params_list = []
        for data in data_list:
            params_list.append([data.get(col) for col in columns])

        return self.execute_many(sql, params_list)

    def update(self, table: str, data: Dict[str, Any], condition: str,
               condition_params: Optional[Union[List, Tuple]] = None) -> int:
        """更新记录

        Args:
            table (str): 表名
            data (Dict[str, Any]): 要更新的字段字典
            condition (str): WHERE 条件, 使用 %s/%d 占位
            condition_params (Optional[Union[List, Tuple]]): 条件参数

        Returns:
            int: 影响的行数
        """
        set_clause = ", ".join([f"{col} = %s" for col in data.keys()])
        sql = f"UPDATE {table} SET {set_clause} WHERE {condition}"

        params = list(data.values())
        if condition_params:
            params.extend(condition_params)

        return self.execute(sql, params)

    def delete(self, table: str, condition: str,
               condition_params: Optional[Union[List, Tuple]] = None) -> int:
        """删除记录

        Args:
            table (str): 表名
            condition (str): WHERE 条件
            condition_params (Optional[Union[List, Tuple]]): 条件参数

        Returns:
            int: 影响的行数
        """
        sql = f"DELETE FROM {table} WHERE {condition}"
        return self.execute(sql, condition_params)

    # endregion ---------------------------- 写入操作 ----------------------------

    # region ---------------------------- 事务操作 ----------------------------

    def begin_transaction(self):
        """手动开始事务(关闭自动提交)"""
        conn = self.get_connection()
        conn.autocommit(False)

    def commit_transaction(self):
        """提交事务"""
        conn = self.get_connection()
        conn.commit()
        conn.autocommit(True)

    def rollback_transaction(self):
        """回滚事务"""
        conn = self.get_connection()
        conn.rollback()
        conn.autocommit(True)

    # endregion ---------------------------- 事务操作 ----------------------------

    def table_exists(self, table: str) -> bool:
        """检查表是否存在

        Args:
            table (str): 表名

        Returns:
            bool: 是否存在
        """
        result = self.select_one(
            "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME = %s",
            params=[table]
        )
        return result is not None

    def get_table_columns(self, table: str) -> List[Dict[str, Any]]:
        """获取表的列信息

        Args:
            table (str): 表名

        Returns:
            List[Dict[str, Any]]: 列信息列表
        """
        return self.select("""
            SELECT COLUMN_NAME, DATA_TYPE, IS_NULLABLE, COLUMN_DEFAULT
            FROM INFORMATION_SCHEMA.COLUMNS
            WHERE TABLE_NAME = %s
            ORDER BY ORDINAL_POSITION
        """, params=[table])
