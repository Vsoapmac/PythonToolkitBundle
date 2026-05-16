# -*- coding: utf-8 -*-
# 基于 Polars 的数据处理工具类, 提供接近 pandas 的 API 体验, 同时利用 Polars 的高性能
# ------------ common ------------
from pathlib import Path
from typing import (
    Any,
    Dict,
    List,
    Literal,
    Optional,
    Sequence,
    Tuple,
    Union
)

# ------------ polars ------------
import polars as pl
from polars.dataframe import DataFrame as PolarsDataFrame
from polars.series import Series as PolarsSeries


class PolarsUtils:
    """基于 Polars 的数据处理工具类, API 设计贴近 pandas 的使用习惯

    在底层使用 Polars 的高性能 DataFrame 引擎, 但对外暴露的方法名和行为
    尽量与 pandas 保持一致, 降低迁移成本。

    Usage:
        >>> df = PolarsUtils.read_csv("data.csv")
        >>> df.head()
        >>> filtered = df[df["age"] > 18]
        >>> grouped = df.groupby("city").agg({"score": "mean"})
    """
    _data: Optional[PolarsDataFrame] = None  # 内部持有的 Polars DataFrame

    def __init__(self, data: Optional[Any] = None):
        """初始化 PolarsUtils

        Args:
            data (Optional[Any]): 初始化数据, 支持 Polars DataFrame、PolarsUtils 对象或 None

        Example:
            >>> df = PolarsUtils()
            >>> df2 = PolarsUtils(pl.DataFrame({"x": [1, 2, 3]}))
        """
        if data is None:
            self._data = pl.DataFrame()
        elif isinstance(data, PolarsUtils):
            self._data = data._data.clone()
        elif isinstance(data, PolarsDataFrame):
            self._data = data.clone()
        else:
            self._data = pl.DataFrame(data)

    # region ---------------------------- 属性访问(pandas 兼容) ----------------------------

    @property
    def shape(self) -> Tuple[int, int]:
        """返回 DataFrame 的形状 (行数, 列数)

        Returns:
            Tuple[int, int]: (行数, 列数)

        Example:
            >>> df = PolarsUtils({"a": [1, 2], "b": [3, 4]})
            >>> df.shape
            (2, 2)
        """
        return self._data.shape

    @property
    def columns(self) -> List[str]:
        """返回列名列表

        Returns:
            List[str]: 列名列表

        Example:
            >>> df = PolarsUtils({"a": [1], "b": [2]})
            >>> df.columns
            ['a', 'b']
        """
        return self._data.columns

    @property
    def dtypes(self) -> Dict[str, str]:
        """返回每列的数据类型字典

        Returns:
            Dict[str, str]: 列名到类型名称的映射

        Example:
            >>> df = PolarsUtils({"a": [1], "b": [1.0]})
            >>> list(df.dtypes.keys())
            ['a', 'b']
        """
        return {col.name: str(col.dtype) for col in self._data}

    @property
    def size(self) -> int:
        """返回 DataFrame 中的元素总数

        Returns:
            int: 元素总数

        Example:
            >>> df = PolarsUtils({"a": [1, 2], "b": [3, 4]})
            >>> df.size
            4
        """
        return self._data.height * self._data.width

    @property
    def empty(self) -> bool:
        """判断 DataFrame 是否为空

        Returns:
            bool: 是否为空

        Example:
            >>> df = PolarsUtils()
            >>> df.empty
            True
        """
        return self._data.is_empty()

    @property
    def values(self) -> List[List[Any]]:
        """返回数据的嵌套列表形式

        Returns:
            List[List[Any]]: 二维列表数据

        Example:
            >>> df = PolarsUtils({"a": [1, 2]})
            >>> df.values
            [(1,), (2,)]
        """
        return self._data.rows()

    def __len__(self) -> int:
        """返回行数"""
        return self._data.height

    def __repr__(self) -> str:
        """返回 DataFrame 的字符串表示"""
        return self._data.__repr__()

    def __getitem__(self, key: Any) -> Any:
        """支持类似 pandas 的索引和切片操作

        Args:
            key: 支持列名(str)、列名列表(list of str)、布尔表达式(pl.Expr) 和 Polars 表达式

        Returns:
            Any: 根据 key 类型返回 PolarsSeries、PolarsUtils 或值

        Example:
            >>> df = PolarsUtils({"name": ["A", "B"], "age": [20, 30]})
            >>> df["name"]  # 取单列
            >>> df[df["age"] > 20]  # 布尔过滤
        """
        if isinstance(key, str):
            return self._data[key]
        elif isinstance(key, list):
            return PolarsUtils(self._data.select(key))
        elif isinstance(key, PolarsSeries):
            return PolarsUtils(self._data.filter(key.to_physical().cast(pl.Boolean)))
        elif isinstance(key, pl.Expr):
            return PolarsUtils(self._data.filter(key))
        return PolarsUtils(self._data.__getitem__(key))

    def __setitem__(self, key: str, value: Any):
        """支持类似 pandas 的列赋值

        Args:
            key (str): 列名
            value (Any): 列数据

        Example:
            >>> df = PolarsUtils({"a": [1, 2]})
            >>> df["b"] = [3, 4]
        """
        if isinstance(value, PolarsUtils):
            self._data = self._data.with_columns(value._data.to_series().alias(key))
        elif isinstance(value, PolarsSeries):
            self._data = self._data.with_columns(value.alias(key))
        else:
            self._data = self._data.with_columns(pl.Series(key, value))

    # endregion ---------------------------- 属性访问(pandas 兼容) ----------------------------

    # region ---------------------------- I/O 类方法(类似 pandas.read_*) ----------------------------

    @classmethod
    def read_csv(cls, file_path: Union[str, Path], **kwargs) -> "PolarsUtils":
        """读取 CSV 文件(类似 pandas.read_csv)

        Args:
            file_path (Union[str, Path]): CSV 文件路径
            **kwargs: 传递给 polars.read_csv 的额外参数

        Returns:
            PolarsUtils: 包含 CSV 数据的 PolarsUtils 对象

        Example:
            >>> df = PolarsUtils.read_csv("data.csv")
            >>> df.shape
            (100, 5)
        """
        return cls(pl.read_csv(file_path, **kwargs))

    @classmethod
    def read_excel(cls, file_path: Union[str, Path], sheet_name: Optional[str] = None, **kwargs) -> "PolarsUtils":
        """读取 Excel 文件(类似 pandas.read_excel)

        Args:
            file_path (Union[str, Path]): Excel 文件路径
            sheet_name (Optional[str]): 工作表名称, 为 None 时读取第一个工作表
            **kwargs: 传递给 polars.read_excel 的额外参数

        Returns:
            PolarsUtils: 包含 Excel 数据的 PolarsUtils 对象

        Example:
            >>> df = PolarsUtils.read_excel("data.xlsx", sheet_name="Sheet1")
            >>> df.shape
            (50, 3)
        """
        return cls(pl.read_excel(file_path, sheet_name=sheet_name, **kwargs))

    @classmethod
    def read_parquet(cls, file_path: Union[str, Path], **kwargs) -> "PolarsUtils":
        """读取 Parquet 文件

        Args:
            file_path (Union[str, Path]): Parquet 文件路径
            **kwargs: 传递给 polars.read_parquet 的额外参数

        Returns:
            PolarsUtils: 包含 Parquet 数据的 PolarsUtils 对象

        Example:
            >>> df = PolarsUtils.read_parquet("data.parquet")
            >>> df.shape
            (200, 10)
        """
        return cls(pl.read_parquet(file_path, **kwargs))

    @classmethod
    def read_json(cls, file_path: Union[str, Path], **kwargs) -> "PolarsUtils":
        """读取 JSON 文件

        Args:
            file_path (Union[str, Path]): JSON 文件路径
            **kwargs: 传递给 polars.read_json 的额外参数

        Returns:
            PolarsUtils: 包含 JSON 数据的 PolarsUtils 对象

        Example:
            >>> df = PolarsUtils.read_json("data.json")
            >>> df.shape
            (30, 4)
        """
        return cls(pl.read_json(file_path, **kwargs))

    # endregion ---------------------------- I/O 类方法(类似 pandas.read_*) ----------------------------

    # region ---------------------------- 数据预览方法 ----------------------------

    def head(self, n: int = 5) -> "PolarsUtils":
        """返回前 n 行数据(类似 pandas.DataFrame.head)

        Args:
            n (int): 返回的行数, 默认为 5

        Returns:
            PolarsUtils: 包含前 n 行数据的 PolarsUtils 对象

        Example:
            >>> df = PolarsUtils({"a": [1, 2, 3, 4, 5, 6]})
            >>> df.head(3).shape
            (3, 1)
        """
        return PolarsUtils(self._data.head(n))

    def tail(self, n: int = 5) -> "PolarsUtils":
        """返回后 n 行数据(类似 pandas.DataFrame.tail)

        Args:
            n (int): 返回的行数, 默认为 5

        Returns:
            PolarsUtils: 包含后 n 行数据的 PolarsUtils 对象

        Example:
            >>> df = PolarsUtils({"a": [1, 2, 3, 4]})
            >>> df.tail(2).shape
            (2, 1)
        """
        return PolarsUtils(self._data.tail(n))

    def sample(self, n: Optional[int] = None, frac: Optional[float] = None, seed: Optional[int] = None) -> "PolarsUtils":
        """随机采样行数据(类似 pandas.DataFrame.sample)

        Args:
            n (Optional[int]): 指定采样行数
            frac (Optional[float]): 指定采样比例, 与 n 互斥
            seed (Optional[int]): 随机种子

        Returns:
            PolarsUtils: 采样结果

        Example:
            >>> df = PolarsUtils({"a": [1, 2, 3, 4, 5]})
            >>> df.sample(n=2).shape
            (2, 1)
        """
        if frac is not None:
            n = int(self._data.height * frac)
        return PolarsUtils(self._data.sample(n=n, seed=seed))

    def describe(self) -> "PolarsUtils":
        """返回数值列的统计摘要(类似 pandas.DataFrame.describe)

        Returns:
            PolarsUtils: 统计摘要结果

        Example:
            >>> df = PolarsUtils({"a": [1, 2, 3], "b": [4, 5, 6]})
            >>> desc = df.describe()
            >>> desc.shape[0] > 0
            True
        """
        return PolarsUtils(self._data.describe())

    def info(self) -> str:
        """打印 DataFrame 的简要信息(类似 pandas.DataFrame.info)

        Returns:
            str: 信息字符串

        Example:
            >>> df = PolarsUtils({"a": [1, 2], "b": [3.0, 4.0]})
            >>> info_str = df.info()
            >>> "a" in info_str
            True
        """
        lines = [f"<class 'PolarsUtils'>"]
        lines.append(f"行数: {self._data.height}, 列数: {self._data.width}")
        lines.append("")
        for col in self._data.columns:
            series = self._data[col]
            dtype = series.dtype
            null_count = series.null_count()
            lines.append(f"  #{self._data.columns.index(col)}  {col}  {null_count} non-null  {dtype}")
        lines.append(f"数据类型: {self._data.dtypes}")
        return "\n".join(lines)

    # endregion ---------------------------- 数据预览方法 ----------------------------

    # region ---------------------------- 数据操作(pandas 兼容) ----------------------------

    def rename(self, mapper: Dict[str, str]) -> "PolarsUtils":
        """重命名列(类似 pandas.DataFrame.rename)

        Args:
            mapper (Dict[str, str]): 旧列名到新列名的映射

        Returns:
            PolarsUtils: 重命名后的结果

        Example:
            >>> df = PolarsUtils({"old": [1, 2]})
            >>> df.rename({"old": "new"}).columns
            ['new']
        """
        return PolarsUtils(self._data.rename(mapper))

    def drop(self, columns: Union[str, List[str]]) -> "PolarsUtils":
        """删除指定列(类似 pandas.DataFrame.drop)

        Args:
            columns (Union[str, List[str]]): 要删除的列名或列名列表

        Returns:
            PolarsUtils: 删除列后的结果

        Example:
            >>> df = PolarsUtils({"a": [1], "b": [2], "c": [3]})
            >>> df.drop(["a", "b"]).columns
            ['c']
        """
        if isinstance(columns, str):
            columns = [columns]
        return PolarsUtils(self._data.drop(columns))

    def fillna(self, value: Any) -> "PolarsUtils":
        """填充空值(类似 pandas.DataFrame.fillna)

        Args:
            value (Any): 用于填充空值的值

        Returns:
            PolarsUtils: 填充后的结果

        Example:
            >>> import polars as pl
            >>> df = PolarsUtils({"a": [1, pl.Null, 3]})
            >>> df.fillna(0).to_dict()
            {'a': [1, 0, 3]}
        """
        return PolarsUtils(self._data.fill_null(value))

    def dropna(self, subset: Optional[Union[str, List[str]]] = None) -> "PolarsUtils":
        """删除包含空值的行(类似 pandas.DataFrame.dropna)

        Args:
            subset (Optional[Union[str, List[str]]]): 检查空值的列子集

        Returns:
            PolarsUtils: 删除空值行后的结果

        Example:
            >>> import polars as pl
            >>> df = PolarsUtils({"a": [1, pl.Null, 3]})
            >>> df.dropna().shape
            (2, 1)
        """
        if subset is not None:
            if isinstance(subset, str):
                subset = [subset]
            return PolarsUtils(self._data.drop_nulls(subset=subset))
        return PolarsUtils(self._data.drop_nulls())

    def sort_values(self, by: Union[str, List[str]], ascending: Union[bool, List[bool]] = True) -> "PolarsUtils":
        """按指定列排序(类似 pandas.DataFrame.sort_values)

        Args:
            by (Union[str, List[str]]): 排序依据的列名
            ascending (Union[bool, List[bool]]): 升序或降序, 默认为 True

        Returns:
            PolarsUtils: 排序后的结果

        Example:
            >>> df = PolarsUtils({"a": [3, 1, 2]})
            >>> df.sort_values("a").to_dict()
            {'a': [1, 2, 3]}
        """
        if isinstance(by, str):
            by = [by]
        if isinstance(ascending, bool):
            ascending = [ascending]
        if len(by) == 1:
            return PolarsUtils(self._data.sort(by[0], descending=not ascending[0]))
        result = self._data
        for col_name, is_ascending in zip(reversed(by), reversed(ascending)):
            result = result.sort(col_name, descending=not is_ascending)
        return PolarsUtils(result)

    def query(self, expression: str) -> "PolarsUtils":
        """使用 Polars 表达式语法过滤数据(类似 pandas.DataFrame.query 但使用 Polars 语法)

        Args:
            expression (str): Polars 表达式字符串, 如 "pl.col('age') > 18"

        Returns:
            PolarsUtils: 过滤后的结果

        Example:
            >>> df = PolarsUtils({"age": [15, 25, 35]})
            >>> df.query("pl.col('age') > 18").shape
            (2, 1)
        """
        expr = eval(expression)
        return PolarsUtils(self._data.filter(expr))

    def copy(self) -> "PolarsUtils":
        """返回 DataFrame 的深拷贝

        Returns:
            PolarsUtils: 拷贝结果

        Example:
            >>> df1 = PolarsUtils({"a": [1, 2]})
            >>> df2 = df1.copy()
            >>> df2["a"] = [3, 4]
            >>> df1.to_dict()["a"][0] == 1
            True
        """
        return PolarsUtils(self._data.clone())

    # endregion ---------------------------- 数据操作(pandas 兼容) ----------------------------

    # region ---------------------------- 分组与聚合 ----------------------------

    def groupby(self, by: Union[str, List[str]]) -> "_GroupBy":
        """按指定列分组(类似 pandas.DataFrame.groupby)

        Args:
            by (Union[str, List[str]]): 分组依据的列名

        Returns:
            _GroupBy: 分组对象, 支持 .agg() 操作

        Example:
            >>> df = PolarsUtils({"city": ["BJ", "SH", "BJ"], "score": [80, 90, 85]})
            >>> result = df.groupby("city").agg({"score": "mean"})
            >>> "BJ" in str(result.to_dict())
            True
        """
        return _GroupBy(self._data, by)

    def pivot(self, index: Union[str, List[str]], columns: Union[str, List[str]],
              values: Union[str, List[str]], agg: str = "first") -> "PolarsUtils":
        """数据透视(类似 pandas.DataFrame.pivot / pivot_table)

        Args:
            index (Union[str, List[str]]): 行索引列
            columns (Union[str, List[str]]): 列索引列
            values (Union[str, List[str]]): 值列
            agg (str): 聚合函数名, 默认为 "first"

        Returns:
            PolarsUtils: 透视结果

        Example:
            >>> df = PolarsUtils({"city": ["BJ", "SH"], "year": [2020, 2020], "val": [100, 200]})
            >>> result = df.pivot(index="year", columns="city", values="val")
            >>> result.shape[1] >= 2
            True
        """
        return PolarsUtils(self._data.pivot(
            index=index, on=columns, values=values, aggregate_function=agg
        ))

    def melt(self, id_vars: Union[str, List[str]], value_vars: Union[str, List[str]],
             var_name: str = "variable", value_name: str = "value") -> "PolarsUtils":
        """将宽表转为长表(类似 pandas.melt)

        Args:
            id_vars (Union[str, List[str]]): 标识变量列
            value_vars (Union[str, List[str]]): 值变量列
            var_name (str): 变量名列名, 默认为 "variable"
            value_name (str): 值列名, 默认为 "value"

        Returns:
            PolarsUtils: 转换后的长表

        Example:
            >>> df = PolarsUtils({"id": [1], "a": [10], "b": [20]})
            >>> melted = df.melt(id_vars="id", value_vars=["a", "b"])
            >>> melted.shape
            (2, 3)
        """
        return PolarsUtils(self._data.unpivot(
            index=id_vars, on=value_vars,
            variable_name=var_name, value_name=value_name
        ))

    # endregion ---------------------------- 分组与聚合 ----------------------------

    # region ---------------------------- 合并与连接 ----------------------------

    def merge(self, right: "PolarsUtils", on: Optional[Union[str, List[str]]] = None,
              how: Literal["inner", "left", "outer", "cross"] = "inner",
              suffixes: Tuple[str, str] = ("_x", "_y")) -> "PolarsUtils":
        """合并两个 DataFrame(类似 pandas.DataFrame.merge)

        Args:
            right (PolarsUtils): 右侧 DataFrame
            on (Optional[Union[str, List[str]]]): 连接键列名
            how (str): 连接方式, 可选 inner/left/outer/cross, 默认为 inner
            suffixes (Tuple[str, str]): 重名列后缀, 默认为 ("_x", "_y")

        Returns:
            PolarsUtils: 合并结果

        Example:
            >>> left = PolarsUtils({"id": [1, 2], "val": ["a", "b"]})
            >>> right = PolarsUtils({"id": [1, 3], "val2": ["x", "y"]})
            >>> merged = left.merge(right, on="id")
            >>> merged.shape
            (1, 3)
        """
        right_df = right._data if isinstance(right, PolarsUtils) else right
        return PolarsUtils(self._data.join(right_df, on=on, how=how, suffix=suffixes[1]))

    def concat(self, others: List["PolarsUtils"]) -> "PolarsUtils":
        """纵向拼接多个 DataFrame(类似 pandas.concat)

        Args:
            others (List[PolarsUtils]): 其他 PolarsUtils 对象列表

        Returns:
            PolarsUtils: 拼接结果

        Example:
            >>> df1 = PolarsUtils({"a": [1]})
            >>> df2 = PolarsUtils({"a": [2]})
            >>> df1.concat([df2]).shape
            (2, 1)
        """
        all_dfs = [self._data] + [o._data for o in others]
        return PolarsUtils(pl.concat(all_dfs))

    # endregion ---------------------------- 合并与连接 ----------------------------

    # region ---------------------------- 输出方法 ----------------------------

    def to_dict(self, as_series: bool = False) -> Dict[str, Any]:
        """将 DataFrame 转为字典(类似 pandas.DataFrame.to_dict)

        Args:
            as_series (bool): 是否返回 Series 字典, 默认为 False(返回列表字典)

        Returns:
            Dict[str, Any]: 字典形式的数据

        Example:
            >>> df = PolarsUtils({"a": [1, 2]})
            >>> df.to_dict()
            {'a': [1, 2]}
        """
        if as_series:
            return {col: self._data[col] for col in self._data.columns}
        return self._data.to_dict(as_series=False)

    def to_dicts(self) -> List[Dict]:
        """将 DataFrame 转为字典列表(类似 pandas.DataFrame.to_dict)

        Returns:
            List[Dict]: 字典列表形式的数据

        Example:
            >>> df = PolarsUtils({"a": [1, 2]})
            >>> df.to_dicts()
            [{'a': 1}, {'a': 2}]
        """
        return self._data.to_dicts()
    
    def to_csv(self, file_path: Union[str, Path], **kwargs):
        """导出为 CSV 文件

        Args:
            file_path (Union[str, Path]): 输出路径
            **kwargs: 传递给 polars.DataFrame.write_csv 的参数

        Example:
            >>> df = PolarsUtils({"a": [1, 2]})
            >>> df.to_csv("/tmp/test_out.csv")
        """
        self._data.write_csv(file_path, **kwargs)

    def to_excel(self, file_path: Union[str, Path], sheet_name: str = "Sheet1"):
        """导出为 Excel 文件(需安装 xlsxwriter 或 openpyxl)

        Args:
            file_path (Union[str, Path]): 输出路径
            sheet_name (str): 工作表名称, 默认为 "Sheet1"

        Example:
            >>> df = PolarsUtils({"a": [1, 2]})
            >>> df.to_excel("/tmp/test_out.xlsx")
        """
        self._data.write_excel(file_path, sheet_name=sheet_name)

    def to_pandas(self):
        """转为 pandas DataFrame

        Returns:
            pd.DataFrame: pandas DataFrame

        Example:
            >>> df = PolarsUtils({"a": [1, 2]})
            >>> pd_df = df.to_pandas()
            >>> pd_df.shape[0]
            2
        """
        return self._data.to_pandas()

    def to_polars(self) -> PolarsDataFrame:
        """返回内部的 Polars DataFrame

        Returns:
            PolarsDataFrame: 内部的 Polars DataFrame

        Example:
            >>> df = PolarsUtils({"a": [1]})
            >>> pl_df = df.to_polars()
            >>> isinstance(pl_df, pl.DataFrame)
            True
        """
        return self._data.clone()

    # endregion ---------------------------- 输出方法 ----------------------------

    # region ---------------------------- 窗口与行操作 ----------------------------

    def apply(self, func, axis: int = 0, *args, **kwargs) -> "PolarsUtils":
        """对每列或每行应用函数(类似 pandas.DataFrame.apply)

        Args:
            func: 应用的函数
            axis (int): 0 表示对每列应用, 1 表示对每行应用
            *args: 传递给 func 的额外位置参数
            **kwargs: 传递给 func 的额外关键字参数

        Returns:
            PolarsUtils: 应用结果

        Example:
            >>> df = PolarsUtils({"a": [1.0, 2.0], "b": [3.0, 4.0]})
            >>> result = df.apply(lambda x: x.sum())
            >>> result.shape[1] == 2
            True
        """
        if axis == 0:
            result = {col: func(self._data[col], *args, **kwargs) for col in self._data.columns}
            return PolarsUtils(result)
        else:
            results = [func(row, *args, **kwargs) for row in self._data.iter_rows()]
            return PolarsUtils({"result": results})

    def unique(self, subset: Optional[Union[str, List[str]]] = None) -> "PolarsUtils":
        """返回唯一值行(类似 pandas.DataFrame.drop_duplicates)

        Args:
            subset (Optional[Union[str, List[str]]]): 检查唯一性的列子集

        Returns:
            PolarsUtils: 去重后的结果

        Example:
            >>> df = PolarsUtils({"a": [1, 1, 2]})
            >>> df.unique().shape
            (2, 1)
        """
        if subset is not None:
            if isinstance(subset, str):
                subset = [subset]
            return PolarsUtils(self._data.unique(subset=subset))
        return PolarsUtils(self._data.unique())

    def isin(self, column: str, values: Sequence[Any]) -> "PolarsUtils":
        """过滤某列值在指定集合中的行

        Args:
            column (str): 列名
            values (Sequence[Any]): 值的集合

        Returns:
            PolarsUtils: 过滤结果

        Example:
            >>> df = PolarsUtils({"a": [1, 2, 3]})
            >>> df.isin("a", [1, 3]).shape
            (2, 1)
        """
        return PolarsUtils(self._data.filter(pl.col(column).is_in(values)))

    # endregion ---------------------------- 窗口与行操作 ----------------------------

    def pipe(self, func, *args, **kwargs) -> Any:
        """支持链式调用(类似 pandas.DataFrame.pipe)

        Args:
            func: 对 DataFrame 进行变换的函数
            *args: 传递给 func 的位置参数
            **kwargs: 传递给 func 的关键字参数

        Returns:
            Any: 函数调用的结果

        Example:
            >>> df = PolarsUtils({"a": [3, 1, 2]})
            >>> result = df.pipe(lambda x: x.sort_values("a"))
            >>> result.to_dict()["a"]
            [1, 2, 3]
        """
        return func(self, *args, **kwargs)


