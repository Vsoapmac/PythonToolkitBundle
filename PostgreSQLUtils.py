# -*- coding: utf-8 -*-
# PostgreSQL 数据库操作工具类，提供连接管理、CRUD、事务、批量操作等功能
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
import psycopg2
import psycopg2.extras
from psycopg2.pool import ThreadedConnectionPool


class PostgreSQLUtils:
    """PostgreSQL 数据库操作工具类

    提供连接池管理、增删改查、批量操作和事务支持。
    基于 psycopg2 + 连接池实现。

    Usage:
        >>> db = PostgreSQLUtils(host="localhost", user="postgres", password="xxx", database="test")
        >>> results = db.select("SELECT * FROM users WHERE age > %s", params=[18])
        >>> db.close()
    """
    _pool: Optional[ThreadedConnectionPool] = None  # 数据库连接池

    def __init__(self, host: str = "localhost", port: int = 5432,
                 user: str = "postgres", password: str = "",
                 database: str = "", min_connections: int = 2,
                 max_connections: int = 10, **kwargs):
        """初始化 PostgreSQL 连接池

        Args:
            host (str): 数据库主机地址，默认为 localhost
            port (int): 端口号，默认为 5432
            user (str): 数据库用户名，默认为 postgres
            password (str): 数据库密码
            database (str): 数据库名
            min_connections (int): 连接池最小连接数，默认为 2
            max_connections (int): 连接池最大连接数，默认为 10
            **kwargs: 传递给 psycopg2 的其他参数

        Example:
            >>> db = PostgreSQLUtils(host="localhost", user="postgres", password="123456", database="test")
            >>> db._pool is not None
            True
            >>> db.close()
        """
        self._pool = ThreadedConnectionPool(
            minconn=min_connections,
            maxconn=max_connections,
            host=host,
            port=port,
            user=user,
            password=password,
            dbname=database,
            **kwargs
        )

    # region ---------------------------- 连接管理 ----------------------------

    def get_connection(self):
        """从连接池获取一个连接

        Returns:
            connection: psycopg2 连接对象
        """
        return self._pool.getconn()

    def put_connection(self, conn):
        """将连接归还到连接池

        Args:
            conn: psycopg2 连接对象
        """
        self._pool.putconn(conn)

    def close(self):
        """关闭连接池，释放所有连接资源"""
        if self._pool:
            self._pool.closeall()
            self._pool = None

    def __enter__(self) -> "PostgreSQLUtils":
        """进入上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器，自动关闭连接池"""
        self.close()

    # endregion ---------------------------- 连接管理 ----------------------------

    # region ---------------------------- 查询操作 ----------------------------

    def select(self, sql: str, params: Optional[Union[List, Tuple, Dict]] = None,
               size: int = -1) -> List[Dict[str, Any]]:
        """执行查询语句，返回结果列表

        Args:
            sql (str): SQL 查询语句，使用 %s 作为占位符
            params (Optional[Union[List, Tuple, Dict]]): 查询参数
            size (int): 返回行数，-1 表示返回全部，默认为 -1

        Returns:
            List[Dict[str, Any]]: 查询结果字典列表

        Example:
            >>> db = PostgreSQLUtils(host="localhost", user="postgres", password="123456", database="test")
            >>> results = db.select("SELECT * FROM users WHERE age > %s", params=[18])
            >>> isinstance(results, list)
            True
            >>> db.close()
        """
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql, params)
                if size == -1:
                    return [dict(row) for row in cursor.fetchall()]
                return [dict(row) for row in cursor.fetchmany(size)]
        finally:
            self.put_connection(conn)

    def select_one(self, sql: str, params: Optional[Union[List, Tuple, Dict]] = None) -> Optional[Dict[str, Any]]:
        """查询单条记录

        Args:
            sql (str): SQL 查询语句
            params (Optional[Union[List, Tuple, Dict]]): 查询参数

        Returns:
            Optional[Dict[str, Any]]: 单条记录字典，无结果时返回 None

        Example:
            >>> db = PostgreSQLUtils(host="localhost", user="postgres", password="123456", database="test")
            >>> user = db.select_one("SELECT * FROM users WHERE id = %s", params=[1])
            >>> db.close()
        """
        conn = self.get_connection()
        try:
            with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cursor:
                cursor.execute(sql, params)
                row = cursor.fetchone()
                return dict(row) if row else None
        finally:
            self.put_connection(conn)

    # endregion ---------------------------- 查询操作 ----------------------------

    # region ---------------------------- 写入操作 ----------------------------

    def execute(self, sql: str, params: Optional[Union[List, Tuple, Dict]] = None) -> int:
        """执行单条 SQL（INSERT/UPDATE/DELETE）

        Args:
            sql (str): SQL 语句
            params (Optional[Union[List, Tuple, Dict]]): 参数

        Returns:
            int: 影响的行数

        Example:
            >>> db = PostgreSQLUtils(host="localhost", user="postgres", password="123456", database="test")
            >>> affected = db.execute("UPDATE users SET name = %s WHERE id = %s", params=["new_name", 1])
            >>> db.close()
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, params)
                conn.commit()
                return cursor.rowcount
        except Exception:
            conn.rollback()
            raise
        finally:
            self.put_connection(conn)

    def execute_many(self, sql: str, params_list: List[Union[List, Tuple, Dict]]) -> int:
        """批量执行 SQL

        Args:
            sql (str): SQL 语句
            params_list (List[Union[List, Tuple, Dict]]): 参数列表

        Returns:
            int: 影响的总行数

        Example:
            >>> db = PostgreSQLUtils(host="localhost", user="postgres", password="123456", database="test")
            >>> affected = db.execute_many(
            ...     "INSERT INTO users(name, age) VALUES(%s, %s)",
            ...     [["Alice", 20], ["Bob", 25]]
            ... )
            >>> db.close()
        """
        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                psycopg2.extras.execute_batch(cursor, sql, params_list)
                conn.commit()
                return len(params_list)
        except Exception:
            conn.rollback()
            raise
        finally:
            self.put_connection(conn)

    def insert(self, table: str, data: Dict[str, Any]) -> int:
        """插入单条记录并返回自增 ID

        Args:
            table (str): 表名
            data (Dict[str, Any]): 字段名到值的字典

        Returns:
            int: 自增 ID（RETURNING id）

        Example:
            >>> db = PostgreSQLUtils(host="localhost", user="postgres", password="123456", database="test")
            >>> new_id = db.insert("users", {"name": "Alice", "age": 20})
            >>> db.close()
        """
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["%s"] * len(data))
        sql = f"INSERT INTO {table} ({columns}) VALUES ({placeholders}) RETURNING id"

        conn = self.get_connection()
        try:
            with conn.cursor() as cursor:
                cursor.execute(sql, list(data.values()))
                conn.commit()
                return cursor.fetchone()[0]
        except Exception:
            conn.rollback()
            raise
        finally:
            self.put_connection(conn)

    def insert_batch(self, table: str, data_list: List[Dict[str, Any]]) -> int:
        """批量插入多条记录

        Args:
            table (str): 表名
            data_list (List[Dict[str, Any]]): 数据字典列表

        Returns:
            int: 影响的行数

        Example:
            >>> db = PostgreSQLUtils(host="localhost", user="postgres", password="123456", database="test")
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
            condition (str): WHERE 条件，使用 %s 占位
            condition_params (Optional[Union[List, Tuple]]): 条件参数

        Returns:
            int: 影响的行数

        Example:
            >>> db = PostgreSQLUtils(host="localhost", user="postgres", password="123456", database="test")
            >>> affected = db.update("users", {"age": 26}, "name = %s", condition_params=["Alice"])
            >>> db.close()
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
            condition (str): WHERE 条件，使用 %s 占位
            condition_params (Optional[Union[List, Tuple]]): 条件参数

        Returns:
            int: 影响的行数
        """
        sql = f"DELETE FROM {table} WHERE {condition}"
        return self.execute(sql, condition_params)

    # endregion ---------------------------- 写入操作 ----------------------------

    # region ---------------------------- 事务操作 ----------------------------

    def transaction(self) -> "_PostgreSQLTransaction":
        """开始一个事务，返回事务对象

        Returns:
            _PostgreSQLTransaction: 事务对象，支持 commit/rollback
        """
        conn = self.get_connection()
        conn.autocommit = False
        return _PostgreSQLTransaction(conn, self)

    # endregion ---------------------------- 事务操作 ----------------------------

    def table_exists(self, table: str) -> bool:
        """检查表是否存在

        Args:
            table (str): 表名

        Returns:
            bool: 是否存在
        """
        result = self.select_one(
            "SELECT table_name FROM information_schema.tables WHERE table_schema = 'public' AND table_name = %s",
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
            SELECT column_name, data_type, is_nullable, column_default
            FROM information_schema.columns
            WHERE table_schema = 'public' AND table_name = %s
            ORDER BY ordinal_position
        """, params=[table])


class _PostgreSQLTransaction:
    """PostgreSQL 事务对象，由 PostgreSQLUtils.transaction() 创建"""
    _conn = None  # 事务专用连接
    _pool_ref = None  # 连接池引用

    def __init__(self, conn, pool_ref):
        """初始化事务对象

        Args:
            conn: psycopg2 连接对象
            pool_ref (PostgreSQLUtils): 连接池引用
        """
        self._conn = conn
        self._pool_ref = pool_ref

    def execute(self, sql: str, params: Optional[Union[List, Tuple, Dict]] = None) -> int:
        """在事务中执行 SQL

        Args:
            sql (str): SQL 语句
            params (Optional[Union[List, Tuple, Dict]]): 参数

        Returns:
            int: 影响的行数
        """
        with self._conn.cursor() as cursor:
            cursor.execute(sql, params)
            return cursor.rowcount

    def commit(self):
        """提交事务并归还连接"""
        try:
            self._conn.commit()
        finally:
            self._pool_ref.put_connection(self._conn)

    def rollback(self):
        """回滚事务并归还连接"""
        try:
            self._conn.rollback()
        finally:
            self._pool_ref.put_connection(self._conn)
