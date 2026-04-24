# -*- coding: utf-8 -*-
"""
日志类Logger.py
若要使用, 则使用pip install loguru 安装loguru库
"""
import sys
from loguru import logger


def remove(handler_id: int = None):
    """移除配置

    Args:
        handler_id (int, optional): handler id. Defaults to None (移除所有).
    """
    if handler_id is not None:
        try:
            logger.remove(handler_id)
        except ValueError:
            pass
    else:
        logger.remove()


def add_config(sink=None,
               level: str | int = 'INFO',
               format: str = "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | pid: <yellow>{process}</yellow> | tid: <magenta>{thread}</magenta> | <cyan>{name}:{function}:{line}</cyan> | <level>{level}</level> | {message}",
               filter=None,
               backtrace=False,
               diagnose=False,
               enqueue=False,
               serialize=False,
               colorize=True,
               **kwargs):
    """增加配置, 配置参考loguru.logger.add()

    Args:
        sink (Any): 日志消息的输出位置, 可以是文件路径、标准输出(sys.stdout)、标准错误(sys.stderr, 默认)或其他自定义的输出位置
        level (str, optional): 记录级别. Defaults to 'INFO'.
        format (str, optional): 格式字符串. Defaults to "{time} {level} {message}".
        filter (Any, optional): 过滤器. Defaults to None.
        backtrace (bool, optional): 是否记录回溯信息. Defaults to False.
        diagnose (bool, optional): 是否在处理程序内部出现错误时记录诊断信息. Defaults to False.
        enqueue (bool, optional): 是否放入队列中处理, 通常应用在多线程中避免阻塞. Defaults to False.
        serialize (bool, optional): 是否进行序列化处理. Defaults to False.
        colorize (bool, optional): 是否进行着色处理. Defaults to True.

    Returns:
        int: handler id
    """
    return logger.add(
        sink=sys.stdout if sink is None else sink,
        level=level,
        format=format,
        filter=filter,
        backtrace=backtrace,
        diagnose=diagnose,
        enqueue=enqueue,
        serialize=serialize,
        colorize=colorize,
        **kwargs
    )

def get_logger(user_opt: bool = True, **kwargs):
    """获取logger

    Args:
        user_opt (bool, optional): 是否使用logger.opt. Defaults to True.
        **kwargs: opt配置, 详情参考logger.opt. Defaults to None.

    Returns:
        logger: logger
    """
    if user_opt:
        return logger.opt(**kwargs)
    else:
        return logger


class Logger:
    """logger懒人类"""

    def __init__(self, sys_log_level: str = "INFO", sys_log_args: dict = None,
                 enqueue: bool = False,
                 log_file_path: str = None, log_file_level: str = "INFO", log_file_args: dict = None):
        """初始化logger类

        Args:
            sys_log_level (str, optional): 系统输出的log等级. Defaults to "INFO".
            sys_log_args (dict, optional): 系统输出的logger配置, 配置参考loguru.logger.add(). Defaults to None.
            enqueue (bool, optional): 是否放入队列中处理, 通常应用在多线程中避免阻塞. Defaults to False.
            log_file_path (str, optional): log文件目录. Defaults to None.
            log_file_level (str, optional): log文件输出的log等级. Defaults to "INFO".
            log_file_args (dict, optional): log文件的logger配置, 配置参考loguru.logger.add(). Defaults to None.
        """
        remove()
        # 输出到控制台的log设置
        sys_kwargs = {
            "level": sys_log_level,
            "format": "<green>{time:YYYY-MM-DD HH:mm:ss}</green> | pid: <yellow>{process}</yellow> | tid: <magenta>{thread}</magenta> | <cyan>{name}:{function}:{line}</cyan> | <level>{level}</level> | {message}",
            "colorize": True,
            "backtrace": True,
            "enqueue": enqueue,
        }
        if sys_log_args:
            sys_kwargs.update(sys_log_args)
        add_config(**sys_kwargs)
        if log_file_path:
            # 输出到文件的log设置
            file_kwargs = {
                "sink": log_file_path,
                "level": log_file_level,
                "format": "{time:YYYY-MM-DD HH:mm:ss} | pid: {process} | tid: {thread} | {name}:{function}:{line} | {level} | {message}",
                "colorize": False,
                "enqueue": enqueue,
                "catch": True,
                "backtrace": True,
            }
            if log_file_args:
                file_kwargs.update(log_file_args)
            add_config(**file_kwargs)

    def get_logger(self, depth: int = 1):
        """获取logger

        Args:
            depth (int, optional): 调用深度. Defaults to 1.

        Returns:
            loguru.logger
        """
        return get_logger(user_opt=True, depth=depth)
