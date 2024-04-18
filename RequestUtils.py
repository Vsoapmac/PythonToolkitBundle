"""request工具类 RequestUtils, 若使用请执行如下命令安装第三方库: \n
\npip install requests
\npip install beautifulsoup4
\npip install lxml
"""
import requests, json, lxml, lxml.html
from bs4 import BeautifulSoup, Tag


def request(url: str, request_method: str="get", data: dict=None, params: dict=None, 
            headers: dict=None, cookies: dict=None, timeout: int=60) -> requests.Response:
    """发送请求并返回响应对象

    Args:
        url (str): 请求的url地址
        request_method (str, optional): 请求方法, 分别有 get|post|put|delete|head. Defaults to "get".
        data (dict, optional): 请求体, 使用get请求时通常可以忽略. Defaults to None.
        params (dict, optional): url参数, 这将在url中体现. Defaults to None.
        headers (dict, optional): 请求头. Defaults to None.
        cookies (dict, optional): 要发送的Cookie. Defaults to None.
        timeout (int, optional): 请求的超时时间. Defaults to 60.

    Returns:
        requests.Response: 响应对象
    """
    if request_method == "get":
        return requests.get(url, params=params, headers=headers, cookies=cookies, timeout=timeout)
    elif request_method == "post":
        return requests.post(url, data=data, headers=headers, cookies=cookies, timeout=timeout)
    elif request_method == "put":
        return requests.put(url, data=data, headers=headers, cookies=cookies, timeout=timeout)
    elif request_method == "delete":
        return requests.delete(url, data=data, headers=headers, cookies=cookies, timeout=timeout)
    elif request_method == "head":
        return requests.head(url, headers=headers, cookies=cookies, timeout=timeout)

def get_response_detail(url_or_response: str|requests.Response, request_method: str="get", data: dict=None, 
                        params: dict=None, headers: dict=None, cookies: dict=None, timeout: int=60) -> dict:
    """获取响应的详细信息

    Args:
        url (str|requests.Response): 请求的url地址或Response对象
        request_method (str, optional): 请求方法, 分别有 get|post|put|delete|head. Defaults to "get".
        data (dict, optional): 请求体, 使用get请求时通常可以忽略. Defaults to None.
        params (dict, optional): url参数, 这将在url中体现. Defaults to None.
        headers (dict, optional): 请求头. Defaults to None.
        cookies (dict, optional): 要发送的Cookie. Defaults to None.
        timeout (int, optional): 请求的超时时间. Defaults to 60.

    Returns:
        dict: 响应的详细信息, 包括url、状态码(status_code)、头部(headers)、cookies、编码(encoding)、内容(content)、文本(text)。
    """
    if isinstance(url_or_response, str):
        if request_method == "get":
            response = requests.get(url_or_response, data=data, params=params, headers=headers, cookies=cookies, timeout=timeout)
        elif request_method == "post":
            response = requests.post(url_or_response, data=data, params=params, headers=headers, cookies=cookies, timeout=timeout)
        elif request_method == "put":
            response = requests.put(url_or_response, data=data, params=params, headers=headers, cookies=cookies, timeout=timeout)
        elif request_method == "delete":
            response = requests.delete(url_or_response, data=data, params=params, headers=headers, cookies=cookies, timeout=timeout)
        elif request_method == "head":
            response = requests.head(url_or_response, data=data, params=params, headers=headers, cookies=cookies, timeout=timeout)
    elif isinstance(url_or_response, requests.Response):
        response = url_or_response
    return {
        "url": response.url,
        "status_code": response.status_code,
        "headers": response.headers,
        "cookies": response.cookies,
        "encoding": response.encoding,
        "content": response.content,
        "text": response.text
    }

