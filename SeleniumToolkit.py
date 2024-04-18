import requests, os
from selenium import webdriver
from ddddocr import DdddOcr
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.remote.webdriver import WebElement
from selenium.webdriver.support import expected_conditions as EC


class EdgeOptionsSetter:
    _edge_options = None
    
    def __init__(self):
        """初始化edge启动参数"""
        self._edge_options = webdriver.EdgeOptions()

    def get_options(self) -> webdriver.EdgeOptions:
        """获取edge启动参数"""
        return self._edge_options

    def set_user_agent(self, user_agent: bool|str):
        """设置用户代理字符串, 让edge认为是在实际的浏览器上运行。
        
        Args:
            user_agent (bool | str): 用户代理字符串
        """
        self._edge_options.add_argument(f'--user-agent="{user_agent}"')
    
    def set_incognito(self):
        """无痕模式, 不会保留浏览记录"""
        self._edge_options.add_argument('--incognito')
        
    def set_headless(self):
        """无头模式, 浏览器不提供可视化界面"""
        self._edge_options.add_argument('--headless')
        
    def set_start_maximized(self):
        """最大化运行(全屏窗口)"""
        self._edge_options.add_argument('--start-maximized')
        
    def set_window_size(self, width: int, height: int):
        """设置浏览器分辨率
        Args:
            width (int): 长
            height (int): 宽
        """
        self._edge_options.add_argument(f'--window-size={width}, {height}')
    
    def set_ignore_certificate_errors(self):
        """忽视证书认证的不安全连接的错误"""
        self._edge_options.add_argument("--ignore-certificate-errors")
        
    def set_ignore_ssl_errors(self):
        """忽略SSL证书错误"""
        self._edge_options.add_argument("--ignore-ssl-errors")
        
    def set_disable_infobars(self):
        """禁用浏览器正在被自动化程序控制的提示"""
        self._edge_options.add_argument('--disable-infobars')
        
    def set_no_sandbox(self):
        """禁用沙盒模式(通常用于Linux环境下的无头模式)"""
        self._edge_options.add_argument('--no-sandbox')
        
    def set_disable_gpu(self):
        """禁用GPU加速, 用于解决特定的渲染问题"""
        self._edge_options.add_argument('--disable-gpu')
        
    def set_disable_extensions(self):
        """禁用所有扩展程序"""
        self._edge_options.add_argument('--disable-extensions')
        
    def set_hide_scrollbars(self):
        """隐藏页面滚动条, 用于解决一些特殊页面"""
        self._edge_options.add_argument('--hide-scrollbars')
        
    def set_disable_images(self):
        """在加载页面时不加载图片"""
        self._edge_options.add_argument('--blink-settings=imagesEnabled=false')
        
    @classmethod
    def edge_options_setter(cls, user_agent: bool|str=False, incognito: bool=False, headless: bool=False, start_maximized: bool=False, window_size: bool|tuple = False, 
                            ignore_certificate_errors: bool=True, ignore_ssl_errors: bool=True, disable_infobars: bool=True, 
                            no_sandbox: bool=False, disable_gpu: bool=False, disable_extensions: bool=False, 
                            hide_scrollbars: bool=False, disable_images: bool=False) -> webdriver.EdgeOptions:
        """设置edge启动参数

        Args:
            user_agent (bool | str, optional): 设置用户代理字符串, 让edge认为是在实际的浏览器上运行。若为False则不使用代理. Defaults to False.
            incognito (bool, optional): 无痕模式, 不会保留浏览记录. Defaults to False.
            headless (bool, optional): 无头模式, 浏览器不提供可视化界面. Defaults to False.
            start_maximized (bool, optional): 最大化运行(全屏窗口). Defaults to False.
            window_size (bool | tuple, optional): 设置浏览器分辨率, 若不为False输入分别率(左长, 右宽), eg:(1920, 1080). Defaults to False.
            ignore_certificate_errors (bool, optional): 忽视证书认证的不安全连接的错误. Defaults to True.
            ignore_ssl_errors (bool, optional): 忽略SSL证书错误. Defaults to True.
            disable_infobars (bool, optional): 禁用浏览器正在被自动化程序控制的提示. Defaults to True.
            no_sandbox (bool, optional): 禁用沙盒模式(通常用于Linux环境下的无头模式). Defaults to False.
            disable_gpu (bool, optional): 禁用GPU加速, 用于解决特定的渲染问题. Defaults to False.
            disable_extensions (bool, optional): 禁用所有扩展程序. Defaults to False.
            hide_scrollbars (bool, optional): 隐藏页面滚动条, 用于解决一些特殊页面. Defaults to False.
            disable_images (bool, optional): 在加载页面时不加载图片. Defaults to False.

        Returns:
            webdriver.ChromeOptions: edge启动参数
        """
        options = webdriver.EdgeOptions()
        if user_agent:
            options.add_argument(f'--user-agent="{user_agent}"')
        if incognito:
            options.add_argument('--incognito')
        if headless:
            options.add_argument('--headless')
        if start_maximized:
            options.add_argument('--start-maximized')
        if window_size:
            options.add_argument(f'--window-size={window_size[0]}x{window_size[1]}')
        if ignore_certificate_errors:
            options.add_argument("--ignore-certificate-errors")
        if ignore_ssl_errors:
            options.add_argument("--ignore-ssl-errors")
        if disable_infobars:
            options.add_argument('--disable-infobars')
        if no_sandbox:
            options.add_argument('--no-sandbox')
        if disable_gpu:
            options.add_argument('--disable-gpu')
        if disable_extensions:
            options.add_argument('--disable-extensions')
        if hide_scrollbars:
            options.add_argument('--hide-scrollbars')
        if disable_images:
            options.add_argument('--blink-settings=imagesEnabled=false')
        return options
    
