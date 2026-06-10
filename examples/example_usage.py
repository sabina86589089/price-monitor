#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
竞品价格监控系统 - 使用示例
"""

import sys
import os

# 添加父目录到路径
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from price_monitor import PriceMonitor


def main():
    """使用示例"""
    monitor = PriceMonitor()
    
    # 1. 添加产品
    print("=== 添加监控产品 ===")
    result1 = monitor.add_product(
        "https://item.taobao.com/item.htm?id=123456",
        "taobao",
        "测试产品A"
    )
    print(f"添加结果: {result1}")
    
    result2 = monitor.add_product(
        "https://item.jd.com/123456.html",
        "jd",
        "测试产品B"
    )
    print(f"添加结果: {result2}")
    
    # 2. 检查价格
    print("\n=== 检查价格 ===")
    check_results = monitor.check_all()
    for result in check_results:
        if "error" in result:
            print(f"错误: {result['error']}")
        else:
            print(f"产品: {result['name']}")
            print(f"  当前价格: ¥{result['current_price']}")
            print(f"  检查时间: {result['last_check']}")
            if result.get("alert"):
                print(f"  提醒: {result['alert']['message']}")
    
    # 3. 多次检查，观察价格变化
    print("\n=== 模拟多次检查 ===")
    for i in range(3):
        print(f"\n第 {i+1} 次检查:")
        results = monitor.check_all()
        for r in results:
            if "current_price" in r:
                print(f"  {r['name']}: ¥{r['current_price']}")
    
    # 4. 生成报告
    print("\n=== 价格报告 ===")
    report = monitor.get_report()
    for item in report:
        print(f"\n产品: {item['name']}")
        print(f"  平台: {item['platform']}")
        print(f"  当前价: ¥{item['current_price']}")
        print(f"  最低价: ¥{item['min_price']}")
        print(f"  最高价: ¥{item['max_price']}")
        print(f"  平均价: ¥{item['avg_price']}")
        print(f"  检查次数: {item['check_count']}")
    
    # 5. 删除产品（可选）
    # monitor.remove_product("123456")
    
    print("\n=== 完成 ===")
    print(f"数据已保存到: {monitor.data_file}")


if __name__ == "__main__":
    main()
