"""时间工具类 DateTimeUtils"""
import time
from datetime import datetime, timedelta

ACCURACY_TIME = "%Y-%m-%d %H:%M:%S"  # 年 - 月 - 日 时：分：秒
YEAR_MONTH_DAYS = "%Y-%m-%d"  # 年 - 月 - 日
YEAR_MONTHABBR_DAYS = "%Y-%b-%d"  # 年 - 月(缩写) - 日
YYYYmmdd = "%Y%m%d"
HOUR_MINUTE_SECOND = "%H:%M:%S"  # 时：分：秒
YEAR = "%Y"  # 年
MONTH = "%m"  # 月
MONTH_ABBR = "%b"  # 月份缩写名称, 如: Jan, Feb, Mar, Apr, May, Jun, Jul, Aug, Sep, Oct, Nov, Dec
WEEK = "%w"  # 周
DAYS = "%d"  # 日
HOUR = "%H"  # 时, 24 小时
MINUTE = "%M"  # 分
SECOND = "%S"  # 秒
MICROSECOND = "%f"  # 微秒

def load_str_to_datetime(time_str: str, pattern: str) -> datetime:
    """将时间字符串转换成datetime对象

    Args:
        time_str: 时间字符串
        pattern: time_str对应的时间格式

    Returns:
        修改格式后的时间

    Examples:
        >>> DateTimeUtils.load_str_to_datetime("2023-05-11", "%Y-%m-%d") # 修改时间格式为yyyymmdd
    """
    return datetime.strptime(time_str, pattern)

def load_datetime_to_str(datetime: datetime, pattern: str) -> str:
    """将datetime对象转换成时间字符串

    Args:
        datetime: datetime对象
        pattern: 转换成字符串后的时间格式

    Returns:
        修改格式后的时间
    """
    return datetime.strftime(pattern)

def load_timestamp_to_datetime(timestamp: float) -> datetime:
    """
    将datetime对象转换成时间戳

    Args:
        datetime: datetime对象
        pattern: 转换成字符串后的时间格式

    Returns:
        修改格式后的时间
    """
    return datetime.fromtimestamp(timestamp)

def load_datetime_to_timestamp(datetime: datetime) -> float:
    """将datetime对象转换成时间戳

    Args:
        datetime (datetime): datetime对象

    Returns:
        float: 时间戳
    """
    return time.mktime(datetime.timetuple())

def format_datetime(year: int, month: int=1, day: int=1, hour: int=0, minute: int=0, second: int=0, 
                   microsecond: int=0, transfer_to_str: bool=True, pattern: str="%Y-%m-%d %H:%M:%S.%f") -> str|datetime:
    """将时间格式化

    Args:
        year (int): 年
        month (int, optional): 月. Defaults to 1.
        day (int, optional): 日. Defaults to 1.
        hour (int, optional): 时. Defaults to 0.
        minute (int, optional): 分. Defaults to 0.
        second (int, optional): 秒. Defaults to 0.
        microsecond (int, optional): 毫秒. Defaults to 0.
        transfer_to_str (bool, optional): 是否转换成字符串. Defaults to True.
        pattern (str, optional): 时间格式. Defaults to "%Y-%m-%d %H:%M:%S.%f".

    Returns:
        str|datetime: 时间字符串或datetime对象, 取决于transfer_to_str的值
    """
    time = datetime(year, month, day, hour, minute, second, microsecond)
    if transfer_to_str:
        return time.strftime(pattern)  # 转换成字符串格式
    return time

def format_second_to_time(second: int|float|None, keep_millisecond: bool=False) -> str:
    """将秒数转换成时间字符串

    Args:
        second (int | float): 秒, 为None则返回--:--:--
        keep_millisecond (bool, optional): 是否保留毫秒. Defaults to False.

    Returns:
        str: 时间字符串, 格式H:mm:ss或H:mm:ss.ms
    """
    if second is None:
        return "--:--:--"
    total_seconds = timedelta(seconds=second).total_seconds()
    if not keep_millisecond:
        total_seconds = total_seconds - (total_seconds % timedelta(seconds=1).total_seconds())
    return str(timedelta(seconds=total_seconds))