class ChromeOptionsSetter:
    """用于设置chrome启动参数的类"""
    _chrome_options = None
    
    def __init__(self):
        """初始化chrome启动参数"""
        self._chrome_options = webdriver.ChromeOptions()
    
    def get_options(self) -> webdriver.ChromeOptions:
        """获取chrome启动参数"""
        return self._chrome_options
    
    def set_user_agent(self, user_agent: bool|str):
        """设置用户代理字符串, 让chrome认为是在实际的浏览器上运行。

        Args:
            user_agent (bool | str): 用户代理字符串
        """
        self._chrome_options.add_argument(f'--user-agent="{user_agent}"')
    
    def set_incognito(self):
        """无痕模式, 不会保留浏览记录"""
        self._chrome_options.add_argument('--incognito')
    
    def set_headless(self):
        """无头模式, 浏览器不提供可视化界面"""
        self._chrome_options.add_argument('--headless')
    
    def set_start_maximized(self):
        """最大化运行(全屏窗口)"""
        self._chrome_options.add_argument('--start-maximized')
        
    def set_window_size(self, width: int, height: int):
        """设置浏览器分辨率

        Args:
            width (int): 长
            height (int): 宽
        """
        self._chrome_options.add_argument(f'--window-size={width}x{height}')
    
    def set_ignore_certificate_errors(self):
        """忽视证书认证的不安全连接的错误"""
        self._chrome_options.add_argument("--ignore-certificate-errors")
        
    def set_ignore_ssl_errors(self):
        """忽略SSL证书错误"""
        self._chrome_options.add_argument("--ignore-ssl-errors")
        
    def set_disable_infobars(self):
        """禁用浏览器正在被自动化程序控制的提示"""
        self._chrome_options.add_argument('--disable-infobars')
        
    def set_no_sandbox(self):
        """禁用沙盒模式(通常用于Linux环境下的无头模式)"""
        self._chrome_options.add_argument('--no-sandbox')
        
    def set_disable_gpu(self):
        """禁用GPU加速, 用于解决特定的渲染问题"""
        self._chrome_options.add_argument('--disable-gpu')
        
    def set_disable_extensions(self):
        """禁用所有扩展程序"""
        self._chrome_options.add_argument('--disable-extensions')
        
    def set_hide_scrollbars(self):
        """隐藏页面滚动条, 用于解决一些特殊页面"""
        self._chrome_options.add_argument('--hide-scrollbars')
        
    def set_disable_images(self):
        """在加载页面时不加载图片"""
        self._chrome_options.add_argument('--blink-settings=imagesEnabled=false')
    
    @classmethod
    def chrome_options_setter(cls, user_agent: bool|str=False, incognito: bool=False, headless: bool=False, start_maximized: bool=False, window_size: bool|tuple = False, 
                            ignore_certificate_errors: bool=True, ignore_ssl_errors: bool=True, disable_infobars: bool=True, 
                            no_sandbox: bool=False, disable_gpu: bool=False, disable_extensions: bool=False, 
                            hide_scrollbars: bool=False, disable_images: bool=False) -> webdriver.ChromeOptions:
        """设置chrome启动参数

        Args:
            user_agent (bool | str, optional): 设置用户代理字符串, 让chrome认为是在实际的浏览器上运行。若为False则不使用代理. Defaults to False.
            incognito (bool, optional): 无痕模式, 不会保留浏览记录. Defaults to False.
            headless (bool, optional): 无头模式, 浏览器不提供可视化界面. Defaults to False.
            start_maximized (bool, optional): 最大化运行(全屏窗口). Defaults to False.
            window_size (bool | tuple, optional): 设置浏览器分辨率, 若不为False输入分别率(左长, 右宽), eg:(1920, 1080). Defaults to False.
            ignore_certificate_errors (bool, optional): 忽视证书认证的不安全连接的错误. Defaults to True.
            ignore_ssl_errors (bool, optional): 忽略SSL证书错误. Defaults to True.
            disable_infobars (bool, optional): 禁用浏览器正在被自动化程序控制的提示. Defaults to True.
            no_sandbox (bool, optional): 禁用沙盒模式(通常用于Linux环境下的无头模式). Defaults to False.
            disable_gpu (bool, optional): 禁用GPU加速, 用于解决特定的渲染问题. Defaults to False.
            disable_extensions (bool, optional): 禁用所有扩展程序. Defaults to False.
            hide_scrollbars (bool, optional): 隐藏页面滚动条, 用于解决一些特殊页面. Defaults to False.
            disable_images (bool, optional): 在加载页面时不加载图片. Defaults to False.

        Returns:
            webdriver.ChromeOptions: chrome启动参数
        """
        options = webdriver.ChromeOptions()
        if user_agent:
            options.add_argument(f'--user-agent="{user_agent}"')
        if incognito:
            options.add_argument('--incognito')
        if headless:
            options.add_argument('--headless')
        if start_maximized:
            options.add_argument('--start-maximized')
        if window_size:
            options.add_argument(f'--window-size={window_size[0]}x{window_size[1]}')
        if ignore_certificate_errors:
            options.add_argument("--ignore-certificate-errors")
        if ignore_ssl_errors:
            options.add_argument("--ignore-ssl-errors")
        if disable_infobars:
            options.add_argument('--disable-infobars')
        if no_sandbox:
            options.add_argument('--no-sandbox')
        if disable_gpu:
            options.add_argument('--disable-gpu')
        if disable_extensions:
            options.add_argument('--disable-extensions')
        if hide_scrollbars:
            options.add_argument('--hide-scrollbars')
        if disable_images:
            options.add_argument('--blink-settings=imagesEnabled=false')
        return options

