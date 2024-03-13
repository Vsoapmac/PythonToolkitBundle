from sqlalchemy import create_engine, Engine, Column, Integer, String, Sequence
from sqlalchemy.orm import scoped_session, sessionmaker, Query
from sqlalchemy.ext.declarative import declarative_base


class Template_bean(declarative_base()):
    """无作用, 用于演示如何创建实体类"""
    __tablename__ = 'template' # 必须填写，对应数据表名
    id = Column(Integer, Sequence('user_id_seq'), primary_key=True, autoincrement=True)
    name = Column(String(50))
    age = Column(Integer)
    email = Column(String(120), unique=True)


class SqlalchemyToolkit:
    """Sqlalchemy工具类, 使用该类, 请运行如下命令安装所需库存:
    \npip install sqlalchemy
    """
    session = None
    
    def __init__(self, engine: Engine=None, mutiple_thread_session: bool=False):
        if engine:
            if not mutiple_thread_session:
                Session = sessionmaker(bind=engine)
                self.session = Session()
            else:
                Session = scoped_session(sessionmaker(bind=engine))
                self.session = Session()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.session:
            self.session.close_all()
            self.session = None
    
    def create_mysql_engine(self, username: str, password: str, database_name: str, host: str="localhost", port: int=3306, 
                            connect_url_parm: str="?charset=utf8", echo: bool=True, pool_size: int=20) -> Engine:
        """创建mysql引擎, 使用前应该执行如下命令安装数据库驱动: 
        \npip install pymysql
        
        Args:
            username (str): 数据库用户名
            password (str): 数据库密码
            database_name (str): 数据库名
            host (str, optional): 数据库host. Defaults to "localhost".
            port (int, optional): 数据库端口号. Defaults to 3306.
            connect_url_parm (str, optional): 连接参数, 注意第一个字符应该为?. Defaults to "?charset=utf8".
            echo (bool, optional): 系统打印所生成的SQL. Defaults to True.
            pool_size (int, optional): 连接池中保持的连接数. Defaults to 20.

        Returns:
            Engine: 数据库引擎
        """
        return create_engine(f"mysql+pymysql://{username}:{password}@{host}:{port}/{database_name}{connect_url_parm}", echo=echo, pool_size=pool_size)
    
    def create_postgresql_engine(self, username: str, password: str, database_name: str, host: str="localhost", port: int=5432, 
                                 connect_url_parm: str="", echo: bool=True, pool_size: int=20) -> Engine:
        """创建postgresql引擎, 使用前应该执行如下命令安装数据库驱动: 
        \npip install psycopg2

        Args:
            username (str): 数据库用户名
            password (str): 数据库密码
            database_name (str): 数据库名
            host (str, optional): 数据库host. Defaults to "localhost".
            port (int, optional): 数据库端口号. Defaults to 5432.
            connect_url_parm (str, optional): 连接参数, 注意第一个字符应该为?. Defaults to "".
            echo (bool, optional): 系统打印所生成的SQL. Defaults to True.
            pool_size (int, optional): 连接池中保持的连接数. Defaults to 20.

        Returns:
            Engine: 数据库引擎
        """
        return create_engine(f"postgresql+psycopg2://{username}:{password}@{host}:{port}/{database_name}{connect_url_parm}", echo=echo, pool_size=pool_size)
    
    def create_sql_server_engine(self, username: str, password: str, database_name: str, host: str="localhost", port: int=1433, 
                                 connect_url_parm: str="?driver=ODBC+Driver+17+for+SQL+Server", echo: bool=True, pool_size: int=20) -> Engine:
        """创建oracle引擎, 使用前应该执行如下命令安装数据库驱动: 
        \npip install pyodbc

        Args:
            username (str): 数据库用户名
            password (str): 数据库密码
            database_name (str): 数据库名
            host (str, optional): 数据库host. Defaults to "localhost".
            port (int, optional): 数据库端口号. Defaults to 1433.
            connect_url_parm (str, optional): 连接参数, 注意第一个字符应该为?. Defaults to "?driver=ODBC+Driver+17+for+SQL+Server".
            echo (bool, optional): 系统打印所生成的SQL. Defaults to True.
            pool_size (int, optional): 连接池中保持的连接数. Defaults to 20.

        Returns:
            Engine: 数据库引擎
        """
        return create_engine(f"mssql+pyodbc://{username}:{password}@{host}:{port}/{database_name}{connect_url_parm}", echo=echo, pool_size=pool_size)
    
    def create_oracle_engine(self, username: str, password: str, service_name: str, host: str="localhost", port: int=1521, 
                             connect_url_parm: str="", echo: bool=True, pool_size: int=20) -> Engine:
        """创建oracle引擎, 使用前应该执行如下命令安装数据库驱动: 
        \npip install cx_Oracle

        Args:
            username (str): 数据库用户名
            password (str): 数据库密码
            service_name (str): 数据库名
            host (str, optional): 数据库host. Defaults to "localhost".
            port (int, optional): 数据库端口号. Defaults to 1521.
            connect_url_parm (str, optional): 连接参数, 注意第一个字符应该为?. Defaults to "".
            echo (bool, optional): 系统打印所生成的SQL. Defaults to True.
            pool_size (int, optional): 连接池中保持的连接数. Defaults to 20.

        Returns:
            Engine: 数据库引擎
        """
        return create_engine(f"oracle+cx_oracle://{username}:{password}@{host}:{port}/{service_name}{connect_url_parm}", echo=echo, pool_size=pool_size)
    
    def create_session(self, engine: Engine, mutiple_thread_session: bool=False):
        """创建session

        Args:
            engine (Engine): 引擎
            mutiple_thread_session (bool, optional): 是否创建多线程session. Defaults to False.
        """
        if not mutiple_thread_session:
            Session = sessionmaker(bind=engine)
            self.session = Session()
        else:
            Session = scoped_session(sessionmaker(bind=engine))
            self.session = Session()
        
    def close(self, close_all: bool=False):
        """关闭引擎

        Args:
            close_all (bool, optional): 关闭所有的session, 用于线程池连接数据库的逻辑. Defaults to False.
        """
        if not close_all:
            self.session.close()
        else:
            self.session.close_all()
        self.session = None
        
    def execute_SQL(self, SQL: str):
        """执行原生SQL

        Args:
            SQL (str): SQL

        Returns:
            执行结果
        """
        return self.session.execute(SQL)
    
    def insert(self, bean: declarative_base):
        """插入数据

        Args:
            bean (declarative_base): 数据表对象实体类
        """
        try:
            self.session.add(bean)
            self.session.commit()
        except:
            self.session.rollback()
            raise Exception("insert data fail")
        
    def insert_all(self, beans: list[declarative_base]):
        """插入多行数据

        Args:
            beans (list): 数据表对象实体类列表
        """
        try:
            self.session.add_all(beans)
            self.session.commit()
        except:
            self.session.rollback()
            raise Exception("insert data fail")
        
    def delete(self, bean: declarative_base):
        """删除数据

        Args:
            bean (declarative_base): 数据表对象实体类
        """
        try:
            self.session.delete(bean)
            self.session.commit()
        except:
            self.session.rollback()
            raise Exception("delete data fail")
    
    def update(self, bean: declarative_base, update_condition: dict, *condition: bool):
        """更新数据

        Args:
            bean (declarative_base): 数据表对象实体类
            update_condition (dict): 更新条件
            condition (bool): 过滤的条件
        """
        try:
            self.session.query(bean).filter(*condition).update(update_condition)
            self.session.commit()
        except:
            self.session.rollback()
            raise Exception("update data fail")
    
    def query(self, bean: declarative_base) -> Query:
        """返回Query对象, 可用于直接使用sqlalchemy的链式查找

        Args:
            bean (declarative_base): 数据表对象实体类

        Returns:
            Query: Query对象
        """
        return self.session.query(bean)
    
    def count_datas(self, bean: declarative_base) -> int:
        """计算数据表有多少条数据

        Args:
            bean (declarative_base): 数据表对象实体类

        Returns:
            int: 数据条数
        """
        return self.session.query(bean).count()
    
    def select_all(self, bean: declarative_base) -> list:
        """查询所有的数据

        Args:
            bean (declarative_base): 数据表对象实体类

        Returns:
            list: 查询结果
        """
        return self.session.query(bean).all()
        
    def select_first(self, bean: declarative_base):
        """查询数据库第一条数据

        Args:
            bean (declarative_base): 数据表对象实体类

        Returns:
            查询结果
        """
        return self.session.query(bean).first()
    
    def select(self, bean: declarative_base, *condition: bool, group_by: Column=None, having: bool=None, 
               order_by: Column=None, limit: int=None, distinct: bool=None) -> list:
        """根据条件查询数据库

        Args:
            bean (declarative_base): 数据表对象实体类
            condition (bool): 过滤的条件
            group_by (Column, optional): 分组. Defaults to None.
            having (bool, optional): 过滤. Defaults to None.
            order_by (Column, optional): 排序. Defaults to None.
            limit (int, optional): 限制返回的行数. Defaults to None.
            distinct (bool, optional): 去除重复. Defaults to None.

        Returns:
            list: 查询结果
        """
        filter = self.session.query(bean).filter(*condition)
        if group_by:
            filter = filter.group_by(group_by)
        if having:
            filter = filter.having(having)
        if order_by:
            filter = filter.order_by(order_by)
        if group_by:
            filter = filter.group_by(group_by)
        if limit:
            filter = filter.limit(limit)
        if distinct:
            filter = filter.distinct()
        return filter.all()