def get_html(url: str, request_method: str="get", response_encoding: str="UTF-8", 
             data: dict=None, params: dict=None, headers: dict=None, cookies: dict=None, timeout: int=60) -> str:
    """获取html文本

    Args:
        url (str): 请求的url地址
        request_method (str, optional): 请求方法, 分别有 get|post|put|delete|head. Defaults to "get".
        response_encoding (str, optional): 响应编码. Defaults to "UTF-8".
        data (dict, optional): 请求体, 使用get请求时通常可以忽略. Defaults to None.
        params (dict, optional): url参数, 这将在url中体现. Defaults to None.
        headers (dict, optional): 请求头. Defaults to None.
        cookies (dict, optional): 要发送的Cookie. Defaults to None.
        timeout (int, optional): 请求的超时时间. Defaults to 60.

    Returns:
        str: html文本内容
    """
    if request_method == "get":
        response = requests.get(url, data=data, params=params, headers=headers, cookies=cookies, timeout=timeout)
    elif request_method == "post":
        response = requests.post(url, data=data, params=params, headers=headers, cookies=cookies, timeout=timeout)
    elif request_method == "put":
        response = requests.put(url, data=data, params=params, headers=headers, cookies=cookies, timeout=timeout)
    elif request_method == "delete":
        response = requests.delete(url, data=data, params=params, headers=headers, cookies=cookies, timeout=timeout)
    elif request_method == "head":
        response = requests.head(url, data=data, params=params, headers=headers, cookies=cookies, timeout=timeout)
    response.encoding = response_encoding
    return response.text

def parse_html(html_text: str, parse_method: str="lxml", use_original_lxml: bool=False) -> BeautifulSoup|lxml.html.HtmlElement:
    """将html文本解析为BeautifulSoup或lxml.html.HtmlElement对象

    Args:
        html_text (str): html文本
        parse_method (str, optional): 解析方法, 分别有 html.parser|lxml|xml|html5lib. Defaults to "lxml".
        use_original_lxml (bool, optional): 是否加载为lxml.html.HtmlElement对象. Defaults to False.

    Returns:
        BeautifulSoup|lxml.html.HtmlElement: BeautifulSoup对象或lxml.html.HtmlElement对象
    """
    if not use_original_lxml:
        html_parser = BeautifulSoup(html_text, parse_method)
    else:
        html_parser = lxml.html.fromstring(html_text, parse_method)
    return html_parser

def json_fomatter(json_text: str|dict, save_file: str|None=None, print_json: bool=False, indent=4, sort_keys=True) -> str:
    """格式化json文本

    Args:
        json_text (str | dict): json文本, 键值对类型的也支持
        save_file (str | None, optional): 保存文件路径. Defaults to None.
        print_json (bool, optional): 是否打印到控制台. Defaults to False.
        indent (int, optional): 每个级别缩进多少个空格. Defaults to 4.
        sort_keys (bool, optional): 是否对字典进行排序. Defaults to True.

    Returns:
        str: 格式化后的json文本
    """
    dump_json = json.dumps(json_text, indent=indent, sort_keys=sort_keys)
    if save_file:
        with open(save_file, "w", encoding="utf-8") as f:
            f.write(dump_json)
    if print_json:
        print_json(dump_json)
    return dump_json

def html_fomatter(html_text: str, save_file: str|None=None, print_html: bool=False, parse_method: str="lxml") -> str:
    """格式化html文本

    Args:
        html_text (str): html文本
        save_file (str|None, optional): 保存文件路径. Defaults to None.
        print_html (bool, optional): 是否打印到控制台. Defaults to False.
        parse_method (str, optional): 解析方法, 分别有 html.parser|lxml|xml|html5lib. Defaults to "lxml".

    Returns:
        str: 格式化后的html文本内容
    """
    soup = BeautifulSoup(html_text, parse_method)
    pretty_html = soup.prettify()
    if save_file:
        with open(save_file, "w", encoding="utf-8") as f:
            f.write(pretty_html)
    if print_html:
        print(pretty_html)
    return pretty_html

