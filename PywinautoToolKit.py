"""windows工具类集合
\n若使用该工具类, 请使用如下命令安装第三方库:
\npip install pywinauto
\npip install pynput
\npip install pyautogui
"""
import win32api, win32con
from pynput.mouse import Button, Controller as MouseController
from pynput.keyboard import Key, Controller as KeyboardController
from pywinauto import mouse, keyboard
from pywinauto.application import Application, WindowSpecification
import pyautogui as pg


class PynputKeys:
    orighin_key_object = Key
    ENTER = Key.enter
    SHIFT = Key.shift
    CTRL = Key.ctrl
    ALT = Key.alt
    SPACE = Key.space
    BACKSPACE = Key.backspace
    CAPSLOCK = Key.caps_lock
    DELETE = Key.delete
    DOWN_ARROW = Key.down
    UP_ARROW = Key.up
    LEFT_ARROW = Key.left
    RIGHT_ARROW = Key.right
    END = Key.end
    ESC = Key.esc
    HOME = Key.home
    INSERT = Key.insert
    NUMLOCK = Key.num_lock
    PAGEDOWN = Key.page_down
    PAGEUP = Key.page_up
    PRINTSCREEN = Key.print_screen
    SCROLLLOCK = Key.scroll_lock
    TAB = Key.tab

class PywinautoKeys:
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

