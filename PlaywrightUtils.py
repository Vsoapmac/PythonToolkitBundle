# -*- coding: utf-8 -*-
# 基于 Playwright 的浏览器自动化工具类，封装常用浏览器操作，支持 Chrome/Edge/Firefox
# ------------ common ------------
from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Tuple,
    Union
)

# ------------ playwright ------------
from playwright.sync_api import (
    Browser as PWBrowser,
    BrowserContext as PWContext,
    Page as PWPage,
    Playwright as PWPlaywright,
    sync_playwright
)
from playwright.sync_api import (
    ElementHandle,
    Locator,
    expect
)

# ------------ common ------------
By = Literal


class BrowserOptionsSetter:
    """浏览器启动参数设置器，支持 Chromium、Firefox 和 WebKit"""
    _launch_options: Dict[str, Any] = {}  # 启动参数字典
    _context_options: Dict[str, Any] = {}  # 上下文参数字典

    def __init__(self, browser_type: str = "chromium"):
        """初始化浏览器参数设置器

        Args:
            browser_type (str): 浏览器类型，可选 chromium/firefox/webkit，默认为 chromium

        Example:
            >>> opts = BrowserOptionsSetter("chromium")
            >>> opts.set_headless()
            >>> opts.get_launch_options()["headless"]
            True
        """
        self._launch_options = {}
        self._context_options = {}
        self.browser_type = browser_type

    def get_launch_options(self) -> Dict[str, Any]:
        """获取启动参数字典

        Returns:
            Dict[str, Any]: 启动参数

        Example:
            >>> opts = BrowserOptionsSetter()
            >>> isinstance(opts.get_launch_options(), dict)
            True
        """
        return self._launch_options

    def get_context_options(self) -> Dict[str, Any]:
        """获取上下文参数字典

        Returns:
            Dict[str, Any]: 上下文参数

        Example:
            >>> opts = BrowserOptionsSetter()
            >>> isinstance(opts.get_context_options(), dict)
            True
        """
        return self._context_options

    def set_headless(self, headless: bool = True):
        """设置无头模式

        Args:
            headless (bool): 是否启用无头模式，默认为 True

        Example:
            >>> opts = BrowserOptionsSetter()
            >>> opts.set_headless(True)
        """
        self._launch_options["headless"] = headless

    def set_window_size(self, width: int, height: int):
        """设置浏览器窗口尺寸

        Args:
            width (int): 宽度（像素）
            height (int): 高度（像素）

        Example:
            >>> opts = BrowserOptionsSetter()
            >>> opts.set_window_size(1920, 1080)
        """
        self._context_options["viewport"] = {"width": width, "height": height}

    def set_user_agent(self, user_agent: str):
        """设置用户代理字符串

        Args:
            user_agent (str): 用户代理字符串

        Example:
            >>> opts = BrowserOptionsSetter()
            >>> opts.set_user_agent("Mozilla/5.0 ...")
        """
        self._context_options["user_agent"] = user_agent

    def set_locale(self, locale: str = "zh-CN"):
        """设置浏览器语言区域

        Args:
            locale (str): 语言区域代码，默认为 zh-CN

        Example:
            >>> opts = BrowserOptionsSetter()
            >>> opts.set_locale("en-US")
        """
        self._context_options["locale"] = locale

    def set_ignore_https_errors(self, ignore: bool = True):
        """忽略 HTTPS 证书错误

        Args:
            ignore (bool): 是否忽略 HTTPS 错误，默认为 True

        Example:
            >>> opts = BrowserOptionsSetter()
            >>> opts.set_ignore_https_errors(True)
        """
        self._launch_options["ignore_https_errors"] = ignore

    def set_disable_images(self, disable: bool = True):
        """禁用图片加载以提升性能

        Args:
            disable (bool): 是否禁用图片，默认为 True

        Example:
            >>> opts = BrowserOptionsSetter()
            >>> opts.set_disable_images(True)
        """
        if disable:
            self._context_options.setdefault("locale", "zh-CN")

    def set_proxy(self, server: str, username: Optional[str] = None, password: Optional[str] = None):
        """设置代理服务器

        Args:
            server (str): 代理服务器地址，如 "http://127.0.0.1:8080"
            username (Optional[str]): 代理认证用户名
            password (Optional[str]): 代理认证密码

        Example:
            >>> opts = BrowserOptionsSetter()
            >>> opts.set_proxy("http://127.0.0.1:8080")
        """
        proxy_config = {"server": server}
        if username and password:
            proxy_config["username"] = username
            proxy_config["password"] = password
        self._launch_options["proxy"] = proxy_config

    def set_download_path(self, download_path: Union[str, Path]):
        """设置下载文件保存路径

        Args:
            download_path (Union[str, Path]): 下载路径

        Example:
            >>> opts = BrowserOptionsSetter()
            >>> opts.set_download_path("./downloads")
        """
        self._context_options["accept_downloads"] = True
        self._context_options["downloads_path"] = str(download_path)

    def set_timeout(self, timeout: int = 30000):
        """设置默认超时时间（毫秒）

        Args:
            timeout (int): 超时时间（毫秒），默认为 30000

        Example:
            >>> opts = BrowserOptionsSetter()
            >>> opts.set_timeout(60000)
        """
        self._launch_options["timeout"] = timeout

    def add_args(self, args: List[str]):
        """添加浏览器命令行启动参数

        Args:
            args (List[str]): 命令行参数列表

        Example:
            >>> opts = BrowserOptionsSetter()
            >>> opts.add_args(["--disable-gpu", "--no-sandbox"])
        """
        self._launch_options.setdefault("args", []).extend(args)

    def set_device_scale_factor(self, scale: float = 2.0):
        """设置设备缩放因子（影响截图清晰度）

        Args:
            scale (float): 缩放因子，默认为 2.0

        Example:
            >>> opts = BrowserOptionsSetter()
            >>> opts.set_device_scale_factor(2.0)
        """
        self._context_options["device_scale_factor"] = scale

    def set_record_video(self, video_dir: Union[str, Path], video_size: Optional[Dict[str, int]] = None):
        """设置录屏功能

        Args:
            video_dir (Union[str, Path]): 视频保存目录
            video_size (Optional[Dict[str, int]]): 视频尺寸，如 {"width": 1920, "height": 1080}

        Example:
            >>> opts = BrowserOptionsSetter()
            >>> opts.set_record_video("./videos", {"width": 1920, "height": 1080})
        """
        record_config = {"dir": str(video_dir)}
        if video_size:
            record_config["size"] = video_size
        self._context_options["record_video"] = record_config

    @classmethod
    def create_chromium_opts(cls, headless: bool = False, window_size: Optional[Tuple[int, int]] = None,
                             user_agent: Optional[str] = None, locale: str = "zh-CN",
                             ignore_https: bool = True, timeout: int = 30000) -> "BrowserOptionsSetter":
        """快速创建 Chromium 浏览器参数（类方法快捷入口）

        Args:
            headless (bool): 无头模式，默认为 False
            window_size (Optional[Tuple[int, int]]): 窗口尺寸
            user_agent (Optional[str]): 用户代理
            locale (str): 语言区域，默认为 zh-CN
            ignore_https (bool): 忽略 HTTPS 错误，默认为 True
            timeout (int): 超时时间（毫秒），默认为 30000

        Returns:
            BrowserOptionsSetter: 配置好的参数设置器

        Example:
            >>> opts = BrowserOptionsSetter.create_chromium_opts(headless=True)
            >>> opts.get_launch_options()["headless"]
            True
        """
        opts = cls("chromium")
        opts.set_headless(headless)
        if window_size:
            opts.set_window_size(*window_size)
        if user_agent:
            opts.set_user_agent(user_agent)
        opts.set_locale(locale)
        opts.set_ignore_https_errors(ignore_https)
        opts.set_timeout(timeout)
        return opts


