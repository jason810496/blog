---
title: "2025 01 02 Write Unit Test With Mock in Python"
summary: ""
description: ""
date: 2025-02-07T15:43:40+08:00
slug: "write-unit-test-with-mock-in-python"
tags: ["blog","zh-tw"]
# series: ["Documentation"]
# series_order: 9
cascade:
  showEdit: true
  showSummary: true
  hideFeatureImage: false
draft: false
---

## 使用 Mock 撰寫 Python 單元測試的最佳實踐

在撰寫 Python 單元測試時，Mock 是一個非常有用的工具。它允許我們替換掉程式碼中的某些部分，以便我們可以專注於測試特定的功能，而不需要依賴外部資源或其他不相關的部分。以下是一些使用 Mock 的最佳實踐：

### 1. 安裝 Mock

在 Python 3.3 及以上版本中，`unittest.mock` 模組已經內建於標準庫中。如果你使用的是較舊版本的 Python，可以安裝 `mock` 套件：

```bash
pip install mock
```

### 2. 基本用法

以下是一個簡單的例子，展示如何使用 Mock 來替換一個函數：

```python
import unittest
from unittest.mock import Mock

def get_data():
  # 假設這個函數會從某個外部資源獲取資料
  pass

class TestGetData(unittest.TestCase):
  def test_get_data(self):
    # 創建一個 Mock 物件
    mock_get_data = Mock(return_value="mocked data")
    
    # 使用 Mock 物件替換原始的 get_data 函數
    get_data = mock_get_data
    
    # 測試 get_data 函數
    result = get_data()
    self.assertEqual(result, "mocked data")

if __name__ == '__main__':
  unittest.main()
```

### 3. Mock 方法和屬性

Mock 物件可以模擬方法和屬性，這對於測試類別和物件的行為非常有用：

```python
class MyClass:
  def method(self):
    pass

def function_to_test(obj):
  return obj.method()

class TestFunction(unittest.TestCase):
  def test_function_to_test(self):
    mock_obj = Mock()
    mock_obj.method.return_value = "mocked method"
    
    result = function_to_test(mock_obj)
    self.assertEqual(result, "mocked method")

if __name__ == '__main__':
  unittest.main()
```

### 4. 使用 `patch` 裝飾器

`patch` 裝飾器是一個方便的工具，可以臨時替換模組或類別中的物件：

```python
from unittest.mock import patch

@patch('module_under_test.ClassName')
def test_function(mock_class):
  instance = mock_class.return_value
  instance.method.return_value = "mocked method"
  
  result = function_to_test(instance)
  assert result == "mocked method"
```

### 5. 清理 Mock

在測試結束後，確保 Mock 物件被正確清理，以避免對其他測試造成影響。這可以通過 `patch` 裝飾器或 `patch` 上下文管理器來實現：

```python
from unittest.mock import patch

def test_function():
  with patch('module_under_test.ClassName') as mock_class:
    instance = mock_class.return_value
    instance.method.return_value = "mocked method"
    
    result = function_to_test(instance)
    assert result == "mocked method"
```

### 結論

使用 Mock 可以讓我們在撰寫單元測試時更加靈活，並且能夠專注於測試的核心邏輯。通過遵循這些最佳實踐，你可以更有效地撰寫和維護你的 Python 測試代碼。