class PyautoguiToolKit:
    """pyautoGUI工具类
    \n若使用该工具类, 请使用如下命令安装第三方库:
    \npip install pyautogui
    """
    KEY_NAMES = [
        "\t",
        "\n",
        "\r",
        " ",
        "!",
        '"',
        "#",
        "$",
        "%",
        "&",
        "'",
        "(",
        ")",
        "*",
        "+",
        ",",
        "-",
        ".",
        "/",
        "0",
        "1",
        "2",
        "3",
        "4",
        "5",
        "6",
        "7",
        "8",
        "9",
        ":",
        ";",
        "<",
        "=",
        ">",
        "?",
        "@",
        "[",
        "\\",
        "]",
        "^",
        "_",
        "`",
        "a",
        "b",
        "c",
        "d",
        "e",
        "f",
        "g",
        "h",
        "i",
        "j",
        "k",
        "l",
        "m",
        "n",
        "o",
        "p",
        "q",
        "r",
        "s",
        "t",
        "u",
        "v",
        "w",
        "x",
        "y",
        "z",
        "{",
        "|",
        "}",
        "~",
        "accept",
        "add",
        "alt",
        "altleft",
        "altright",
        "apps",
        "backspace",
        "browserback",
        "browserfavorites",
        "browserforward",
        "browserhome",
        "browserrefresh",
        "browsersearch",
        "browserstop",
        "capslock",
        "clear",
        "convert",
        "ctrl",
        "ctrlleft",
        "ctrlright",
        "decimal",
        "del",
        "delete",
        "divide",
        "down",
        "end",
        "enter",
        "esc",
        "escape",
        "execute",
        "f1",
        "f10",
        "f11",
        "f12",
        "f13",
        "f14",
        "f15",
        "f16",
        "f17",
        "f18",
        "f19",
        "f2",
        "f20",
        "f21",
        "f22",
        "f23",
        "f24",
        "f3",
        "f4",
        "f5",
        "f6",
        "f7",
        "f8",
        "f9",
        "final",
        "fn",
        "hanguel",
        "hangul",
        "hanja",
        "help",
        "home",
        "insert",
        "junja",
        "kana",
        "kanji",
        "launchapp1",
        "launchapp2",
        "launchmail",
        "launchmediaselect",
        "left",
        "modechange",
        "multiply",
        "nexttrack",
        "nonconvert",
        "num0",
        "num1",
        "num2",
        "num3",
        "num4",
        "num5",
        "num6",
        "num7",
        "num8",
        "num9",
        "numlock",
        "pagedown",
        "pageup",
        "pause",
        "pgdn",
        "pgup",
        "playpause",
        "prevtrack",
        "print",
        "printscreen",
        "prntscrn",
        "prtsc",
        "prtscr",
        "return",
        "right",
        "scrolllock",
        "select",
        "separator",
        "shift",
        "shiftleft",
        "shiftright",
        "sleep",
        "space",
        "stop",
        "subtract",
        "tab",
        "up",
        "volumedown",
        "volumemute",
        "volumeup",
        "win",
        "winleft",
        "winright",
        "yen",
        "command",
        "option",
        "optionleft",
        "optionright",
    ]
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        pass
    
    def get_screen_size(self) -> tuple:
        """获取当前屏幕大小

        Returns:
            tuple: (width, height)
        """
        width, height = pg.size()
        return (width, height)
    
    def get_mouse_position(self) -> tuple:
        """获取当前鼠标位置

        Returns:
            tuple: (x, y)
        """
        x, y = pg.position()
        return (x, y)
    
    def mouse_press(self, x: int|float=None, y: int|float=None, button: str="PRIMARY", duration: float=0, **args):
        """鼠标长按

        Args:
            x (int | float): x轴, 对应屏幕的位置. 为None则为鼠标当前位置. Defaults to None.
            y (int | float): y轴, 对应屏幕的位置. 为None则为鼠标当前位置. Defaults to None.
            button (str, optional): 在鼠标点击时, 使用鼠标上面的哪个按钮, 可选为{LEFT, MIDDLE, RIGHT, PRIMARY, SECONDARY}. Defaults to "PRIMARY".
            duration (float, optional): 指定移动鼠标光标到指定坐标所需的时间。如果时间为0, 则鼠标光标会立刻移动到对应位置. Defaults to 0.
        """
        pg.mouseDown(x, y, button, duration, **args)
        
    def mouse_release(self, x: int|float=None, y: int|float=None, button: str="PRIMARY", duration: float=0, **args):
        """释放鼠标

        Args:
            x (int | float): x轴, 对应屏幕的位置. 为None则为鼠标当前位置. Defaults to None.
            y (int | float): y轴, 对应屏幕的位置. 为None则为鼠标当前位置. Defaults to None.
            button (str, optional): 释放鼠标上面的哪个按钮, 可选为{LEFT, MIDDLE, RIGHT, PRIMARY, SECONDARY}. Defaults to "PRIMARY".
            duration (float, optional): 指定移动鼠标光标到指定坐标所需的时间。如果时间为0, 则鼠标光标会立刻移动到对应位置. Defaults to 0.
        """
        pg.mouseUp(x, y, button, duration, **args)
    
    def move_to(self, x: int|float, y: int|float, duration: float=0, **args):
        """将鼠标移动到某一个位置

        Args:
            x (int | float): x轴, 对应屏幕的位置
            y (int | float): y轴, 对应屏幕的位置
            duration (float, optional): 指定移动鼠标光标到指定坐标所需的时间。如果时间为0, 则鼠标光标会立刻移动到对应位置. Defaults to 0.
        """
        pg.moveTo(x, y, duration, **args)
    
    def click(self, x: int|float=None, y: int|float=None, click_times: int=1, interval:int=0, button: str="PRIMARY", **args):
        """鼠标点击

        Args:
            x (int | float): x轴, 对应屏幕的位置. 为None则为鼠标当前位置. Defaults to None.
            y (int | float): y轴, 对应屏幕的位置. 为None则为鼠标当前位置. Defaults to None.
            click_times (int, optional): 点击的次数. Defaults to 1.
            interval (int, optional): 每一次点击之间间隔的时间, 单位为秒. Defaults to 0.
            button (str, optional): 在鼠标点击时, 使用鼠标上面的哪个按钮, 可选为{LEFT, MIDDLE, RIGHT, PRIMARY, SECONDARY}. Defaults to "PRIMARY".
        """
        pg.click(x, y, click_times, interval, button, **args)
    
    def drag_to(self, x: int|float|tuple, y: int|float, duration: float=0, button: str="PRIMARY", **args):
        """鼠标拖拽

        Args:
            x (int | float | tuple): x轴, 对应屏幕的位置。也可以是向左(对于负值)或向右(对于正值)移动鼠标光标的位置。如果是一个元组, 则用于x和y坐标
            y (int | float): y轴, 对应屏幕的位置。也可以是向上（对于负值）或向下（对于正值）移动鼠标光标的位置
            duration (float, optional): 指定移动鼠标光标到指定坐标所需的时间。如果时间为0, 则鼠标光标会立刻移动到对应位置. Defaults to 0.
            button (str, optional): 在鼠标点击时, 使用鼠标上面的哪个按钮, 可选为{LEFT, MIDDLE, RIGHT, PRIMARY, SECONDARY}. Defaults to "PRIMARY".
        """
        pg.dragTo(x, y, duration, button=button, **args)
    
    def scroll(self, scrolling_times: int, **args):
        """操作鼠标滚轮

        Args:
            scrolling_times (int): 滚动多少次, 正数向上, 负数向下
        """
        pg.scroll(scrolling_times, **args)
    
    def type_keys(self, key: str, press_times: int=1, interval: int=0, **args):
        """按下键盘上的按键(不支持组合按键)

        Args:
            key (str): 按键代码, 详情请查看类变量KEY_NAMES
            press_times (int, optional): 按下多少次. Defaults to 1.
            interval (int, optional): 每一次按下按键的间隔时间, 单位为秒. Defaults to 0.
        """
        pg.press(key, press_times, interval, **args)
    
    def send_text(self, text: str|list[str], interval: int=0, **args):
        """发送一连串的文本(不支持组合按键)

        Args:
            text (str | list[str]): 文本或者文本序列
            interval (int, optional): 每一次按下按键的间隔时间, 单位为秒. Defaults to 0.
        """
        pg.typewrite(text, interval, **args)
        
    def hot_key(self, *keys, interval: float=0, **args):
        """按下组合键

        Args:
            keys (str): 组合键代码, 详情请查看类变量KEY_NAMES
            interval (int, optional): 每一次按下按键的间隔时间, 单位为秒. Defaults to 0.
            
        Example:
            >>> hot_key("ctrl", "shift", "a")
            >>> hot_key("ctrl", "a", interval=1)
        """
        pg.hotkey(*keys, interval=interval, **args)
    
    def screenshot(self, save_image_path: str, region: tuple=None):
        """屏幕截图

        Args:
            save_image_path (str): 保存截图路径
            region (tuple): 截图区域框, 输入为一个四元组, 格式为(x1, y1, x2, y2), (x1, y1)代表的是区域框的左上角, (x2, y2)代表的是区域框的右下角. Defaults to None.
        """
        img = pg.screenshot()
        if region:
            img = img.crop(region)
        img.save(save_image_path)
    
    def locate_image_on_screen(self, image_path: str, grayscale: bool=False, region: tuple=None, confidence: float=0.8, **args) -> tuple:
        """通过图像识别, 识别屏幕上对应图片的位置

        Args:
            image_path (str): 图像路径
            grayscale (bool, optional): 是否使用灰度模式进行匹配, 如果设置为True, 则以灰度模式进行图像匹配, 这样可以提高匹配速度, 但可能稍微降低准确性. Defaults to False.
            region (tuple, optional): 指定一个矩形区域，在该区域内搜索图像, 输入为一个四元组, 格式为(x1, y1, x2, y2), (x1, y1)代表的是区域框的左上角, (x2, y2)代表的是区域框的右下角. Defaults to None.
            confidence (float, optional): 指定匹配时所需的置信度水平。取值范围是 0 到 1, 其中 1 表示完全匹配. Defaults to 0.8.

        Returns:
            tuple: 对应位置的中心点
            
        Raises:
            pyautogui.ImageNotFoundException: 无法在屏幕找到对应图片位置
        """
        x, y = pg.locateCenterOnScreen(image_path, grayscale=grayscale, region=region, confidence=confidence, **args)
        return (x, y)
    
    def click_by_image(self, image_path: str, grayscale: bool=False, region: tuple=None, confidence: float=0.8, 
                       click_times: int=1, interval:int=0, button: str="PRIMARY", **args):
        """通过图像识别点击对应位置

        Args:
            image_path (str): 图像路径
            grayscale (bool, optional): 是否使用灰度模式进行匹配, 如果设置为True, 则以灰度模式进行图像匹配, 这样可以提高匹配速度, 但可能稍微降低准确性. Defaults to False.
            region (tuple, optional): 指定一个矩形区域，在该区域内搜索图像, 输入为一个四元组, 格式为(x1, y1, x2, y2), (x1, y1)代表的是区域框的左上角, (x2, y2)代表的是区域框的右下角. Defaults to None.
            confidence (float, optional): 指定匹配时所需的置信度水平。取值范围是 0 到 1, 其中 1 表示完全匹配. Defaults to 0.8.
            click_times (int, optional): 点击的次数. Defaults to 1.
            interval (int, optional): 每一次点击之间间隔的时间, 单位为秒. Defaults to 0.
            button (str, optional): 在鼠标点击时, 使用鼠标上面的哪个按钮, 可选为{LEFT, MIDDLE, RIGHT, PRIMARY, SECONDARY}. Defaults to "PRIMARY".
        """
        x, y = pg.locateCenterOnScreen(image_path, grayscale=grayscale, region=region, confidence=confidence, **args)
        pg.click(x, y, click_times, interval, button, **args)