def find(html: str|BeautifulSoup|Tag|lxml.html.HtmlElement, tag: str=None, attrs: dict=None, xpath: str=None, 
         recursive: bool=True, text: str=None, parse_method: str="lxml", **kwargs) -> Tag|lxml.html.HtmlElement:
    """寻找第一个符合条件的标签

    Args:
        html (str | BeautifulSoup | Tag | lxml.html.HtmlElement): html文本、BeautifulSoup对象、Tag对象、lxml.html.HtmlElement对象
        tag (str, optional): 标签名. Defaults to None.
        attrs (dict, optional): 标签属性, eg:{"class": "tag-class"}. Defaults to None.
        xpath (str, optional): xpath表达式. Defaults to None.
        recursive (bool, optional): 是否递归返回该标签的子标签. Defaults to True.
        text (str | None, optional): 标签的文本, 会根据标签中的文本搜索对应的标签. Defaults to None.
        parse_method (str, optional): 解析方法, 分别有 html.parser|lxml|xml|html5lib. Defaults to "html.parser".

    Raises:
        Exception: 无法找到对应标签

    Returns:
        Tag|lxml.html.HtmlElement: Tag或lxml.html.HtmlElement对象
    """
    # ---------- 为字符串并且没有传入xpath时变为BeautifulSoup对象 ----------
    if isinstance(html, str) and xpath is None:
        soup = BeautifulSoup(html, parse_method)
        tag = soup.find(tag, attrs, recursive, text, **kwargs)
    # ---------- 为字符串并且传入xpath时变为lxml.html.HtmlElement对象 ----------
    elif isinstance(html, str) and xpath:
        html_parser = lxml.html.fromstring(html, parse_method)
        tag = html_parser.xpath(xpath)[0] if len(html_parser.xpath(xpath)) > 0 else None
    # ---------- 为BeautifulSoup对象或Tag对象并且没有传入xpath时使用对应对象执行 ----------
    elif isinstance(html, BeautifulSoup) or isinstance(html, Tag) and xpath is None:
        tag = html.find(tag, attrs, recursive, text, **kwargs)
    # ---------- 为BeautifulSoup对象或Tag对象并且传入xpath时变为lxml.html.HtmlElement对象 ----------
    elif isinstance(html, BeautifulSoup) or isinstance(html, Tag) and xpath:
        html_parser = lxml.html.fromstring(str(html), parse_method)
        tag = html_parser.xpath(xpath)[0] if len(html_parser.xpath(xpath)) > 0 else None
    # ---------- 为lxml.html.HtmlElement对象时使用对应对象执行 ----------
    elif isinstance(html, lxml.html.HtmlElement):
        tag = html.xpath(xpath)[0] if len(html.xpath(xpath)) > 0 else None
    if tag is None:
        raise Exception("Could not find the specific tag.")
    return tag

def find_all(html: str|BeautifulSoup|Tag|lxml.html.HtmlElement, tag: str=None, attrs: dict=None, xpath: str=None, 
             recursive: bool=True, text: str=None, limit: int=None, parse_method: str="lxml", **kwargs) -> list[Tag|lxml.html.HtmlElement]:
    """寻找所有符合条件的标签

    Args:
        html (str | BeautifulSoup | Tag | lxml.html.HtmlElement): html文本、BeautifulSoup对象、Tag对象、lxml.html.HtmlElement对象
        tag (str, optional): 标签名. Defaults to None.
        attrs (dict, optional): 标签属性, eg:{"class": "tag-class"}. Defaults to None.
        xpath (str, optional): xpath表达式. Defaults to None.
        recursive (bool, optional): 是否递归返回该标签的子标签. Defaults to True.
        text (str | None, optional): 标签的文本, 会根据标签中的文本搜索对应的标签. Defaults to None.
        limit (int, optional): 限制返回标签的数量, 假设为1, 则返回一个标签, 以此类推. Defaults to None.
        parse_method (str, optional): 解析方法, 分别有 html.parser|lxml|xml|html5lib. Defaults to "lxml".

    Raises:
        Exception: 无法找到对应标签

    Returns:
        list[Tag|lxml.html.HtmlElement]: Tag或lxml.html.HtmlElement对象列表
    """
    # ---------- 为字符串并且没有传入xpath时变为BeautifulSoup对象 ----------
    if isinstance(html, str) and xpath is None:
        soup = BeautifulSoup(html, parse_method)
        tags = soup.find_all(tag, attrs, recursive, text, limit, **kwargs)
        tags = list(tags)
    # ---------- 为字符串并且传入xpath时变为lxml.html.HtmlElement对象 ----------
    elif isinstance(html, str) and xpath:
        html_parser = lxml.html.fromstring(html, parse_method)
        tags = html_parser.xpath(xpath)[:limit] if limit else html_parser.xpath(xpath)
    # ---------- 为BeautifulSoup对象或Tag对象并且没有传入xpath时使用对应对象执行 ----------
    elif isinstance(html, BeautifulSoup) or isinstance(html, Tag) and xpath is None:
        tags = html.find_all(tag, attrs, recursive, text, limit, **kwargs)
        tags = list(tags)
    # ---------- 为BeautifulSoup对象或Tag对象并且传入xpath时变为lxml.html.HtmlElement对象 ----------
    elif isinstance(html, BeautifulSoup) or isinstance(html, Tag) and xpath:
        html_parser = lxml.html.fromstring(str(html), parse_method)
        tags = html_parser.xpath(xpath)[:limit] if limit else html_parser.xpath(xpath)
    # ---------- 为lxml.html.HtmlElement对象时使用对应对象执行 ----------
    elif isinstance(html, lxml.html.HtmlElement):
        tags = html.xpath(xpath)
        tags = tags[:limit] if limit else tags
    if len(tags) == 0:
        raise Exception("Could not find the specific tags.")
    return tags

