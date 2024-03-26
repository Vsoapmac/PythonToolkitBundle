import uiautomator2 as u2
from airtest.core.api import *
from airtest.core.android.android import Android


class AirtestAdapter:
    d = None
    UUID = None
    
    def globel_device(self, device: Android):
        """全局化device变量

        Args:
            device (Android): device变量
        """
        self.d = device
    
    def connect_device(self, UUID: str) -> Android:
        """连接设备

        Args:
            UUID (str): 设备UUID

        Returns:
            Android: 设备抽象类
        """
        self.UUID = UUID
        return init_device(uuid=UUID)

    def get_window_size(self) -> tuple:
        """获取窗口大小

        Returns:
            tuple: 窗口大小, 第一个为weight, 第二个为hight
        """
        return self.d.get_current_resolution()
    
    def install_app(self, app_file_path: str):
        """安装app应用

        Args:
            app_file_path (str): app文件路径
        """
        self.d.install_app(app_file_path)

    def start_app(self, app_package: str):
        """打开app

        Args:
            app_package (str): app包名
        """
        self.d.start_app(app_package)
        
    def stop_app(self, app_package: str):
        """停止app

        Args:
            app_package (str): app包名
        """
        self.d.stop_app(app_package)
    
    def Template(self, img_file_path: str, threshold: float=0.7, target_pos: int=5, 
                 record_pos: tuple[float]=None, resolution: tuple[int]=()) -> Template:
        """图片Template抽象类

        Args:
            img_file_path (str): 识别图片路径
            threshold (float, optional): 识别阈值, 越大识别时越严肃, 范围是[0, 1]. Defaults to 0.7.
            target_pos (int, optional): 图片点击位置, 123为图片的上面, 46为图片的两边, 5即图片的中心点, 789为图片的下面. Defaults to 5.
            record_pos (tuple[float], optional): 图片坐标对应手机屏幕中心点的偏移值相对于手机分辨率的百分比, 匹配时会优先匹配这附近的画面. Defaults to None.
            resolution (tuple[int], optional): 手机分辨率。当脚本执行时的手机不是录制时的手机时, Airtest会对屏幕截图按照分辨率进行缩放. Defaults to ().
            
        Returns:
            Template: 图片Template抽象类
        """
        return Template(img_file_path, threshold, target_pos, record_pos, resolution)
    
    def wait(self, template: Template, timeout: int=60, interval: float=0.5):
        """等待元素出现

        Args:
            template (Template): 图片Template抽象类
            timeout (int, optional): 等待超时时间. Defaults to 60.
            interval (float, optional): 识别间隔, 每隔几秒识别一次. Defaults to 0.5.
        """
        wait(template, timeout, interval)
        
    def get_element_position(self, template: Template, timeout: int=60, interval: float=0.5) -> tuple:
        """获取元素坐标位置

        Args:
            template (Template): 图片Template抽象类
            timeout (int, optional): 等待超时时间. Defaults to 60.
            interval (float, optional): 识别间隔, 每隔几秒识别一次. Defaults to 0.5.

        Returns:
            tuple: 元素坐标位置
        """
        return wait(template, timeout, interval)
        
    def exists(self, template: Template, timeout: int=3, interval: float=0.5) -> bool:
        """判断元素是否存在

        Args:
            template (Template): 图片Template抽象类
            timeout (int, optional): 等待超时时间. Defaults to 3.
            interval (float, optional): 识别间隔, 每隔几秒识别一次. Defaults to 0.5.

        Returns:
            bool: 判断结果
        """
        try:
            wait(template, timeout, interval)
            return True
        except:
            return False
    
    def touch(self, template: Template, timeout: int=60, interval: float=0.5):
        """点击元素

        Args:
            template (Template): 图片Template抽象类
            timeout (int, optional): 等待超时时间. Defaults to 60.
            interval (float, optional): 识别间隔, 每隔几秒识别一次. Defaults to 0.5.
        """
        wait(template, timeout, interval)
        touch(template)

    def touch_pos(self, x: int|float, y: int|float):
        """根据坐标点击元素

        Args:
            x (int | float): x
            y (int | float): y
        """
        touch((x, y))
        
    def long_touch(self, template: Template, duration: float=0.5, timeout: int=60, interval: float=0.5):
        """长按元素

        Args:
            template (Template): 图片Template抽象类
            duration (float, optional): 长按时间. Defaults to 0.5.
            timeout (int, optional): 等待超时时间. Defaults to 60.
            interval (float, optional): 识别间隔, 每隔几秒识别一次. Defaults to 0.5.
        """
        wait(template, timeout, interval)
        touch(template, duration=duration)
    
    def send_text(self, text: str, enter: bool=False, search: bool=True):
        """发送文本, 通常与touch一起用

        Args:
            text (str): 文本
            enter (bool, optional): 输入文本后是否点击回车键. Defaults to False.
            search (bool, optional): 输入文本后是否点击搜索键. Defaults to True.
        """
        text(text, enter=enter, search=search)
        
    def press(self, key: int|str):
        """模拟按键, 一般用于按主页键等

        Args:
            key (int | str): 按键名称或代号
        """
        keyevent(key)
    
    def swipe(self, direction: str="up", scale: float=0.5, position_box: tuple[int]=None, template_box: tuple[Template]=None):
        """滑动

        Args:
            direction (str, optional): 方向, 选项分别为: up|down|left|right. Defaults to "up".
            scale (float, optional): 滑动距离. Defaults to 0.5.
            position_box (tuple[int], optional): 滑动坐标, 第一、二个元素为开始滑动的坐标, 第三、四个元素为结束滑动的坐标, 若为None则使用规定方向滑动. Defaults to None.
            template_box (tuple[Template], optional): 图片template滑动, 第一个元素为开始滑动的图片, 第二个元素为结束滑动的图片, 若为None则使用规定方向滑动. Defaults to None.
        """
        if position_box:
            swipe((position_box[0], position_box[1]), (position_box[2], position_box[3]))
        elif template_box:
            swipe(template_box[0], template_box[1])
        else:
            w, h = self.d.get_current_resolution()
            if direction == "up":
                swipe([0.5*w, 0], vector=[0, scale])
            elif direction == "down":
                swipe([0.5*w, h], vector=[0, scale*-1])
            elif direction == "left":
                swipe([w, 0.5*h], vector=[scale*-1, 0])
            elif direction == "right":
                swipe([0, 0.5*h], vector=[scale, 0])

    def pinch(self, in_or_out: str="in", center: tuple[int]=None, percent: float=0.5):
        """放大/缩小手势操作

        Args:
            in_or_out (str, optional): 操作类型, 可输入 in|out, 意思是缩小、放大. Defaults to "in".
            center (tuple[int], optional): 操作的中心点, 为None则表示为屏幕中心. Defaults to None.
            percent (float, optional): 缩放比例. Defaults to 0.5.
        """
        pinch(in_or_out, center, percent)
    
    def screenshot(self, file_path: str, quality: int=None, max_size: int=None):
        """截图

        Args:
            file_path (str): 截图后保存路径
            quality (int, optional): 图像质量, 范围为[1, 99]. Defaults to None.
            max_size (int, optional): 最大图像尺寸. Defaults to None.
        """
        snapshot(file_path, quality=quality, max_size=max_size)
    
    def shell(self, command: str) -> str:
        """执行adb shell命令

        Args:
            command (str): 命令

        Returns:
            str: 执行结果
        """
        return self.d.shell(command)
    
    def enable_wifi(self) -> str:
        """开启wifi

        Returns:
            str: 执行结果
        """
        return self.d.shell("svc wifi enable")
    
    def disable_wifi(self) -> str:
        """关闭wifi

        Returns:
            str: 执行结果
        """
        return self.d.shell("svc wifi disable")
    
    def enable_data(self) -> str:
        """开启数据流量

        Returns:
            str: 执行结果
        """
        return self.d.shell("svc data enable")
    
    def disable_data(self) -> str:
        """关闭数据流量

        Returns:
            str: 执行结果
        """
        return self.d.shell("svc data disable")
    
    def send_remote_file(self, from_file_path: str, to_file_path: str):
        """发送文件至手机

        Args:
            from_file_path (str): 文件路径
            to_file_path (str): 发送目标位置
        """
        os.system(f"adb -s {self.UUID} push {from_file_path} {to_file_path}")
    
    def get_remote_file(self, from_file_path: str, to_file_path: str):
        """获取手机的文件, 并保存在本地

        Args:
            from_file_path (str): 文件路径
            to_file_path (str): 发送目标位置
        """
        os.system(f"adb -s {self.UUID} pull {from_file_path} {to_file_path}")