class SeleniumToolkit:
    """Selenium工具类, 用于封装selenium。使用该类, 请运行如下命令安装所需库存:
    \npip install selenium
    \npip install ddddocr
    \npip install requests
    \n请注意, selenium版本>=4.18
    """
    driver = None
    by = By
    keys = Keys
    
    def __init__(self, driver_type: str="chrome", remote_url: str=None, options=None):
        """初始化selenium driver

        Args:
            driver_type (str, optional): driver类型, 选项有:chrome|edge|firefox|remote. Defaults to "chrome".
            remote_url (str, optional): 远程selenium的url. Defaults to None.
            options (_type_, optional): selenium的启动参数. Defaults to None.

        Raises:
            Exception: 没有对应的driver type
        """
        if driver_type == "chrome":
            self.driver = webdriver.Chrome(options)
        elif driver_type == "edge":
            self.driver = webdriver.Edge(options)
        elif driver_type == "firefox":
            self.driver = webdriver.Firefox(options)
        elif driver_type == "remote":
            self.driver = webdriver.Remote(remote_url, options=options)
        else:
            raise Exception(f"No type found for {driver_type}")

    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.driver:
            self.driver.quit()
            self.driver = None
    
    def start_web(self, url: str, wait_element_locator: tuple=None, wait_timeout: int=60):
        """开启web页面

        Args:
            url (str): web的url
            wait_element_locator (tuple, optional): 页面元素定位器, 用于等待某元素加载完毕. Defaults to None.
            wait_timeout (int, optional): 等待超时时间. Defaults to 60.
        
        Example:
            >>> driver = SeleniumToolkit()
            >>> driver.start_web("web-site-url")
            >>> driver.start_web("web-site-url", (driver.by.ID, "ID"))
        """
        self.driver.get(url)
        if wait_element_locator:
            WebDriverWait(self.driver, wait_timeout).until(EC.presence_of_element_located(wait_element_locator))

    def close(self):
        """关闭引擎"""
        self.driver.quit()
        self.driver = None
    
    def max_window(self):
        """最大化运行(全屏窗口)"""
        self.driver.maximize_window()
    
    def set_window_size(self, width: int, height: int):
        """设置浏览器分辨率

        Args:
            width (int): 长
            height (int): 宽
        """
        self.driver.set_window_size(width, height)
    
    def screenshot(self, output_file_path: str):
        """对屏幕进行截图

        Args:
            output_file_path (str): 截图输出路径, 推荐格式为.png
            
        Example:
            >>> driver = SeleniumToolkit()
            >>> driver.start_web("web-site-url")
            >>> driver.screenshot("./current_page.png") # 短截图
            >>> driver.close()
            >>> 
            >>> driver = SeleniumToolkit(SeleniumToolkit.chrome_options_setter(headless=True))
            >>> driver.start_web("web-site-url")
            >>> width = driver.execute_script("return document.documentElement.scrollWidth")
            >>> height = driver.execute_script("return document.documentElement.scrollHeight")
            >>> driver.set_window_size(width, height)
            >>> driver.screenshot("./all_page.png") # 对整个页面进行长截图
            >>> driver.close()
        """
        self.driver.save_screenshot(output_file_path)
    
    def reflesh(self):
        """刷新页面"""
        self.driver.refresh()

    def back(self):
        """返回到上一页"""
        self.driver.back()
    
    def forward(self):
        """前进到下一页"""
        self.driver.forward()
    
    def wait_until_element_disappear(self, by: str, value: str, timeout: int=60):
        """等待直至某元素不存在于DOM树或消失

        Args:
            by (str): 元素获取策略
            value (str): 元素定位值
            timeout (int, optional): 等待超时时间. Defaults to 60.
        """
        WebDriverWait(self.driver, timeout).until(EC.invisibility_of_element_located((by, value)))
    
    def find_element_until_appear(self, by: str, value: str, timeout: int=60) -> WebElement:
        """获取页面可见的元素

        Args:
            by (str): 元素获取策略
            value (str): 元素定位值
            timeout (int, optional): 等待超时时间. Defaults to 60.

        Returns:
            WebElement: 对应元素
        """
        return WebDriverWait(self.driver, timeout).until(EC.visibility_of_element_located((by, value)))
    
    def find_element(self, by: str, value: str, element: WebElement=None, timeout: int=60) -> WebElement:
        """获取元素, 该方法会判断元素是否被加载到了DOM树里, 并不代表该元素一定可见

        Args:
            by (str): 元素获取策略
            value (str): 元素定位值
            element (WebElement, optional): 元素,不为None则获取该元素的子元素 . Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.

        Returns:
            WebElement: 对应元素
        """
        if element is None:
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
        else:
            return element.find_element(by, value)

    def find_elements(self, by: str, value: str, element: WebElement=None, timeout: int=60) -> list[WebElement]:
        """获取一系列元素

        Args:
            by (str): 元素获取策略
            value (str): 元素定位值
            element (WebElement, optional): 元素,不为None则获取该元素的子元素 . Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.

        Returns:
            list[WebElement]: 对应的所有元素
        """
        if element is None:
            return WebDriverWait(self.driver, timeout).until(EC.presence_of_all_elements_located((by, value)))
        else:
            return element.find_elements(by, value)

    def click(self, by: str=None, value: str=None, element: WebElement=None, timeout: int=60):
        """点击元素

        Args:
            by (str, optional): 元素获取策略. Defaults to None.
            value (str, optional): 元素定位值. Defaults to None.
            element (WebElement, optional): 元素, 输入后by和value无效. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            
        Example:
            >>> driver = SeleniumToolkit()
            >>> driver.start_web("web-site-url")
            >>> driver.click(driver.by.XPATH, "XPATH")
            >>> ele = driver.find_element(driver.by.XPATH, "XPATH")
            >>> driver.click(element=ele, timeout=100)
            >>> driver.close()
        """
        element.click() if element else WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value))).click()
    
    def select_combobox(self, select_type: str="index", by: str=None, value: str=None, element: WebElement=None, select_value: int | str=0, timeout: int=60):
        """选择<select></select>标签的选项

        Args:
            select_type (str, optional): 选择策略, 选项有:index|value_attr|value. Defaults to "index".
            by (str, optional): 元素获取策略. Defaults to None.
            value (str, optional): 元素定位值. Defaults to None.
            element (WebElement, optional): 元素, 输入后by和value无效. Defaults to None.
            select_value (int | str, optional): 选择值, 若为index则从0开始. Defaults to 0.
            timeout (int, optional): 等待超时时间. Defaults to 60.
        """
        if element == None:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
        select = Select(element)
        if select_type == "index":
            select.select_by_index(select_value)
        elif select_type == "value_attr":
            select.select_by_value(select_value)
        elif select_type == "value":
            select.select_by_visible_text(select_value)
    
    def deselect_combobox(self, deselect_type: str="all", by: str=None, value: str=None, element: WebElement=None, deselect_value: int | str=0, timeout: int=60):
        """取消选择<select></select>标签的选项

        Args:
            deselect_type (str, optional): 取消选择策略, 选项有:all|index|value_attr|value. Defaults to "all".
            by (str, optional): 元素获取策略. Defaults to None.
            value (str, optional): 元素定位值. Defaults to None.
            element (WebElement, optional): 元素, 输入后by和value无效. Defaults to None.
            deselect_value (int | str, optional): 选择值, 若为index则从0开始. Defaults to 0.
            timeout (int, optional): 等待超时时间. Defaults to 60.
        """
        if element == None:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
        select = Select(element)
        if deselect_type == "all":
            select.deselect_all()
        elif deselect_type == "index":
            select.deselect_by_index(deselect_value)
        elif deselect_type == "value_attr":
            select.deselect_by_value(deselect_value)
        elif deselect_type == "value":
            select.deselect_by_visible_text(deselect_value)
    
    def mouse_move_to_element(self, element: WebElement):
        """将鼠标移动到元素上, 也用于鼠标悬停触发元素的hover事件

        Args:
            element (WebElement): 元素
        """
        ActionChains(self.driver).move_to_element(element).perform()
    
    def mouse_click(self, element: WebElement=None):
        """鼠标点击

        Args:
            element (WebElement, optional): 点击的元素, 若为None则点击鼠标当前停留位置. Defaults to None.
        """
        ActionChains(self.driver).click(element).perform()
    
    def mouse_double_click(self, element: WebElement=None):
        """鼠标双击

        Args:
            element (WebElement, optional): 双击的元素, 若为None则双击鼠标当前停留位置. Defaults to None.
        """
        ActionChains(self.driver).double_click(element).perform()

    def mouse_right_click(self, element: WebElement=None):
        """鼠标右击

        Args:
            element (WebElement, optional): 右击的元素, 若为None则右击鼠标当前停留位置. Defaults to None.
        """
        ActionChains(self.driver).move_to_element(element).context_click(element).perform()

    def mouse_click_and_hold(self, element: WebElement=None):
        """鼠标点击并保持一段时间

        Args:
            element (WebElement, optional): 点击的元素, 若为None则点击鼠标当前停留位置. Defaults to None.
        """
        ActionChains(self.driver).click_and_hold(element).perform()

    def mouse_drag_and_drop(self, from_by: str=None, from_value: str=None, from_element: WebElement=None, 
                            to_by: str=None, to_value: str=None, to_element: WebElement=None, from_timeout: int=60, to_timeout: int=60):
        """鼠标拖动元素到另外一个元素中

        Args:
            from_by (str, optional): 被拖拽元素获取策略. Defaults to None.
            from_value (str, optional): 被拖拽元素定位值. Defaults to None.
            from_element (WebElement, optional): 被拖拽元素, 输入后from_by和from_value无效. Defaults to None.
            to_by (str, optional): 目标元素获取策略. Defaults to None.
            to_value (str, optional): 目标元素定位值. Defaults to None.
            to_element (WebElement, optional): 目标元素, 输入后to_by和to_value无效. Defaults to None.
            from_timeout (int, optional): 被拖拽元素等待超时时间. Defaults to 60.
            to_timeout (int, optional): 目标元素等待超时时间. Defaults to 60.
        """
        if from_element == None:
            from_element = WebDriverWait(self.driver, from_timeout).until(EC.presence_of_element_located((from_by, from_value)))
        if to_element == None:
            to_element = WebDriverWait(self.driver, to_timeout).until(EC.presence_of_element_located((to_by, to_value)))
        ActionChains(self.driver).drag_and_drop(from_element, to_element).perform()
        
    def get_text(self, by: str=None, value: str=None, element: WebElement=None, timeout: int=60) -> str:
        """获取元素文本

        Args:
            by (str, optional): 元素获取策略. Defaults to None.
            value (str, optional): 元素定位值. Defaults to None.
            element (WebElement, optional): 元素, 输入后by和value无效. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.

        Returns:
            str: 元素文本
        """
        return element.text() if element else WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value))).text()

    def send_text(self, by: str=None, value: str=None, element: WebElement=None, text_value: str="", timeout: int=60):
        """发送文本

        Args:
            by (str, optional): 元素获取策略. Defaults to None.
            value (str, optional): 元素定位值. Defaults to None.
            element (WebElement, optional): 元素, 输入后by和value无效. Defaults to None.
            text_value (str): 文本, 对input输入文件路径时会上传对应的文件. Defaults to "".
            timeout (int, optional): 等待超时时间. Defaults to 60.
            
        Example:
            >>> driver = SeleniumToolkit()
            >>> driver.start_web("web-site-url")
            >>> driver.send_text(driver.by.XPATH, "INPUT_XPATH", text_value="hello world") # 发送文本
            >>> driver.send_text(driver.by.XPATH, "INPUT_FILE_XPATH", text_value="./test.txt") # 发送文件
            >>> ele = driver.find_element(driver.by.XPATH, "INPUT_XPATH")
            >>> driver.send_text(element=ele, text_value="hello world", timeout=100)
            >>> driver.close()
        """
        element.send_keys(text_value) if element else WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value))).send_keys(text_value)
    
    def save_element_image(self, by: str=None, value: str=None, element: WebElement=None, image_box_attr: str="src", target_image_path: str="./capture_image.png", timeout: int=60):
        """保存元素图片

        Args:
            by (str, optional): 元素获取策略. Defaults to None.
            value (str, optional): 元素定位值. Defaults to None.
            element (WebElement, optional): 元素, 输入后by和value无效. Defaults to None.
            image_box_attr (str, optional): 图片box中的url属性, 会通过该url下载图片. Defaults to "src".
            target_image_path (str, optional): 目标保存路径. Defaults to "./capture_image.png".
            timeout (int, optional): 等待超时时间. Defaults to 60.
        """
        if element == None:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
        image_url = element.get_attribute(image_box_attr)
        response = requests.get(image_url, stream=True)
        if response.status_code == 200:
            with open(target_image_path, 'wb') as f:
                for chunk in response.iter_content(1024):
                    f.write(chunk)
        else:
            raise Exception(f"response status code not 200, is: {response.status_code}, can not download images")
    
    def type_keys(self, *key: str, by: str=None, value: str=None, element: WebElement=None, timeout: int=60):
        """输入模拟按键

        Args:
            key (str, optional): 模拟按键
            by (str, optional): 元素获取策略. Defaults to None.
            value (str, optional): 元素定位值. Defaults to None.
            element (WebElement, optional): 元素, 输入后by和value无效. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            
        Example:
            >>> driver = SeleniumToolkit()
            >>> driver.start_web("web-site-url")
            >>> driver.type_keys(driver.keys.ENTER, by=driver.by.XPATH, value="INPUT_XPATH") # 输入Enter
            >>> driver.type_keys(driver.keys.CONTROL, "a", by=driver.by.XPATH, value="INPUT_XPATH") # 输入Ctrl+a
            >>> ele = driver.find_element(driver.by.XPATH, "INPUT_XPATH")
            >>> driver.type_keys(driver.keys.ENTER, element=ele, timeout=100)
            >>> driver.close()
        """
        element.send_keys(key) if element else WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value))).send_keys(key)
    
    def ocr_code(self, by: str=None, value: str=None, element: WebElement=None, code_box_attr: str="src", 
                 cache_image_path: str="./cache_code_image.png", auto_delete_image: bool=True, timeout: int=60) -> str:
        """使用ocr检测验证码

        Args:
            by (str, optional): 元素获取策略. Defaults to None.
            value (str, optional): 元素定位值. Defaults to None.
            element (WebElement, optional): 元素, 输入后by和value无效. Defaults to None.
            code_box_attr (str, optional): 验证码box中的url属性, 会通过该url下载图片. Defaults to "src".
            cache_image_path (str, optional): 缓存图片路径. Defaults to "./cache_code_image.png".
            auto_delete_image (bool, optional): 自动删除缓存图片. Defaults to True.
            timeout (int, optional): 等待超时时间. Defaults to 60.

        Returns:
            str: 验证码
        """
        if element == None:
            element = WebDriverWait(self.driver, timeout).until(EC.presence_of_element_located((by, value)))
        image_url = element.get_attribute(code_box_attr)
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
    
    def switch_to_window(self, window_name: str):
        """切换浏览器标签页

        Args:
            window_name (str): 标签名
        """
        self.driver.switch_to.window(window_name)
    
    def switch_to_iframe(self, iframe_reference: str | int | WebElement):
        """切换iframe

        Args:
            iframe_reference (str | int | WebElement): 浏览器的iframe, 可以是iframe的name、id, 也可以通过获取iframe元素传入
        """
        self.driver.switch_to.frame(iframe_reference)
        
    def switch_to_default_content(self):
        """切换到默认文档, 通常用于切换iframe后切换出来主页面文档"""
        self.driver.switch_to.default_content()
    
    def execute_script(self, script_context: str, element: WebElement=None):
        """执行javascript脚本

        Args:
            script_context (str): javascript脚本
            element (WebElement, optional): 元素. Defaults to None.
        """
        self.driver.execute_script(script_context, element)
    
    def get_HTML(self) -> str:
        """获取整个页面的HTML文档

        Returns:
            str: HTML文档
        """
        return self.driver.page_source
    
    def get_element_HTML(self, by: str=None, value: str=None, element: WebElement=None, timeout: int=60, innerHTML: bool=False, outerHTML: bool=True) -> str:
        """获取元素的HTML文档

        Args:
            by (str, optional): 元素获取策略. Defaults to None.
            value (str, optional): 元素定位值. Defaults to None.
            element (WebElement, optional): 元素, 输入后by和value无效. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            innerHTML (bool, optional): 获取元素的内部HTML(不包括元素本身的标签). Defaults to False.
            outerHTML (bool, optional): 获取元素及其内部的完整HTML(包括元素本身的标签). Defaults to True.

        Returns:
            str: 元素的HTML文档
        """
        if outerHTML:
            html_content = element.get_attribute('outerHTML') if element else self.find_element(by, value, timeout).get_attribute('outerHTML')
        elif innerHTML:
            html_content = element.get_attribute('innerHTML') if element else self.find_element(by, value, timeout).get_attribute('innerHTML')
        return html_content
    
    def operate_alert(self, op_type: str="accept", send_text: str=None) -> str:
        """操作弹窗

        Args:
            op_type (str, optional): 操作类型. Defaults to "accept".
            send_text (str, optional): 发送到弹窗的文本. Defaults to None.

        Returns:
            str: 弹窗文本
        """
        alert = self.driver.switch_to.alert()
        if op_type == "accept":
            alert.accept()
        elif op_type == "dismiss":
            alert.dismiss()
        elif op_type == "send_keys":
            alert.send_keys(send_text)
        return alert.text()
    
    def get_cookie(self, cookie_name) -> dict:
        """获取cookie

        Args:
            cookie_name: cookie名

        Returns:
            dict: cookie
        """
        return self.driver.get_cookie(cookie_name)
    
    def get_cookies(self) -> list[dict]:
        """获取页面所有的cookie

        Returns:
            list[dict]: 所有的cookie
        """
        return self.driver.get_cookies()
    
    def add_cookie(self, cookie: dict):
        """增加cookie

        Args:
            cookie (dict): cookie
        """
        self.driver.add_cookie(cookie)
        
    def delete_cookie(self, cookie_name):
        """删除cookie

        Args:
            cookie_name: cookie名
        """
        self.driver.delete_cookie(cookie_name)
        
    def delete_all_cookies(self):
        """删除所有的cookie"""
        self.driver.delete_all_cookies()