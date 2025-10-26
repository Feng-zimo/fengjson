import unittest
import sys
import os
import tempfile
import json

# 添加src到Python路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '../src'))

from fengjson.core import read_json_to_dict, xiervjson, json_to_dict


class TestReadJsonToDict(unittest.TestCase):
    """测试 read_json_to_dict 函数"""

    def setUp(self):
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_read_valid_json(self):
        """测试读取有效的JSON文件"""
        file_path = os.path.join(self.test_data_dir, 'valid_json.json')
        result = read_json_to_dict(file_path)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["name"], "测试用户")
        self.assertEqual(result["age"], 25)
        self.assertEqual(result["hobbies"], ["阅读", "编程", "音乐"])

    def test_read_nested_json(self):
        """测试读取嵌套的JSON文件"""
        file_path = os.path.join(self.test_data_dir, 'nested_json.json')
        result = read_json_to_dict(file_path)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["user"]["profile"]["name"], "张三")
        self.assertEqual(result["user"]["profile"]["settings"]["theme"], "dark")

    def test_read_empty_json(self):
        """测试读取空JSON文件"""
        file_path = os.path.join(self.test_data_dir, 'empty_json.json')
        result = read_json_to_dict(file_path)
        
        self.assertEqual(result, {})

    def test_read_nonexistent_file(self):
        """测试读取不存在的文件"""
        result = read_json_to_dict("nonexistent_file.json")
        self.assertIsNone(result)

    def test_read_nonexistent_file_with_default(self):
        """测试读取不存在的文件时返回默认值"""
        default = {"default": "value"}
        result = read_json_to_dict("nonexistent_file.json", default=default)
        self.assertEqual(result, default)

    def test_read_with_different_encoding(self):
        """测试使用不同编码读取文件"""
        file_path = os.path.join(self.test_data_dir, 'valid_json.json')
        result = read_json_to_dict(file_path, encoding='utf-8')
        self.assertIsInstance(result, dict)

    def test_invalid_file_path_type(self):
        """测试无效的文件路径类型"""
        result = read_json_to_dict(123)  # 非字符串路径
        self.assertIsNone(result)

    def test_invalid_default_type(self):
        """测试无效的默认值类型"""
        result = read_json_to_dict("test.json", default="invalid")  # 非字典默认值
        self.assertIsNone(result)

    def test_directory_instead_of_file(self):
        """测试传入目录而不是文件"""
        result = read_json_to_dict(self.test_data_dir)
        self.assertIsNone(result)


