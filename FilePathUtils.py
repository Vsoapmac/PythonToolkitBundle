"""文件工具类 FilePathUtils"""
import os, sys, json, time, shutil, hashlib
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def load_str_as_pathlib(*path_str: str | Path) -> Path:
    """将字符串的path转换成pathlib的对象

    Args:
        *path_str: 字符串的path, 可传入多个参数

    Returns:
        对应path的patblib对象

    Examples:
        >>> FilePathUtils.load_str_as_pathlib("D:/test", "test01", "test001", "test.exe")
        D:\\test\\test01\\test001\\test.exe
    """
    return Path(*path_str)

def path_joint_str(original_path: str | Path, *path_str: str | Path, to_Path=False) -> str | Path:
    """将路径拼接上原始的路径

    Args:
        original_path: 原始路径的Path
        *path_str: 字符串的path, 可传入多个参数
        to_Path: 结果是否转化为pathlib对象, 默认False

    Returns:
        拼接完成后的路径

    Examples:
        >>> FilePathUtils.path_joint_str("D:/assassin", "test", "test01", "test001", "test.exe")
        D:\\assassin\\test\\test01\\test001\\test.exe
    """
    original_path = Path(original_path, *path_str)
    if not to_Path:
        return str(original_path.resolve())
    else:
        return original_path

def get_project_folder_path(project_name: str = '', file_level: int = -1) -> Path:
    """获取项目绝对路径

    Args:
        project_name: 项目名称
        file_level: 文件在当前项目的哪一层, 在当前文件夹下为0, 在项目子文件夹下为1, 在项目子文件夹下的子文件夹为2, 以此类推。
        当file_level > 0时, 形参project_name就不会起作用了, 只有file_level=-1时才会起作用。默认为-1

    Returns:
        项目绝对路径

    Raises:
        Exception: 路径不存在则抛出异常
    """
    cwd = Path.cwd()
    if file_level == -1:
        python_file_path = str(cwd.resolve())
        project_folder_path = Path(python_file_path[0:python_file_path.find(project_name) + len(project_name)])
        if not project_folder_path.exists():
            raise Exception(f"路径{project_folder_path}不存在, 检查输入形参中的项目名称【{project_name}】是否正确")
        else:
            return project_folder_path
    elif file_level == 0:
        return cwd
    elif file_level > 0:
        current = cwd.parent
        for _ in range(file_level - 1):
            current = current.parent
        return current

def get_file_modify_day(file_path: str | Path, time_format="%Y%m%d") -> str:
    """查看文件修改日期

    Args:
        file_path: 文件路径, 如 D:\\test.txt
        time_format: 日期格式, 默认%Y%m%d, 也就是年月日

    Returns:
        文件修改日期
    """
    mtime = os.path.getmtime(file_path)
    return datetime.fromtimestamp(mtime).strftime(time_format)

def get_file_md5(file_path: str) -> str:
    """查看文件md5
    
    Args:
        file_path: 文件路径, 如 D:\\test.txt

    Returns:
        文件的md5
    """
    with open(file_path, 'rb') as f:
        data = f.read()
    md5_hash = hashlib.md5()
    md5_hash.update(data)
    md5_value = md5_hash.hexdigest()
    return md5_value

def get_file_info(file_path: str | Path, beatiful_print=False) -> dict:
    """获取文件完整信息

    Args:
        file_path: 文件路径
        beatiful_print: 是否格式化打印出来, 默认False

    Returns:
        装有文件详细信息的字典
        返回值参数说明：
        - "full_name"：文件完整名(包含后缀)
        - "name"：文件名(不包含后缀)
        - "suffix"：文件后缀(.xx格式)
        - "size"：文件大小, 单位MB
        - "last_modify_day"：文件最新修改日期, 格式YYYY-MM-DD HH:MM:SS
        - "root"：文件根目录
        - "path_symbol"：文件目录符
        - "parent"：文件父目录
        - "parents"：文件父目录集
        - "system"：文件所在系统类型
    """
    file = Path(file_path).resolve()
    parent_path_list = []
    for parent_path in file.parents:
        parent_path_list.append(str(parent_path))
    parent_path_list.remove(parent_path_list[-1])
    file_info = {
        "full_name": file.name,
        "name": file.name.replace(file.suffix, ""),
        "suffix": file.suffix,
        "size": round(os.path.getsize(file) / 1024, 2),
        "last_modify_day": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(os.path.getmtime(file))),
        "root": file.anchor,
        "path_symbol": file.root,
        "parent": str(file.parent),
        "parents": parent_path_list,
        "system": sys.platform,
    }
    if beatiful_print:
        print(json.dumps(file_info, indent=2))
    return file_info

def listdir(folder_path: str | Path) -> list:
    """将文件夹下的文件以列表的形式返回

    Args:
        folder_path: 文件夹路径

    Returns:
        文件夹下的文件(包含文件夹与文件)的列表
    """
    return os.listdir(folder_path)

