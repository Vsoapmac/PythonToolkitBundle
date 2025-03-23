"""文件工具类 FilePathUtils"""
import os, sys, json, time, shutil, hashlib, getpass
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

def get_project_dir(project_files_or_dirs: str|Path|list=None, max_levels: int=10) -> str:
    """获取项目绝对路径
    \n若在项目扫描不到project_file_or_dir参数中提供的文件或文件夹, 或project_file_or_dir为None时项目不存在如下文件或文件夹时会返回`Path.cwd()`
    \n.git
    \nrequirements.txt
    \n.gitignore
    \nREADME.md
    
    Args:
        project_file_or_dir (str | Path | list, optional): 项目下的文件或者文件夹, 用于扫描, 可以传入多个。传入多个时, 只要存在其中一个文件或文件夹就会返回项目路径. Defaults to None.
        max_levels (int, optional): 最大向上查找层级. Defaults to 10.

    Returns:
        str: 项目路径
    """
    cwd = Path.cwd()
    current = cwd
    for _ in range(max_levels):
        # 检查当前目录是否包含项目标识文件或目录
        if project_files_or_dirs is None:
            if (current / ".git").exists() or (current / "requirements.txt").exists() or (current / ".gitignore").exists() or (current / "README.md").exists():
                return current
        else:
            if isinstance(project_files_or_dirs, list):
                for project_file_or_dir in project_files_or_dirs:
                    if (current / project_file_or_dir).exists():
                        return current
            elif (current / project_files_or_dirs).exists():
                    return current
        # 继续向上查找, 到达根目录立刻断开
        if current.parent == current:
            break
        current = current.parent

    # 如果没有找到标识文件，返回直接返回cwd
    return str(cwd)

def get_user() -> str:
    """获取系统用户名

    Returns:
        str: 系统用户名
    """
    return getpass.getuser()

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

def is_path_exists(path: str | Path) -> bool:
    """判断路径是否存在, 可以是文件夹或文件

    Args:
        path (str | Path): 文件或文件夹路径

    Returns:
        bool: 是否存在
    """
    path = Path(path) if isinstance(path, str) else path
    return path.exists()

def read_file(file_path: str | Path, encoding=None, **args) -> str:
    """读取文件

    Args:
        file_path (str | Path): 文件路径
        encoding (str, optional): 文件编码. Defaults to None.

    Raises:
        Exception: 文件不存在或不可读则抛出异常

    Returns:
        str: 文件内容
    """
    path = Path(file_path) if isinstance(file_path, str) else file_path
    if path.exists():
        with open(path, "r", encoding=encoding, **args) as file:
            if file.readable():
                return file.read()
            else:
                raise Exception(f"file {path} is not able to read")

def write_file(file_path: str | Path, content, encoding=None, **args):
    """写入文件, 文件不存在则自动创建

    Args:
        file_path (str | Path): 文件路径
        content (any): 写入的内容
        encoding (str, optional): 文件编码. Defaults to None.

    Raises:
        Exception: 文件不可写则抛出异常
    """
    path = Path(file_path) if isinstance(file_path, str) else file_path
    with open(path, "w", encoding=encoding, **args) as file:
        if file.writable():
            file.write(content)
        else:
            raise Exception(f"file {path} is not able to write")

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