class PynputToolKit:
    """pynput工具类, 用于操作和监听鼠标键盘
    \n若使用该工具类, 请使用如下命令安装第三方库:
    \npip install pynput
    """
    _mouse_button_map = {"LEFT": Button.left, "RIGHT": Button.right, "MIDDLE": Button.middle}
    
    def __init__(self):
        self.mouse_controller = MouseController()
        self.keyboard_controller = KeyboardController()
    
    def __enter__(self):
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        self.mouse_controller = None
        self.keyboard_controller = None
    
    def click(self, button: str='LEFT', count: int=1):
        """使用鼠标点击

        Args:
            button (str, optional): 鼠标按键, 可以是{LEFT, MIDDLE, RIGHT}. Defaults to 'LEFT'.
            count (int, optional): 点击次数. Defaults to 1.
        """
        self.mouse_controller.click(button=self._mouse_button_map[button], count=count)
        
    def mouse_press(self, button: str = 'LEFT'):
        """鼠标长按

        Args:
            button (str, optional): 鼠标按键, 可以是{LEFT, MIDDLE, RIGHT}. Defaults to 'LEFT'.
        """
        self.mouse_controller.press(button=self._mouse_button_map[button])
        
    def mouse_release(self, button: str = 'LEFT'):
        """释放鼠标

        Args:
            button (str, optional): 鼠标按键, 可以是{LEFT, MIDDLE, RIGHT}. Defaults to 'LEFT'.
        """
        self.mouse_controller.release(button=self._mouse_button_map[button])
        
    def mouse_scroll(self, scroll_x: int=0, scroll_y: int=1):
        """鼠标滚动

        Args:
            scroll_x (int, optional): 设置水平方向的滑动单位, 数字>0向右滑动, 数字<0向左滑动, 数字=0则不滑动. Defaults to 0.
            scroll_y (int, optional): 设置垂直方向的滑动单位, 数字>0向上滑动, 数字<0向下滑动, 数字=0则不滑动. Defaults to 1.
        """
        self.mouse_controller.scroll(scroll_x, scroll_y)
    
    def type_keys(self, key: str):
        """输入按键(不支持组合按键)

        Args:
            key (str): 按键代号, 按键请参考或使用PynputKeys类
        """
        self.keyboard_controller.tap(key)
        
    def press_keys(self, key: str):
        """按住按键(单次调用不支持组合按键)

        Args:
            key (str): 按键代号, 按键请参考或使用PynputKeys类
            
        Examples:
            >>> # 按住某个按键
            >>> press_keys("a")
            >>> # 组合键ctrl+a
            >>> press_keys(PynputKeys.CTRL)
            >>> press_keys("a")
        """
        self.keyboard_controller.press(key)

    def release_keys(self, key: str):
        """释放按键

        Args:
            key (str): 按键代号, 按键请参考或使用PynputKeys类
        """
        self.keyboard_controller.release(key)
    
    def send_text(self, text: str):
        """发送一连串的文本(不支持组合按键)

        Args:
            text (str): 文本
        """
        self.keyboard_controller.type(text)
        
