"""python注释工具类 PythonCommentUtils"""
import re, os, shutil, autopep8
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor


def remove_comments(file_path: str, backup_old_file=True, delete_mode=2, encoding="UTF-8", write_back=True):
    """移除python代码中所有的注释并格式化

    Args:
        file_path: python文件路径
        backup_old_file: 备份旧文件, 备份在源文件同级目录并命名为xxx_remove_backup, 默认True
        delete_mode: 删除模式, 0为只删除单行注释, 1为只删除多行注释, 2为全部删除(默认)
        encoding: python编码, 默认UTF-8
        write_back: 是否写回python文件, 默认True

    Returns:
        处理后的python代码
    """
    path = Path(file_path)
    if backup_old_file:
        to_folder = Path(path.resolve().parent, str(path.name) + "_remove_backup")
        print(f'备份源文件到路径: {to_folder.resolve()}')
        shutil.copy(path.resolve(), to_folder.resolve())
        del to_folder
    code = path.open(encoding=encoding).read()
    """删除注释并格式化代码"""
    if delete_mode == 0 or delete_mode == 2:
        code = re.sub(r"#[^\n]*", "", code)  # 删除单行注释
    if delete_mode == 1 or delete_mode == 2:
        code = re.sub(r'""".*?"""', "", code, flags=re.DOTALL)  # 删除多行注释
    code = autopep8.fix_code(code)  # 格式化代码
    """写回文件"""
    if write_back:
        path.write_text(code, encoding=encoding)
    return code

def remove_folder_comments(folder_path: str, backup_old_folder=True, max_workers=5, delete_mode=2, encoding="UTF-8", write_back=True):
    """移除文件夹下所有.py文件的注释并格式化(包括子文件夹)

    Args:
        folder_path: 文件夹路径
        backup_old_folder: 备份旧文件夹, 备份在源文件夹同级目录并命名为xxx_remove_backup默认True
        max_workers: 提交线程数, 默认5个
        delete_mode: 删除模式, 0为只删除单行注释, 1为只删除多行注释, 2为全部删除(默认)
        encoding: python编码, 默认UTF-8
        write_back: 是否写回python文件, 默认True
    """
    if backup_old_folder:
        target_folder = Path(folder_path)
        to_folder = Path(target_folder.resolve().parent, str(target_folder.name)+"_remove_backup")
        print(f'备份源文件夹到路径: {to_folder.resolve()}')
        shutil.copytree(target_folder.resolve(), to_folder.resolve())
        del target_folder, to_folder
    with ThreadPoolExecutor(max_workers=max_workers) as exe:
        for root, paths, files in os.walk(folder_path):
            for file in files:
                file_path = Path(root, file)
                if file_path.suffix == ".py":
                    print(f"移除文件【{file_path.name}】的所有注释")
                    exe.submit(remove_comments, file_path, False, delete_mode, encoding, write_back)

def check_comment_ratio(file_path: str, encoding="UTF-8", min_comment_ratio=0.2):
    """检查Python代码文件的注释量是否合格。

    Args:
        file_path: Python代码文件的路径
        encoding: python编码, 默认UTF-8
        min_comment_ratio: 最低注释比例, 默认为0.2。

    Returns:
        返回一个元组, 0为代码总行数, 1为注释量比例, 2为是否合格, True或False
    """
    with open(file_path, 'r', encoding=encoding) as file:
        lines = file.readlines()

    total_lines = len(lines)
    comment_lines = 0
    for line in lines:
        line = line.strip()
        if line.startswith('#'):
            comment_lines += 1
        elif line.startswith('"""') or line.startswith("'''"):
            comment_lines += 1
        elif line.startswith('"""') and line.endswith('"""'):
            comment_lines += 1
        elif line.startswith("'''") and line.endswith("'''"):
            comment_lines += 1
    if total_lines != 0:
        comment_ratio = round(comment_lines / total_lines, 3)
        if comment_ratio >= min_comment_ratio:
            return total_lines, comment_ratio, True
        else:
            return total_lines, comment_ratio, False
    else:
        return 0, None, None

def print_folder_comment_ratio(folder_path: str, max_workers=20, encoding="UTF-8", min_comment_ratio=0.2):
    """检查文件夹下Python代码文件的注释量是否合格并打印出来。

    Args:
        folder_path: 文件夹路径
        max_workers: 提交线程数, 默认20个
        encoding: python编码, 默认UTF-8
        min_comment_ratio: 最低注释比例, 默认为0.2。
    """
    Threads = []
    with ThreadPoolExecutor(max_workers=max_workers) as exe:
        for root, paths, files in os.walk(folder_path):
            for file in files:
                file_path = Path(root, file)
                if file_path.suffix == ".py":
                    Threads.append(exe.submit(check_comment_ratio, file_path, encoding, min_comment_ratio))
    for thread in Threads:
        ratio = thread.result()
        print(f"python文件【{file_path.name}】的注释量【合格】, 一共有【{ratio[0]}】行代码, 注释量达【{ratio[1] * 100}%】" 
              if ratio[2] else f"python文件【{file_path.name}】的注释量【不合格】, 一共有【{ratio[0]}】行代码, 注释量只占【{ratio[1] * 100}%】" if
            ratio[2] is False else f"python文件【{file_path.name}】没有代码, 为【空】")