def delete_file(file_path: str | Path, backup_to_dir: str | Path | bool=False, backup_mode: str="R"):
    """删除一个文件

    Args:
        file_path (str | Path): 文件源路径
        backup_to_dir (str | Path | bool, optional): 备份文件夹路径, 如果为False则不备份. Defaults to False.
        backup_mode (str, optional): 备份模式, 可选参数为{'R'(重命名待删除文件), 'M'(将文件移动到备份的文件夹, 如果备份文件夹不存在则创建)}. Defaults to "R".
    """
    file = Path(file_path).resolve() if isinstance(file_path, str) else file_path.resolve()
    parent_dir = file.parent
    re_filename = file.name
    finish_backup = False
    if backup_to_dir and file.exists():
        backup_to_dir = Path(backup_to_dir).resolve() if isinstance(backup_to_dir, str) else backup_to_dir.resolve() if isinstance(backup_to_dir, Path) else backup_to_dir
        # 备份文件夹不存在则创建一个
        if isinstance(backup_to_dir, Path) and (not backup_to_dir.exists()):
            os.makedirs(backup_to_dir)
        # 重命名模式
        if backup_mode == "R":
            file_suffix = file.suffix
            # 参数中输入了确定的备份的文件夹路径
            if isinstance(backup_to_dir, Path):
                is_success = False
                for _ in range(500):
                    new_file = backup_to_dir / f"{re_filename.replace(file_suffix, '')}_{datetime.now().strftime('%Y%m%d%H%M%S')}_bck{file_suffix}"
                    if new_file.exists():
                        time.sleep(1)
                    else:
                        is_success = True
                        break
                if not is_success:
                    raise Exception(f"rename timeout, there are too many files with the same name in {backup_to_dir}, please check.")
                file.rename(new_file)
            # 没有确定, 在当前文件夹下直接重命名
            else:
                is_success = False
                for _ in range(500):
                    new_file = parent_dir / f"{re_filename.replace(file_suffix, '')}_{datetime.now().strftime('%Y%m%d%H%M%S')}_bck{file_suffix}"
                    if new_file.exists():
                        time.sleep(1)
                    else:
                        is_success = True
                        break
                if not is_success:
                    raise Exception(f"rename timeout, there are too many files with the same name in {parent_dir}, please check.")
                file.rename(new_file)
        # 移动模式
        elif backup_mode == "M":
            # 参数中输入了确定的备份的文件夹路径
            if isinstance(backup_to_dir, Path):
                bck_filename = re_filename
                # 防止在移动时, 文件夹下有相同文件的情况
                is_success = False
                for _ in range(500):
                    try:
                        shutil.move(file, backup_to_dir / bck_filename)
                        is_success = True
                        break
                    except:
                        time.sleep(1)
                        bck_filename = f"{re_filename}_{datetime.now().strftime('%H%M%S')}"
                if not is_success:
                    raise Exception(f"move file timeout, there are too many files with the same name in {backup_to_dir}, please check.")
            # 没有确定, 在当前文件夹下创建一个文件夹并移动进去
            else:
                backup_dir = parent_dir / f"{datetime.now().strftime('%Y%m%d')}_delete_backup"
                if not backup_dir.exists():
                    os.makedirs(backup_dir)
                bck_filename = re_filename
                # 防止在移动时, 文件夹下有相同文件的情况
                is_success = False
                for _ in range(500):
                    try:
                        shutil.move(file, backup_dir / bck_filename)
                        is_success = True
                        break
                    except:
                        time.sleep(1)
                        bck_filename = f"{re_filename}_{datetime.now().strftime('%H%M%S')}"
                if not is_success:
                    raise Exception(f"move file timeout, there are too many files with the same name in {backup_to_dir}, please check.")
        finish_backup = True
    if file.exists():
        file.unlink()
        print("File has been successfully deleted.")
    elif (not file.exists()) and (not finish_backup):
        print("The file does not exist, no need to delete.")
    elif finish_backup:
        print("The file has been successfully backed up, no need to delete.")

