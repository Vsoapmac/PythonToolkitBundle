import uiautomator2 as u2
from airtest.core.api import *
from airtest.core.android.android import Android


class AirtestAdapter:
    d = None
    UUID = None
    
    def globel_device(self, device: Android):
        self.d = device
    
    def connect_device(self, UUID: str) -> Android:
        self.UUID = UUID
        return init_device(uuid=UUID)

    def get_window_size(self) -> tuple:
        return self.d.get_current_resolution()
    
    def install_app(self, app_file_path: str):
        self.d.install_app(app_file_path)

    def start_app(self, app_package: str):
        self.d.start_app(app_package)
        
    def stop_app(self, app_package: str):
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
        wait(template, timeout, interval)
        
    def get_element_position(self, template: Template, timeout: int=60, interval: float=0.5) -> tuple:
        return wait(template, timeout, interval)
        
    def exists(self, template: Template, timeout: int=3, interval: float=0.5) -> bool:
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
        touch((x, y))
        
    def long_touch(self, template: Template, duration: float=0.5, timeout: int=60, interval: float=0.5):
        wait(template, timeout, interval)
        touch(template, duration=duration)
    
    def send_text(self, text: str, enter: bool=False, search: bool=True):
        text(text, enter=enter, search=search)
        
    def press(self, key: int|str):
        keyevent(key)
    
    def screenshot(self, file_path: str, quality: int=None, max_size: int=None):
        snapshot(file_path, quality=quality, max_size=max_size)
    
    def shell(self, command: str) -> str:
        return self.d.shell(command)
    
    def enable_wifi(self) -> str:
        return self.d.shell("svc wifi enable")
    
    def disable_wifi(self) -> str:
        return self.d.shell("svc wifi disable")
    
    def enable_data(self) -> str:
        return self.d.shell("svc data enable")
    
    def disable_data(self) -> str:
        return self.d.shell("svc data disable")
    
    def send_remote_file(self, from_file_path: str, to_file_path: str):
        os.system(f"adb -s {self.UUID} push {from_file_path} {to_file_path}")
    
    def get_remote_file(self, from_file_path: str, to_file_path: str):
        os.system(f"adb -s {self.UUID} pull {from_file_path} {to_file_path}")


class Ui2Adapter:
    d = None
    UUID = None
    
    def globel_device(self, device: u2.Device):
        self.d = device
    
    def connect_device(self, UUID: str) -> u2.Device:
        self.UUID = UUID
        return u2.connect(UUID)

    def get_window_size(self) -> tuple:
        return self.d.window_size()
    
    def set_fastinput_ime(self, enable: bool=True):
        self.d.set_fastinput_ime(enable=enable)
    
    def check_current_ime(self) -> tuple:
        return self.d.current_ime()
    
    def install_app(self, app_file_path: str):
        self.d.app_install(app_file_path)

    def start_app(self, app_package: str):
        self.d.app_start(app_package)
        
    def stop_app(self, app_package: str):
        self.d.app_stop(app_package)

    def find_element(self, timeout: int=60, **UiSelector) -> u2.UiObject:
        self.d(**UiSelector).wait(timeout=timeout)
        return self.d(**UiSelector)
    
    def get_element_info(self, timeout: int=60, **UiSelector) -> dict:
        self.d(**UiSelector).wait(timeout=timeout)
        return self.d(**UiSelector).info
    
    def get_element_position(self, timeout: int=60, **UiSelector) -> tuple:
        return self.d(**UiSelector).wait(timeout=timeout)
    
    def wait(self, timeout: int=60, **UiSelector):
        self.d(**UiSelector).wait(timeout=timeout)
        
    def wait_gone(self, timeout: int=60, **UiSelector):
        self.d(**UiSelector).wait(False, timeout)
    
    def exists(self, timeout: int=3, **UiSelector) -> bool:
        return False if self.d(**UiSelector).exists(timeout) == None else True
    
    def click(self, timeout: int=60, **UiSelector):
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
        return self.d(**UiSelector).get_text()
    
    def send_text(self, text: str, **UiSelector):
        self.d(**UiSelector).set_text(text)
    
    def send_keys(self, text: str, clear: bool=False, **UiSelector):
        self.d.send_keys(text, clear, **UiSelector)
    
    def press(self, key: int|str):
        self.d.press(key)
    
    def swipe(self, direction: str="up", scale: float=0.5, position_box: tuple[float]=None):
        if position_box:
            self.d.swipe(position_box[0], position_box[1], position_box[2], position_box[3])
        else:
            self.d.swipe_ext(direction, scale)
        
    def drag(self, sx: float, sy: float, ex: float, ey: float, duration: float=0.5):
        self.d.drag(sx, sy, ex, ey, duration=duration)
    
    def screenshot(self, file_path: str):
        self.d.screenshot(file_path)
        
    def start_record(self, file_path: str):
        """开始录屏, 若使用请执行如下命令安装如下库:
        \npip install -U "uiautomator2[image]" -i https://pypi.doubanio.com/simple

        Args:
            file_path (str): 录制视频保存路径
        """
        self.d.screenrecord(file_path)
    
    def stop_record(self):
        self.d.screenrecord.stop()
    
    def shell(self, command: str|list[str], stream: bool=False, timeout: int=60) -> str:
        return self.d.shell(command, stream, timeout)
    
    def enable_wifi(self, stream: bool=False, timeout: int=60) -> str:
        return self.d.shell("svc wifi enable", stream, timeout)
    
    def disable_wifi(self, stream: bool=False, timeout: int=60) -> str:
        return self.d.shell("svc wifi disable", stream, timeout)
    
    def enable_data(self, stream: bool=False, timeout: int=60) -> str:
        return self.d.shell("svc data enable", stream, timeout)
    
    def disable_data(self, stream: bool=False, timeout: int=60) -> str:
        return self.d.shell("svc data disable", stream, timeout)
    
    def send_remote_file(self, from_file_path: str, to_file_path: str):
        os.system(f"adb -s {self.UUID} push {from_file_path} {to_file_path}")
    
    def get_remote_file(self, from_file_path: str, to_file_path: str):
        os.system(f"adb -s {self.UUID} pull {from_file_path} {to_file_path}")


class AndroidToolKit:
    DEFAULT_ENGINE = "uiautomator2"
    ENGINE_LIST = ["uiautomator2", "airtest"]
    
    def __init__(self, UUID: str, engine: str=None):
        """engine若为空, 则使用默认引擎"""
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
            