def find_parent(html: str|BeautifulSoup|Tag|lxml.html.HtmlElement, tag: str=None, attrs: dict=None, 
                parse_method: str="lxml", encoding: str='unicode', method: str='html', **kwargs) -> Tag:
    """查找当前元素的父元素(最近的那一个)

    Args:
        html (str | BeautifulSoup | Tag | lxml.html.HtmlElement): html文本、BeautifulSoup对象、Tag对象、lxml.html.HtmlElement对象
        tag (str, optional): 标签名. Defaults to None.
        attrs (dict, optional): 标签属性, eg:{"class": "tag-class"}. Defaults to None.
        parse_method (str, optional): 解析方法, 分别有 html.parser|lxml|xml|html5lib. Defaults to "lxml".
        encoding (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的编码方式, 分别有 unicode|utf8|utf8-sig. Defaults to 'unicode'.
        method (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的解析方法, 分别有 html|xml. Defaults to 'html'.
        
    Raises:
        Exception: 无法找到对应标签

    Returns:
        Tag: 标签Tag对象
    """
    if isinstance(html, str):
        soup = BeautifulSoup(html, parse_method)
        tag = soup.find_parent(tag, attrs, **kwargs)
    elif isinstance(html, BeautifulSoup) or isinstance(html, Tag):
        tag = html.find_parent(tag, attrs, **kwargs)
    elif isinstance(html, lxml.html.HtmlElement):
        to_str = lxml.etree.tostring(html, encoding=encoding, method=method)
        soup = BeautifulSoup(to_str, parse_method)
        tag = soup.find_parent(tag, attrs, **kwargs)
    if tag is None:
        raise Exception("Could not find the specific tag.")
    return tag

def find_parents(html: str|BeautifulSoup|Tag|lxml.html.HtmlElement, tag: str=None, attrs: dict=None, limit: int=None, 
                 parse_method: str="lxml", encoding: str='unicode', method: str='html', **kwargs) -> list[Tag]:
    """查找当前元素的所有祖先元素

    Args:
        html (str | BeautifulSoup | Tag | lxml.html.HtmlElement): html文本、BeautifulSoup对象、Tag对象、lxml.html.HtmlElement对象
        tag (str, optional): 标签名. Defaults to None.
        attrs (dict, optional): 标签属性, eg:{"class": "tag-class"}. Defaults to None.
        limit (int, optional): 限制返回标签的数量, 假设为1, 则返回一个标签, 以此类推. Defaults to None.
        parse_method (str, optional): 解析方法, 分别有 html.parser|lxml|xml|html5lib. Defaults to "lxml".
        encoding (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的编码方式, 分别有 unicode|utf8|utf8-sig. Defaults to 'unicode'.
        method (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的解析方法, 分别有 html|xml. Defaults to 'html'.
        
    Raises:
        Exception: 无法找到对应标签

    Returns:
        list[Tag]: 标签Tag对象列表
    """
    if isinstance(html, str):
        soup = BeautifulSoup(html, parse_method)
        tags = soup.find_parents(tag, attrs, limit, **kwargs)
    elif isinstance(html, BeautifulSoup) or isinstance(html, Tag):
        tags = html.find_parents(tag, attrs, limit, **kwargs)
    elif isinstance(html, lxml.html.HtmlElement):
        to_str = lxml.html.tostring(html, encoding=encoding, method=method)
        soup = BeautifulSoup(to_str, parse_method)
        tags = soup.find_parents(tag, attrs, limit, **kwargs)
    tags = list(tags)
    if len(tags) == 0:
        raise Exception("Could not find the specific tags.")
    return tags