def delete_folder(folder_path: str | Path, backup_to_dir: str | Path | bool=False, backup_mode: str="R"):
    """删除一个文件夹

    Args:
        folder_path (str | Path): 文件夹源路径
        backup_to_dir (str | Path | bool, optional): 备份文件夹路径, 如果为False则不备份. Defaults to False.
        backup_mode (str, optional): 备份模式, 可选参数为{'R'(重命名待删除文件), 'M'(将文件移动到备份的文件夹, 如果备份文件夹不存在则创建)}. Defaults to "R".
    """
    folder = Path(folder_path).resolve() if isinstance(folder_path, str) else folder_path.resolve()
    parent_dir = folder.parent
    re_foldername = folder.name
    finish_backup = False
    if backup_to_dir and folder.exists():
        backup_to_dir = Path(backup_to_dir).resolve() if isinstance(backup_to_dir, str) else backup_to_dir.resolve() if isinstance(backup_to_dir, Path) else backup_to_dir
        # 备份文件夹不存在则创建一个
        if isinstance(backup_to_dir, Path) and (not backup_to_dir.exists()):
            os.makedirs(backup_to_dir)
        # 重命名模式
        if backup_mode == "R":
            # 参数中输入了确定的备份的文件夹路径
            if isinstance(backup_to_dir, Path):
                is_success = False
                for _ in range(500):
                    new_folder = backup_to_dir / f"{re_foldername}_{datetime.now().strftime('%Y%m%d%H%M%S')}_bck"
                    if new_folder.exists():
                        time.sleep(1)
                    else:
                        is_success = True
                        break
                if not is_success:
                    raise Exception(f"rename timeout, there are too many folders with the same name in {backup_to_dir}, please check.")
                folder.rename(new_folder)
            # 没有确定, 在当前文件夹下直接重命名
            else:
                is_success = False
                for _ in range(500):
                    new_folder = parent_dir / f"{re_foldername}_{datetime.now().strftime('%Y%m%d%H%M%S')}_bck"
                    if new_folder.exists():
                        time.sleep(1)
                    else:
                        is_success = True
                        break
                if not is_success:
                    raise Exception(f"rename timeout, there are too many folders with the same name in {parent_dir}, please check.")
                folder.rename(new_folder)
        # 移动模式
        elif backup_mode == "M":
            # 参数中输入了确定的备份的文件夹路径
            if isinstance(backup_to_dir, Path):
                bck_filename = re_foldername
                # 防止在移动时, 文件夹下有相同文件夹名称的情况
                is_success = False
                for _ in range(500):
                    try:
                        shutil.move(folder, backup_to_dir / bck_filename)
                        is_success = True
                        break
                    except:
                        time.sleep(1)
                        bck_filename = f"{re_foldername}_{datetime.now().strftime('%H%M%S')}"
                if not is_success:
                    raise Exception(f"move folder timeout, there are too many folders with the same name in {backup_to_dir}, please check.")
            # 没有确定, 在当前文件夹下创建一个文件夹并移动进去
            else:
                backup_dir = parent_dir / f"{datetime.now().strftime('%Y%m%d')}_delete_backup"
                if not backup_dir.exists():
                    os.makedirs(backup_dir)
                bck_filename = re_foldername
                # 防止在移动时, 文件夹下有相同文件夹名称的情况
                is_success = False
                for _ in range(500):
                    try:
                        shutil.move(folder, backup_dir / bck_filename)
                        is_success = True
                        break
                    except:
                        time.sleep(1)
                        bck_filename = f"{re_foldername}_{datetime.now().strftime('%H%M%S')}"
                if not is_success:
                    raise Exception(f"move folder timeout, there are too many folders with the same name in {backup_to_dir}, please check.")
        finish_backup = True
    if folder.exists():
        shutil.rmtree(folder)
        print("Folder has been successfully deleted.")
    elif (not folder.exists()) and (not finish_backup):
        print("The folder does not exist, no need to delete.")
    elif finish_backup:
        print("The folder has been successfully backed up, no need to delete.")

def copy_single_file(from_file_path: str | Path, to_dir: str | Path, is_create_to_folder: bool=True):
    """复制单个文件到指定路径

    Args:
        from_file_path (str | Path): 源文件路径
        to_dir (str | Path): 目标文件夹路径
        is_create_to_folder (bool, optional): 目标文件夹不存在时是否创建. Defaults to True.

    Raises:
        Exception: 源文件或目标文件夹不存在则抛出异常(若is_create_to_folder参数设置为False则会抛出这个异常)
    """
    from_file_path = Path(from_file_path).resolve() if isinstance(from_file_path, str) else from_file_path.resolve()
    to_dir = Path(to_dir).resolve() if isinstance(to_dir, str) else to_dir.resolve()
    if not to_dir.exists():
        if is_create_to_folder:
            os.makedirs(to_dir)
        else:
            raise Exception(f"target folder {to_dir} is not exists, please check")
    if from_file_path.exists():
        shutil.copy(from_file_path, to_dir / from_file_path.name)
        del from_file_path
    else:
        raise Exception(f"sources file {from_file_path} is not exists, please check")

def copy_all_files(from_dir: str | Path, to_dir: str | Path, is_create_to_folder: bool=True):
    """复制文件夹中的所有文件到指定路径

    Args:
        from_dir (str | Path): 源文件夹路径
        to_dir (str | Path): 目标文件夹路径
        is_create_to_folder (bool, optional): 目标文件夹不存在时是否创建. Defaults to True.

    Raises:
        Exception: 源文件夹或目标文件夹不存在则抛出异常(若is_create_to_folder参数设置为False则会抛出这个异常)
    """
    from_dir = Path(from_dir).resolve() if isinstance(from_dir, str) else from_dir.resolve()
    to_dir = Path(to_dir).resolve() if isinstance(to_dir, str) else to_dir.resolve()
    if not from_dir.exists():
        raise Exception(f"sources folder {from_dir} is not exists, please check")
    if not to_dir.exists():
        if is_create_to_folder:
            os.makedirs(to_dir)
        else:
            raise Exception(f"target folder {to_dir} is not exists, please check")
    shutil.copytree(from_dir, to_dir)

