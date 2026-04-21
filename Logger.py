# -*- coding: utf-8 -*-
"""
日志类Logger.py
若要使用, 则使用pip install loguru 安装loguru库
"""
import sys
from loguru import logger

def remove(handler_id: int=None):
    """移除配置

    Args:
        handler_id (int, optional): handler id. Defaults to None.
    """
    logger.remove(handler_id)

def add_config(sink=None, 
            level: str | int='INFO', 
            format: str="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | pid: <yellow>{process}</yellow> | tid: <magenta>{thread}</magenta> | <cyan>{name}:{function}:{line}</cyan> | <level>{level}</level> | {message}", 
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
    """
    logger.add(
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
    
def get_logger(user_opt: bool=True, **kwargs):
    """获取logger

    Args:
        user_opt (bool, optional): 是否使用logger.opt. Defaults to True.
        **kwargs: opt配置, 详情参考logger.opt. Defaults to None.

    Returns:
        logger: logger
    """
    if user_opt:
        return logger.opt(kwargs)
    else:
        return logger