def record(global_record: bool=False) -> float:
    """记录当前时间

    Args:
        global_record (bool, optional): 是否全局记录时间变量. Defaults to False.
    
    Returns:
        时间浮点
    """
    if global_record:
        global record_time
    record_time = time.time()
    return record_time

def end_record_and_caculate(start_time: float=None, print_message: bool=False, round_index=3, type="s") -> float:
    """计算时间差, 通常用来记录函数执行所消耗的时间

    Args:
        start_time (float, optional): 开始时间, 为None则使用record_time(需要record函数开启global_record). Defaults to None.
        print_message (bool, optional): 是否打印信息. Defaults to False.
        round_index (int, optional): 结果保留多少位. Defaults to 3.
        type (str, optional): 返回类型, 有秒s、分钟min、小时h. Defaults to "s".

    Raises:
        ValueError: type参数错误

    Returns:
        float: 时间差
        
    Examples:
        >>> DateTimeUtils.record()
        >>> print("test")
        >>> DateTimeUtils.end_record_and_caculate()
        Time spent: 0.001 s
    """
    if start_time is None:
        s = round(time.time() - record_time, round_index)
    else:
        s = round(time.time() - start_time, round_index)
    if print_message:
        time_spend_result = f"{round(s / 60, 3)} min" if 60 * 60 > s > 60  \
            else f"{round(s / 60 / 60, 3)} h" if s > 60 * 60 else f"{round(s, 3)} s"
        print(f"Time spent: {time_spend_result}")
    if type == "s":
        return s
    elif type == "min":
        return round(s / 60, round_index)
    elif type == "h":
        return round(s / 60 / 60, round_index)
    else:
        raise ValueError(f"Unrecognized type, cannot be {type}")

def caculate_times(start: str, end: str, pattern: str = "%H:%M:%S", return_mode="s", ndigits_number=1) -> float:
    """计算两段时间的间隔

    Args:
        start: 开始的准确时间, 格式根据形参pattern的格式输入
        end: 结束的准确时间, 格式根据形参pattern的格式输入
        pattern: 输入和返回时间的基准格式, 默认时:分:秒
        return_mode: 返回什么单位的时间差, 单位为秒s、分钟min、小时h、天day、月month和年year
        ndigits_number: 保留多少位
      
    Returns:
        时间差计算结果
    """
    d1 = datetime.strptime(start, pattern)
    d2 = datetime.strptime(end, pattern)
    d = d2 - d1
    if return_mode == "s":
        return round(d.total_seconds(), ndigits_number)
    elif return_mode == "min":
        return round(d.total_seconds() / 60, ndigits_number)
    elif return_mode == "h":
        return round(d.total_seconds() / 3600, ndigits_number)
    elif return_mode == "day":
        return d.days
    elif return_mode == "month":
        return round(d.days / 30, ndigits_number)
    elif return_mode == "year":
        return round(d.days / 365, ndigits_number)
    else:
        raise ValueError(f"Unrecognized type, cannot be {return_mode}")
      
def caculate_timer(func):
    """以装饰器的形式, 计算函数执行的所需时间, 在函数上@该函数即可

    Args:
        func: 运行函数
    """
    def func_wrapper(*args, **kwargs):
        time_start = time.time()
        result = func(*args, **kwargs)
        time_end = time.time()
        time_spend = time_end - time_start
        time_spend_result = f"{round(time_spend / 60, 3)} min" if 60 * 60 > time_spend > 60  \
            else f"{round(time_spend / 60 / 60, 3)} h" if time_spend > 60 * 60 else f"{round(time_spend, 3)} s"
        print(f"Function [{func.__name__}] total spent time: {time_spend_result}")
        return result
    return func_wrapper

def split_times(time: str, pattern: str) -> dict:
    """分割时间字符串

    Args:
        time: 时间字符串
        pattern: 时间字符串的匹配模式

    Returns:
        结果字典, 格式为{
        "year": xxxxx,
        "month": xxxxx,
        "day": xxxxx,
        "hour": xxxxx,
        "minute": xxxxx,
        "second": xxxxx,
        "microsecond": xxxxx
        }
    """
    time_split = datetime.strptime(time, pattern)
    return {
        "year": time_split.year,
        "month": time_split.month,
        "day": time_split.day,
        "hour": time_split.hour,
        "minute": time_split.minute,
        "second": time_split.second,
        "microsecond": time_split.microsecond,
    }