def find_next_sibling(html: str|BeautifulSoup|Tag|lxml.html.HtmlElement, tag: str=None, attrs: dict=None, text: str=None, 
                      parse_method: str="lxml", encoding: str='unicode', method: str='html', **kwargs) -> Tag:
    """查找当前元素的下一个兄弟元素(最近的那一个)

    Args:
        html (str | BeautifulSoup | Tag | lxml.html.HtmlElement): html文本、BeautifulSoup对象、Tag对象、lxml.html.HtmlElement对象
        tag (str, optional): 标签名. Defaults to None.
        attrs (dict, optional): 标签属性, eg:{"class": "tag-class"}. Defaults to None.
        text (str | None, optional): 标签的文本, 会根据标签中的文本搜索对应的标签. Defaults to None.
        parse_method (str, optional): 解析方法, 分别有 html.parser|lxml|xml|html5lib. Defaults to "lxml".
        encoding (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的编码方式, 分别有 unicode|utf8|utf8-sig. Defaults to 'unicode'.
        method (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的解析方法, 分别有 html|xml. Defaults to 'html'.
        
    Raises:
        Exception: 无法找到对应标签

    Returns:
        Tag: 标签Tag对象
    """
    if isinstance(html, str):
        soup = BeautifulSoup(html, parse_method)
        tag = soup.find_next_sibling(tag, attrs, text, **kwargs)
    elif isinstance(html, BeautifulSoup) or isinstance(html, Tag):
        tag = html.find_next_sibling(tag, attrs, text, **kwargs)
    elif isinstance(html, lxml.html.HtmlElement):
        to_str = lxml.html.tostring(html, encoding=encoding, method=method)
        soup = BeautifulSoup(to_str, parse_method)
        tag = soup.find_next_sibling(tag, attrs, text, **kwargs)
    if tag is None:
        raise Exception("Could not find the specific tag.")
    return tag

def find_next_siblings(html: str|BeautifulSoup|Tag|lxml.html.HtmlElement, tag: str=None, attrs: dict=None, text: str=None, limit: int=None, 
                       parse_method: str="lxml", encoding: str='unicode', method: str='html', **kwargs) -> list[Tag]:
    """查找当前元素的所有后续兄弟元素

    Args:
        html (str | BeautifulSoup | Tag | lxml.html.HtmlElement): html文本、BeautifulSoup对象、Tag对象、lxml.html.HtmlElement对象
        tag (str, optional): 标签名. Defaults to None.
        attrs (dict, optional): 标签属性, eg:{"class": "tag-class"}. Defaults to None.
        text (str | None, optional): 标签的文本, 会根据标签中的文本搜索对应的标签. Defaults to None.
        limit (int, optional): 限制返回标签的数量, 假设为1, 则返回一个标签, 以此类推. Defaults to None.
        parse_method (str, optional): 解析方法, 分别有 html.parser|lxml|xml|html5lib. Defaults to "lxml".
        encoding (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的编码方式, 分别有 unicode|utf8|utf8-sig. Defaults to 'unicode'.
        method (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的解析方法, 分别有 html|xml. Defaults to 'html'.

    Raises:
        Exception: 无法找到对应标签

    Returns:
        list[Tag]: 标签Tag对象列表
    """
    if isinstance(html, str):
        soup = BeautifulSoup(html, parse_method)
        tags = soup.find_next_siblings(tag, attrs, text, limit, **kwargs)
    elif isinstance(html, BeautifulSoup) or isinstance(html, Tag):
        tags = html.find_next_siblings(tag, attrs, text, limit, **kwargs)
    elif isinstance(html, lxml.html.HtmlElement):
        to_str = lxml.html.tostring(html, encoding=encoding, method=method)
        soup = BeautifulSoup(to_str, parse_method)
        tags = soup.find_next_siblings(tag, attrs, text, limit, **kwargs)
    tags = list(tags)
    if len(tags) == 0:
        raise Exception("Could not find the specific tags.")
    return tags

