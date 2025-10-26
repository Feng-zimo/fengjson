import json
import logging
import os
from typing import Dict, Optional, Union

# 配置日志记录
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


def read_json_to_dict(file_path: str,
                      encoding: str = 'utf-8',
                      default: Optional[Dict] = None) -> Union[Dict, None]:
    """
    将 JSON 文件安全地读取为 Python 字典

    参数:
        file_path: JSON 文件路径
        encoding: 文件编码 (默认: 'utf-8')
        default: 读取失败时返回的默认值 (默认: None)

    返回:
        JSON 解析后的字典，或出错时返回 default 值
    """
    # 验证输入参数
    if not isinstance(file_path, str):
        logger.error(f"文件路径必须是字符串，收到: {type(file_path)}")
        return default

    if default is not None and not isinstance(default, dict):
        logger.error(f"默认值必须是字典类型，收到: {type(default)}")
        return None

    # 检查文件是否存在
    if not os.path.exists(file_path):
        logger.error(f"文件不存在: {file_path}")
        return default

    # 检查是否为文件
    if not os.path.isfile(file_path):
        logger.error(f"路径不是文件: {file_path}")
        return default

    try:
        # 打开并读取文件
        with open(file_path, 'r', encoding=encoding) as file:
            content = file.read()

            # 检查文件是否为空
            if not content.strip():
                logger.warning(f"文件为空: {file_path}")
                return default or {}

            # 解析 JSON
            data = json.loads(content)

            # 验证解析结果是否为字典
            if not isinstance(data, dict):
                logger.warning(f"JSON 内容不是字典对象: {type(data)}")
                return default or {}

            return data

    except UnicodeDecodeError as e:
        logger.error(f"编码错误 ({encoding}): {e}")
        return default
    except json.JSONDecodeError as e:
        logger.error(f"JSON 解析错误: {e}")
        return default
    except OSError as e:  # 包括文件权限问题等
        logger.error(f"文件操作错误: {e}")
        return default
    except Exception as e:
        logger.exception(f"未知错误: {e}")
        return default


def xiervjson(data: Dict,
                       file_path: str,
                       indent: int = 4,
                       encoding: str = 'utf-8',
                       ensure_ascii: bool = False) -> bool:
    """
    将字典安全地写入 JSON 文件

    参数:
        data: 要写入的字典数据
        file_path: 输出文件路径
        indent: JSON 缩进 (默认: 4)
        encoding: 文件编码 (默认: 'utf-8')
        ensure_ascii: 是否转义非 ASCII 字符 (默认: False)

    返回:
        成功返回 True，失败返回 False
        :rtype: bool
    """
    # 验证输入参数
    if not isinstance(data, dict):
        logger.error(f"输入数据必须是字典类型，收到: {type(data)}")
        return False

    if not isinstance(file_path, str):
        logger.error(f"文件路径必须是字符串，收到: {type(file_path)}")
        return False

    # 创建目录（如果不存在）
    dir_path = os.path.dirname(file_path)
    if dir_path and not os.path.exists(dir_path):
        try:
            os.makedirs(dir_path, exist_ok=True)
        except OSError as e:
            logger.error(f"无法创建目录 {dir_path}: {e}")
            return False

    try:
        # 尝试序列化数据（提前检测是否可序列化）
        json.dumps(data, indent=indent, ensure_ascii=ensure_ascii)

        # 写入文件
        with open(file_path, 'w', encoding=encoding) as file:
            json.dump(data, file, indent=indent, ensure_ascii=ensure_ascii)

        logger.info(f"成功写入 JSON 文件: {file_path}")
        return True

    except TypeError as e:
        logger.error(f"数据类型不支持 JSON 序列化: {e}")
        return False
    except OSError as e:
        logger.error(f"文件写入错误: {e}")
        return False
    except Exception as e:
        logger.exception(f"未知错误: {e}")
        return False


def json_to_dict(file_path: str,
                 target_dict: Optional[dict] = None,
                 encoding: str = 'utf-8') -> Union[dict, bool]:
    """
    处理JSON文件的通用函数

    参数:
        file_path: JSON文件路径
        target_dict: 可选的目标字典（用于更新）
        encoding: 文件编码

    返回:
        如果target_dict为None → 返回新字典（失败时返回空字典）
        如果target_dict提供 → 成功返回True，失败返回False
    """
    try:
        # 读取文件
        with open(file_path, 'r', encoding=encoding) as f:
            data = json.load(f)

        # 验证数据类型
        if not isinstance(data, dict):
            raise TypeError("JSON内容不是字典格式")

        # 更新模式
        if target_dict is not None:
            if not isinstance(target_dict, dict):
                raise TypeError("目标字典必须是dict类型")
            target_dict.update(data)
            return True

        # 返回模式
        return data

    except FileNotFoundError:
        logger.error(f"文件不存在: {file_path}")
    except json.JSONDecodeError as e:
        logger.error(f"JSON解析错误: {e}")
    except TypeError as e:
        logger.error(str(e))
    except Exception as e:
        logger.error(f"未知错误: {e}")

    # 错误处理
    return {} if target_dict is None else False