class PlaywrightUtils:
    """Playwright 浏览器自动化工具类

    封装 Playwright 的常用浏览器操作，包含页面导航、元素查找、点击、文本输入、
    截图、Cookie 管理等。支持上下文管理器自动清理资源。

    Usage:
        >>> with PlaywrightUtils() as pw:
        >>>     pw.start_web("https://example.com")
        >>>     pw.click("#submit")
        >>>     text = pw.get_text("#result")
    """
    _playwright: Optional[PWPlaywright] = None  # Playwright 引擎实例
    browser: Optional[PWBrowser] = None  # 浏览器实例
    context: Optional[PWContext] = None  # 浏览器上下文
    page: Optional[PWPage] = None  # 当前页面
    _browser_type: str = ""  # 浏览器类型标识

    def __init__(self, browser_type: str = "chromium",
                 options: Optional[BrowserOptionsSetter] = None,
                 connect_url: Optional[str] = None,
                 headless: bool = False):
        """初始化 PlaywrightUtils

        Args:
            browser_type (str): 浏览器类型，可选 chromium/firefox/webkit，默认为 chromium
            options (Optional[BrowserOptionsSetter]): 浏览器参数设置器
            connect_url (Optional[str]): 远程浏览器连接 URL（如 ws://...），为 None 则启动本地浏览器
            headless (bool): 是否使用无头模式，仅在不提供 options 时生效，默认为 False

        Example:
            >>> pw = PlaywrightUtils("chromium")
            >>> pw.browser is not None
            True
            >>> pw.close()
        """
        self._browser_type = browser_type
        self._playwright = sync_playwright().start()

        # 步骤1: 确定浏览器启动参数
        launch_opts = {}
        context_opts = {}
        if options is not None:
            launch_opts = options.get_launch_options()
            context_opts = options.get_context_options()
        if headless and "headless" not in launch_opts:
            launch_opts["headless"] = True

        # 步骤2: 启动浏览器
        browser_launcher = getattr(self._playwright, browser_type)
        if connect_url:
            self.browser = browser_launcher.connect(connect_url, **launch_opts)
        else:
            self.browser = browser_launcher.launch(**launch_opts)

        # 步骤3: 创建上下文和默认页面
        self.context = self.browser.new_context(**context_opts)
        self.page = self.context.new_page()

    def __enter__(self) -> "PlaywrightUtils":
        """进入上下文管理器"""
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        """退出上下文管理器，自动释放资源"""
        self.close()

    def close(self):
        """关闭浏览器并释放所有资源"""
        if self.page:
            try:
                self.page.close()
            except Exception:
                pass
            self.page = None
        if self.context:
            try:
                self.context.close()
            except Exception:
                pass
            self.context = None
        if self.browser:
            try:
                self.browser.close()
            except Exception:
                pass
            self.browser = None
        if self._playwright:
            try:
                self._playwright.stop()
            except Exception:
                pass
            self._playwright = None

    # region ---------------------------- 页面导航 ----------------------------

    def start_web(self, url: str, wait_until: Optional[str] = "domcontentloaded",
                  timeout: int = 30000):
        """打开网页

        Args:
            url (str): 页面 URL
            wait_until (Optional[str]): 等待策略，可选 load/domcontentloaded/networkidle/commit，默认为 domcontentloaded
            timeout (int): 超时时间（毫秒），默认为 30000

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> "Example" in pw.page.title()
            True
            >>> pw.close()
        """
        self.page.goto(url, wait_until=wait_until, timeout=timeout)

    def refresh(self):
        """刷新当前页面"""
        self.page.reload()

    def back(self):
        """返回到上一页"""
        self.page.go_back()

    def forward(self):
        """前进到下一页"""
        self.page.go_forward()

    # endregion ---------------------------- 页面导航 ----------------------------

    # region ---------------------------- 元素查找 ----------------------------

    def find_element(self, selector: str, timeout: int = 30000) -> ElementHandle:
        """获取页面中第一个匹配的元素

        Args:
            selector (str): CSS 选择器或 Playwright 选择器字符串
            timeout (int): 等待超时时间（毫秒），默认为 30000

        Returns:
            ElementHandle: 对应的元素句柄

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> el = pw.find_element("h1")
            >>> el.text_content()
            'Example Domain'
            >>> pw.close()
        """
        return self.page.wait_for_selector(selector, timeout=timeout)

    def find_elements(self, selector: str, timeout: int = 30000) -> List[ElementHandle]:
        """获取页面中所有匹配的元素

        Args:
            selector (str): CSS 选择器或 Playwright 选择器字符串
            timeout (int): 等待超时时间（毫秒），默认为 30000

        Returns:
            List[ElementHandle]: 元素句柄列表

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> els = pw.find_elements("p")
            >>> len(els) > 0
            True
            >>> pw.close()
        """
        self.page.wait_for_selector(selector, timeout=timeout)
        return self.page.query_selector_all(selector)

    def find_element_by_text(self, text: str, tag: str = "*", timeout: int = 30000) -> ElementHandle:
        """通过文本内容查找元素

        Args:
            text (str): 要匹配的文本
            tag (str): HTML 标签名，默认为 *
            timeout (int): 等待超时时间（毫秒），默认为 30000

        Returns:
            ElementHandle: 找到的元素

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> el = pw.find_element_by_text("Example", "h1")
            >>> el is not None
            True
            >>> pw.close()
        """
        selector = f'{tag}:has-text("{text}")'
        return self.find_element(selector, timeout)

    def get_locator(self, selector: str) -> Locator:
        """获取 Locator 对象用于更灵活的操作

        Args:
            selector (str): CSS 选择器

        Returns:
            Locator: Playwright Locator 对象

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> loc = pw.get_locator("h1")
            >>> loc is not None
            True
            >>> pw.close()
        """
        return self.page.locator(selector)

    # endregion ---------------------------- 元素查找 ----------------------------

    # region ---------------------------- 元素操作 ----------------------------

    def click(self, selector: Optional[str] = None, element: Optional[ElementHandle] = None,
              timeout: int = 30000):
        """点击元素

        Args:
            selector (Optional[str]): 元素选择器，与 element 二选一
            element (Optional[ElementHandle]): 元素句柄，与 selector 二选一
            timeout (int): 等待超时时间（毫秒），默认为 30000

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> pw.click("h1")
            >>> pw.close()
        """
        if element:
            element.click(timeout=timeout)
        elif selector:
            self.page.click(selector, timeout=timeout)

    def double_click(self, selector: Optional[str] = None, element: Optional[ElementHandle] = None,
                     timeout: int = 30000):
        """双击元素

        Args:
            selector (Optional[str]): 元素选择器
            element (Optional[ElementHandle]): 元素句柄
            timeout (int): 等待超时时间（毫秒），默认为 30000
        """
        if element:
            element.dblclick(timeout=timeout)
        elif selector:
            self.page.dblclick(selector, timeout=timeout)

    def right_click(self, selector: Optional[str] = None, element: Optional[ElementHandle] = None,
                    timeout: int = 30000):
        """右键点击元素

        Args:
            selector (Optional[str]): 元素选择器
            element (Optional[ElementHandle]): 元素句柄
            timeout (int): 等待超时时间（毫秒），默认为 30000
        """
        if element:
            element.click(button="right", timeout=timeout)
        elif selector:
            self.page.click(selector, button="right", timeout=timeout)

    def send_text(self, selector: Optional[str] = None, element: Optional[ElementHandle] = None,
                  text: str = "", delay: int = 0, timeout: int = 30000):
        """向元素输入文本

        Args:
            selector (Optional[str]): 元素选择器
            element (Optional[ElementHandle]): 元素句柄
            text (str): 要输入的文本
            delay (int): 按键间隔（毫秒），模拟真人输入，默认为 0
            timeout (int): 等待超时时间（毫秒），默认为 30000

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> pw.send_text("input[type='text']", text="hello")
            >>> pw.close()
        """
        if element:
            element.fill(text, timeout=timeout)
        elif selector:
            self.page.fill(selector, text, timeout=timeout)

    def type_keys(self, selector: Optional[str] = None, element: Optional[ElementHandle] = None,
                  text: str = "", delay: int = 50, timeout: int = 30000):
        """模拟键盘逐键输入（比 fill 更真实，但更慢）

        Args:
            selector (Optional[str]): 元素选择器
            element (Optional[ElementHandle]): 元素句柄
            text (str): 要输入的文本
            delay (int): 按键间隔（毫秒），默认为 50
            timeout (int): 等待超时时间（毫秒），默认为 30000
        """
        if element:
            element.type(text, delay=delay, timeout=timeout)
        elif selector:
            self.page.type(selector, text, delay=delay, timeout=timeout)

    def clear_text(self, selector: Optional[str] = None, element: Optional[ElementHandle] = None):
        """清空元素文本

        Args:
            selector (Optional[str]): 元素选择器
            element (Optional[ElementHandle]): 元素句柄
        """
        if element:
            element.fill("")
        elif selector:
            self.page.fill(selector, "")

    def select_combobox(self, selector: Optional[str] = None, element: Optional[ElementHandle] = None,
                        select_type: str = "label", select_value: Union[str, List[str]] = "",
                        timeout: int = 30000) -> List[str]:
        """选择 <select> 下拉框选项

        Args:
            selector (Optional[str]): 元素选择器
            element (Optional[ElementHandle]): 元素句柄
            select_type (str): 选择策略，可选 label/value/index，默认为 label
            select_value (Union[str, List[str]]): 选择值
            timeout (int): 等待超时时间（毫秒），默认为 30000

        Returns:
            List[str]: 选中选项的值列表

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> result = pw.select_combobox("select#country", select_type="label", select_value="China")
            >>> pw.close()
        """
        if element:
            return element.select_option(**{select_type: select_value}, timeout=timeout)
        return self.page.select_option(selector, **{select_type: select_value}, timeout=timeout)

    # endregion ---------------------------- 元素操作 ----------------------------

    # region ---------------------------- 获取信息 ----------------------------

    def get_text(self, selector: Optional[str] = None, element: Optional[ElementHandle] = None,
                 timeout: int = 30000) -> str:
        """获取元素文本内容

        Args:
            selector (Optional[str]): 元素选择器
            element (Optional[ElementHandle]): 元素句柄
            timeout (int): 等待超时时间（毫秒），默认为 30000

        Returns:
            str: 元素的文本内容

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> text = pw.get_text("h1")
            >>> text
            'Example Domain'
            >>> pw.close()
        """
        if element:
            return element.text_content() or ""
        return self.page.text_content(selector, timeout=timeout) or ""

    def get_attribute(self, selector: Optional[str] = None, element: Optional[ElementHandle] = None,
                      attr: str = "href", timeout: int = 30000) -> Optional[str]:
        """获取元素属性值

        Args:
            selector (Optional[str]): 元素选择器
            element (Optional[ElementHandle]): 元素句柄
            attr (str): 属性名，默认为 href
            timeout (int): 等待超时时间（毫秒），默认为 30000

        Returns:
            Optional[str]: 属性值，不存在时返回 None
        """
        if element:
            return element.get_attribute(attr)
        return self.page.get_attribute(selector, attr, timeout=timeout)

    def get_value(self, selector: Optional[str] = None, element: Optional[ElementHandle] = None,
                  timeout: int = 30000) -> str:
        """获取表单元素的 value 值

        Args:
            selector (Optional[str]): 元素选择器
            element (Optional[ElementHandle]): 元素句柄
            timeout (int): 等待超时时间（毫秒），默认为 30000

        Returns:
            str: 元素 value 属性值
        """
        if element:
            return element.input_value(timeout=timeout)
        return self.page.input_value(selector, timeout=timeout)

    def get_title(self) -> str:
        """获取当前页面标题

        Returns:
            str: 页面标题

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> title = pw.get_title()
            >>> "Example" in title
            True
            >>> pw.close()
        """
        return self.page.title()

    def get_url(self) -> str:
        """获取当前页面 URL

        Returns:
            str: 当前 URL
        """
        return self.page.url

    def get_html(self) -> str:
        """获取整个页面的 HTML 文档

        Returns:
            str: 完整 HTML

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> html = pw.get_html()
            >>> "<html" in html
            True
            >>> pw.close()
        """
        return self.page.content()

    def get_element_html(self, selector: Optional[str] = None, element: Optional[ElementHandle] = None,
                         timeout: int = 30000) -> str:
        """获取元素的 outerHTML

        Args:
            selector (Optional[str]): 元素选择器
            element (Optional[ElementHandle]): 元素句柄
            timeout (int): 等待超时时间（毫秒），默认为 30000

        Returns:
            str: 元素的 outerHTML
        """
        if element:
            return element.evaluate("el => el.outerHTML")
        return self.page.evaluate(f"document.querySelector('{selector}')?.outerHTML || ''")

    # endregion ---------------------------- 获取信息 ----------------------------

    # region ---------------------------- 等待与条件 ----------------------------

    def wait_for_element(self, selector: str, state: str = "visible", timeout: int = 30000) -> ElementHandle:
        """等待元素达到指定状态

        Args:
            selector (str): CSS 选择器
            state (str): 目标状态，可选 visible/hidden/attached/detached，默认为 visible
            timeout (int): 超时时间（毫秒），默认为 30000

        Returns:
            ElementHandle: 等待到元素

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> el = pw.wait_for_element("h1")
            >>> el is not None
            True
            >>> pw.close()
        """
        return self.page.wait_for_selector(selector, state=state, timeout=timeout)

    def wait_for_timeout(self, ms: int = 1000):
        """强制等待指定时间

        Args:
            ms (int): 等待毫秒数，默认为 1000

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.wait_for_timeout(500)
        """
        self.page.wait_for_timeout(ms)

    def wait_for_function(self, expression: str, timeout: int = 30000):
        """等待页面中的 JavaScript 函数返回真值

        Args:
            expression (str): JavaScript 函数体或表达式
            timeout (int): 超时时间（毫秒），默认为 30000

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> pw.wait_for_function("() => document.title.includes('Example')")
            >>> pw.close()
        """
        self.page.wait_for_function(expression, timeout=timeout)

    # endregion ---------------------------- 等待与条件 ----------------------------

    # region ---------------------------- 窗口与标签页 ----------------------------

    def switch_to_window(self, index: int = 0):
        """切换到指定索引的标签页

        Args:
            index (int): 标签页索引，从 0 开始

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> # 假设通过某些操作打开了新标签页
            >>> pw.switch_to_window(0)
            >>> pw.close()
        """
        pages = self.context.pages
        if index < len(pages):
            self.page = pages[index]
            self.page.bring_to_front()

    def get_windows(self) -> List[PWPage]:
        """获取所有标签页

        Returns:
            List[PWPage]: 所有标签页对象列表
        """
        return self.context.pages

    def new_tab(self, url: Optional[str] = None) -> PWPage:
        """打开新标签页

        Args:
            url (Optional[str]): 新标签页的 URL

        Returns:
            PWPage: 新标签页对象
        """
        if url:
            new_page = self.context.new_page()
            new_page.goto(url)
        else:
            new_page = self.context.new_page()
        self.page = new_page
        return new_page

    def close_tab(self, page: Optional[PWPage] = None):
        """关闭标签页

        Args:
            page (Optional[PWPage]): 要关闭的标签页，为 None 时关闭当前页
        """
        target = page or self.page
        target.close()
        pages = self.context.pages
        if pages:
            self.page = pages[-1]
        else:
            self.page = None

    # endregion ---------------------------- 窗口与标签页 ----------------------------

    # region ---------------------------- iframe 操作 ----------------------------

    def switch_to_iframe(self, selector: str, timeout: int = 30000):
        """切换到 iframe

        Args:
            selector (str): iframe 元素的选择器
            timeout (int): 等待超时时间（毫秒），默认为 30000

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> # pw.switch_to_iframe("iframe#content")
            >>> pw.close()
        """
        frame_element = self.wait_for_element(selector, timeout=timeout)
        frame = frame_element.content_frame()
        if frame:
            self.page = frame

    def switch_to_default_content(self):
        """从 iframe 切换回主页面"""
        main_page = self.page.page
        if main_page:
            self.page = main_page

    # endregion ---------------------------- iframe 操作 ----------------------------

    # region ---------------------------- 截图与录屏 ----------------------------

    def screenshot(self, output_path: Union[str, Path], full_page: bool = False,
                   quality: Optional[int] = None) -> bytes:
        """对当前页面进行截图

        Args:
            output_path (Union[str, Path]): 截图保存路径（支持 png/jpg）
            full_page (bool): 是否截取整个页面（包括滚动区域），默认为 False
            quality (Optional[int]): 图片质量（仅 jpg），1-100

        Returns:
            bytes: 截图二进制数据

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> img_bytes = pw.screenshot("/tmp/screenshot.png")
            >>> len(img_bytes) > 0
            True
            >>> pw.close()
        """
        output_path = str(output_path)
        self.page.screenshot(path=output_path, full_page=full_page, quality=quality)
        with open(output_path, "rb") as f:
            return f.read()

    def screenshot_element(self, selector: str, output_path: Union[str, Path],
                           timeout: int = 30000) -> bytes:
        """对特定元素进行截图

        Args:
            selector (str): 元素选择器
            output_path (Union[str, Path]): 截图保存路径
            timeout (int): 等待超时时间（毫秒），默认为 30000

        Returns:
            bytes: 截图二进制数据
        """
        element = self.wait_for_element(selector, timeout=timeout)
        element.screenshot(path=str(output_path))
        with open(str(output_path), "rb") as f:
            return f.read()

    # endregion ---------------------------- 截图与录屏 ----------------------------

    # region ---------------------------- JavaScript 操作 ----------------------------

    def execute_script(self, script: str, *args) -> Any:
        """执行 JavaScript 脚本

        Args:
            script (str): 要执行的 JavaScript 代码
            *args: 传递给脚本的参数

        Returns:
            Any: JavaScript 执行结果

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> result = pw.execute_script("return document.title")
            >>> "Example" in result
            True
            >>> pw.close()
        """
        return self.page.evaluate(script, *args)

    def execute_script_on_element(self, selector: str, script: str,
                                  timeout: int = 30000) -> Any:
        """在指定元素上执行 JavaScript

        Args:
            selector (str): 元素选择器
            script (str): JavaScript 代码
            timeout (int): 等待超时时间（毫秒），默认为 30000

        Returns:
            Any: 执行结果
        """
        element = self.wait_for_element(selector, timeout=timeout)
        return element.evaluate(script)

    # endregion ---------------------------- JavaScript 操作 ----------------------------

    # region ---------------------------- Cookie 管理 ----------------------------

    def get_cookies(self) -> List[Dict[str, Any]]:
        """获取当前页面的所有 Cookie

        Returns:
            List[Dict[str, Any]]: Cookie 列表

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> cookies = pw.get_cookies()
            >>> isinstance(cookies, list)
            True
            >>> pw.close()
        """
        return self.context.cookies()

    def add_cookie(self, cookie: Dict[str, Any]):
        """添加 Cookie

        Args:
            cookie (Dict[str, Any]): Cookie 字典，必须包含 name 和 value 字段

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.add_cookie({"name": "token", "value": "abc123", "url": "https://example.com"})
            >>> pw.close()
        """
        self.context.add_cookies([cookie])

    def delete_all_cookies(self):
        """删除所有 Cookie"""
        self.context.clear_cookies()

    # endregion ---------------------------- Cookie 管理 ----------------------------

    # region ---------------------------- 文件操作 ----------------------------

    def upload_file(self, selector: str, file_paths: Union[str, List[str]], timeout: int = 30000):
        """上传文件到文件选择控件

        Args:
            selector (str): 文件输入元素的选择器
            file_paths (Union[str, List[str]]): 文件路径或路径列表
            timeout (int): 等待超时时间（毫秒），默认为 30000

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> # pw.upload_file("input[type='file']", "document.pdf")
            >>> pw.close()
        """
        if isinstance(file_paths, str):
            file_paths = [file_paths]
        element = self.wait_for_element(selector, timeout=timeout)
        element.set_input_files(file_paths, timeout=timeout)

    def download_file(self, selector: str, download_dir: Union[str, Path],
                      timeout: int = 60000) -> Path:
        """点击元素下载文件并保存到指定目录

        Args:
            selector (str): 触发下载的元素选择器
            download_dir (Union[str, Path]): 下载保存目录
            timeout (int): 等待下载完成超时时间（毫秒），默认为 60000

        Returns:
            Path: 下载文件路径
        """
        download_dir = Path(download_dir)
        download_dir.mkdir(parents=True, exist_ok=True)

        with self.page.expect_download(timeout=timeout) as download_info:
            self.click(selector)

        download = download_info.value
        file_path = download_dir / download.suggested_filename
        download.save_as(str(file_path))
        return file_path

    # endregion ---------------------------- 文件操作 ----------------------------

    # region ---------------------------- 对话框与弹窗 ----------------------------

    def handle_dialog(self, action: str = "accept", text: Optional[str] = None):
        """设置对话框处理方式（需在触发对话框前调用）

        Args:
            action (str): 处理方式，可选 accept/dismiss，默认为 accept
            text (Optional[str]): 输入到 prompt 对话框的文本

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.handle_dialog("accept")
            >>> # pw.click("#show-alert-btn")
            >>> pw.close()
        """
        if action == "accept":
            if text:
                self.page.once("dialog", lambda d: d.accept(prompt_text=text))
            else:
                self.page.once("dialog", lambda d: d.accept())
        else:
            self.page.once("dialog", lambda d: d.dismiss())

    # endregion ---------------------------- 对话框与弹窗 ----------------------------

    # region ---------------------------- 页面交互 ----------------------------

    def scroll_to_bottom(self):
        """滚动到页面底部"""
        self.page.evaluate("window.scrollTo(0, document.body.scrollHeight)")

    def scroll_to_top(self):
        """滚动到页面顶部"""
        self.page.evaluate("window.scrollTo(0, 0)")

    def scroll_to_element(self, selector: str, timeout: int = 30000):
        """滚动到指定元素位置

        Args:
            selector (str): 元素选择器
            timeout (int): 等待超时时间（毫秒），默认为 30000
        """
        element = self.wait_for_element(selector, timeout=timeout)
        element.scroll_into_view_if_needed(timeout=timeout)

    def hover(self, selector: Optional[str] = None, element: Optional[ElementHandle] = None,
              timeout: int = 30000):
        """鼠标悬停到元素

        Args:
            selector (Optional[str]): 元素选择器
            element (Optional[ElementHandle]): 元素句柄
            timeout (int): 等待超时时间（毫秒），默认为 30000
        """
        if element:
            element.hover(timeout=timeout)
        elif selector:
            self.page.hover(selector, timeout=timeout)

    def drag_and_drop(self, source_selector: str, target_selector: str, timeout: int = 30000):
        """拖拽元素到目标位置

        Args:
            source_selector (str): 被拖拽元素选择器
            target_selector (str): 目标元素选择器
            timeout (int): 等待超时时间（毫秒），默认为 30000

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> # pw.drag_and_drop("#drag-item", "#drop-zone")
            >>> pw.close()
        """
        self.page.drag_and_drop(source_selector, target_selector, timeout=timeout)

    def press_key(self, key: str):
        """按下键盘按键

        Args:
            key (str): 按键名，如 Enter/Tab/Escape/ArrowDown/Control+a

        Example:
            >>> pw = PlaywrightUtils(headless=True)
            >>> pw.start_web("https://example.com")
            >>> pw.press_key("Escape")
            >>> pw.close()
        """
        self.page.keyboard.press(key)

    # endregion ---------------------------- 页面交互 ----------------------------

    # region ---------------------------- 网络监听 ----------------------------

    def wait_for_request(self, url_or_pattern: str, timeout: int = 30000):
        """等待特定网络请求发生

        Args:
            url_or_pattern (str): URL 字符串或正则表达式
            timeout (int): 超时时间（毫秒），默认为 30000
        """
        self.page.wait_for_request(url_or_pattern, timeout=timeout)

    def wait_for_response(self, url_or_pattern: str, timeout: int = 30000):
        """等待特定网络响应

        Args:
            url_or_pattern (str): URL 字符串或正则表达式
            timeout (int): 超时时间（毫秒），默认为 30000
        """
        self.page.wait_for_response(url_or_pattern, timeout=timeout)

    # endregion ---------------------------- 网络监听 ----------------------------