class _GroupBy:
    """分组对象, 由 PolarsUtils.groupby 返回, 支持链式聚合操作"""
    _data: PolarsDataFrame  # 原始 DataFrame
    _by: Union[str, List[str]]  # 分组列名

    def __init__(self, data: PolarsDataFrame, by: Union[str, List[str]]):
        """初始化 _GroupBy

        Args:
            data (PolarsDataFrame): 原始 DataFrame
            by (Union[str, List[str]]): 分组列名
        """
        self._data = data
        self._by = by

    def agg(self, aggregations: Dict[str, str]) -> PolarsUtils:
        """执行聚合操作

        Args:
            aggregations (Dict[str, str]): 列名到聚合函数名的映射, 
                支持 sum/mean/count/min/max/std/var/first/last/median

        Returns:
            PolarsUtils: 聚合结果

        Example:
            >>> df = PolarsUtils({"g": ["a", "a", "b"], "v": [1, 2, 3]})
            >>> result = df.groupby("g").agg({"v": "sum"})
            >>> result.shape[0] == 2
            True
        """
        exprs = []
        for col_name, agg_func in aggregations.items():
            exprs.append(getattr(pl.col(col_name), agg_func)().alias(f"{col_name}_{agg_func}"))
        return PolarsUtils(self._data.group_by(self._by).agg(exprs))
