import pytest
import sys
import os
import tempfile
import json

# 添加src到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

@pytest.fixture
def sample_data():
    """提供样例数据"""
    return {
        "name": "测试数据",
        "value": 42,
        "nested": {
            "key": "value"
        },
        "list": [1, 2, 3]
    }

@pytest.fixture
def temp_file():
    """创建临时文件"""
    with tempfile.NamedTemporaryFile(mode='w', suffix='.json', delete=False) as f:
        yield f.name
    # 测试结束后删除临时文件
    if os.path.exists(f.name):
        os.unlink(f.name)

@pytest.fixture
def test_data_dir():
    """返回测试数据目录路径"""
    return os.path.join(os.path.dirname(__file__), 'data')

@pytest.fixture
def non_serializable_data():
    """提供不可序列化的数据"""
    return {
        "valid": "data",
        "invalid": object()  # 不可JSON序列化的对象
    }