def find_previous_sibling(html: str|BeautifulSoup|Tag|lxml.html.HtmlElement, tag: str=None, attrs: dict=None, text: str=None, 
                          parse_method: str="lxml", encoding: str='unicode', method: str='html', **kwargs) -> Tag:
    """查找当前元素的上一个兄弟元素

    Args:
        html (str | BeautifulSoup | Tag | lxml.html.HtmlElement): html文本、BeautifulSoup对象、Tag对象、lxml.html.HtmlElement对象
        tag (str, optional): 标签名. Defaults to None.
        attrs (dict, optional): 标签属性, eg:{"class": "tag-class"}. Defaults to None.
        text (str | None, optional): 标签的文本, 会根据标签中的文本搜索对应的标签. Defaults to None.
        parse_method (str, optional): 解析方法, 分别有 html.parser|lxml|xml|html5lib. Defaults to "lxml".
        encoding (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的编码方式, 分别有 unicode|utf8|utf8-sig. Defaults to 'unicode'.
        method (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的解析方法, 分别有 html|xml. Defaults to 'html'.

    Raises:
        Exception: 无法找到对应标签

    Returns:
        Tag: 标签Tag对象
    """
    if isinstance(html, str):
        soup = BeautifulSoup(html, parse_method)
        tag = soup.find_previous_sibling(tag, attrs, text, **kwargs)
    elif isinstance(html, BeautifulSoup) or isinstance(html, Tag):
        tag = html.find_previous_sibling(tag, attrs, text, **kwargs)
    elif isinstance(html, lxml.html.HtmlElement):
        to_str = lxml.html.tostring(html, encoding=encoding, method=method)
        soup = BeautifulSoup(to_str, parse_method)
        tag = soup.find_previous_sibling(tag, attrs, text, **kwargs)
    if tag is None:
        raise Exception("Could not find the specific tag.")
    return tag

def find_previous_siblings(html: str|BeautifulSoup|Tag|lxml.html.HtmlElement, tag: str=None, attrs: dict=None, text: str=None, limit: int=None, 
                           parse_method: str="lxml", encoding: str='unicode', method: str='html', **kwargs) -> list[Tag]:
    """查找当前元素的所有前面的兄弟元素

    Args:
        html (str | BeautifulSoup | Tag | lxml.html.HtmlElement): html文本、BeautifulSoup对象、Tag对象、lxml.html.HtmlElement对象
        tag (str, optional): 标签名. Defaults to None.
        attrs (dict, optional): 标签属性, eg:{"class": "tag-class"}. Defaults to None.
        text (str | None, optional): 标签的文本, 会根据标签中的文本搜索对应的标签. Defaults to None.
        limit (int, optional): 限制返回标签的数量, 假设为1, 则返回一个标签, 以此类推. Defaults to None.
        parse_method (str, optional): 解析方法, 分别有 html.parser|lxml|xml|html5lib. Defaults to "lxml".
        encoding (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的编码方式, 分别有 unicode|utf8|utf8-sig. Defaults to 'unicode'.
        method (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的解析方法, 分别有 html|xml. Defaults to 'html'.

    Raises:
        Exception: 无法找到对应标签

    Returns:
        list[Tag]: 标签Tag对象列表
    """
    if isinstance(html, str):
        soup = BeautifulSoup(html, parse_method)
        tags = soup.find_previous_siblings(tag, attrs, text, limit, **kwargs)
    elif isinstance(html, BeautifulSoup) or isinstance(html, Tag):
        tags = html.find_previous_siblings(tag, attrs, text, limit, **kwargs)
    elif isinstance(html, lxml.html.HtmlElement):
        to_str = lxml.html.tostring(html, encoding=encoding, method=method)
        soup = BeautifulSoup(to_str, parse_method)
        tags = soup.find_previous_siblings(tag, attrs, text, limit, **kwargs)
    tags = list(tags)
    if len(tags) == 0:
        raise Exception("Could not find the specific tags.")
    return tags

