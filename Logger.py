import logging, sys, os


class Logger:
    """log设置类"""
    logger = None

    def __init__(self, log_name=None, log_level=logging.INFO):
        """
        初始化logger

        Args:
            log_name: 自定义log名称。若log名称为None则使用根logger, 此时在任意模块中使用logging.info也可以调用该类的设置。默认None
            log_level: 全局log等级, 默认INFO。
        """
        self.logger = logging.getLogger(log_name)
        self.logger.setLevel(log_level)

    def set_logger_formatter(self,formatter: str = '%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                             dateformatter: str = '%Y-%m-%d %H:%M:%S'):
        """
        设置log格式

        Args:
            formatter: 打印格式, 默认%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s
            dateformatter: 日期格式, 默认%Y%m%d %H:%M:%S

        Returns:
            logging.Formatter
        """
        return logging.Formatter(formatter, datefmt=dateformatter)

    def set_write_log(self, file_path: str, formatter: logging.Formatter, level=logging.INFO):
        """
        设置log写入文件

        Args:
            file_path: 日志路径
            formatter: 打印格式
            level: 写入日志的level, 默认INFO
        """
        file_handler = logging.FileHandler(file_path)
        file_handler.setFormatter(formatter)
        file_handler.setLevel(level)
        self.logger.addHandler(file_handler)

    def set_print_log(self, formatter: logging.Formatter, level=logging.INFO):
        """
        设置打印log文本

        Args:
            formatter: 打印的格式
            level: 日志的level, 默认INFO
        """
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setFormatter(formatter)  # %(asctime)s
        console_handler.setLevel(level)
        self.logger.addHandler(console_handler)

    def log_file_helper(self, folder_path: str, file_name: str):
        """
        自动创建文件夹与日志文件

        Args:
            folder_path: 文件夹路径
            file_name: 日志文件名
        """
        # 文件夹不存在则创建
        if not os.path.exists(folder_path):
            os.makedirs(folder_path)
        full_file_name = os.path.join(folder_path, file_name)
        # 文件不存在则创建
        if not os.path.exists(full_file_name):
            with open(full_file_name, 'w', encoding="utf-8") as f:
                f.close()