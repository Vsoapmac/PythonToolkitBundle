from faker import Faker
from datetime import datetime

class FakerUtils:
    """随机生成数据的工具类, 若使用该工具类, 请使用如下命令安装第三方库: 
    \npip install Faker
    """
    fake = None
    LOCALE = {
        "简体中文": "zh_CN",
        "繁体中文": "zh_TW",
        "美国英文": "en_US",
        "英国英文": "en_GB",
        "德文": "de_DE",
        "日文": "ja_JP",
        "韩文": "ko_KR",
        "法文": "fr_FR",
    }
    
    def __init__(self, language="zh_CN"):
        self.fake = Faker(language)
        
    def full_address(self) -> str:
        """随机生成完整的地址, 比如海南省成市丰都深圳路p座 425541

        Returns:
            str: 完整的地址
        """
        return self.fake.address()
    
    def street_address(self) -> str:
        """随机生成街道+地址, 比如兴城路A座

        Returns:
            str: 街道+地址
        """
        return self.fake.street_address()
    
    def street(self) -> str:
        """随机生成街道名, 比如宜都街

        Returns:
            str: 街道名
        """
        return self.fake.street_name()
    
    def city_name(self) -> str:
        """随机生成城市名,比如兰州

        Returns:
            str: 城市名
        """
        return self.fake.city_name()
    
    def city(self) -> str:
        """随机生成城市,比如兰州市

        Returns:
            str: 城市
        """
        return self.fake.city()
    
    def province(self) -> str:
        """随机生成省份名,比如陕西省

        Returns:
            str: 省份名
        """
        return self.fake.province()
    
    def postcode(self) -> str:
        """随机生成邮编

        Returns:
            str: 邮编
        """
        return self.fake.postcode()
    
    def country(self) -> str:
        """随机生成国家

        Returns:
            str: 国家
        """
        return self.fake.country()
    
    def company(self) -> str:
        """随机生成完整公司名, 比如惠派国际公司信息有限公司

        Returns:
            str: 完整公司名
        """
        return self.fake.company()
    
    def company_suffix(self) -> str:
        """随机生成公司名后缀(公司性质), 比如网络有限公司

        Returns:
            str: 公司名后缀(公司性质)
        """
        return self.fake.company_suffix()
        
    def company_prefix(self) -> str:
        """随机生成公司名前缀, 比如鑫博腾飞

        Returns:
            str: 公司名前缀
        """
        return self.fake.company_prefix()
    
    def company_email(self) -> str:
        """随机生成企业邮箱
        
        Returns:
            str: 企业邮箱
        """
        return self.fake.company_email()
    
    def email(self) -> str:
        """随机生成邮箱

        Returns:
            str: 邮箱
        """
        return self.fake.email()
    
    def name(self) -> str:
        """随机生成姓名

        Returns:
            str: 姓名
        """
        return self.fake.name()
    
    def phone_number(self) -> str:
        """随机生成电话号码

        Returns:
            str: 电话号码
        """
        return self.fake.phone_number()
    
    def job(self) -> str:
        """随机生成工作

        Returns:
            str: 工作
        """
        return self.fake.job()
    
    def username(self) -> str:
        """随机生成账号

        Returns:
            str: 账号
        """
        return self.fake.user_name()
    
    def password(self, length=10, special_chars=True, digits=True, upper_case=True, lower_case=True) -> str:
        """随机生成密码

        Args:
            length (int, optional): 生成的密码长度. Defaults to 10.
            special_chars (bool, optional): 是否能使用特殊字符. Defaults to True.
            digits (bool, optional): 是否包含数字. Defaults to True.
            upper_case (bool, optional): 是否包含大写字母. Defaults to True.
            lower_case (bool, optional): 是否包含小写字母. Defaults to True.

        Returns:
            str: 密码
        """
        return self.fake.password(length=length, 
                                  special_chars=special_chars, 
                                  digits=digits, 
                                  upper_case=upper_case, lower_case=lower_case)
    
    def text(self) -> str:
        """随机文章

        Returns:
            str: 文章
        """
        return self.fake.text()
    
    def random_date(self, pattern: str="%Y-%m-%d", end_datetime: datetime=None) -> str:
        """随机日期

        Args:
            pattern (str, optional): 日期输出格式. Defaults to "%Y-%m-%d".
            end_datetime (datetime, optional): 以什么日期结束. Defaults to None.

        Returns:
            str: 日期
        """
        return self.fake.date(pattern=pattern, end_datetime=end_datetime)
    
    def random_int(self, from_num: int, to_num: int) -> int:
        """随机整数

        Args:
            from_num (int): 从什么数字开始, 随机数会取等于或大于该数字的值
            to_num (int): 从什么数字结束, 随机数会取等于或小于该数字的值

        Returns:
            int: 整数
        """
        return self.fake.random.randint(from_num, to_num)
    
    def random_float(self, from_num: float, to_num: float) -> float:
        """随机浮点数

        Args:
            from_num (float): 从什么数字开始, 随机数会取等于或大于该数字的值
            to_num (float): 从什么数字结束, 随机数会取等于或小于该数字的值

        Returns:
            int: 浮点数
        """
        return self.fake.random.uniform(from_num, to_num)
 