def find_next(html: str|BeautifulSoup|Tag|lxml.html.HtmlElement, tag: str=None, attrs: dict=None, text: str=None, 
              parse_method: str="lxml", encoding: str='unicode', method: str='html', **kwargs) -> Tag:
    """查找当前元素的下一个元素

    Args:
        html (str | BeautifulSoup | Tag | lxml.html.HtmlElement): html文本、BeautifulSoup对象、Tag对象、lxml.html.HtmlElement对象
        tag (str, optional): 标签名. Defaults to None.
        attrs (dict, optional): 标签属性, eg:{"class": "tag-class"}. Defaults to None.
        text (str | None, optional): 标签的文本, 会根据标签中的文本搜索对应的标签. Defaults to None.
        parse_method (str, optional): 解析方法, 分别有 html.parser|lxml|xml|html5lib. Defaults to "lxml".
        encoding (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的编码方式, 分别有 unicode|utf8|utf8-sig. Defaults to 'unicode'.
        method (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的解析方法, 分别有 html|xml. Defaults to 'html'.

    Raises:
        Exception: 无法找到对应标签

    Returns:
        Tag: 标签Tag对象
    """
    if isinstance(html, str):
        soup = BeautifulSoup(html, parse_method)
        tag = soup.find_next(tag, attrs, text, **kwargs)
    elif isinstance(html, BeautifulSoup) or isinstance(html, Tag):
        tag = html.find_next(tag, attrs, text, **kwargs)
    elif isinstance(html, lxml.html.HtmlElement):
        to_str = lxml.html.tostring(html, encoding=encoding, method=method)
        soup = BeautifulSoup(to_str, parse_method)
        tag = soup.find_next(tag, attrs, text, **kwargs)
    if tag is None:
        raise Exception("Could not find the specific tag.")
    return tag

def find_all_next(html: str|BeautifulSoup|Tag|lxml.html.HtmlElement, tag: str=None, attrs: dict=None, text: str=None, limit: int=None, 
                  parse_method: str="lxml", encoding: str='unicode', method: str='html', **kwargs) -> list[Tag]:
    """查找当前元素后面的所有元素

    Args:
        html (str | BeautifulSoup | Tag | lxml.html.HtmlElement): html文本、BeautifulSoup对象、Tag对象、lxml.html.HtmlElement对象
        tag (str, optional): 标签名. Defaults to None.
        attrs (dict, optional): 标签属性, eg:{"class": "tag-class"}. Defaults to None.
        text (str | None, optional): 标签的文本, 会根据标签中的文本搜索对应的标签. Defaults to None.
        limit (int, optional): 限制返回标签的数量, 假设为1, 则返回一个标签, 以此类推. Defaults to None.
        parse_method (str, optional): 解析方法, 分别有 html.parser|lxml|xml|html5lib. Defaults to "lxml".
        encoding (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的编码方式, 分别有 unicode|utf8|utf8-sig. Defaults to 'unicode'.
        method (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的解析方法, 分别有 html|xml. Defaults to 'html'.

    Raises:
        Exception: 无法找到对应标签

    Returns:
        list[Tag]: 标签Tag对象列表
    """
    if isinstance(html, str):
        soup = BeautifulSoup(html, parse_method)
        tags = soup.find_all_next(tag, attrs, text, limit, **kwargs)
    elif isinstance(html, BeautifulSoup) or isinstance(html, Tag):
        tags = html.find_all_next(tag, attrs, text, limit, **kwargs)
    elif isinstance(html, lxml.html.HtmlElement):
        to_str = lxml.html.tostring(html, encoding=encoding, method=method)
        soup = BeautifulSoup(to_str, parse_method)
        tags = soup.find_all_next(tag, attrs, text, limit, **kwargs)
    tags = list(tags)
    if len(tags) == 0:
        raise Exception("Could not find the specific tags.")
    return tags

def find_previous(html: str|BeautifulSoup|Tag|lxml.html.HtmlElement, tag: str=None, attrs: dict=None, text: str=None, 
                  parse_method: str="lxml", encoding: str='unicode', method: str='html', **kwargs) -> Tag:
    """查找当前元素的上一个元素

    Args:
        html (str | BeautifulSoup | Tag | lxml.html.HtmlElement): html文本、BeautifulSoup对象、Tag对象、lxml.html.HtmlElement对象
        tag (str, optional): 标签名. Defaults to None.
        attrs (dict, optional): 标签属性, eg:{"class": "tag-class"}. Defaults to None.
        text (str | None, optional): 标签的文本, 会根据标签中的文本搜索对应的标签. Defaults to None.
        parse_method (str, optional): 解析方法, 分别有 html.parser|lxml|xml|html5lib. Defaults to "lxml".
        encoding (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的编码方式, 分别有 unicode|utf8|utf8-sig. Defaults to 'unicode'.
        method (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的解析方法, 分别有 html|xml. Defaults to 'html'.

    Raises:
        Exception: 无法找到对应标签

    Returns:
        Tag: 标签Tag对象
    """
    if isinstance(html, str):
        soup = BeautifulSoup(html, parse_method)
        tag = soup.find_previous(tag, attrs, text, **kwargs)
    elif isinstance(html, BeautifulSoup) or isinstance(html, Tag):
        tag = html.find_previous(tag, attrs, text, **kwargs)
    elif isinstance(html, lxml.html.HtmlElement):
        to_str = lxml.html.tostring(html, encoding=encoding, method=method)
        soup = BeautifulSoup(to_str, parse_method)
        tag = soup.find_previous(tag, attrs, text, **kwargs)
    if tag is None:
        raise Exception("Could not find the specific tag.")
    return tag