def get_day_by_caculate(time: str, days=-1, pattern: str = "%Y-%m-%d") -> str:
    """计算参数时间为基准的时间

    Args:
        time: 基准时间,年-月-日
        days: 计算的时间, -1为昨天
        pattern: 输入和返回日期的基准格式, 默认年-月-日

    Returns:
        计算后时间, 格式以pattern为基准

    Examples:
        >>> caculate = DateTimeUtils.get_day_by_caculate("2023-05-11")
        2023-05-10
        >>> caculate = DateTimeUtils.get_day_by_caculate("2023-04-12", days=1)
        2023-04-13
        >>> caculate = DateTimeUtils.get_day_by_caculate("2023-04-12", days=-366) # 获取一年前的日期
        2022-04-13
    """
    base_time = datetime.strptime(time, pattern)
    caculate = base_time + timedelta(days=days)
    return caculate.strftime(pattern)

def get_day(days=0, pattern: str = "%Y-%m-%d", transfer_to_str=True) -> str | datetime:
    """获取某日期

    Args:
        days: 今天为0, 昨天为-1, 以此类推
        pattern: 输入和返回日期的基准格式, 默认年-月-日

    Returns:
        日期, 格式以pattern为基准

    Examples:
        >>> DateTimeUtils.get_day() # 假设今天是2023-05-11
        2023-05-11
        >>> DateTimeUtils.get_day(-1)
        2023-05-10
    """
    now = datetime.now()
    day = now + timedelta(days=days)
    if transfer_to_str:
        return day.strftime(pattern)
    else:
        return day

def get_week_day(time: str, pattern: str = "%Y-%m-%d") -> int:
    """判断时间字符串是星期几

    Args:
        time (str): 时间字符串
        pattern (str, optional): 输入日期的基准格式. Defaults to "%Y-%m-%d".

    Returns:
        int: 星期几, 星期一到星期日按时间顺序为: 1, 2, 3, 4, 5, 6, 7
    """
    date_obj = datetime.strptime(time, pattern)
    return date_obj.weekday()+1

def get_month_end_day(month: int, pattern: str = "%Y-%m-%d") -> str:
    """获取某月月底

    Args:
        month: 月份
        pattern: 返回日期的基准格式, 默认年-月-日

    Returns:
        该月月底, 格式以pattern为基准
    """
    if month < 1 or month > 12:
        raise Exception(f"Invalid input parameters, there is no month {month}")
    next_month = month + 1 if month != 12 else 1
    next_month_start_day = get_day(pattern=f"%Y-0{next_month}-01") if next_month < 10 else get_day(pattern=f"%Y-{next_month}-01")  # 找到这个月的下一个月月初, 以此减一从而获取这个月月底
    month_end_day = get_day_by_caculate(next_month_start_day)
    if pattern == "%Y-%m-%d":
        return month_end_day
    else:
        return change_pattern(month_end_day, "%Y-%m-%d", pattern)

def change_pattern(time: str, re_pattern: str, pattern: str) -> str:
    """修改时间格式

    Args:
        time: 时间
        re_pattern: 输入时间的原格式
        pattern: 修改后的格式

    Returns:
        修改格式后的时间

    Examples:
        >>> DateTimeUtils.change_pattern("2023-05-11", "%Y-%m-%d","%Y%m%d") # 修改时间格式为yyyymmdd
        20230510
    """
    return datetime.strptime(time, re_pattern).strftime(pattern)

def check_pattern(time: str, pattern: str) -> bool:
    """检查是否时间字符串是否为对应的匹配格式

    Args:
        time: 待匹配时间字符串
        pattern: 对应匹配格式

    Returns:
        True或False

    Examples:
        >>> DateTimeUtils.check_pattern("2023-09-06", "%Y%m%d")
        False
        >>> DateTimeUtils.check_pattern("2023-09-06", "%Y-%m-%d")
        True
    """
    try:
        datetime.strptime(time, pattern)
        return True
    except:
        return False
