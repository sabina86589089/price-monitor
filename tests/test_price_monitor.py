#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
价格监控系统 - 单元测试
"""

import unittest
import sys
import os
from pathlib import Path

# 添加父目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent))

from price_monitor import PriceMonitor


class TestPriceMonitor(unittest.TestCase):
    """价格监控器测试用例"""
    
    def setUp(self):
        """测试前准备"""
        self.test_data_file = "test_price_data.json"
        self.monitor = PriceMonitor(data_file=self.test_data_file)
    
    def tearDown(self):
        """测试后清理"""
        if os.path.exists(self.test_data_file):
            os.remove(self.test_data_file)
    
    def test_add_product(self):
        """测试添加产品"""
        result = self.monitor.add_product(
            "https://item.taobao.com/item.htm?id=123456",
            "taobao",
            "测试产品"
        )
        self.assertIn("success", result)
        self.assertEqual(len(self.monitor.products), 1)
    
    def test_add_product_invalid_url(self):
        """测试添加无效URL"""
        result = self.monitor.add_product(
            "invalid_url",
            "taobao",
            "测试产品"
        )
        # 应该成功（使用哈希作为ID）
        self.assertIn("success", result)
    
    def test_remove_product(self):
        """测试删除产品"""
        # 先添加
        self.monitor.add_product(
            "https://item.taobao.com/item.htm?id=123456",
            "taobao",
            "测试产品"
        )
        
        # 获取产品ID
        product_id = list(self.monitor.products.keys())[0]
        
        # 删除
        result = self.monitor.remove_product(product_id)
        self.assertIn("success", result)
        self.assertEqual(len(self.monitor.products), 0)
    
    def test_remove_nonexistent_product(self):
        """测试删除不存在的产品"""
        result = self.monitor.remove_product("nonexistent")
        self.assertIn("error", result)
    
    def test_check_price(self):
        """测试价格检查"""
        # 添加产品
        self.monitor.add_product(
            "https://item.taobao.com/item.htm?id=123456",
            "taobao",
            "测试产品"
        )
        
        # 获取产品ID
        product_id = list(self.monitor.products.keys())[0]
        
        # 检查价格
        result = self.monitor.check_price(product_id)
        self.assertIn("current_price", result)
        self.assertIn("alert", result)
    
    def test_check_all(self):
        """测试检查所有产品"""
        # 添加多个产品
        self.monitor.add_product(
            "https://item.taobao.com/item.htm?id=123456",
            "taobao",
            "产品A"
        )
        self.monitor.add_product(
            "https://item.jd.com/789012.html",
            "jd",
            "产品B"
        )
        
        # 检查所有
        results = self.monitor.check_all()
        self.assertEqual(len(results), 2)
    
    def test_get_report(self):
        """测试生成报告"""
        # 添加产品并检查价格
        self.monitor.add_product(
            "https://item.taobao.com/item.htm?id=123456",
            "taobao",
            "测试产品"
        )
        
        product_id = list(self.monitor.products.keys())[0]
        self.monitor.check_price(product_id)
        
        # 生成报告
        report = self.monitor.get_report(product_id)
        self.assertEqual(len(report), 1)
        self.assertIn("current_price", report[0])
        self.assertIn("min_price", report[0])
    
    def test_price_alert(self):
        """测试价格提醒功能"""
        # 添加产品
        self.monitor.add_product(
            "https://item.taobao.com/item.htm?id=123456",
            "taobao",
            "测试产品"
        )
        
        product_id = list(self.monitor.products.keys())[0]
        
        # 第一次检查（生成初始价格）
        result1 = self.monitor.check_price(product_id)
        initial_price = result1["current_price"]
        
        # 手动修改最后一次检查的价格，模拟大幅降价
        product = self.monitor.products[product_id]
        # 确保有至少2条记录
        if len(product["price_history"]) < 2:
            # 添加第二条记录，价格降低10%
            product["price_history"].append({
                "time": "2026-06-10T20:00:00",
                "price": initial_price * 0.85  # 降价15%
            })
        
        # 第三次检查（应该触发alert）
        result = self.monitor.check_price(product_id)
        
        # 应该有提醒（价格变化>5%）
        self.assertIsNotNone(result.get("alert"))


if __name__ == "__main__":
    unittest.main()