def count_folder_files(folder_path: str | Path) -> int:
    """计算文件夹下面所有的文件(不包含子文件夹)

    Args:
        folder_path: 文件夹路径

    Returns:
        文件夹下的文件数量
    """
    for root, dirs, files in os.walk(folder_path):
        return len(files)

def count_all_folder_files(folder_path: str | Path) -> int:
    """计算文件夹下面所有的文件(包含子文件夹)

    Args:
        folder_path: 文件夹路径

    Returns:
        文件夹下的文件数量
    """
    count = 0
    for root, dirs, files in os.walk(folder_path):
        count += len(files)
    return count

def create_folder(folder_path: str | Path):
    """创建文件夹

    Args:
        folder_path: 文件夹路径
    """
    path = Path(folder_path)
    if not path.exists():
        os.makedirs(path)
    del path

def read_file(file_path: str | Path, encoding="UTF-8") -> str:
    """读取文件

    Args:
        file_path: 文件路径
        encoding: 文件编码

    Returns:
        文件内容

    Raises:
        Exception: 文件不存在或不可读则抛出异常
    """
    path = Path(file_path)
    if path.exists():
        with path.open(encoding=encoding) as file:
            if file.readable():
                return file.read()
            else:
                raise Exception(f"文件{path}不可读")

def write_file(file_path: str | Path, content, encoding="UTF-8"):
    """写入文件, 文件不存在则自动创建

    Args:
        file_path: 文件路径
        content: 写入的内容
        encoding: 文件编码, 默认UTF-8

    Raises:
        Exception: 文件不可写则抛出异常
    """
    path = Path(file_path)
    with path.open(mode="w", encoding=encoding) as file:
        if file.writable():
            file.write(content)
        else:
            raise Exception(f"文件{path}不可写")

def rename_file(old_file_path: str | Path, new_file_name: str) -> Path:
    """重命名文件或文件夹

    Args:
        old_file_path: 源文件路径
        new_file_name: 新文件名

    Returns:
        新的文件名绝对路径
    """
    old_file_path = Path(old_file_path).resolve()
    path = old_file_path.parent
    return old_file_path.rename(path / new_file_name)

def copy_single_file(from_file_path: str | Path, to_file_folder: str | Path):
    """复制单个文件到指定路径

    Args:
        from_file_path: 源文件路径
        to_file_folder: 目标文件夹路径

    Raises:
        Exception: 源文件不存在则抛出异常
    """
    from_file_path = Path(from_file_path).resolve()
    to_file_path = Path(to_file_folder, from_file_path.name).resolve()
    if from_file_path.exists():
        shutil.copy(from_file_path, to_file_path)
        del from_file_path, to_file_path
    else:
        raise Exception(f"源文件{from_file_path}不存在, 请检查")

def copy_folder(from_folder_path: str | Path, to_folder_path: str | Path):
    """复制文件夹中的所有文件到指定路径

    Args:
        from_folder_path: 源文件夹路径
        to_folder_path: 目标文件夹路径

    Raises:
        Exception: check_file_exists打开后, 源文件不存在则抛出异常
    """
    shutil.copytree(from_folder_path, to_folder_path)

def copy_multiple_file(from_folder_path: str | Path, to_folder_path: str | Path, file_name_list: list, max_workers=1):
    """复制文件夹中指定的多个文件到指定路径

    Args:
        from_folder_path: 源文件夹路径
        to_folder_path: 目标文件夹路径
        file_name_list: 源文件夹中的文件名列表
        max_workers: 一次执行的最大线程数, 默认1
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for file_name in file_name_list:
            from_path = Path(from_folder_path, file_name)
            to_path = Path(to_folder_path, file_name)
            executor.submit(shutil.copy, from_path, to_path)
            del from_path, to_path

def move_single_file(from_file_path: str | Path, to_file_folder: str | Path):
    """移动单个文件

    Args:
        from_file_path: 源文件路径
        to_file_folder: 目标文件夹路径

    Raises:
        Exception: 源文件不存在则抛出异常
    """
    from_file_path = Path(from_file_path).resolve()
    to_file_path = Path(to_file_folder, from_file_path.name).resolve()
    if from_file_path.exists():
        shutil.move(from_file_path, to_file_path)
        del from_file_path, to_file_path
    else:
        raise Exception(f"源文件{from_file_path}不存在, 请检查")

def move_folder(from_folder_path: str | Path, to_folder_path: str | Path):
    """将文件夹中的所有文件移动到指定路径

    Args:
        from_folder_path: 源文件夹路径
        to_folder_path: 目标文件夹路径
    """
    shutil.move(from_folder_path, to_folder_path)

def move_multiple_file(from_folder_path: str | Path, to_folder_path: str | Path, file_name_list: list, max_workers=1):
    """移动文件夹中指定的多个文件到指定路径

    Args:
        from_folder_path: 源文件夹路径
        to_folder_path: 目标文件夹路径
        file_name_list: 源文件夹中的文件名列表
        max_workers: 一次执行的最大线程数, 默认1
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for file_name in file_name_list:
            from_path = Path(from_folder_path, file_name)
            to_path = Path(to_folder_path, file_name)
            executor.submit(shutil.move, from_path, to_path)
            del from_path, to_path