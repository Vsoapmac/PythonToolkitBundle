from pywinauto.application import Application, WindowSpecification
from pywinauto import mouse, keyboard

class Keys:
    ENTER = "{ENTER}"
    SHIFT = "+"
    CTRL = "^"
    ALT = "%"
    SPACE = "{SPACE}"
    BACKSPACE = "{BACKSPACE}"
    BREAK = "{BREAK}"
    CAPSLOCK = "{CAPSLOCK}"
    DELETE = "{DELETE}"
    DOWN_ARROW = "{DOWN}"
    UP_ARROW = "{UP}"
    LEFT_ARROW = "{LEFT}"
    RIGHT_ARROW = "{RIGHT}"
    END = "{END}"
    ESC = "{ESC}"
    HOME = "{HOME}"
    INSERT = "{INSERT}"
    NUMLOCK = "{NUMLOCK}"
    PAGEDOWN = "{PGDN}"
    PAGEUP = "{PGUP}"
    PRINTSCREEN = "{PRTSC}"
    SCROLLLOCK = "{SCROLLLOCK}"
    TAB = "{TAB}"
    HELP = "{HELP}"

class PywinautoToolKit:
    """pywinauto工具类, 适用于windows的app, 控件和窗口在该处的概念都为windows
    \n若使用该工具类, 请使用如下命令安装第三方库:
    \npip install pywinauto
    """
    app = None
    key = Keys
    
    def __init__(self, app_path: str=None, backend: str="win32"):
        if app_path:
            self.app = Application(backend).start(app_path)
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.app != None:
            self.app.kill()
            self.app = None
    
    def start_application(self, app_path: str, backend: str="win32"):
        """打开一个应用

        Args:
            app_path (str): exe文件路径, 若不写路径, 则需要该app可以在终端中输入该exe文件名称并直接打开
            backend (str, optional): 后端识别类型, 类型有(win32|uia). Defaults to "win32".
        """
        self.app = Application(backend).start(app_path)
    
    def connect_application(self, app_path: str=None, process: int=None, backend: str='win32'):
        """连接到一个现有应用

        Args:
            app_path (str, optional): exe文件路径, 若不写路径, 则需要该app可以在终端中输入该exe文件名称并直接打开. Defaults to None.
            process (int, optional): 应用进程号, 进程号在任务管理器->详细信息中可以查看. Defaults to None.
            backend (str, optional): 后端识别类型, 类型有(win32|uia). Defaults to 'win32'.
        """
        if app_path:
            self.app = Application(backend=backend).connect(path=app_path)
        elif process:
            self.app = Application(backend=backend).connect(process=process)
            
    def close(self):
        """关闭整个app"""
        self.app.kill()
    
    def find_window(self, window_title: str, timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5) -> WindowSpecification:
        """查找窗口

        Args:
            window_title (str): 窗口标题
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.

        Returns:
            WindowSpecification: 窗口对象
        """
        window = self.app[window_title]
        window.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        return window
    
    def find_window_by_regular(self, window_title: str, timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5) -> WindowSpecification:
        """模糊查找窗口

        Args:
            window_title (str): 窗口标题
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.

        Returns:
            WindowSpecification: 窗口对象
        """
        window = self.app.window(title_re=f".*{window_title}.*")
        window.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        return window
    
    def find_child_window(self, window_title: str, child_window_title: str=None, child_window_auto_id: str=None, 
                          timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5) -> WindowSpecification:
        """查找子窗口

        Args:
            window_title (str): 窗口标题
            child_window_title (str, optional): 子窗口标题. Defaults to None.
            child_window_auto_id (str, optional): 子窗口auto id. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.

        Returns:
            WindowSpecification: 窗口对象
        """
        if child_window_title:
            window = self.app[window_title].child_window(title=child_window_title)
        elif child_window_auto_id:
            window = self.app[window_title].child_window(auto_id=child_window_auto_id)
        window.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        return window
        
    def select_menu(self, window_title: str=None, window: WindowSpecification=None, menu_list: list=[], 
                    timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
        """选择窗口的菜单

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            window (WindowSpecification, optional): 窗口对象. Defaults to None.
            menu_list (list, optional): 菜单列表, 会选择列表下的对应选项. Defaults to [].
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        """
        menu_str = "".join([menu.join("->") for menu in menu_list])
        menu_str = menu_str.rstrip("->")
        if window_title and window == None:
            window = self.app[window_title]
            window.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        window.menu_select(menu_str)
    
    def window_close(self, window_title: str=None, window: WindowSpecification=None, 
                    timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
        """关闭窗口

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            window (WindowSpecification, optional): 窗口对象. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        """
        if window_title and window == None:
            window = self.app[window_title]
            window.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        window.close()
        
    def window_set_focus(self, window_title: str=None, window: WindowSpecification=None, 
                    timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
        """设置窗口聚焦, 若窗口隐藏会显示在最上层

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            window (WindowSpecification, optional): 窗口对象. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        """
        if window_title and window == None:
            window = self.app[window_title]
            window.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        window.set_focus()
        
    def window_minimize(self, window_title: str=None, window: WindowSpecification=None, 
                    timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
        """窗口最小化

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            window (WindowSpecification, optional): 窗口对象. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        """
        if window_title and window == None:
            window = self.app[window_title]
            window.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        window.minimize()
        
    def window_maximize(self, window_title: str=None, window: WindowSpecification=None, 
                    timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
        """窗口最大化

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            window (WindowSpecification, optional): 窗口对象. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        """
        if window_title and window == None:
            window = self.app[window_title]
            window.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        window.maximize()
        
    def window_restore(self, window_title: str=None, window: WindowSpecification=None, 
                    timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
        """将窗口恢复为正常大小

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            window (WindowSpecification, optional): 窗口对象. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        """
        if window_title and window == None:
            window = self.app[window_title]
            window.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        window.restore()
        
    def is_window_exists(self, window_title: str=None, window: WindowSpecification=None, 
                    timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5) -> bool:
        """判断窗口是否存在

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            window (WindowSpecification, optional): 窗口对象. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.

        Returns:
            bool: 窗口是否存在
        """
        if window_title and window == None:
            window = self.app[window_title]
            window.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        return window.exists()
        
    def find_element(self, window_title: str, element_title: str=None, element_auto_id: str=None, 
                     timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5) -> WindowSpecification:
        """寻找窗口控件

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            element_title (str, optional): 控件标题. Defaults to None.
            element_auto_id (str, optional): 控件auto id. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.

        Returns:
            WindowSpecification: 控件对象
        """
        if element_title:
            element = self.app[window_title].window(title=element_title)
        elif element_auto_id:
            element = self.app[window_title].window(auto_id=element_auto_id)
        element.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        return element
    
    def wait_until_element_disappear(self, window_title: str, element_title: str=None, element_auto_id: str=None, 
                     timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
        """等待控件消失

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            element_title (str, optional): 控件标题. Defaults to None.
            element_auto_id (str, optional): 控件auto id. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        """
        if element_title:
            element = self.app[window_title].window(title=element_title)
        elif element_auto_id:
            element = self.app[window_title].window(auto_id=element_auto_id)
        element.wait_not(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
    
    def window_capture(self, window: WindowSpecification, capture_image_path: str):
        """窗口截图

        Args:
            window (WindowSpecification): 窗口对象
            capture_image_path (str): 保存图像路径
        """
        window.capture_as_image().save(capture_image_path)
        
    def print_control_identifiers(self, window: WindowSpecification, depth: int=None, filename: str=None):
        """打印窗口控件树

        Args:
            window (WindowSpecification): 窗口对象
            depth (int, optional): 递归打印控件标识符信息的深度. Defaults to None.
            filename (str, optional): 将控件标识符信息输出到的文件名. Defaults to None.
        """
        window.print_control_identifiers(depth=depth, filename=filename)
    
    def get_text(self, window_title: str=None, element_title: str=None, element_auto_id: str=None, 
              element: WindowSpecification=None, timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5) -> str:
        """获取控件文本

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            element_title (str, optional): 控件标题. Defaults to None.
            element_auto_id (str, optional): 控件auto id. Defaults to None.
            element (WindowSpecification, optional): 控件对象. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.

        Returns:
            str: 控件文本
        """
        if element == None:
            if element_title:
                element = self.app[window_title].window(title=element_title)
            elif element_auto_id:
                element = self.app[window_title].window(auto_id=element_auto_id)
            element.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        return element.window_text()
    
    def select_tab(self, window_title: str=None, tab_title: str=None, tab_auto_id: str=None, 
              tab_window: WindowSpecification=None, tab_value: int | str = 0, timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
        """选择窗口标签

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            tab_title (str, optional): 标签窗口标题. Defaults to None.
            tab_auto_id (str, optional): 标签窗口auto id. Defaults to None.
            tab_window (WindowSpecification, optional): 标签窗口对象. Defaults to None.
            tab_value (int | str, optional): 标签index或标签名. Defaults to 0.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        """
        if tab_window == None:
            if tab_title:
                tab_window = self.app[window_title].window(title=tab_title)
            elif tab_auto_id:
                tab_window = self.app[window_title].window(auto_id=tab_auto_id)
            tab_window.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        tab_window.select(tab_value)
        
    def click(self, window_title: str=None, element_title: str=None, element_auto_id: str=None, 
              element: WindowSpecification=None, timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
        """点击控件

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            element_title (str, optional): 控件标题. Defaults to None.
            element_auto_id (str, optional): 控件auto id. Defaults to None.
            element (WindowSpecification, optional): 控件对象. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        """
        if element == None:
            if element_title:
                element = self.app[window_title].window(title=element_title)
            elif element_auto_id:
                element = self.app[window_title].window(auto_id=element_auto_id)
            element.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        element.click()
    
    def double_click(self, window_title: str=None, element_title: str=None, element_auto_id: str=None, 
              element: WindowSpecification=None, timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
        """双击控件

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            element_title (str, optional): 控件标题. Defaults to None.
            element_auto_id (str, optional): 控件auto id. Defaults to None.
            element (WindowSpecification, optional): 控件对象. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        """
        if element == None:
            if element_title:
                element = self.app[window_title].window(title=element_title)
            elif element_auto_id:
                element = self.app[window_title].window(auto_id=element_auto_id)
            element.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        element.double_click()
        
    def click_input(self, window_title: str=None, element_title: str=None, element_auto_id: str=None, 
              element: WindowSpecification=None, timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
        """点击控件, 该方法会将鼠标移动到对应控件位置

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            element_title (str, optional): 控件标题. Defaults to None.
            element_auto_id (str, optional): 控件auto id. Defaults to None.
            element (WindowSpecification, optional): 控件对象. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        """
        if element == None:
            if element_title:
                element = self.app[window_title].window(title=element_title)
            elif element_auto_id:
                element = self.app[window_title].window(auto_id=element_auto_id)
            element.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        element.click_input()
        
    def double_click_input(self, window_title: str=None, element_title: str=None, element_auto_id: str=None, 
              element: WindowSpecification=None, timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
        """双击控件, 该方法会将鼠标移动到对应控件位置

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            element_title (str, optional): 控件标题. Defaults to None.
            element_auto_id (str, optional): 控件auto id. Defaults to None.
            element (WindowSpecification, optional): 控件对象. Defaults to None.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        """
        if element == None:
            if element_title:
                element = self.app[window_title].window(title=element_title)
            elif element_auto_id:
                element = self.app[window_title].window(auto_id=element_auto_id)
            element.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        element.double_click_input()
        
    def send_text(self, window_title: str=None, element_title: str=None, element_auto_id: str=None, 
              element: WindowSpecification=None, value: int|str|any="", timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
        """发送文本

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            element_title (str, optional): 控件标题. Defaults to None.
            element_auto_id (str, optional): 控件auto id. Defaults to None.
            element (WindowSpecification, optional): 控件对象. Defaults to None.
            value (int | str | any, optional): 文本. Defaults to "".
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        """
        if element == None:
            if element_title:
                element = self.app[window_title].window(title=element_title)
            elif element_auto_id:
                element = self.app[window_title].window(auto_id=element_auto_id)
            element.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        element.set_text(value)
        
    def type_keys(self, window_title: str=None, element_title: str=None, element_auto_id: str=None, 
              element: WindowSpecification=None, keys: str="", timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
        """发送按键

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            element_title (str, optional): 控件标题. Defaults to None.
            element_auto_id (str, optional): 控件auto id. Defaults to None.
            element (WindowSpecification, optional): 控件对象. Defaults to None.
            keys (str, optional): 按键代号. Defaults to "".
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        """
        if element == None:
            if element_title:
                element = self.app[window_title].window(title=element_title)
            elif element_auto_id:
                element = self.app[window_title].window(auto_id=element_auto_id)
            element.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        element.type_keys(keys)
        
    def select_option(self, window_title: str=None, element_title: str=None, element_auto_id: str=None, 
              element: WindowSpecification=None, option_value: str="", timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
        """选择下拉列表中的选项

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            element_title (str, optional): 控件标题. Defaults to None.
            element_auto_id (str, optional): 控件auto id. Defaults to None.
            element (WindowSpecification, optional): 控件对象. Defaults to None.
            option_value (str, optional): 选项. Defaults to "".
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        """
        if element == None:
            if element_title:
                element = self.app[window_title].window(title=element_title)
            elif element_auto_id:
                element = self.app[window_title].window(auto_id=element_auto_id)
            element.wait(wait_for=wait_for, timeout=timeout, retry_interval=retry_interval)
        element.select(option_value)
        
    def mouse_click(self, coords: tuple=None):
        """使用鼠标点击

        Args:
            coords (tuple, optional): 坐标, 会将鼠标移动到该坐标进行操作, 如果为None则会在当前鼠标位置进行操作. Defaults to None.
        """
        mouse.click(coords=coords)
        
    def mouse_double_click(self, coords: tuple=None):
        """使用鼠标双击

        Args:
            coords (tuple, optional): 坐标, 会将鼠标移动到该坐标进行操作, 如果为None则会在当前鼠标位置进行操作. Defaults to None.
        """
        mouse.double_click(coords=coords)
        
    def mouse_right_click(self, coords: tuple=None):
        """使用鼠标右击

        Args:
            coords (tuple, optional): 坐标, 会将鼠标移动到该坐标进行操作, 如果为None则会在当前鼠标位置进行操作. Defaults to None.
        """
        mouse.right_click(coords=coords)
        
    def mouse_press(self, coords: tuple=None):
        """使用鼠标长按, 注意该方法会让鼠标一直按下去

        Args:
            coords (tuple, optional): 坐标, 会将鼠标移动到该坐标进行操作, 如果为None则会在当前鼠标位置进行操作. Defaults to None.
        """
        mouse.press(coords=coords)
        
    def mouse_release(self, coords: tuple=None):
        """释放鼠标, 一般与press结合

        Args:
            coords (tuple, optional): 坐标, 会将鼠标移动到该坐标进行操作, 如果为None则会在当前鼠标位置进行操作. Defaults to None.
        """
        mouse.release(coords=coords)
        
    def mouse_scroll(self, coords: tuple=None, wheel_dist: int=1):
        """鼠标滚动

        Args:
            coords (tuple, optional): 坐标, 会将鼠标移动到该坐标进行操作, 如果为None则会在当前鼠标位置进行操作. Defaults to None.
            wheel_dist (int, optional): 滚轮滚动的量或距离, 以滚轮“点击”或“刻度”为单位. Defaults to 1.
        """
        mouse.scroll(coords=coords, wheel_dist=wheel_dist)
        
    def keybord_send_keys(self, keys: str):
        """模拟键盘按键

        Args:
            keys (str): 按键代号
        """
        keyboard.SendKeys(keys)