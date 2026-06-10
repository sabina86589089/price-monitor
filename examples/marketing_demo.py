#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
竞品价格监控系统 - 营销Demo
展示核心价值：帮助电商卖家/创业者监控竞品价格，优化决策
"""

import json
import time
from datetime import datetime, timedelta
from pathlib import Path


class PriceMonitorDemo:
    """Demo版价格监控器 - 模拟真实场景"""
    
    def __init__(self):
        self.products = {
            "taobao_123456": {
                "name": "无线蓝牙耳机Pro版",
                "platform": "taobao",
                "url": "https://item.taobao.com/item.htm?id=123456",
                "price_history": self._generate_mock_history(399, 299, 30),
                "competitors": [
                    {"name": "京东同款", "price": 349, "platform": "jd"},
                    {"name": "拼多多同款", "price": 279, "platform": "pinduoduo"}
                ]
            },
            "jd_789012": {
                "name": "机械键盘 Cherry轴",
                "platform": "jd",
                "url": "https://item.jd.com/789012.html",
                "price_history": self._generate_mock_history(599, 499, 30),
                "competitors": [
                    {"name": "淘宝同款", "price": 569, "platform": "taobao"},
                    {"name": "拼多多同款", "price": 459, "platform": "pinduoduo"}
                ]
            }
        }
    
    def _generate_mock_history(self, high_price, low_price, days):
        """生成模拟价格历史（先高后低，模拟降价）"""
        history = []
        base_time = datetime.now() - timedelta(days=days)
        
        for i in range(days):
            # 前20天高价，后10天降价
            if i < 20:
                price = high_price - (i * 2) + (i % 3 * 5)
            else:
                price = low_price + ((i - 20) * 3) + (i % 2 * 10)
            
            history.append({
                "time": (base_time + timedelta(days=i)).isoformat(),
                "price": max(price, low_price)  # 不低于最低价
            })
        
        return history
    
    def show_demo(self):
        """展示完整demo"""
        print("=" * 60)
        print("竞品价格监控系统 - 价值展示")
        print("=" * 60)
        print()
        
        # 1. 展示监控的产品
        self._show_monitored_products()
        
        # 2. 展示价格趋势分析
        self._show_price_trends()
        
        # 3. 展示竞品对比
        self._show_competitor_comparison()
        
        # 4. 展示降价提醒
        self._show_price_alert()
        
        # 5. 展示商业价值
        self._show_business_value()
        
        print("\n" + "=" * 60)
        print("Demo完成 - 联系方式见末尾")
        print("=" * 60)
    
    def _show_monitored_products(self):
        """展示监控的产品列表"""
        print("【1/5】监控的竞品列表")
        print("-" * 60)
        
        for pid, pdata in self.products.items():
            current_price = pdata["price_history"][-1]["price"]
            min_price = min(h["price"] for h in pdata["price_history"])
            max_price = max(h["price"] for h in pdata["price_history"])
            
            print(f"产品: {pdata['name']}")
            print(f"  平台: {pdata['platform']}")
            print(f"  当前价: ¥{current_price:.2f}")
            print(f"  历史最低: ¥{min_price:.2f}")
            print(f"  历史最高: ¥{max_price:.2f}")
            print()
    
    def _show_price_trends(self):
        """展示价格趋势分析"""
        print("【2/5】价格趋势分析")
        print("-" * 60)
        
        for pid, pdata in self.products.items():
            print(f"产品: {pdata['name']}")
            
            # 最近7天价格
            recent = pdata["price_history"][-7:]
            prices = [h["price"] for h in recent]
            
            print(f"  最近7天价格: {[f'¥{p:.0f}' for p in prices]}")
            print(f"  趋势: {'↓ 下降' if prices[-1] < prices[0] else '↑ 上升'}")
            
            # 降价建议
            if prices[-1] < sum(prices) / len(prices):
                print(f"  💡 建议: 价格处于低位，可考虑采购")
            else:
                print(f"  💡 建议: 价格处于高位，建议观望")
            print()
        
        time.sleep(1)  # 模拟思考
    
    def _show_competitor_comparison(self):
        """展示竞品对比"""
        print("【3/5】多平台竞品对比")
        print("-" * 60)
        
        for pid, pdata in self.products.items():
            print(f"主产品: {pdata['name']} (¥{pdata['price_history'][-1]['price']:.2f})")
            print("  竞品对比:")
            
            for comp in pdata["competitors"]:
                diff = comp["price"] - pdata["price_history"][-1]["price"]
                diff_pct = (diff / pdata["price_history"][-1]["price"]) * 100
                
                if diff < 0:
                    print(f"    ✅ {comp['name']}: ¥{comp['price']} (低{diff_pct:.1f}%)")
                else:
                    print(f"    ⚠️  {comp['name']}: ¥{comp['price']} (高{diff_pct:.1f}%)")
            print()
        
        time.sleep(1)
    
    def _show_price_alert(self):
        """展示降价提醒功能"""
        print("【4/5】降价提醒（模拟）")
        print("-" * 60)
        
        print("监控中...")
        time.sleep(1)
        print("...")
        time.sleep(1)
        print()
        print("🔔 提醒: 无线蓝牙耳机Pro版 价格变化!")
        print("  之前: ¥349.00")
        print("  现在: ¥299.00")
        print("  降幅: -14.3% (¥50.00)")
        print("  💡 建议: 立即采购!")
        print()
        
        time.sleep(1)
    
    def _show_business_value(self):
        """展示商业价值"""
        print("【5/5】商业价值")
        print("-" * 60)
        
        print("💰 帮你省钱:")
        print("  - 及时发现降价，降低采购成本")
        print("  - 避免高价采购，节省10-30%成本")
        print()
        
        print("⏰ 帮你省时间:")
        print("  - 自动监控，无需手动查看")
        print("  - 每天节省1-2小时")
        print()
        
        print("📊 帮你做决策:")
        print("  - 价格趋势分析，科学采购")
        print("  - 竞品对比，优化定价策略")
        print()
        
        print("🚀 付费版功能 (¥99/月):")
        print("  ✅ 无限产品监控")
        print("  ✅ 每小时自动监控")
        print("  ✅ 价格图表可视化")
        print("  ✅ 微信/邮件提醒")
        print("  ✅ 多平台价格对比")
        print("  ✅ 库存监控")
        print("  ✅ 评论情感分析")
        print()
        
        print("📞 联系我们:")
        print("  - 微信: xueba-ai")
        print("  - 邮箱: xueba@qclaw.com")
        print("  - 免费试用: 5个产品，永久免费")


def main():
    """运行demo"""
    demo = PriceMonitorDemo()
    demo.show_demo()


if __name__ == "__main__":
    main()
