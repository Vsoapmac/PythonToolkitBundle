import uiautomator2 as u2
from airtest.core.api import *
from airtest.core.android.android import Android


class AirtestAdapter:
    d = None
    
    def globel_device(self, device: Android):
        self.d = device
    
    def connect_device(self, UUID: str) -> Android:
        return init_device(uuid=UUID)

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
        
    def touch(self, template: Template, timeout: int=60, interval: float=0.5):
        """点击元素

        Args:
            template (Template): 图片Template抽象类
            timeout (int, optional): 等待超时时间. Defaults to 60.
            interval (float, optional): 识别间隔, 每隔几秒识别一次. Defaults to 0.5.
        """
        wait(template, timeout, interval)
        touch(template)


class Ui2Adapter:
    d = None
    
    def globel_device(self, device: u2.Device):
        self.d = device
    
    def connect_device(self, UUID: str) -> u2.Device:
        return u2.connect(UUID)

    def install_app(self, app_file_path: str):
        self.d.install_app(app_file_path)

    def start_app(self, app_package: str):
        self.d.start_app(app_package)
        
    def stop_app(self, app_package: str):
        self.d.stop_app(app_package)


class AndroidToolKit:
    DEFAULT_ENGINE = "uiautomator2"
    ENGINE_LIST = ["uiautomator2", "airtest"]
    
    def __init__(self, UUID: str, engine: str=None):
        """engine若为空, 则使用默认引擎"""
        if engine is None:
            engine = self.DEFAULT_ENGINE
        if engine == "uiautomator2":
            self.engine_ada = Ui2Adapter()
            self.device = self.engine_ada.connect_device(UUID)
            self.engine_ada.globel_device(device=self.device)
        elif engine == "airtest":
            self.engine_ada = AirtestAdapter()
            self.device = self.engine_ada.connect_device(UUID)
            self.engine_ada.globel_device(self.device)
            