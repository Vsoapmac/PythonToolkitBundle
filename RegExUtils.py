"""正则表达式工具类 RegExUtils"""
import re


ANY_STR_PATTERN = r'\w+' # 匹配任意字符
ANY_NUMBER_PATTERN = r'\d+' # 匹配数字
ANY_WORD_PATTERN = r'[a-zA-Z]+' # 匹配字母
ANY_EMAIL_PATTERN = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}' # 匹配email
ANY_URL_PATTERN = r'https?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\\(\\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+' # 匹配url
ANY_CHINESE_PATTERN = r'[\u4e00-\u9fa5]+' # 匹配中文
ANY_CHINA_PHONE_NUMBER_PATTERN = r'1[3-9]\d{9}' # 匹配中国大陆手机号
ANY_CHINA_PERSONAL_ID_NUMBER_PATTERN = r'\d{17}(\d|X|x)$' # 匹配中国大陆身份证号
ANY_YYYY_MM_DD_PATTERN = r'\d{4}-\d{2}-\d{2}$' # 匹配日期(YYYY-MM-DD)
ANY_HH_MM_SS_PATTERN = r'\d{2}:\d{2}:\d{2}$' # 匹配时间(HH:MM:SS)

def match(text: str, pattern: str) -> str:
    """匹配文本和正则表达式
    
    Args:
        text (str): 文本
        pattern (str): 正则表达式

    Returns:
        str: 匹配结果
    """
    result = re.match(pattern, text)
    if result:
        return result.group()
    else:
        return ""
    
def match_index(text: str, pattern: str, mode: str="start") -> int|tuple[int, int]:
    """匹配文本和正则表达式

    Args:
        text (str): 文本
        pattern (str): 正则表达式
        mode (str, optional): 模式, 选项有 start|end|span. Defaults to "start".

    Returns:
        int|tuple[int, int]: 匹配结果的索引
    """
    result = re.match(pattern, text)
    if result:
        if mode == "start":
            return result.start()
        elif mode == "end":
            return result.end()
        elif mode == "span":
            return result.span()
        else:
            raise Exception(f"unexpected mode for: {mode}")
    else:
        return -1
    
def match_groups(text: str, pattern: str) -> tuple:
    """匹配文本和正则表达式

    Args:
        text (str): 文本
        pattern (str): 正则表达式

    Returns:
        tuple: 匹配结果的分组
    """
    result = re.match(pattern, text)
    if result:
        return result.groups()
    else:
        return ()

def search(text: str, pattern: str) -> str:
    """搜索文本和正则表达式

    Args:
        text (str): 文本
        pattern (str): 正则表达式

    Returns:
        str: 匹配结果
    """
    result = re.search(pattern, text)
    if result:
        return result.group()
    else:
        return ""
    
def search_index(text: str, pattern: str, mode: str="start") -> int|tuple[int, int]:
    """搜索文本和正则表达式

    Args:
        text (str): 文本
        pattern (str): 正则表达式
        mode (str, optional): 模式, 选项有 start|end|span. Defaults to "start".

    Returns:
        int|tuple[int, int]: 匹配结果的索引
    """
    result = re.search(pattern, text)
    if result:
        if mode == "start":
            return result.start()
        elif mode == "end":
            return result.end()
        elif mode == "span":
            return result.span()
        else:
            raise Exception(f"unexpected mode for: {mode}")
    else:
        return -1
    
def search_groups(text: str, pattern: str) -> tuple:
    """搜索文本和正则表达式

    Args:
        text (str): 文本
        pattern (str): 正则表达式

    Returns:
        tuple: 匹配结果的分组
    """
    result = re.search(pattern, text)
    if result:
        return result.groups()
    else:
        return ()
    
def replace(pattern_text: str, pattern: str, replace_with: str):
    """替换文本和正则表达式

    Args:
        pattern_text (str): 文本
        pattern (str): 正则表达式
        replace_with (str): 替换文本
    """
    re.sub(pattern, replace_with, pattern_text)

def spilt(text: str, pattern: str) -> list:
    """根据正则表达式分割文本

    Args:
        text (str): 文本
        pattern (str): 正则表达式

    Returns:
        list: 分割后的列表
    """
    return re.split(pattern, text)