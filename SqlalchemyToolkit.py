# -*- coding: utf-8 -*-
"""SQLAlchemy工具类 SqlalchemyToolkit.py"""

# ------------ common ------------
import os
from typing import (
    Any, 
    List, 
    Dict, 
    Optional, 
    Tuple
)

# ------------ database ------------
from sqlalchemy import create_engine, Engine, Column, Integer, String, Sequence, text
from sqlalchemy.orm import scoped_session, sessionmaker, Query, declarative_base


class Template_bean(declarative_base()):
    """模板实体类, 用于演示如何创建实体类
    
    Attributes:
        id (int): 主键ID, 自增
        name (str): 姓名
        age (int): 年龄
        email (str): 邮箱, 唯一约束
    """
    __tablename__ = 'template'  # 必须填写, 对应数据表名
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, autoincrement=True)
    name = Column(String(50))
    age = Column(Integer)
    email = Column(String(120), unique=True)


def create_sqlite_engine(db_path: str, echo: bool = False, pool_size: int = 5) -> Engine:
    """创建 SQLite 数据库引擎
    
    SQLite 是嵌入式数据库, 无需额外安装驱动。适用于本地存储和小型应用。
    
    Args:
        db_path (str): 数据库文件路径, 例如: 'test.db' 或 '/path/to/database.db'
                      可以使用 ':memory:' 创建内存数据库
        echo (bool, optional): 是否打印生成的 SQL 语句, 用于调试。Defaults to False.
        pool_size (int, optional): 连接池大小。Defaults to 5.
    
    Returns:
        Engine: SQLite 数据库引擎
        
    Example:
        >>> engine = create_sqlite_engine('test.db')
        >>> print(engine)
        >>> Engine(sqlite:///test.db)
    """
    # 确保数据库文件所在目录存在
    if db_path != ':memory:' and not db_path.startswith('sqlite://'):
        # 如果是文件路径, 确保目录存在
        dir_path = os.path.dirname(db_path)
        if dir_path and not os.path.exists(dir_path):
            os.makedirs(dir_path)
    
    # 构建连接URL
    if db_path == ':memory:' or db_path.startswith('sqlite://'):
        db_url = db_path if db_path.startswith('sqlite://') else f'sqlite:///{db_path}'
    else:
        db_url = f'sqlite:///{db_path}'
    
    return create_engine(db_url, echo=echo, pool_size=pool_size)


def create_mysql_engine(username: str, password: str, database_name: str, host: str = "localhost", 
                        port: int = 3306, connect_url_parm: str = "?charset=utf8mb4", 
                        echo: bool = False, pool_size: int = 20) -> Engine:
    """创建 MySQL 数据库引擎
    
    使用前需要安装数据库驱动: pip install pymysql
    
    Args:
        username (str): 数据库用户名
        password (str): 数据库密码
        database_name (str): 数据库名
        host (str, optional): 数据库主机地址。Defaults to "localhost".
        port (int, optional): 数据库端口号。Defaults to 3306.
        connect_url_parm (str, optional): 连接参数, 注意第一个字符应该为?。 
                                          Defaults to "?charset=utf8mb4".
        echo (bool, optional): 是否打印生成的 SQL 语句, 用于调试。Defaults to False.
        pool_size (int, optional): 连接池中保持的连接数。Defaults to 20.
    
    Returns:
        Engine: MySQL 数据库引擎
        
    Raises:
        ImportError: 如果未安装 pymysql 驱动
        
    Example:
        >>> engine = create_mysql_engine('root', 'password', 'mydb')
        >>> print(engine)
        >>> Engine(mysql+pymysql://root:***@localhost:3306/mydb?charset=utf8mb4)
    """
    try:
        import pymysql
        pymysql.install_as_MySQLdb() # PyMySQL 伪装成旧驱动 MySQLdb, 兼容 SQLAlchemy 的 mysql+mysqldb 连接方式
    except ImportError:
        raise ImportError("MySQL 驱动未安装, 请执行: pip install pymysql")
    
    return create_engine(
        f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}{connect_url_parm}",
        echo=echo, pool_size=pool_size
    )