class TestXiervjson(unittest.TestCase):
    """测试 xiervjson 函数"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()
        self.test_data = {
            "name": "测试写入",
            "data": [1, 2, 3],
            "config": {
                "timeout": 30,
                "retry": True
            }
        }

    def tearDown(self):
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_write_valid_data(self):
        """测试写入有效数据"""
        file_path = os.path.join(self.temp_dir, 'test_output.json')
        result = xiervjson(self.test_data, file_path)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(file_path))
        
        # 验证写入的内容
        with open(file_path, 'r', encoding='utf-8') as f:
            written_data = json.load(f)
        self.assertEqual(written_data, self.test_data)

    def test_write_to_nonexistent_directory(self):
        """测试写入到不存在的目录"""
        file_path = os.path.join(self.temp_dir, 'new_dir', 'test.json')
        result = xiervjson(self.test_data, file_path)
        
        self.assertTrue(result)
        self.assertTrue(os.path.exists(file_path))

    def test_write_non_dict_data(self):
        """测试写入非字典数据"""
        file_path = os.path.join(self.temp_dir, 'test.json')
        result = xiervjson(["list", "data"], file_path)
        
        self.assertFalse(result)
        self.assertFalse(os.path.exists(file_path))

    def test_write_with_invalid_file_path(self):
        """测试使用无效文件路径"""
        result = xiervjson(self.test_data, 123)  # 非字符串路径
        self.assertFalse(result)

    def test_write_with_special_characters(self):
        """测试写入包含特殊字符的数据"""
        test_data = {
            "unicode": "中文测试 🚀",
            "special_chars": "line1\nline2\ttab",
            "emojis": "😀🎉🌟"
        }
        file_path = os.path.join(self.temp_dir, 'special_chars.json')
        result = xiervjson(test_data, file_path, ensure_ascii=False)
        
        self.assertTrue(result)
        
        # 验证特殊字符正确保存
        with open(file_path, 'r', encoding='utf-8') as f:
            written_data = json.load(f)
        self.assertEqual(written_data, test_data)

    def test_write_with_different_indent(self):
        """测试使用不同缩进写入"""
        file_path = os.path.join(self.temp_dir, 'test_indent.json')
        result = xiervjson(self.test_data, file_path, indent=2)
        
        self.assertTrue(result)
        
        # 检查文件内容
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()
        self.assertIn('\n  "', content)  # 检查缩进


class TestJsonToDict(unittest.TestCase):
    """测试 json_to_dict 函数"""

    def setUp(self):
        self.test_data_dir = os.path.join(os.path.dirname(__file__), 'data')

    def test_json_to_dict_return_mode(self):
        """测试返回模式（无target_dict）"""
        file_path = os.path.join(self.test_data_dir, 'valid_json.json')
        result = json_to_dict(file_path)
        
        self.assertIsInstance(result, dict)
        self.assertEqual(result["name"], "测试用户")

    def test_json_to_dict_update_mode(self):
        """测试更新模式（有target_dict）"""
        file_path = os.path.join(self.test_data_dir, 'valid_json.json')
        target_dict = {"existing": "data"}
        
        result = json_to_dict(file_path, target_dict=target_dict)
        
        self.assertTrue(result)
        self.assertEqual(target_dict["existing"], "data")
        self.assertEqual(target_dict["name"], "测试用户")

    def test_json_to_dict_nonexistent_file(self):
        """测试读取不存在的文件"""
        result = json_to_dict("nonexistent.json")
        self.assertEqual(result, {})  # 应该返回空字典
        
        target_dict = {}
        result = json_to_dict("nonexistent.json", target_dict=target_dict)
        self.assertFalse(result)  # 更新模式返回False

    def test_json_to_dict_invalid_target_dict(self):
        """测试无效的target_dict"""
        file_path = os.path.join(self.test_data_dir, 'valid_json.json')
        result = json_to_dict(file_path, target_dict="invalid")
        
        self.assertFalse(result)

    def test_json_to_dict_with_empty_json(self):
        """测试读取空JSON文件"""
        file_path = os.path.join(self.test_data_dir, 'empty_json.json')
        result = json_to_dict(file_path)
        
        self.assertEqual(result, {})


class TestIntegration(unittest.TestCase):
    """集成测试：读写组合测试"""

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp()

    def tearDown(self):
        import shutil
        if os.path.exists(self.temp_dir):
            shutil.rmtree(self.temp_dir)

    def test_read_write_cycle(self):
        """测试完整的读写循环"""
        original_data = {
            "test": "集成测试",
            "numbers": [1, 2, 3],
            "nested": {"key": "value"}
        }
        
        # 写入文件
        file_path = os.path.join(self.temp_dir, 'integration_test.json')
        write_result = xiervjson(original_data, file_path)
        self.assertTrue(write_result)
        
        # 读取文件
        read_result = read_json_to_dict(file_path)
        self.assertEqual(read_result, original_data)
        
        # 使用json_to_dict读取
        dict_result = json_to_dict(file_path)
        self.assertEqual(dict_result, original_data)

    def test_update_existing_dict(self):
        """测试更新现有字典"""
        file_path = os.path.join(self.test_data_dir, 'valid_json.json')
        existing_dict = {"custom": "data"}
        
        # 更新字典
        result = json_to_dict(file_path, target_dict=existing_dict)
        self.assertTrue(result)
        
        # 验证合并结果
        self.assertEqual(existing_dict["custom"], "data")
        self.assertEqual(existing_dict["name"], "测试用户")


if __name__ == '__main__':
    unittest.main()
