import requests, os
from pathlib import Path
from DrissionPage.common import By # 用于给其他模块导入By
from DrissionPage import Chromium, ChromiumOptions, SessionOptions
from ddddocr import DdddOcr


class ChromeOptionsSetter:
    """用于设置chrome启动参数的类"""
    _chrome_options = None
    
    def __init__(self, read_file: bool=True, ini_path: str|Path=None):
        """初始化chrome启动参数

        Args:
            read_file (bool, optional): 是否从默认ini文件中读取配置信息. Defaults to True.
            ini_path (str | Path, optional): ini文件路径, 为None则读取默认ini文件. Defaults to None.
        """
        self._chrome_options = ChromiumOptions(read_file, ini_path)
    
    def get_options(self) -> ChromiumOptions:
        """获取chrome启动参数"""
        return self._chrome_options
    
    def add_argument(self, arg: str, value: str|bool=None):
        """设置启动参数

        Args:
            arg (str): 参数名
            value (str | bool, optional): 参数值, 没有值的参数传入None, 如传入False, 删除该项. Defaults to None.
        """
        self._chrome_options.set_argument(arg, value)
    
    def set_user_agent(self, user_agent: bool|str):
        """设置用户代理字符串, 让chrome认为是在实际的浏览器上运行。

        Args:
            user_agent (bool | str): 用户代理字符串
        """
        self._chrome_options.set_user(user_agent)
    
    def set_mute(self):
        """静音"""
        self._chrome_options.mute()
    
    def set_incognito(self):
        """无痕模式, 不会保留浏览记录"""
        self._chrome_options.incognito()
    
    def set_headless(self):
        """无头模式, 浏览器不提供可视化界面"""
        self._chrome_options.headless()
    
    def set_start_maximized(self):
        """最大化运行(全屏窗口)"""
        self._chrome_options.set_argument('--start-maximized')
        
    def set_window_size(self, width: int, height: int):
        """设置浏览器分辨率

        Args:
            width (int): 长
            height (int): 宽
        """
        self._chrome_options.set_argument(f'--window-size={width}x{height}')
    
    def set_ignore_certificate_errors(self):
        """忽视证书认证的不安全连接的错误"""
        self._chrome_options.ignore_certificate_errors()
        
    def set_ignore_ssl_errors(self):
        """忽略SSL证书错误"""
        self._chrome_options.set_argument("--ignore-ssl-errors")
        
    def set_disable_infobars(self):
        """禁用浏览器正在被自动化程序控制的提示"""
        self._chrome_options.set_argument('--disable-infobars')
        
    def set_no_sandbox(self):
        """禁用沙盒模式(通常用于Linux环境下的无头模式)"""
        self._chrome_options.set_argument('--no-sandbox')
        
    def set_disable_gpu(self):
        """禁用GPU加速, 用于解决特定的渲染问题"""
        self._chrome_options.set_argument('--disable-gpu')
        
    def set_disable_extensions(self):
        """禁用所有扩展程序"""
        self._chrome_options.set_argument('--disable-extensions')
        
    def set_hide_scrollbars(self):
        """隐藏页面滚动条, 用于解决一些特殊页面"""
        self._chrome_options.set_argument('--hide-scrollbars')
        
    def set_disable_images(self):
        """在加载页面时不加载图片"""
        self._chrome_options.no_imgs()
        # self._chrome_options.set_argument('--blink-settings=imagesEnabled=false')
        
    def set_disable_javascript(self):
        """在加载页面时禁用javascript"""
        self._chrome_options.no_js()