class Ui2Adapter:
    d = None
    UUID = None
    
    def globel_device(self, device: u2.Device):
        """全局化device变量

        Args:
            device (u2.Device): device变量
        """
        self.d = device
    
    def connect_device(self, UUID: str) -> u2.Device:
        """连接设备

        Args:
            UUID (str): 设备UUID

        Returns:
            u2.Device: 设备抽象类
        """
        self.UUID = UUID
        return u2.connect(UUID)

    def get_window_size(self) -> tuple:
        """获取窗口大小

        Returns:
            tuple: 窗口大小, 第一个为weight, 第二个为hight
        """
        return self.d.window_size()
    
    def set_fastinput_ime(self, enable: bool=True):
        """切换成ui2的输入法

        Args:
            enable (bool, optional): 是否开启, 当传入False时会使用系统默认输入法. Defaults to True.
        """
        self.d.set_fastinput_ime(enable=enable)
    
    def check_current_ime(self) -> tuple:
        """查看当前输入法

        Returns:
            tuple: 当前输入法信息
        """
        return self.d.current_ime()
    
    def install_app(self, app_file_path: str):
        """安装app

        Args:
            app_file_path (str): app文件路径
        """
        self.d.app_install(app_file_path)

    def start_app(self, app_package: str):
        """打开app

        Args:
            app_package (str): app包名
        """
        self.d.app_start(app_package)
        
    def stop_app(self, app_package: str):
        """停止app

        Args:
            app_package (str): app包名
        """
        self.d.app_stop(app_package)

    def find_element(self, timeout: int=60, **UiSelector) -> u2.UiObject:
        """寻找元素

        Args:
            timeout (int, optional): 超时时间. Defaults to 60.

        Returns:
            u2.UiObject: 元素
        """
        self.d(**UiSelector).wait(timeout=timeout)
        return self.d(**UiSelector)
    
    def get_element_info(self, timeout: int=60, **UiSelector) -> dict:
        """获取元素信息

        Args:
            timeout (int, optional): 超时时间. Defaults to 60.

        Returns:
            dict: 元素信息
        """
        self.d(**UiSelector).wait(timeout=timeout)
        return self.d(**UiSelector).info
    
    def get_element_position(self, timeout: int=60, **UiSelector) -> tuple:
        """获取元素坐标位置

        Args:
            timeout (int, optional): 超时时间. Defaults to 60.

        Returns:
            tuple: 元素坐标位置
        """
        return self.d(**UiSelector).wait(timeout=timeout)
    
    def wait(self, timeout: int=60, **UiSelector):
        """等待元素出现

        Args:
            timeout (int, optional): 超时时间. Defaults to 60.
        """
        self.d(**UiSelector).wait(timeout=timeout)
        
    def wait_gone(self, timeout: int=60, **UiSelector):
        """等待元素消失

        Args:
            timeout (int, optional): 超时时间. Defaults to 60.
        """
        self.d(**UiSelector).wait(False, timeout)
    
    def exists(self, timeout: int=3, **UiSelector) -> bool:
        """判断元素是否存在

        Args:
            timeout (int, optional): 超时时间. Defaults to 3.

        Returns:
            bool: 是否存在
        """
        return False if self.d(**UiSelector).exists(timeout) == None else True
    
    def click(self, timeout: int=60, **UiSelector):
        """点击

        Args:
            timeout (int, optional): 超时时间. Defaults to 60.
        """
        self.d(**UiSelector).click(timeout)
    
    def click_pos(self, x: int|float, y: int|float):
        """坐标点击

        Args:
            x (int | float): x
            y (int | float): y
        """
        self.d.click(x, y)
    
    def long_click(self, duration: float=0.5, timeout: int=60, **UiSelector):
        """长按

        Args:
            duration (float, optional): 按住多少秒. Defaults to 0.5.
            timeout (int, optional): 等待超时时间. Defaults to 60.
        """
        self.d(**UiSelector).long_click(duration, timeout)
    
    def get_text(self, **UiSelector) -> str:
        """获取元素的文本内容

        Returns:
            str: 文本内容
        """
        return self.d(**UiSelector).get_text()
    
    def send_text(self, text: str, **UiSelector):
        """发送文本

        Args:
            text (str): 文本
        """
        self.d(**UiSelector).set_text(text)
    
    def send_keys(self, text: str, clear: bool=False, **UiSelector):
        """模拟输入, 通常与click连用, 点击输入输入框后输入文本

        Args:
            text (str): 文本
            clear (bool, optional): 在输入文本前是否清楚文本框. Defaults to False.
        """
        self.d.send_keys(text, clear, **UiSelector)
    
    def press(self, key: int|str):
        """模拟按键, 比如说电源键等

        Args:
            key (int | str): 按键代码或名称
        """
        self.d.press(key)
    
    def swipe(self, direction: str="up", scale: float=0.5, position_box: tuple[float]=None):
        """滑动

        Args:
            direction (str, optional): 方向, 选项分别为: up|down|left|right. Defaults to "up".
            scale (float, optional): 滑动距离. Defaults to 0.5.
            position_box (tuple[float], optional): 滑动坐标, 第一、二个元素为开始滑动的坐标, 第三、四个元素为结束滑动的坐标, 若为None则使用规定方向滑动. Defaults to None.
        """
        if position_box:
            self.d.swipe(position_box[0], position_box[1], position_box[2], position_box[3])
        else:
            self.d.swipe_ext(direction, scale)
        
    def drag(self, sx: float, sy: float, ex: float, ey: float, duration: float=0.5):
        """拖拽

        Args:
            sx (float): 开始坐标x
            sy (float): 开始坐标y
            ex (float): 结束坐标x
            ey (float): 结束坐标y
            duration (float, optional): 滑动距离. Defaults to 0.5.
        """
        self.d.drag(sx, sy, ex, ey, duration=duration)
    
    def screenshot(self, file_path: str):
        """截图

        Args:
            file_path (str): 保存图片路径
        """
        self.d.screenshot(file_path)
        
    def start_record(self, file_path: str):
        """开始录屏, 若使用请执行如下命令安装如下库:
        \npip install -U "uiautomator2[image]" -i https://pypi.doubanio.com/simple

        Args:
            file_path (str): 录制视频保存路径
        """
        self.d.screenrecord(file_path)
    
    def stop_record(self):
        """停止录屏"""
        self.d.screenrecord.stop()
    
    def shell(self, command: str|list[str], stream: bool=False, timeout: int=60) -> str:
        """执行adb shell命令, 返回命令执行结果

        Args:
            command (str | list[str]): 命令
            stream (bool, optional): 是否以流式输出模式执行命令. Defaults to False.
            timeout (int, optional): 命令执行的超时时间. Defaults to 60.

        Returns:
            str: 执行结果
        """
        return self.d.shell(command, stream, timeout)
    
    def enable_wifi(self, stream: bool=False, timeout: int=60) -> str:
        """开启wifi

        Args:
            stream (bool, optional): 是否以流式输出模式执行命令. Defaults to False.
            timeout (int, optional): 命令执行的超时时间. Defaults to 60.

        Returns:
            str: 执行结果
        """
        return self.d.shell("svc wifi enable", stream, timeout)
    
    def disable_wifi(self, stream: bool=False, timeout: int=60) -> str:
        """关闭wifi

        Args:
            stream (bool, optional): 是否以流式输出模式执行命令. Defaults to False.
            timeout (int, optional): 命令执行的超时时间. Defaults to 60.

        Returns:
            str: 执行结果
        """
        return self.d.shell("svc wifi disable", stream, timeout)
    
    def enable_data(self, stream: bool=False, timeout: int=60) -> str:
        """开启数据流量

        Args:
            stream (bool, optional): 是否以流式输出模式执行命令. Defaults to False.
            timeout (int, optional): 命令执行的超时时间. Defaults to 60.

        Returns:
            str: 执行结果
        """
        return self.d.shell("svc data enable", stream, timeout)
    
    def disable_data(self, stream: bool=False, timeout: int=60) -> str:
        """关闭数据流量

        Args:
            stream (bool, optional): 是否以流式输出模式执行命令. Defaults to False.
            timeout (int, optional): 命令执行的超时时间. Defaults to 60.

        Returns:
            str: 执行结果
        """
        return self.d.shell("svc data disable", stream, timeout)
    
    def send_remote_file(self, from_file_path: str, to_file_path: str):
        """发送文件至手机

        Args:
            from_file_path (str): 文件路径
            to_file_path (str): 发送目标位置
        """
        os.system(f"adb -s {self.UUID} push {from_file_path} {to_file_path}")
    
    def get_remote_file(self, from_file_path: str, to_file_path: str):
        """获取手机的文件, 并保存在本地

        Args:
            from_file_path (str): 文件路径
            to_file_path (str): 发送目标位置
        """
        os.system(f"adb -s {self.UUID} pull {from_file_path} {to_file_path}")


class AndroidToolKit:
    DEFAULT_ENGINE = "uiautomator2"
    ENGINE_LIST = ["uiautomator2", "airtest"]
    
    def __init__(self, UUID: str, engine: str=None):
        """初始化引擎

        Args:
            UUID (str): 设备的UUID
            engine (str, optional): 引擎类型, 为None则使用默认引擎. Defaults to None.
        """
        if engine is None:
            engine = self.DEFAULT_ENGINE
        if engine == "uiautomator2":
            self.engine = Ui2Adapter()
            self.device = self.engine.connect_device(UUID)
            self.engine.globel_device(device=self.device)
        elif engine == "airtest":
            self.engine = AirtestAdapter()
            self.device = self.engine.connect_device(UUID)
            self.engine.globel_device(self.device)
            