class PywinautoToolKit:
    """pywinauto工具类, 适用于windows的app, 控件和窗口在该处的概念都为windows
    \n若使用该工具类, 请使用如下命令安装第三方库:
    \npip install pywinauto
    \npip install pynput
    """
    app = None
    
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
    
    def get_screen_size(self) -> tuple:
        """获取当前屏幕大小

        Returns:
            tuple: (width, height)
        """
        return win32api.GetSystemMetrics(win32con.SM_CXSCREEN), win32api.GetSystemMetrics(win32con.SM_CYSCREEN)
    
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
              element: WindowSpecification=None, value: int|str="", timeout: int=60, wait_for: str="enabled", retry_interval: float=0.5):
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
        """发送按键(支持组合按键)

        Args:
            window_title (str, optional): 窗口标题. Defaults to None.
            element_title (str, optional): 控件标题. Defaults to None.
            element_auto_id (str, optional): 控件auto id. Defaults to None.
            element (WindowSpecification, optional): 控件对象. Defaults to None.
            keys (str, optional): 按键代号, 按键请参考或使用PywinautoKeys类. Defaults to "".
            timeout (int, optional): 等待超时时间. Defaults to 60.
            wait_for (str, optional): 指定了等待的条件或状态, 通常这些值表示窗口的可见性、激活状态、存在性, 类型有(exists(等待窗口实际存在)|visible(等待窗口实际存在)|active(等待窗口激活)|enabled(等待窗口启用, 可接受用户输入)|ready(等待窗口准备好进行交互, 通常意味着它的所有子控件都已加载并可用)). Defaults to "enabled".
            retry_interval (float, optional): 尝试检查wait_for条件之间应该等待的时间间隔(以秒为单位). Defaults to 0.5.
        
        Examples:
            >>> # 按下a
            >>> type_keys(keys="a")
            >>> # 组合键 ctrl+a
            >>> type_keys(keys="f{PywinautoKeys.CTRL}a")
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
    
    def mouse_click(self, coords: tuple, button: str='left'):
        """使用鼠标点击

        Args:
            coords (tuple, optional): 坐标, 会将鼠标移动到该坐标进行操作
            button (str, optional): 鼠标按键, 可以是'left', 'right', 'middle'. Defaults to 'left'.
        """
        mouse.click(button=button, coords=coords)
        
    def mouse_double_click(self, coords: tuple, button: str='left'):
        """使用鼠标双击

        Args:
            coords (tuple, optional): 坐标, 会将鼠标移动到该坐标进行操作
            button (str, optional): 鼠标按键, 可以是'left', 'right', 'middle'. Defaults to 'left'.
        """
        mouse.double_click(button=button, coords=coords)
        
    def mouse_right_click(self, coords: tuple):
        """使用鼠标右击

        Args:
            coords (tuple, optional): 坐标, 会将鼠标移动到该坐标进行操作
        """
        mouse.right_click(coords=coords)
        
    def mouse_press(self, coords: tuple, button: str='left'):
        """鼠标长按

        Args:
            coords (tuple, optional): 坐标, 会将鼠标移动到该坐标进行操作
            button (str, optional): 鼠标按键, 可以是'left', 'right', 'middle'. Defaults to 'left'.
        """
        mouse.press(button=button, coords=coords)
        
    def mouse_release(self, coords: tuple, button: str='left'):
        """释放鼠标

        Args:
            coords (tuple, optional): 坐标, 会将鼠标移动到该坐标进行操作
            button (str, optional): 鼠标按键, 可以是'left', 'right', 'middle'. Defaults to 'left'.
        """
        mouse.release(button=button, coords=coords)
        
    def mouse_scroll(self, coords: tuple, wheel: int=1):
        """鼠标滚动

        Args:
            coords (tuple, optional): 坐标, 会将鼠标移动到该坐标进行操作
            wheel (int, optional): 向上滑动(数字>0)或向下滑动(数字<0). Defaults to 1.
        """
        mouse.scroll(coords=coords, wheel_dist=wheel)
        
    def keybord_send_keys(self, keys: str):
        """模拟键盘按键(支持组合按键)

        Args:
            keys (str): 按键代号, 按键请参考或使用PywinautoKeys类
            
        Examples:
            >>> # 按下a
            >>> keybord_send_keys(keys="a")
            >>> # 组合键 ctrl+a
            >>> keybord_send_keys(keys=f"{PywinautoKeys.CTRL}a")
        """
        keyboard.SendKeys(keys)