def find_all_previous(html: str|BeautifulSoup|Tag|lxml.html.HtmlElement, tag: str=None, attrs: dict=None, text: str=None, limit: int=None, 
                      parse_method: str="lxml", encoding: str='unicode', method: str='html', **kwargs) -> list[Tag]:
    """查找当前元素前面的所有元素

    Args:
        html (str | BeautifulSoup | Tag | lxml.html.HtmlElement): html文本、BeautifulSoup对象、Tag对象、lxml.html.HtmlElement对象
        tag (str, optional): 标签名. Defaults to None.
        attrs (dict, optional): 标签属性, eg:{"class": "tag-class"}. Defaults to None.
        text (str | None, optional): 标签的文本, 会根据标签中的文本搜索对应的标签. Defaults to None.
        limit (int, optional): 限制返回标签的数量, 假设为1, 则返回一个标签, 以此类推. Defaults to None.
        parse_method (str, optional): 解析方法, 分别有 html.parser|lxml|xml|html5lib. Defaults to "lxml".
        encoding (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的编码方式, 分别有 unicode|utf8|utf8-sig. Defaults to 'unicode'.
        method (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的解析方法, 分别有 html|xml. Defaults to 'html'.

    Raises:
        Exception: 无法找到对应标签

    Returns:
        list[Tag]: 标签Tag对象列表
    """
    if isinstance(html, str):
        soup = BeautifulSoup(html, parse_method)
        tags = soup.find_all_previous(tag, attrs, text, limit, **kwargs)
    elif isinstance(html, BeautifulSoup) or isinstance(html, Tag):
        tags = html.find_all_previous(tag, attrs, text, limit, **kwargs)
    elif isinstance(html, lxml.html.HtmlElement):
        to_str = lxml.html.tostring(html, encoding=encoding, method=method)
        soup = BeautifulSoup(to_str, parse_method)
        tags = soup.find_all_previous(tag, attrs, text, limit, **kwargs)
    tags = list(tags)
    if len(tags) == 0:
        raise Exception("Could not find the specific tags.")
    return tags

def to_string(element: Tag|lxml.html.HtmlElement, encoding: str="unicode", method: str="html") -> str:
    """将BeautifulSoup或lxml.html.HtmlElement对象转换为字符串形式

    Args:
        element (Tag | lxml.html.HtmlElement): BeautifulSoup或lxml.html.HtmlElement对象
        encoding (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的编码方式, 分别有 unicode|utf8|utf8-sig. Defaults to 'unicode'.
        method (str, optional): 针对lxml.html.HtmlElement对象转换成字符串格式的解析方法, 分别有 html|xml. Defaults to 'html'.

    Returns:
        str: 字符串形式的内容
    """
    if isinstance(element, Tag):
        return str(element)
    elif isinstance(element, lxml.html.HtmlElement):
        return lxml.html.tostring(element, encoding=encoding, method=method)

def get_text(tag_or_element: Tag|lxml.html.HtmlElement) -> str:
    """获取标签文本

    Args:
        tag_or_element (Tag | lxml.html.HtmlElement): Tag对象或lxml.html.HtmlElement对象

    Returns:
        str: 标签文本
    """
    return tag_or_element.text

def get_attr(tag_or_element: Tag|lxml.html.HtmlElement, attr_name: str) -> str:
    """获取标签属性值

    Args:
        tag_or_element (Tag | lxml.html.HtmlElement): Tag对象或lxml.html.HtmlElement对象
        attr_name (str): 属性名, eg: "class"、"href"、"id"等

    Returns:
        str: 属性值, 如果没有该属性, 则返回空字符串""
    """
    attr_result = tag_or_element.get(attr_name)
    return attr_result if attr_result is not None else ""