def create_postgresql_engine(username: str, password: str, database_name: str, host: str = "localhost",
                             port: int = 5432, connect_url_parm: str = "", echo: bool = False,
                             pool_size: int = 20) -> Engine:
    """创建 PostgreSQL 数据库引擎
    
    使用前需要安装数据库驱动: pip install psycopg2
    
    Args:
        username (str): 数据库用户名
        password (str): 数据库密码
        database_name (str): 数据库名
        host (str, optional): 数据库主机地址。Defaults to "localhost".
        port (int, optional): 数据库端口号。Defaults to 5432.
        connect_url_parm (str, optional): 连接参数, 注意第一个字符应该为?。Defaults to "".
        echo (bool, optional): 是否打印生成的 SQL 语句, 用于调试。Defaults to False.
        pool_size (int, optional): 连接池中保持的连接数。Defaults to 20.
    
    Returns:
        Engine: PostgreSQL 数据库引擎
        
    Raises:
        ImportError: 如果未安装 psycopg2 驱动
        
    Example:
        >>> engine = create_postgresql_engine('postgres', 'password', 'mydb')
        >>> print(engine)
        >>> Engine(postgresql+psycopg2://postgres:***@localhost:5432/mydb)
    """
    try:
        import psycopg2
    except ImportError:
        raise ImportError("PostgreSQL 驱动未安装, 请执行: pip install psycopg2")
    
    return create_engine(
        f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}{connect_url_parm}",
        echo=echo, pool_size=pool_size
    )


def create_sql_server_engine(username: str, password: str, database_name: str, host: str = "localhost",
                             port: int = 1433, connect_url_parm: str = "?driver=ODBC+Driver+17+for+SQL+Server",
                             echo: bool = False, pool_size: int = 20) -> Engine:
    """创建 SQL Server 数据库引擎
    
    使用前需要安装数据库驱动: pip install pyodbc
    
    Args:
        username (str): 数据库用户名
        password (str): 数据库密码
        database_name (str): 数据库名
        host (str, optional): 数据库主机地址。Defaults to "localhost".
        port (int, optional): 数据库端口号。Defaults to 1433.
        connect_url_parm (str, optional): 连接参数, 注意第一个字符应该为?。
                                          Defaults to "?driver=ODBC+Driver+17+for+SQL+Server".
        echo (bool, optional): 是否打印生成的 SQL 语句, 用于调试。Defaults to False.
        pool_size (int, optional): 连接池中保持的连接数。Defaults to 20.
    
    Returns:
        Engine: SQL Server 数据库引擎
        
    Raises:
        ImportError: 如果未安装 pyodbc 驱动
        
    Example:
        >>> engine = create_sql_server_engine('sa', 'password', 'mydb')
        >>> print(engine)
        >>> Engine(mssql+pyodbc://sa:***@localhost:1433/mydb?driver=ODBC+Driver+17+for+SQL+Server)
    """
    try:
        import pyodbc
    except ImportError:
        raise ImportError("SQL Server 驱动未安装, 请执行: pip install pyodbc")
    
    return create_engine(
        f"mssql+pyodbc://{username}:{password}@{host}:{port}/{database_name}{connect_url_parm}",
        echo=echo, pool_size=pool_size
    )


def create_oracle_engine(username: str, password: str, service_name: str, host: str = "localhost",
                         port: int = 1521, connect_url_parm: str = "", echo: bool = False,
                         pool_size: int = 20) -> Engine:
    """创建 Oracle 数据库引擎
    
    使用前需要安装数据库驱动: pip install cx_Oracle
    
    Args:
        username (str): 数据库用户名
        password (str): 数据库密码
        service_name (str): 数据库服务名
        host (str, optional): 数据库主机地址。Defaults to "localhost".
        port (int, optional): 数据库端口号。Defaults to 1521.
        connect_url_parm (str, optional): 连接参数, 注意第一个字符应该为?。Defaults to "".
        echo (bool, optional): 是否打印生成的 SQL 语句, 用于调试。Defaults to False.
        pool_size (int, optional): 连接池中保持的连接数。Defaults to 20.
    
    Returns:
        Engine: Oracle 数据库引擎
        
    Raises:
        ImportError: 如果未安装 cx_Oracle 驱动
        
    Example:
        >>> engine = create_oracle_engine('system', 'password', 'ORCL')
        >>> print(engine)
        >>> Engine(oracle+cx_oracle://system:***@localhost:1521/ORCL)
    """
    try:
        import cx_Oracle
    except ImportError:
        raise ImportError("Oracle 驱动未安装, 请执行: pip install cx_Oracle")
    
    return create_engine(
        f"oracle+cx_oracle://{username}:{password}@{host}:{port}/{service_name}{connect_url_parm}",
        echo=echo, pool_size=pool_size
    )


