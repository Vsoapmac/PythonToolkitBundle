"""文件工具类 FilePathUtils"""
import os, sys, json, time, shutil, hashlib
from datetime import datetime
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def load_str_as_pathlib(*path_str: str | Path) -> Path:
    """将字符串的path转换成pathlib的对象

    Returns:
        Path: 对应path的patblib对象
    
    Examples:
        >>> FilePathUtils.load_str_as_pathlib("D:/test", "test01", "test001", "test.exe")
        D:\\test\\test01\\test001\\test.exe
    """
    return Path(*path_str)

def path_joint_str(original_path: str | Path, *path_str: str | Path, to_Path: bool=False, is_resolve: bool=True) -> str | Path:
    """将路径拼接上原始的路径

    Args:
        original_path (str | Path): 原始路径的Path
        to_Path (bool, optional): 结果是否转化为pathlib对象. Defaults to False.
        is_resolve (bool, optional): 是否返回绝对路径. Defaults to True.

    Returns:
        str | Path: 拼接结果
    """
    original_path = Path(original_path, *path_str)
    if not to_Path:
        return str(original_path.resolve()) if is_resolve else str(original_path)
    else:
        return original_path

def get_parent(path: str, to_Path: bool=False, is_resolve: bool=True) -> str | Path:
    """获取父路径

    Args:
        path (str): 文件路径
        to_Path (bool, optional): 结果是否转化为pathlib对象. Defaults to False.
        is_resolve (bool, optional): 是否返回绝对路径. Defaults to True.

    Returns:
        str | Path: 父路径
    """
    return Path(path).parent.resolve() if is_resolve else Path(path).parent if to_Path else str(Path(path).parent.resolve()) if is_resolve else str(Path(path).parent)

def get_parents(path: str, is_resolve: bool=True) -> list[str]:
    """获取父路径列表

    Args:
        path (str): 文件路径
        is_resolve (bool, optional): 是否返回绝对路径. Defaults to True.

    Returns:
        list[str]: 父路径列表
        
    Examples:
        >>> FilePathUtils.get_parents("D:/test/test01/test001/test.exe")
        ['D:\\test\\test01\\test001', 'D:\\test\\test01', 'D:\\test', 'D:\\']
    """
    return [str(parent) for parent in Path(path).resolve().parents] if is_resolve else [str(parent) for parent in Path(path).parents]

def get_project_dir(project_name: str = '', file_level: int = -1) -> Path:
    """获取项目绝对路径

    Args:
        project_name (str, optional): 项目名称. Defaults to ''.
        file_level (int, optional): 文件在当前项目的哪一层, 在当前文件夹下为0, 在项目子文件夹下为1, 在项目子文件夹下的子文件夹为2, 以此类推。当file_level > 0时, 形参project_name就不会起作用了, 只有file_level=-1时才会起作用. Defaults to -1.

    Raises:
        Exception: 路径不存在则抛出异常

    Returns:
        Path: 项目绝对路径
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
        file_path (str | Path): 文件路径, 如 D:\\test.txt
        time_format (str, optional): 日期格式. Defaults to "%Y%m%d".

    Returns:
        str: 文件修改日期
    """
    mtime = os.path.getmtime(file_path)
    return datetime.fromtimestamp(mtime).strftime(time_format)

def get_file_md5(file_path: str) -> str:
    """查看文件md5

    Args:
        file_path (str): 文件路径, 如 D:\\test.txt

    Returns:
        str: 文件的md5
    """
    with open(file_path, 'rb') as f:
        data = f.read()
    md5_hash = hashlib.md5()
    md5_hash.update(data)
    md5_value = md5_hash.hexdigest()
    return md5_value

def get_file_size(file_path: str | Path, file_size_type: str="KB", ndigits: int=2) -> float:
    """获取文件大小

    Args:
        file_path (str | Path): 文件路径
        file_size_type (str, optional): 文件大小单位, 可输入有: B|KB|MB|GB|TB. Defaults to "KB".
        ndigits (int, optional): 输出保留多少位. Defaults to 2.

    Returns:
        float: 文件大小
    """
    file = Path(file_path).resolve() if isinstance(file_path, str) else file_path.resolve()
    file_size = os.path.getsize(file)
    if file_size_type == "KB":
        return round(file_size / 1024, ndigits)
    elif file_size_type == "MB":
        return round(file_size / 1024 / 1024, ndigits)
    elif file_size_type == "GB":
        return round(file_size / 1024 / 1024 / 1024, ndigits)
    elif file_size_type == "TB":
        return round(file_size / 1024 / 1024 / 1024 / 1024, ndigits)
    else:
        return round(file_size, ndigits)