def copy_multiple_files(from_dir: str | Path, file_name_list: list, to_dir: str | Path, is_create_to_folder: bool=True, max_workers=1):
    """复制文件夹中指定的多个文件到指定路径

    Args:
        from_dir (str | Path): 源文件所在的文件夹路径
        to_dir (str | Path): 目标文件夹路径
        file_name_list (list): 源文件夹中的文件名列表
        is_create_to_folder (bool, optional): 目标文件夹不存在时是否创建. Defaults to True.
        max_workers (int, optional): 一次执行的最大线程数. Defaults to 1.

    Raises:
        Exception: 源文件夹或目标文件夹不存在则抛出异常(若is_create_to_folder参数设置为False则会抛出这个异常)
    """
    from_dir = Path(from_dir).resolve() if isinstance(from_dir, str) else from_dir.resolve()
    to_dir = Path(to_dir).resolve() if isinstance(to_dir, str) else to_dir.resolve()
    if not from_dir.exists():
        raise Exception(f"sources folder {from_dir} is not exists, please check")
    if not to_dir.exists():
        if is_create_to_folder:
            os.makedirs(to_dir)
        else:
            raise Exception(f"target folder {to_dir} is not exists, please check")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for file_name in file_name_list:
            from_path = from_dir / file_name
            to_path = to_dir / file_name
            executor.submit(shutil.copy, from_path, to_path)
            del from_path, to_path

def move_single_file(from_file_path: str | Path, to_dir: str | Path, is_create_to_folder: bool=True):
    """移动单个文件

    Args:
        from_file_path (str | Path): 源文件路径
        to_dir (str | Path): 目标文件夹路径
        is_create_to_folder (bool, optional): 目标文件夹不存在时是否创建. Defaults to True.

    Raises:
        Exception: 源文件不存在或目标文件夹不存在则抛出异常(若is_create_to_folder参数设置为False则会抛出这个异常)
    """
    from_file_path = Path(from_file_path).resolve() if isinstance(from_file_path, str) else from_file_path.resolve()
    to_dir = Path(to_dir).resolve() if isinstance(to_dir, str) else to_dir.resolve()
    if not to_dir.exists():
        if is_create_to_folder:
            os.makedirs(to_dir)
        else:
            raise Exception(f"target folder {to_dir} is not exists, please check")
    if from_file_path.exists():
        shutil.move(from_file_path, to_dir / from_file_path.name)
        del from_file_path
    else:
        raise Exception(f"sources file {from_file_path} is not exists, please check")

def move_all_files(from_dir: str | Path, to_dir: str | Path, is_create_to_folder: bool=True):
    """将文件夹中的所有文件移动到指定路径

    Args:
        from_dir (str | Path): 源文件夹路径
        to_dir (str | Path): 目标文件夹路径
        is_create_to_folder (bool, optional): 目标文件夹不存在时是否创建. Defaults to True.

    Raises:
        Exception: 源文件夹或目标文件夹不存在则抛出异常(若is_create_to_folder参数设置为False则会抛出这个异常)
    """
    from_dir = Path(from_dir).resolve() if isinstance(from_dir, str) else from_dir.resolve()
    to_dir = Path(to_dir).resolve() if isinstance(to_dir, str) else to_dir.resolve()
    if not from_dir.exists():
        raise Exception(f"sources folder {from_dir} is not exists, please check")
    if not to_dir.exists():
        if is_create_to_folder:
            os.makedirs(to_dir)
        else:
            raise Exception(f"target folder {to_dir} is not exists, please check")
    shutil.move(from_dir, to_dir)

def move_multiple_files(from_dir: str | Path, file_name_list: list, to_dir: str | Path, is_create_to_folder: bool=True, max_workers=1):
    """移动文件夹中指定的多个文件到指定路径

    Args:
        from_dir (str | Path): 源文件所在的文件夹路径
        file_name_list (list): 源文件夹中的文件名列表
        to_dir (str | Path): 目标文件夹路径
        is_create_to_folder (bool, optional): 目标文件夹不存在时是否创建. Defaults to True.
        max_workers (int, optional): 一次执行的最大线程数. Defaults to 1.

    Raises:
        Exception: 源文件夹或目标文件夹不存在则抛出异常(若is_create_to_folder参数设置为False则会抛出这个异常)
    """
    from_dir = Path(from_dir).resolve() if isinstance(from_dir, str) else from_dir.resolve()
    to_dir = Path(to_dir).resolve() if isinstance(to_dir, str) else to_dir.resolve()
    if not from_dir.exists():
        raise Exception(f"sources folder {from_dir} is not exists, please check")
    if not to_dir.exists():
        if is_create_to_folder:
            os.makedirs(to_dir)
        else:
            raise Exception(f"target folder {to_dir} is not exists, please check")
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        for file_name in file_name_list:
            from_path = from_dir / file_name
            to_path = to_dir / file_name
            executor.submit(shutil.move, from_path, to_path)
            del from_path, to_path