def create_generic_engine(database_url: str, echo: bool = False, pool_size: int = 20, **kwargs) -> Engine:
    """创建通用数据库引擎
    
    使用 SQLAlchemy 支持的任意数据库连接 URL 创建引擎。
    
    Args:
        database_url (str): 数据库连接 URL, 例如:
                           - 'sqlite:///test.db'
                           - 'mysql+pymysql://user:pass@localhost/dbname'
                           - 'postgresql+psycopg2://user:pass@localhost/dbname'
        echo (bool, optional): 是否打印生成的 SQL 语句, 用于调试。Defaults to False.
        pool_size (int, optional): 连接池中保持的连接数。Defaults to 20.
        **kwargs: 其他传递给 create_engine 的参数
    
    Returns:
        Engine: 数据库引擎
        
    Example:
        >>> engine = create_generic_engine('sqlite:///test.db')
        >>> print(engine)
        >>> Engine(sqlite:///test.db)
    """
    return create_engine(database_url, echo=echo, pool_size=pool_size, **kwargs)


class SqlalchemyToolkit:
    """SQLAlchemy 工具类
    
    该类封装了 SQLAlchemy 的常用操作, 提供简洁的 API 进行数据库操作。
    支持多种数据库引擎, 提供完整的 ORM 操作功能。
    
    Attributes:
        session (Session): SQLAlchemy Session 对象
        engine (Engine): SQLAlchemy Engine 对象（如果提供）
    
    Example:
        >>> from utils.SqlalchemyToolkit import create_sqlite_engine, SqlalchemyToolkit
        >>> engine = create_sqlite_engine('test.db')
        >>> with SqlalchemyToolkit(engine) as toolkit:
        >>>     # 执行数据库操作
        >>>     users = toolkit.select_all(User)
        >>>     print(f"找到 {len(users)} 个用户")
    """
    
    session = None
    engine = None
    
    def __init__(self, engine: Engine = None, multiple_thread_session: bool = False):
        """初始化 SqlalchemyToolkit 实例
        
        Args:
            engine (Engine, optional): SQLAlchemy 引擎对象。如果提供, 会自动创建 Session。
            multiple_thread_session (bool, optional): 是否创建多线程安全的 Session。
                                                      Defaults to False.
        
        Example:
            >>> engine = create_sqlite_engine('test.db')
            >>> toolkit = SqlalchemyToolkit(engine)
            >>> print(toolkit.session is not None)
            >>> True
        """
        if engine:
            self.engine = engine
            self.create_session(engine, multiple_thread_session)
    
    def __enter__(self):
        """上下文管理器入口
        
        支持 with 语句, 自动管理 Session 生命周期。
        """
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """上下文管理器出口
        
        自动关闭 Session, 释放资源。
        """
        self.close()
    
    def create_session(self, engine: Engine, multiple_thread_session: bool = False):
        """创建 Session
        
        Args:
            engine (Engine): SQLAlchemy 引擎对象
            multiple_thread_session (bool, optional): 是否创建多线程安全的 Session。
                                                      Defaults to False.
        
        Example:
            >>> toolkit = SqlalchemyToolkit()
            >>> toolkit.create_session(engine)
            >>> print(toolkit.session is not None)
            >>> True
        """
        self.engine = engine
        if not multiple_thread_session:
            Session = sessionmaker(bind=engine)
            self.session = Session()
        else:
            Session = scoped_session(sessionmaker(bind=engine))
            self.session = Session()
    
    def close(self, close_all: bool = False):
        """关闭 Session
        
        Args:
            close_all (bool, optional): 是否关闭所有 Session（用于线程池连接）。
                                        Defaults to False.
        
        Example:
            >>> toolkit = SqlalchemyToolkit(engine)
            >>> toolkit.close()
            >>> print(toolkit.session is None)
            >>> True
        """
        if self.session:
            if not close_all:
                self.session.close()
            else:
                self.session.close_all()
            self.session = None
    
    def execute_sql(self, sql: str, params: Dict = None) -> Any:
        """执行原生 SQL 语句
        
        Args:
            sql (str): SQL 语句
            params (Dict, optional): SQL 参数, 用于参数化查询防止 SQL 注入。
        
        Returns:
            Any: 执行结果
            
        Example:
            >>> toolkit.execute_sql("SELECT * FROM users WHERE age > :age", {"age": 18})
            >>> # 返回查询结果
        """
        if params:
            return self.session.execute(text(sql), params)
        else:
            return self.session.execute(text(sql))
    
    def insert(self, bean: declarative_base) -> declarative_base:
        """插入单条数据
        
        Args:
            bean (declarative_base): 数据表对象实体类
        
        Returns:
            declarative_base: 插入后的实体对象（包含生成的ID等）
            
        Raises:
            sqlalchemy.exc.SQLAlchemyError: 数据库操作失败时抛出
            ValueError: 参数无效时抛出
            
        Example:
            >>> user = User(name='Alice', age=25)
            >>> inserted_user = toolkit.insert(user)
            >>> print(f"插入成功, ID: {inserted_user.id}")
        """
        try:
            self.session.add(bean)
            self.session.commit()
            self.session.refresh(bean)  # 刷新以获取数据库生成的ID等
            return bean
        except ValueError as e:
            self.session.rollback()
            raise ValueError(f"插入数据参数无效: {str(e)}")
        except Exception as e:
            self.session.rollback()
            from sqlalchemy.exc import SQLAlchemyError
            if isinstance(e, SQLAlchemyError):
                raise e
            else:
                raise SQLAlchemyError(f"插入数据失败: {str(e)}")
    
    def insert_all(self, beans: List[declarative_base]) -> List[declarative_base]:
        """批量插入多条数据
        
        Args:
            beans (List[declarative_base]): 数据表对象实体类列表
        
        Returns:
            List[declarative_base]: 插入后的实体对象列表
            
        Raises:
            sqlalchemy.exc.SQLAlchemyError: 数据库操作失败时抛出
            ValueError: 参数无效时抛出
            
        Example:
            >>> users = [User(name='Alice', age=25), User(name='Bob', age=30)]
            >>> inserted_users = toolkit.insert_all(users)
            >>> print(f"批量插入 {len(inserted_users)} 条记录成功")
        """
        try:
            self.session.add_all(beans)
            self.session.commit()
            # 刷新每个对象以获取数据库生成的ID等
            for bean in beans:
                self.session.refresh(bean)
            return beans
        except ValueError as e:
            self.session.rollback()
            raise ValueError(f"批量插入数据参数无效: {str(e)}")
        except Exception as e:
            self.session.rollback()
            from sqlalchemy.exc import SQLAlchemyError
            if isinstance(e, SQLAlchemyError):
                raise e
            else:
                raise SQLAlchemyError(f"批量插入数据失败: {str(e)}")
    
    def delete(self, bean: declarative_base) -> bool:
        """删除单条数据
        
        Args:
            bean (declarative_base): 要删除的数据表对象实体类
        
        Returns:
            bool: 删除成功返回 True, 否则返回 False
            
        Raises:
            Exception: 删除数据失败时抛出异常
            
        Example:
            >>> toolkit.delete(user)
            >>> print("删除成功")
        """
        try:
            self.session.delete(bean)
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise Exception(f"删除数据失败: {str(e)}")
    
    def delete_by_condition(self, bean_class: declarative_base, *conditions) -> int:
        """根据条件删除多条数据
        
        Args:
            bean_class (declarative_base): 数据表对象实体类（类本身, 不是实例）
            *conditions: 过滤条件, 使用 SQLAlchemy 的 filter 语法
        
        Returns:
            int: 删除的行数
            
        Example:
            >>> # 删除所有年龄大于30的用户
            >>> deleted_count = toolkit.delete_by_condition(User, User.age > 30)
            >>> print(f"删除了 {deleted_count} 条记录")
        """
        try:
            result = self.session.query(bean_class).filter(*conditions).delete(synchronize_session=False)
            self.session.commit()
            return result
        except Exception as e:
            self.session.rollback()
            raise Exception(f"根据条件删除数据失败: {str(e)}")
    
    def update(self, bean: declarative_base) -> bool:
        """更新单条数据
        
        注意：此方法要求 bean 对象已经存在于 Session 中（即通过查询获取的对象）。
        如果要更新新创建的对象, 请先调用 session.add() 或使用 update_by_condition 方法。
        
        Args:
            bean (declarative_base): 要更新的数据表对象实体类
        
        Returns:
            bool: 更新成功返回 True, 否则返回 False
            
        Raises:
            Exception: 更新数据失败时抛出异常
            
        Example:
            >>> user = toolkit.select_first(User, User.id == 1)
            >>> user.name = 'New Name'
            >>> toolkit.update(user)
            >>> print("更新成功")
        """
        try:
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise Exception(f"更新数据失败: {str(e)}")
    
    def update_by_condition(self, bean_class: declarative_base, updates: Dict, *conditions) -> int:
        """根据条件更新多条数据
        
        Args:
            bean_class (declarative_base): 数据表对象实体类（类本身, 不是实例）
            updates (Dict): 要更新的字段和值, 例如: {'name': 'New Name', 'age': 30}
            *conditions: 过滤条件, 使用 SQLAlchemy 的 filter 语法
        
        Returns:
            int: 更新的行数
            
        Example:
            >>> # 将所有年龄大于30的用户的部门改为'资深部'
            >>> updated_count = toolkit.update_by_condition(User, {'department': '资深部'}, User.age > 30)
            >>> print(f"更新了 {updated_count} 条记录")
        """
        try:
            result = self.session.query(bean_class).filter(*conditions).update(updates, synchronize_session=False)
            self.session.commit()
            return result
        except Exception as e:
            self.session.rollback()
            raise Exception(f"根据条件更新数据失败: {str(e)}")
    
    def select_all(self, bean_class: declarative_base, *conditions) -> List[declarative_base]:
        """查询所有数据（可带条件）
        
        Args:
            bean_class (declarative_base): 数据表对象实体类（类本身, 不是实例）
            *conditions: 过滤条件, 使用 SQLAlchemy 的 filter 语法
        
        Returns:
            List[declarative_base]: 查询结果列表
            
        Example:
            >>> # 查询所有用户
            >>> users = toolkit.select_all(User)
            >>> print(f"找到 {len(users)} 个用户")
            >>> 
            >>> # 查询所有年龄大于25的用户
            >>> adult_users = toolkit.select_all(User, User.age > 25)
            >>> print(f"找到 {len(adult_users)} 个成年用户")
        """
        query = self.session.query(bean_class)
        if conditions:
            query = query.filter(*conditions)
        return query.all()
    
    def select_first(self, bean_class: declarative_base, *conditions) -> Optional[declarative_base]:
        """查询第一条数据（可带条件）
        
        Args:
            bean_class (declarative_base): 数据表对象实体类（类本身, 不是实例）
            *conditions: 过滤条件, 使用 SQLAlchemy 的 filter 语法
        
        Returns:
            Optional[declarative_base]: 查询结果, 如果没有结果则返回 None
            
        Example:
            >>> # 查询第一个用户
            >>> first_user = toolkit.select_first(User)
            >>> if first_user:
            >>>     print(f"第一个用户: {first_user.name}")
            >>> 
            >>> # 查询第一个年龄大于25的用户
            >>> first_adult = toolkit.select_first(User, User.age > 25)
        """
        query = self.session.query(bean_class)
        if conditions:
            query = query.filter(*conditions)
        return query.first()
    
    def select_by_id(self, bean_class: declarative_base, id_value: Any) -> Optional[declarative_base]:
        """根据ID查询数据
        
        Args:
            bean_class (declarative_base): 数据表对象实体类（类本身, 不是实例）
            id_value (Any): 主键ID值
        
        Returns:
            Optional[declarative_base]: 查询结果, 如果没有结果则返回 None
            
        Example:
            >>> user = toolkit.select_by_id(User, 1)
            >>> if user:
            >>>     print(f"用户ID 1: {user.name}")
        """
        return self.session.query(bean_class).get(id_value)
    
    def count_datas(self, bean_class: declarative_base, *conditions) -> int:
        """统计数据条数（可带条件）
        
        Args:
            bean_class (declarative_base): 数据表对象实体类（类本身, 不是实例）
            *conditions: 过滤条件, 使用 SQLAlchemy 的 filter 语法
        
        Returns:
            int: 数据条数
            
        Example:
            >>> # 统计所有用户数量
            >>> total_users = toolkit.count_datas(User)
            >>> print(f"总用户数: {total_users}")
            >>> 
            >>> # 统计年龄大于25的用户数量
            >>> adult_count = toolkit.count_datas(User, User.age > 25)
            >>> print(f"成年用户数: {adult_count}")
        """
        query = self.session.query(bean_class)
        if conditions:
            query = query.filter(*conditions)
        return query.count()
    
    def select_paginate(self, bean_class: declarative_base, page: int = 1, per_page: int = 20, 
                       *conditions) -> Tuple[List[declarative_base], int, int]:
        """分页查询数据
        
        Args:
            bean_class (declarative_base): 数据表对象实体类（类本身, 不是实例）
            page (int, optional): 页码, 从1开始。Defaults to 1.
            per_page (int, optional): 每页条数。Defaults to 20.
            *conditions: 过滤条件, 使用 SQLAlchemy 的 filter 语法
        
        Returns:
            Tuple[List[declarative_base], int, int]: (当前页数据列表, 总页数, 总条数)
            
        Example:
            >>> # 查询第2页, 每页10条
            >>> users, total_pages, total_count = toolkit.select_paginate(User, page=2, per_page=10)
            >>> print(f"第2页, 共{total_pages}页, 总计{total_count}条记录")
        """
        query = self.session.query(bean_class)
        if conditions:
            query = query.filter(*conditions)
        
        total_count = query.count()
        total_pages = (total_count + per_page - 1) // per_page
        
        # 调整页码范围
        if page < 1:
            page = 1
        elif page > total_pages and total_pages > 0:
            page = total_pages
        
        offset = (page - 1) * per_page
        data = query.offset(offset).limit(per_page).all()
        
        return data, total_pages, total_count
    
    def exists(self, bean_class: declarative_base, *conditions) -> bool:
        """检查是否存在满足条件的数据
        
        Args:
            bean_class (declarative_base): 数据表对象实体类（类本身, 不是实例）
            *conditions: 过滤条件, 使用 SQLAlchemy 的 filter 语法
        
        Returns:
            bool: 如果存在返回 True, 否则返回 False
            
        Example:
            >>> # 检查是否存在名为'Alice'的用户
            >>> exists = toolkit.exists(User, User.name == 'Alice')
            >>> print(f"用户Alice存在: {exists}")
        """
        query = self.session.query(bean_class).filter(*conditions)
        return self.session.query(query.exists()).scalar()
    
    def execute_raw_sql(self, sql: str, params: Dict = None, return_result: bool = True) -> Any:
        """执行原生 SQL 语句（返回原始结果）
        
        Args:
            sql (str): SQL 语句
            params (Dict, optional): SQL 参数, 用于参数化查询防止 SQL 注入。
            return_result (bool, optional): 是否返回结果。Defaults to True.
        
        Returns:
            Any: 执行结果, 如果 return_result=False 则返回 None
            
        Example:
            >>> # 执行查询
            >>> result = toolkit.execute_raw_sql("SELECT * FROM users WHERE age > :age", {"age": 18})
            >>> for row in result:
            >>>     print(row)
            >>> 
            >>> # 执行更新（不返回结果）
            >>> toolkit.execute_raw_sql("UPDATE users SET status = 'active' WHERE id = :id", 
            >>>                        {"id": 1}, return_result=False)
        """
        if params:
            result = self.session.execute(text(sql), params)
        else:
            result = self.session.execute(text(sql))
        
        if return_result:
            return result
        else:
            return None
    
    def get_table_names(self) -> List[str]:
        """获取数据库中所有表名
        
        Returns:
            List[str]: 表名列表
            
        Example:
            >>> tables = toolkit.get_table_names()
            >>> print(f"数据库中有 {len(tables)} 个表: {tables}")
        """
        if not self.engine:
            raise Exception("未设置数据库引擎")
        
        from sqlalchemy import inspect
        inspector = inspect(self.engine)
        return inspector.get_table_names()
    
    def get_table_columns(self, table_name: str) -> List[Dict]:
        """获取指定表的列信息
        
        Args:
            table_name (str): 表名
        
        Returns:
            List[Dict]: 列信息列表, 每个字典包含列名、类型、是否可为空等信息
            
        Example:
            >>> columns = toolkit.get_table_columns('users')
            >>> for col in columns:
            >>>     print(f"列名: {col['name']}, 类型: {col['type']}, 是否可为空: {col['nullable']}")
        """
        if not self.engine:
            raise Exception("未设置数据库引擎")
        
        from sqlalchemy import inspect
        inspector = inspect(self.engine)
        return inspector.get_columns(table_name)
    
    def create_table(self, bean_class: declarative_base) -> bool:
        """创建表（如果不存在）
        
        Args:
            bean_class (declarative_base): 数据表对象实体类（类本身, 不是实例）
        
        Returns:
            bool: 创建成功返回 True, 否则返回 False
            
        Example:
            >>> toolkit.create_table(User)
            >>> print("用户表创建成功")
        """
        try:
            bean_class.metadata.create_all(self.engine)
            return True
        except Exception as e:
            raise Exception(f"创建表失败: {str(e)}")
    
    def drop_table(self, bean_class: declarative_base) -> bool:
        """删除表（如果存在）
        
        Args:
            bean_class (declarative_base): 数据表对象实体类（类本身, 不是实例）
        
        Returns:
            bool: 删除成功返回 True, 否则返回 False
            
        Example:
            >>> toolkit.drop_table(User)
            >>> print("用户表删除成功")
        """
        try:
            bean_class.metadata.drop_all(self.engine)
            return True
        except Exception as e:
            raise Exception(f"删除表失败: {str(e)}")
    
    def transaction(self):
        """事务上下文管理器
        
        使用 with 语句管理事务, 自动提交或回滚。
        
        Example:
            >>> with toolkit.transaction():
            >>>     toolkit.insert(user1)
            >>>     toolkit.insert(user2)
            >>>     # 如果出现异常, 事务会自动回滚
        """
        class TransactionContext:
            def __init__(self, toolkit):
                self.toolkit = toolkit
            
            def __enter__(self):
                return self.toolkit
            
            def __exit__(self, exc_type, exc_val, exc_tb):
                if exc_type:
                    self.toolkit.session.rollback()
                else:
                    self.toolkit.session.commit()
        
        return TransactionContext(self)
    
    def bulk_insert(self, bean_class: declarative_base, data_list: List[Dict]) -> int:
        """批量插入数据（高性能）
        
        使用 SQLAlchemy 的 bulk_insert_mappings 方法, 性能优于 insert_all。
        
        Args:
            bean_class (declarative_base): 数据表对象实体类（类本身, 不是实例）
            data_list (List[Dict]): 数据列表, 每个字典对应一行数据
        
        Returns:
            int: 插入的行数
            
        Example:
            >>> users_data = [
            >>>     {'name': 'Alice', 'age': 25},
            >>>     {'name': 'Bob', 'age': 30},
            >>>     {'name': 'Charlie', 'age': 35}
            >>> ]
            >>> inserted_count = toolkit.bulk_insert(User, users_data)
            >>> print(f"批量插入了 {inserted_count} 条记录")
        """
        try:
            result = self.session.bulk_insert_mappings(bean_class, data_list)
            self.session.commit()
            return len(data_list)
        except Exception as e:
            self.session.rollback()
            raise Exception(f"批量插入数据失败: {str(e)}")
    
    def bulk_update(self, bean_class: declarative_base, data_list: List[Dict], 
                   update_keys: List[str]) -> int:
        """批量更新数据（高性能）
        
        使用 SQLAlchemy 的 bulk_update_mappings 方法, 性能优于 update_by_condition。
        
        Args:
            bean_class (declarative_base): 数据表对象实体类（类本身, 不是实例）
            data_list (List[Dict]): 数据列表, 每个字典对应一行数据, 必须包含主键
            update_keys (List[str]): 要更新的字段名列表
        
        Returns:
            int: 更新的行数
            
        Example:
            >>> users_data = [
            >>>     {'id': 1, 'name': 'Alice Updated', 'age': 26},
            >>>     {'id': 2, 'name': 'Bob Updated', 'age': 31}
            >>> ]
            >>> updated_count = toolkit.bulk_update(User, users_data, ['name', 'age'])
            >>> print(f"批量更新了 {updated_count} 条记录")
        """
        try:
            result = self.session.bulk_update_mappings(bean_class, data_list)
            self.session.commit()
            return len(data_list)
        except Exception as e:
            self.session.rollback()
            raise Exception(f"批量更新数据失败: {str(e)}")
    
    def query_builder(self, bean_class: declarative_base) -> Query:
        """获取查询构建器
        
        提供更灵活的查询构建能力。
        
        Args:
            bean_class (declarative_base): 数据表对象实体类（类本身, 不是实例）
        
        Returns:
            Query: SQLAlchemy Query 对象
            
        Example:
            >>> query = toolkit.query_builder(User)
            >>> users = query.filter(User.age > 25).order_by(User.name).limit(10).all()
            >>> print(f"找到 {len(users)} 个用户")
        """
        return self.session.query(bean_class)
    
    def sqlite_only_vacuum(self) -> bool:
        """SQLite 专用：执行 VACUUM 命令（压缩数据库文件）
        
        仅适用于 SQLite 数据库, 用于回收未使用的空间, 优化数据库性能。
        
        Returns:
            bool: 执行成功返回 True, 否则返回 False
            
        Raises:
            Exception: 如果不是 SQLite 数据库或执行失败
            
        Example:
            >>> toolkit.sqlite_only_vacuum()
            >>> print("数据库压缩完成")
        """
        if not self.engine or 'sqlite' not in str(self.engine.url):
            raise Exception("VACUUM 命令仅适用于 SQLite 数据库")
        
        try:
            self.session.execute(text("VACUUM"))
            self.session.commit()
            return True
        except Exception as e:
            self.session.rollback()
            raise Exception(f"执行 VACUUM 命令失败: {str(e)}")
    
    def sqlite_only_backup(self, backup_path: str) -> bool:
        """SQLite 专用：备份数据库文件
        
        仅适用于 SQLite 数据库, 通过复制文件的方式备份。
        
        Args:
            backup_path (str): 备份文件路径
        
        Returns:
            bool: 备份成功返回 True, 否则返回 False
            
        Raises:
            Exception: 如果不是 SQLite 数据库或备份失败
            
        Example:
            >>> toolkit.sqlite_only_backup('backup.db')
            >>> print("数据库备份完成")
        """
        if not self.engine or 'sqlite' not in str(self.engine.url):
            raise Exception("备份功能仅适用于 SQLite 数据库")
        
        try:
            import shutil
            # 获取原始数据库文件路径
            db_url = str(self.engine.url)
            if db_url.startswith('sqlite:///'):
                original_path = db_url[10:]  # 移除 'sqlite:///'
                if original_path == ':memory:':
                    raise Exception("无法备份内存数据库")
                
                # 确保备份目录存在
                backup_dir = os.path.dirname(backup_path)
                if backup_dir and not os.path.exists(backup_dir):
                    os.makedirs(backup_dir)
                
                # 复制数据库文件
                shutil.copy2(original_path, backup_path)
                return True
            else:
                raise Exception("不支持的 SQLite 连接 URL 格式")
        except Exception as e:
            raise Exception(f"备份数据库失败: {str(e)}")
    
    def mysql_only_show_tables(self) -> List[str]:
        """MySQL 专用：显示所有表（使用 SHOW TABLES 命令）
        
        仅适用于 MySQL 数据库, 使用原生 SQL 命令显示所有表。
        
        Returns:
            List[str]: 表名列表
            
        Raises:
            Exception: 如果不是 MySQL 数据库或执行失败
            
        Example:
            >>> tables = toolkit.mysql_only_show_tables()
            >>> print(f"MySQL 数据库中有 {len(tables)} 个表")
        """
        if not self.engine or 'mysql' not in str(self.engine.url):
            raise Exception("SHOW TABLES 命令仅适用于 MySQL 数据库")
        
        try:
            result = self.execute_raw_sql("SHOW TABLES")
            tables = [row[0] for row in result]
            return tables
        except Exception as e:
            raise Exception(f"执行 SHOW TABLES 命令失败: {str(e)}")
    
    def postgresql_only_show_tables(self) -> List[str]:
        """PostgreSQL 专用：显示所有表（使用 \\dt 等效命令）
        
        仅适用于 PostgreSQL 数据库, 使用原生 SQL 命令显示所有表。
        
        Returns:
            List[str]: 表名列表
            
        Raises:
            Exception: 如果不是 PostgreSQL 数据库或执行失败
            
        Example:
            >>> tables = toolkit.postgresql_only_show_tables()
            >>> print(f"PostgreSQL 数据库中有 {len(tables)} 个表")
        """
        if not self.engine or 'postgresql' not in str(self.engine.url):
            raise Exception("此功能仅适用于 PostgreSQL 数据库")
        
        try:
            result = self.execute_raw_sql("""
                SELECT table_name 
                FROM information_schema.tables 
                WHERE table_schema = 'public' 
                AND table_type = 'BASE TABLE'
            """)
            tables = [row[0] for row in result]
            return tables
        except Exception as e:
            raise Exception(f"查询 PostgreSQL 表失败: {str(e)}")
    
    def sql_server_only_show_tables(self) -> List[str]:
        """SQL Server 专用：显示所有表
        
        仅适用于 SQL Server 数据库, 使用原生 SQL 命令显示所有表。
        
        Returns:
            List[str]: 表名列表
            
        Raises:
            Exception: 如果不是 SQL Server 数据库或执行失败
            
        Example:
            >>> tables = toolkit.sql_server_only_show_tables()
            >>> print(f"SQL Server 数据库中有 {len(tables)} 个表")
        """
        if not self.engine or 'mssql' not in str(self.engine.url):
            raise Exception("此功能仅适用于 SQL Server 数据库")
        
        try:
            result = self.execute_raw_sql("SELECT name FROM sys.tables")
            tables = [row[0] for row in result]
            return tables
        except Exception as e:
            raise Exception(f"查询 SQL Server 表失败: {str(e)}")
    
    def oracle_only_show_tables(self) -> List[str]:
        """Oracle 专用：显示所有表
        
        仅适用于 Oracle 数据库, 使用原生 SQL 命令显示所有表。
        
        Returns:
            List[str]: 表名列表
            
        Raises:
            Exception: 如果不是 Oracle 数据库或执行失败
            
        Example:
            >>> tables = toolkit.oracle_only_show_tables()
            >>> print(f"Oracle 数据库中有 {len(tables)} 个表")
        """
        if not self.engine or 'oracle' not in str(self.engine.url):
            raise Exception("此功能仅适用于 Oracle 数据库")
        
        try:
            result = self.execute_raw_sql("SELECT table_name FROM user_tables")
            tables = [row[0] for row in result]
            return tables
        except Exception as e:
            raise Exception(f"查询 Oracle 表失败: {str(e)}")
    
    def __repr__(self) -> str:
        """返回对象的字符串表示
        
        Returns:
            str: 对象的字符串表示
        """
        engine_info = f"Engine: {self.engine.url}" if self.engine else "Engine: None"
        session_info = f"Session: {self.session}" if self.session else "Session: None"
        return f"SqlalchemyToolkit({engine_info}, {session_info})"
    
    def __str__(self) -> str:
        """返回对象的字符串表示
        
        Returns:
            str: 对象的字符串表示
        """
        return self.__repr__()
    
    def __del__(self):
        """析构函数, 确保资源被正确释放"""
        self.close()
