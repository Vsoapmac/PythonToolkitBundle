"""yaml工具类 YamlUtils, 若使用该工具类, 请使用如下命令安装第三方库:
\npip install pyyaml
"""
import yaml


def load_yaml_file(file_path: str, encoding: str = "UTF-8") -> dict:
    """加载yaml文件

    Args:
        file_path: yaml文件路径
        encoding: 编码, 默认为uft-8

    Returns:
        yaml转换后的数据
    """
    with open(file_path, mode="r", encoding=encoding) as f:
        load_data = yaml.safe_load(f)
    return load_data

def dump_data_to_yaml(file_path: str, dict_data: dict, encoding: str="UTF-8"):
    """将数据写入yaml文件
    !!!注意该方法会覆盖yaml中的全部数据, 任何注释将会全部消失!!!

    Args:
        file_path: yaml文件路径
        dict_data: 字典数据
        encoding: 编码, 默认为uft-8
    """
    dump_data = yaml.safe_dump(dict_data)
    with open(file_path, mode="w", encoding=encoding) as f:
        f.write(dump_data)

def get_value(dict_data: dict, key):
    """获取字典中的值

    Args:
        dict_data: 字典数据
        key: key

    Returns:
        对应key的值

    Examples:
        >>> load_data = YamlUtils.loadYamlFile("example.yml")
        >>> value = YamlUtils.getValue(load_data)
    """
    return dict_data[key]