class DrissionPageToolKit:
    """DrissionPage工具类, 用于封装DrissionPage。DrissionPage官方文档请浏览: https://www.drissionpage.cn/
    \n使用该类, 请运行如下命令安装所需库存:
    \npip install DrissionPage
    \npip install ddddocr
    \npip install requests
    \n使用By时, 请使用from package.DrissionPageToolKit import By
    """
    broswer = None
    tab = None
    
    def __init__(self, addr_or_opts: str|int|ChromiumOptions|ChromeOptionsSetter=None, session_options: SessionOptions=None):
        """初始化DrissionPageToolKit类

        Args:
            addr_or_opts (str | int | ChromiumOptions, optional): 浏览器地址:端口、ChromiumOptions对象或端口数字(int). Defaults to None.
            session_options (SessionOptions, optional): 使用双模Tab时使用的默认Session配置, 为None使用ini文件配置, 为False不从ini读取. Defaults to None.
        """
        if isinstance(addr_or_opts, ChromeOptionsSetter):
            addr_or_opts = addr_or_opts.get_options()
        self.broswer = Chromium(addr_or_opts, session_options)
        self.tab = self.broswer.latest_tab
        
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.tab = None
        if self.broswer:
            self.broswer.quit()
            self.broswer = None

    def close(self, timeout: float=5, force: bool=False, del_data: bool=False):
        """关闭浏览器

        Args:
            timeout (float, optional): 等待浏览器关闭超时时间（秒）. Defaults to 5.
            force (bool, optional): 是否立刻强制终止进程. Defaults to False.
            del_data (bool, optional): 是否删除用户文件夹. Defaults to False.
        """
        self.tab = None
        self.broswer.quit(timeout, force, del_data)
        self.broswer = None
    
    def set_current_tab(self, tab=None):
        """设置当前标签页

        Args:
            tab (optional): 标签页对象, 若为空则返回最新的标签页. Defaults to None.
        """
        if tab:
            self.tab = tab
        else:
            self.tab = self.broswer.latest_tab
    
    def get_tab(self, id_or_num: str|int=None, title: str=None, url: str=None, 
                tab_type: str|list|tuple="page", as_id: bool=False):
        """获取标签页

        Args:
            id_or_num (str | int, optional): 要获取的标签页id或序号, 序号从1开始, 可传入负数获取倒数第几个, 不是视觉排列顺序, 而是激活顺序。不为None时, 后面几个参数无效. Defaults to None.
            title (str, optional): 要匹配title的文本, 模糊匹配, 为None则匹配所有. Defaults to None.
            url (str, optional): 要匹配url的文本, 模糊匹配, 为None则匹配所有. Defaults to None.
            tab_type (str | list | tuple, optional): tab类型, 可用列表输入多个, 如page,iframe等, 为None则匹配所有. Defaults to 'page'.
            as_id (bool, optional): 是否返回标签页id而不是标签页对象. Defaults to False.

        Returns:
            MixTab: 标签页对象
        """
        return self.broswer.get_tab(id_or_num, title, url, tab_type, as_id)

    def get_tabs(self, title: str=None, url: str=None, tab_type: str|list|tuple="page", as_id: bool=False) -> list:
        """获取标签页列表

        Args:
            title (str, optional): 要匹配title的文本, 模糊匹配, 为None则匹配所有. Defaults to None.
            url (str, optional): 要匹配url的文本, 模糊匹配, 为None则匹配所有. Defaults to None.
            tab_type (str | list | tuple, optional): tab类型, 可用列表输入多个, 如page,iframe等, 为None则匹配所有. Defaults to 'page'.
            as_id (bool, optional): 是否返回标签页id而不是标签页对象. Defaults to False.

        Returns:
            list: 标签页对象列表
        """
        self.broswer.get_tabs(title, url, tab_type, as_id)

    def new_tab(self, url: str=None, new_window: bool=False, background: bool=False, new_context: bool=False):
        """新建一个标签页

        Args:
            url (str, optional): 新标签页跳转到的网址, 为None时新建空标签页. Defaults to None.
            new_window (bool, optional): 是否在新窗口打开标签页, 隐身模式下无效. Defaults to False.
            background (bool, optional): 是否不激活新标签页, 隐身模式和访客模式及new_window为True时无效. Defaults to False.
            new_context (bool, optional): 是否创建独立环境, 隐身模式和访客模式下无效. Defaults to False.
            
        Returns:
            MixTab: 标签页对象
        """
        return self.broswer.new_tab(url, new_window, background, new_context)

    def close_tabs(self, tabs_or_ids: str|list|tuple, others: bool=False):
        """关闭标签页, 可传入多个

        Args:
            tabs_or_ids (str | list): 指定的标签页对象或id, 可用列表或元组传入多个
            others (bool, optional): 是否关闭指定标签页之外的. Defaults to False.
        """
        self.broswer.close_tabs(tabs_or_ids, others)
    
    def reflesh(self):
        """刷新页面"""
        self.tab.refresh()

    def back(self, steps: int=1):
        """返回到上页

        Args:
            steps (int, optional): 返回上几页. Defaults to 1.
        """
        self.tab.back(steps)
    
    def forward(self, steps: int=1):
        """前进到下页
        
        Args:
            steps (int, optional): 前进到下几页. Defaults to 1.
        """
        self.tab.forward(steps)
    
    def screenshot(self, output_path: str=None, name: str=None, as_bytes: str|bool=None, as_base64: str|bool=None, 
                   full_page: bool=False, left_top: tuple[int, int]=None, right_bottom: tuple[int, int]=None) -> bytes|str:
        """页面截图

        Args:
            output_path (str, optional): 保存图片的路径, 为None时保存在当前文件夹. Defaults to None.
            name (str, optional): 完整文件名, 后缀可选{'jpg', 'jpeg', 'png', 'webp'}, 为None时以用jpg格式. Defaults to None.
            as_bytes (str | True, optional): 是否以字节形式返回图片, 可选{'jpg', 'jpeg', 'png', 'webp'}, 为None时output_path参数无效, 为True时选用jpg格式. Defaults to None.
            as_base64 (str | True, optional): 是否以base64形式返回图片, 可选{'jpg', 'jpeg', 'png', 'webp'}, 为None时output_path参数无效, 为True时选用jpg格式. Defaults to None.
            full_page (bool, optional): 是否整页截图, 为True截取整个网页, 为False截取可视窗口. Defaults to False.
            left_top (tuple, optional): 截取范围左上角坐标. Defaults to None.
            right_bottom (tuple, optional): 截取范围右下角坐标. Defaults to None.
            
        Returns:
            bytes: as_bytes生效时返回图片字节
            str: as_bytes和as_base64都为None时返回图片完整路径
            str: as_base64生效时返回base64格式的字符串
        """
        return self.tab.get_screenshot(output_path, name, as_bytes, as_base64, full_page, left_top, right_bottom)
    
    def start_web(self, url: str, wait_type: str|bool=False, loc_or_ele: str|tuple=None, wait_timeout: float=60, any_one: bool=False):
        """打开一个网址

        Args:
            url (str): 新标签页跳转到的网址, 为None时新建空标签页
            wait_type (str | False, optional): 在开启网址后等待元素的逻辑, 可选{display(元素出现), load(元素加载在DOM树中)}, 为False则不等待. Defaults to False.
            loc_or_ele (str | tuple, optional): 元素对象或者定位. Defaults to None.
            wait_timeout (float, optional): 等待超时时间. Defaults to 60.
            any_one (bool, optional): 是否等待到一个就返回, wait_type为load则生效. Defaults to False.
        """
        self.tab.get(url)
        if wait_type == "display":
            self.tab.wait.ele_displayed(loc_or_ele, wait_timeout, True)
        elif wait_type == "load":
            self.tab.wait.eles_loaded(loc_or_ele, wait_timeout, any_one, True)

    def wait_until_element_hidden(self, loc_or_ele: str|tuple, timeout: float=60):
        """等待直至某元素从显示状态变成隐藏状态

        Args:
            loc_or_ele (str | tuple): 元素对象或者定位
            timeout (int, optional): 等待超时时间. Defaults to 60.
        """
        self.tab.wait.ele_hidden(loc_or_ele, timeout, True)

    def wait_until_element_deleted(self, loc_or_ele: str|tuple, timeout: float=60):
        """等待直至某元素从DOM树中删除

        Args:
            loc_or_ele (str | tuple): 元素对象或者定位
            timeout (int, optional): 等待超时时间. Defaults to 60.
        """
        self.tab.wait.ele_deleted(loc_or_ele, timeout, True)
    
    def find_element_until_appear(self, loc_or_ele: str|tuple, timeout: float=60):
        """获取页面可见的元素

        Args:
            loc_or_ele (str | tuple): 元素对象或者定位
            timeout (int, optional): 等待超时时间. Defaults to 60.

        Returns:
            ChromiumElement: 对应元素
        """
        return self.tab.wait.ele_displayed(loc_or_ele, timeout, True)
    
    def find_element(self, locator: str|tuple, index: int=1, timeout: float=60):
        """寻找元素, 会返回第一个符合条件的元素

        Args:
            locator (str | tuple): 元素的定位信息, 可以是元素对象, loc元组, 或查询字符串
            index (int, optional): 获取第几个, 从1开始, 可传入负数获取倒数第几个. Defaults to 1.
            timeout (float, optional): 查找元素超时时间(秒). Defaults to 60.

        Returns:
            ChromiumElement: 对应元素
        """
        return self.tab.ele(locator, index, timeout)

    def find_elements(self, locator: str|tuple, timeout: float=60) -> list:
        """获取一系列元素

        Args:
            locator (str | tuple): 元素的定位信息, 可以是元素对象, loc元组, 或查询字符串
            timeout (float, optional): 查找元素超时时间(秒). Defaults to 60.

        Returns:
            list: 对应的所有元素
        """
        return self.tab.eles(locator, timeout)

    def click(self, locator: str|tuple=None, index: int=1, timeout: float=60, element=None):
        """点击元素

        Args:
            locator (str | tuple): 元素的定位信息, 可以是元素对象, loc元组, 或查询字符串. Defaults to None.
            index (int, optional): 获取第几个, 从1开始, 可传入负数获取倒数第几个. Defaults to 1.
            timeout (float, optional): 查找元素超时时间(秒). Defaults to 60.
            element (ChromiumElement, optional): 元素对象, 输入后locator、index和timeout无效. Defaults to None.
        """
        self.tab.ele(locator, index, timeout).click() if element is None else element.click()
    
    def send_text(self, locator: str|tuple=None, text_values: str|list="", clear: bool=True, by_js: bool=False, index: int=1, timeout: float=60, element=None):
        """向元素输入文本或组合键, 也可用于输入文件路径到上传控件

        Args:
            locator (str | tuple): 元素的定位信息, 可以是元素对象, loc元组, 或查询字符串. Defaults to None.
            text_values (str | list, optional): 文本值或按键组合, 对文件上传控件时输入路径字符串或其组成的列表. Defaults to "".
            clear (bool, optional): 输入前是否清空文本框. Defaults to True.
            by_js (bool, optional): 是否用js方式输入, 为True时不能输入组合键. Defaults to False.
            index (int, optional): 获取第几个, 从1开始, 可传入负数获取倒数第几个. Defaults to 1.
            timeout (float, optional): 查找元素超时时间(秒). Defaults to 60.
            element (ChromiumElement, optional): 元素对象, 输入后locator、index和timeout无效. Defaults to None.
        """
        self.tab.ele(locator, index, timeout).input(text_values, clear, by_js) if element is None else element.input(text_values, clear, by_js)
    
    def get_text(self, locator: str|tuple=None, index: int=1, timeout: float=60, element=None) -> str:
        """获取元素文本

        Args:
            locator (str | tuple): 元素的定位信息, 可以是元素对象, loc元组, 或查询字符串. Defaults to None.
            index (int, optional): 获取第几个, 从1开始, 可传入负数获取倒数第几个. Defaults to 1.
            timeout (float, optional): 查找元素超时时间(秒). Defaults to 60.
            element (ChromiumElement, optional): 元素对象, 输入后其他参数无效. Defaults to None.

        Returns:
            str: 元素文本
        """
        return self.tab.ele(locator, index, timeout).text() if element is None else element.text()
    
    def get_texts(self, locator: str|tuple=None, index: int=1, timeout: float=60, element=None) -> list:
        """获取元素的所有文本

        Args:
            locator (str | tuple): 元素的定位信息, 可以是元素对象, loc元组, 或查询字符串. Defaults to None.
            index (int, optional): 获取第几个, 从1开始, 可传入负数获取倒数第几个. Defaults to 1.
            timeout (float, optional): 查找元素超时时间(秒). Defaults to 60.
            element (ChromiumElement, optional): 元素对象, 输入后其他参数无效. Defaults to None.

        Returns:
            list: 元素文本列表
        """
        return self.tab.ele(locator, index, timeout).texts() if element is None else element.texts()
    
    def select_combobox(self, locator: str|tuple=None, index: int=1, timeout: float=60, element=None, 
                        select_type: str="index", select_value: int|str|tuple|list=0):
        """选择<select>元素的选项

        Args:
            locator (str | tuple): 元素的定位信息, 可以是元素对象, loc元组, 或查询字符串. Defaults to None.
            index (int, optional): 获取第几个, 从1开始, 可传入负数获取倒数第几个. Defaults to 1.
            timeout (float, optional): 查找元素超时时间(秒). Defaults to 60.
            element (ChromiumElement, optional): 元素对象, 输入后locator、index无效. Defaults to None.
            select_type (str, optional): 选择策略, 选项有:{all, index, text, value}. Defaults to "index".
            select_value (int | str | tuple | list, optional): 选择定位值. Defaults to 0.
        """
        if element is None:
            element = self.tab.ele(locator, index, timeout)
        if select_type == "index":
            element.select.by_index(select_value, timeout)
        elif select_type == "all":
            element.select.all()
        elif select_type == "text":
            element.select.by_text(select_value, timeout)
        elif select_type == "value":
            element.select.by_value(select_value, timeout)
    
    def deselect_combobox(self, locator: str|tuple=None, index: int=1, timeout: float=60, element=None, 
                          deselect_type: str="all", deselect_value: int|str|tuple|list=0):
        """取消选择<select>元素的选项

        Args:
            locator (str | tuple): 元素的定位信息, 可以是元素对象, loc元组, 或查询字符串. Defaults to None.
            index (int, optional): 获取第几个, 从1开始, 可传入负数获取倒数第几个. Defaults to 1.
            timeout (float, optional): 查找元素超时时间(秒). Defaults to 60.
            element (ChromiumElement, optional): 元素对象, 输入后locator、index无效. Defaults to None.
            deselect_type (str, optional): 选择策略, 选项有:{all, index, text, value}. Defaults to "all".
            deselect_value (int | str | tuple | list, optional): 取消选择定位值. Defaults to 0.
        """
        if element is None:
            element = self.tab.ele(locator, index, timeout)
        if deselect_type == "all":
            element.select.clear()
        elif deselect_type == "index":
            element.select.cancel_by_index(deselect_value, timeout)
        elif deselect_type == "text":
            element.select.cancel_by_text(deselect_value, timeout)
        elif deselect_type == "value":
            element.select.cancel_by_value(deselect_value, timeout)
    
    def mouse_move_to_element(self, loc_or_ele: str|tuple, offset_x: float=0, offset_y: float=0, duration: float=0.5):
        """将鼠标移动到元素上, 也用于鼠标悬停触发元素的hover事件

        Args:
            loc_or_ele (str | tuple): 元素对象、绝对坐标或文本定位符, 坐标为tuple(int, int)形式
            offset_x (float, optional): 偏移量x. Defaults to 0.
            offset_y (float, optional): 偏移量y. Defaults to 0.
            duration (float, optional): 拖动用时, 传入0即瞬间到达. Defaults to 0.5.
            
        Returns:
            Actions: 动作链本身
        """
        return self.tab.actions.move_to(loc_or_ele, offset_x, offset_y, duration)
    
    def mouse_click(self, element: str=None, times: int=1):
        """点击鼠标左键

        Args:
            element (ChromiumElement | str, optional): 元素对象或文本定位符. Defaults to None.
            times (int, optional): 点击次数. Defaults to 1.

        Returns:
            Actions: 动作链本身
        """
        return self.tab.actions.click(element, times)
    
    def mouse_right_click(self, element: str=None, times: int=1):
        """点击鼠标右键

        Args:
            element (ChromiumElement | str, optional): 元素对象或文本定位符. Defaults to None.
            times (int, optional): 点击次数. Defaults to 1.

        Returns:
            Actions: 动作链本身
        """
        return self.tab.actions.r_click(element, times)
    
    def mouse_middle_click(self, element: str=None, times: int=1):
        """点击鼠标中键

        Args:
            element (ChromiumElement | str, optional): 元素对象或文本定位符. Defaults to None.
            times (int, optional): 点击次数. Defaults to 1.

        Returns:
            Actions: 动作链本身
        """
        return self.tab.actions.m_click(element, times)

    def mouse_hold(self, element: str=None):
        """按住鼠标左键不放

        Args:
            element (ChromiumElement | str, optional): 元素对象或文本定位符. Defaults to None.
            
        Returns:
            Actions: 动作链本身
        """
        return self.tab.actions.hold(element)

    def mouse_right_hold(self, element: str=None):
        """按住鼠标右键不放

        Args:
            element (ChromiumElement | str, optional): 元素对象或文本定位符. Defaults to None.
            
        Returns:
            Actions: 动作链本身
        """
        return self.tab.actions.r_hold(element)

    def mouse_middle_hold(self, element: str=None):
        """按住鼠标中键不放

        Args:
            element (ChromiumElement | str, optional): 元素对象或文本定位符. Defaults to None.
            
        Returns:
            Actions: 动作链本身
        """
        return self.tab.actions.r_hold(element)

    def mouse_release(self, element: str=None):
        """释放鼠标左键

        Args:
            element (ChromiumElement | str, optional): 元素对象或文本定位符. Defaults to None.
            
        Returns:
            Actions: 动作链本身
        """
        return self.tab.actions.release(element)

    def mouse_right_release(self, element: str=None):
        """释放鼠标右键

        Args:
            element (ChromiumElement | str, optional): 元素对象或文本定位符. Defaults to None.
            
        Returns:
            Actions: 动作链本身
        """
        return self.tab.actions.r_release(element)

    def mouse_middle_release(self, element: str=None):
        """释放鼠标中键

        Args:
            element (ChromiumElement | str, optional): 元素对象或文本定位符. Defaults to None.
            
        Returns:
            Actions: 动作链本身
        """
        return self.tab.actions.m_release(element)

    def save_element_image(self, locator: str|tuple=None, index: int=1, timeout: float=60, 
                           element=None, image_box_attr: str="src", target_image_path: str="./capture_image.png"):
        """保存元素图片

        Args:
            locator (str | tuple): 元素的定位信息, 可以是元素对象, loc元组, 或查询字符串. Defaults to None.
            index (int, optional): 获取第几个, 从1开始, 可传入负数获取倒数第几个. Defaults to 1.
            timeout (float, optional): 查找元素超时时间(秒). Defaults to 60.
            element (ChromiumElement, optional): 元素对象, 输入后locator、index和timeout无效. Defaults to None.
            image_box_attr (str, optional): 图片box中的url属性, 会通过该url下载图片. Defaults to "src".
            target_image_path (str, optional): 目标保存路径. Defaults to "./capture_image.png".
            timeout (int, optional): 等待超时时间. Defaults to 60.
        """
        if element is None:
            element = self.tab.ele(locator, index, timeout)
        image_url = element.attr(image_box_attr)
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(target_image_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
        else:
            raise Exception(f"response status code not 200, is: {response.status_code}, can not download images")
    
    def ocr_code(self, locator: str|tuple=None, index: int=1, timeout: float=60, element=None, 
                 code_box_attr: str="src", cache_image_path: str="./cache_code_image.png", auto_delete_image: bool=True) -> str:
        """使用ocr检测验证码

        Args:
            locator (str | tuple): 元素的定位信息, 可以是元素对象, loc元组, 或查询字符串. Defaults to None.
            index (int, optional): 获取第几个, 从1开始, 可传入负数获取倒数第几个. Defaults to 1.
            timeout (float, optional): 查找元素超时时间(秒). Defaults to 60.
            element (ChromiumElement, optional): 元素对象, 输入后locator、index和timeout无效. Defaults to None.
            code_box_attr (str, optional): 验证码box中的url属性, 会通过该url下载图片. Defaults to "src".
            cache_image_path (str, optional): 缓存图片路径. Defaults to "./cache_code_image.png".
            auto_delete_image (bool, optional): 自动删除缓存图片. Defaults to True.

        Returns:
            str: 验证码
        """
        if element is None:
            element = self.tab.ele(locator, index, timeout)
        image_url = element.attr(code_box_attr)
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(cache_image_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
        else:
            raise Exception(f"response status code not 200, is: {response.status_code}, can not download images")
        ocr = DdddOcr()
        with open(cache_image_path, 'rb') as f:
            img_bytes = f.read()
        res = ocr.classification(img_bytes)
        if auto_delete_image:
            os.remove(cache_image_path)
        return res
    
    def execute_script(self, script_context: str, as_expr: bool=False, timeout: float=60):
        """执行javascript脚本

        Args:
            script_context (str): js文本或js文件路径
            as_expr (bool, optional): 是否作为表达式运行. Defaults to False.
            timeout (float, optional): js超时时间(秒), 为None则使用页面timeouts.script设置. Defaults to 60.

        Returns:
            执行结果
        """
        return self.tab.run_js(script_context, as_expr=as_expr, timeout=timeout)
    
    def get_HTML(self) -> str:
        """获取整个页面的HTML文档

        Returns:
            str: HTML文档
        """
        return self.tab.html
    
    def get_element_HTML(self, locator: str|tuple=None, index: int=1, timeout: float=60, element=None, innerHTML: bool=False, outerHTML: bool=True) -> str:
        """获取元素的HTML文档

        Args:
            locator (str | tuple): 元素的定位信息, 可以是元素对象, loc元组, 或查询字符串. Defaults to None.
            index (int, optional): 获取第几个, 从1开始, 可传入负数获取倒数第几个. Defaults to 1.
            timeout (float, optional): 查找元素超时时间(秒). Defaults to 60.
            element (ChromiumElement, optional): 元素对象, 输入后locator、index和timeout无效. Defaults to None.
            innerHTML (bool, optional): 获取元素的内部HTML(不包括元素本身的标签). Defaults to False.
            outerHTML (bool, optional): 获取元素及其内部的完整HTML(包括元素本身的标签). Defaults to True.

        Returns:
            str: 元素的HTML文档
        """
        if outerHTML:
            html_content = element.html if element else self.tab.ele(locator, index, timeout).html
        elif innerHTML:
            html_content = element.inner_html if element else self.tab.ele(locator, index, timeout).inner_html
        return html_content
    
    def get_cookies(self, all_domains: bool=False, all_info: bool=False) -> list:
        """获取cookies

        Args:
            all_domains (bool, optional): 是否返回所有域的cookies. Defaults to False.
            all_info (bool, optional): 是否返回所有信息, False则只返回name、value、domain. Defaults to False.

        Returns:
            list: cookies信息
        """
        return self.tab.cookies(all_domains, all_info)
    
    def add_cookie(self, cookie: dict):
        """增加cookie

        Args:
            cookie (dict): cookie
        """
        self.tab.set.cookies(cookie)
        
    def delete_cookie(self, cookie_name: str, url: str=None, domain: str=None, path: str=None):
        """删除cookie

        Args:
            cookie_name (str): cookie的name字段
            url (str, optional): cookie的url字段, 可选, d模式时才有效. Defaults to None.
            domain (str, optional): cookie的domain字段, 可选, d模式时才有效. Defaults to None.
            path (str, optional): cookie的path字段, 可选, d模式时才有效. Defaults to None.
        """
        self.tab.set.cookies.remove(cookie_name, url, domain, path)
        
    def delete_all_cookies(self):
        """删除所有的cookie"""
        self.tab.set.cookies.clear()