def get_file_info(file_path: str | Path, beatiful_print=False) -> dict:
    """获取文件完整信息

    Args:
        file_path (str | Path): 文件路径
        beatiful_print (bool, optional): 是否格式化打印出来. Defaults to False.

    Returns:
        dict: 文件详细信息
        返回值参数说明: 
        - "full_name"：文件完整名(包含后缀)
        - "name"：文件名(不包含后缀)
        - "suffix"：文件后缀(.xx格式)
        - "size"：文件大小, 单位KB
        - "last_modify_day"：文件最新修改日期, 格式YYYY-MM-DD HH:MM:SS
        - "root"：文件根目录
        - "path_symbol"：文件目录符
        - "parent"：文件父目录
        - "parents"：文件父目录集
        - "system"：文件所在系统类型
    """
    file = Path(file_path).resolve() if isinstance(file_path, str) else file_path.resolve()
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
        folder_path (str | Path): 文件夹路径

    Returns:
        list: 文件夹下的文件(包含文件夹与文件)的列表
    """
    return os.listdir(folder_path)

def count_folder_files(folder_path: str | Path) -> int:
    """计算文件夹下面所有的文件(不包含子文件夹)

    Args:
        folder_path (str | Path): 文件夹路径

    Returns:
        int: 文件夹下的文件数量
    """
    for root, dirs, files in os.walk(folder_path):
        return len(files)

def count_all_folder_files(folder_path: str | Path) -> int:
    """计算文件夹下面所有的文件(包含子文件夹)

    Args:
        folder_path (str | Path): 文件夹路径

    Returns:
        int: 文件夹下的文件数量
    """
    count = 0
    for root, dirs, files in os.walk(folder_path):
        count += len(files)
    return count

def create_folder(folder_path: str | Path):
    """创建文件夹, 会自动判断是否存在该文件夹, 如果存在则不创建, 如果不存在则创建该文件夹, 如果文件夹路径不存在则自动创建路径

    Args:
        folder_path (str | Path): 文件夹路径
    """
    path = Path(folder_path)
    if not path.exists():
        os.makedirs(path)
    del path

def read_file(file_path: str | Path, encoding="UTF-8") -> str:
    """读取文件

    Args:
        file_path (str | Path): 文件路径
        encoding (str, optional): 文件编码. Defaults to "UTF-8".

    Raises:
        Exception: 文件不存在或不可读则抛出异常

    Returns:
        str: 文件内容
    """
    path = Path(file_path) if isinstance(file_path, str) else file_path
    if path.exists():
        with path.open(encoding=encoding) as file:
            if file.readable():
                return file.read()
            else:
                raise Exception(f"文件{path}不可读")

def write_file(file_path: str | Path, content, encoding="UTF-8"):
    """写入文件, 文件不存在则自动创建

    Args:
        file_path (str | Path): 文件路径
        content (any): 写入的内容
        encoding (str, optional): 文件编码. Defaults to "UTF-8".

    Raises:
        Exception: 文件不可写则抛出异常
    """
    path = Path(file_path) if isinstance(file_path, str) else file_path
    with path.open(mode="w", encoding=encoding) as file:
        if file.writable():
            file.write(content)
        else:
            raise Exception(f"文件{path}不可写")

def rename_file(old_file_path: str | Path, new_file_name: str) -> Path:
    """重命名文件或文件夹

    Args:
        old_file_path (str | Path): 源文件路径
        new_file_name (str): 新文件名

    Returns:
        Path: 新的文件名绝对路径
    """
    old_file_path = Path(old_file_path).resolve() if isinstance(old_file_path, str) else old_file_path.resolve()
    path = old_file_path.parent
    return old_file_path.rename(path / new_file_name)

def copy_single_file(from_file_path: str | Path, to_file_folder: str | Path):
    """复制单个文件到指定路径

    Args:
        from_file_path (str | Path): 源文件路径
        to_file_folder (str | Path): 目标文件夹路径

    Raises:
        Exception: 源文件不存在则抛出异常
    """
    from_file_path = Path(from_file_path).resolve() if isinstance(from_file_path, str) else from_file_path.resolve()
    to_file_path = Path(to_file_folder, from_file_path.name).resolve()
    if from_file_path.exists():
        shutil.copy(from_file_path, to_file_path)
        del from_file_path, to_file_path
    else:
        raise Exception(f"源文件{from_file_path}不存在, 请检查")

def copy_folder(from_folder_path: str | Path, to_folder_path: str | Path):
    """复制文件夹中的所有文件到指定路径

    Args:
        from_folder_path (str | Path): 源文件夹路径
        to_folder_path (str | Path): 目标文件夹路径
    """
    shutil.copytree(from_folder_path, to_folder_path)

def copy_multiple_file(from_folder_path: str | Path, to_folder_path: str | Path, file_name_list: list, max_workers=1):
    """复制文件夹中指定的多个文件到指定路径

    Args:
        from_folder_path (str | Path): 源文件夹路径
        to_folder_path (str | Path): 目标文件夹路径
        file_name_list (list): 源文件夹中的文件名列表
        max_workers (int, optional): 一次执行的最大线程数. Defaults to 1.
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
        from_file_path (str | Path): 源文件路径
        to_file_folder (str | Path): 目标文件夹路径

    Raises:
        Exception: 源文件不存在则抛出异常
    """
    from_file_path = Path(from_file_path).resolve() if isinstance(from_file_path, str) else from_file_path.resolve()
    to_file_path = Path(to_file_folder, from_file_path.name).resolve()
    if from_file_path.exists():
        shutil.move(from_file_path, to_file_path)
        del from_file_path, to_file_path
    else:
        raise Exception(f"源文件{from_file_path}不存在, 请检查")

def move_folder(from_folder_path: str | Path, to_folder_path: str | Path):
    """将文件夹中的所有文件移动到指定路径

    Args:
        from_folder_path (str | Path): 源文件夹路径
        to_folder_path (str | Path): 目标文件夹路径
    """
    shutil.move(from_folder_path, to_folder_path)

def move_multiple_file(from_folder_path: str | Path, to_folder_path: str | Path, file_name_list: list, max_workers=1):
    """移动文件夹中指定的多个文件到指定路径

    Args:
        from_folder_path (str | Path): 源文件夹路径
        to_folder_path (str | Path): 目标文件夹路径
        file_name_list (list): 源文件夹中的文件名列表
        max_workers (int, optional): 一次执行的最大线程数. Defaults to 1.
    """
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for file_name in file_name_list:
            from_path = Path(from_folder_path, file_name)
            to_path = Path(to_folder_path, file_name)
            executor.submit(shutil.move, from_path, to_path)
            del from_path, to_path
