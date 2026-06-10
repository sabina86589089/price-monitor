#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
竞品价格监控系统 v2.0 (MVP完整版)
功能：模拟竞品数据、自动监控、价格提醒、趋势分析
作者：学霸
"""

import json
import time
import random
from datetime import datetime, timedelta
from pathlib import Path


# ============================================================
# 模拟数据源：模拟竞品商品数据
# ============================================================

def generate_mock_products():
    """生成模拟竞品商品数据（演示用）"""
    return {
        "iPhone 16 128GB": {
            "competitors": [
                {"name": "天猫-Apple旗舰店", "price": 5999, "sales": 12500, "rating": 4.9},
                {"name": "京东-Apple产品自营店", "price": 6099, "sales": 8200, "rating": 4.8},
                {"name": "拼多多-百亿补贴", "price": 5699, "sales": 35000, "rating": 4.7},
                {"name": "苏宁易购", "price": 6199, "sales": 2100, "rating": 4.6},
            ]
        },
        "戴森V15吸尘器": {
            "competitors": [
                {"name": "天猫-戴森官方旗舰店", "price": 5499, "sales": 3800, "rating": 4.9},
                {"name": "京东-戴森旗舰店", "price": 5599, "sales": 2900, "rating": 4.8},
                {"name": "拼多多-品牌好货", "price": 4999, "sales": 15000, "rating": 4.6},
                {"name": "小红书-达人店铺", "price": 5299, "sales": 890, "rating": 4.7},
            ]
        },
        "SK-II神仙水230ml": {
            "competitors": [
                {"name": "天猫-SK-II官方旗舰店", "price": 1699, "sales": 5600, "rating": 4.9},
                {"name": "京东-丝芙兰", "price": 1729, "sales": 3200, "rating": 4.8},
                {"name": "拼多多-海淘", "price": 1399, "sales": 28000, "rating": 4.5},
                {"name": "网易考拉", "price": 1549, "sales": 4100, "rating": 4.7},
            ]
        },
    }


def simulate_price_fluctuation(price, volatility=0.03):
    """模拟价格波动（±volatility）"""
    change = random.uniform(-volatility, volatility)
    return round(price * (1 + change), 0)


# ============================================================
# 核心监控类
# ============================================================

class CompetitorMonitor:
    """竞品监控系统"""

    def __init__(self, data_file="competitor_data.json"):
        self.data_file = Path(data_file)
        self.config = self._load_config()
        self._load_data()

    def _load_config(self):
        """加载配置"""
        return {
            "alert_threshold": 5,       # 价格变化超过5%提醒
            "check_interval_hours": 6,  # 检查间隔
            "price_unit": "¥",
            "auto_refresh": True,
        }

    def _load_data(self):
        """加载历史数据"""
        if self.data_file.exists():
            with open(self.data_file, 'r', encoding='utf-8') as f:
                raw = json.load(f)
                self.products = raw.get("products", {})
                self.price_history = raw.get("price_history", {})
        else:
            self.products = {}
            self.price_history = {}
        # 初始化模拟数据
        self._init_mock_data()

    def _init_mock_data(self):
        """初始化模拟数据"""
        if not self.products:
            mock = generate_mock_products()
            now = datetime.now().isoformat()
            for product, data in mock.items():
                self.products[product] = {
                    "competitors": data["competitors"],
                    "watch": True,
                    "created_at": now,
                }
                # 模拟7天历史价格
                self.price_history[product] = []
                base_prices = {c["name"]: c["price"] for c in data["competitors"]}
                for days_ago in range(7, 0, -1):
                    timestamp = (datetime.now() - timedelta(days=days_ago)).isoformat()
                    snapshot = {}
                    for comp_name, base_price in base_prices.items():
                        snapshot[comp_name] = simulate_price_fluctuation(base_price)
                    self.price_history[product].append({
                        "timestamp": timestamp,
                        "prices": snapshot,
                    })
                # 今天的价格用当前价格
                self.price_history[product].append({
                    "timestamp": now,
                    "prices": {c["name"]: c["price"] for c in data["competitors"]},
                })
            self._save_data()

    def _save_data(self):
        """保存数据"""
        with open(self.data_file, 'w', encoding='utf-8') as f:
            json.dump({
                "products": self.products,
                "price_history": self.price_history,
            }, f, ensure_ascii=False, indent=2)

    # --------------------- 数据操作 ---------------------

    def add_product(self, product_name, competitors):
        """添加监控商品"""
        now = datetime.now().isoformat()
        self.products[product_name] = {
            "competitors": competitors,
            "watch": True,
            "created_at": now,
        }
        self.price_history[product_name] = [{
            "timestamp": now,
            "prices": {c["name"]: c["price"] for c in competitors},
        }]
        self._save_data()
        return {"success": True, "product": product_name, "competitors": len(competitors)}

    def remove_product(self, product_name):
        """移除监控商品"""
        if product_name in self.products:
            del self.products[product_name]
            self.price_history.pop(product_name, None)
            self._save_data()
            return {"success": True, "removed": product_name}
        return {"success": False, "error": "商品不存在"}

    def refresh_prices(self):
        """刷新所有商品价格（模拟）"""
        now = datetime.now().isoformat()
        results = []
        for product_name, data in self.products.items():
            # 模拟价格变化
            new_prices = {}
            for comp in data["competitors"]:
                new_prices[comp["name"]] = simulate_price_fluctuation(comp["price"], volatility=0.02)
                # 更新基准价
                comp["price"] = new_prices[comp["name"]]

            # 记录历史
            self.price_history[product_name].append({
                "timestamp": now,
                "prices": new_prices,
            })
            # 只保留30天历史
            if len(self.price_history[product_name]) > 30:
                self.price_history[product_name] = self.price_history[product_name][-30:]

            results.append({"product": product_name, "prices": new_prices, "time": now})

        self._save_data()
        return results

    # --------------------- 分析功能 ---------------------

    def get_dashboard(self):
        """获取监控仪表盘"""
        dashboards = []

        for product_name, data in self.products.items():
            if not data.get("watch"):
                continue

            history = self.price_history.get(product_name, [])
            if len(history) < 2:
                continue

            latest = history[-1]["prices"]
            prev = history[-2]["prices"]
            week_ago = history[-7]["prices"] if len(history) >= 7 else history[0]["prices"]

            comps = data["competitors"]

            # 当前最低价
            current_prices = [(c["name"], c["price"]) for c in comps]
            current_prices.sort(key=lambda x: x[1])
            lowest = current_prices[0]

            # 价格变化
            changes = []
            alerts = []
            for comp in comps:
                comp_name = comp["name"]
                curr = latest.get(comp_name, comp["price"])
                prev_price = prev.get(comp_name, comp["price"])

                if prev_price > 0:
                    pct = (curr - prev_price) / prev_price * 100
                    changes.append({"competitor": comp_name, "change_pct": round(pct, 2)})
                    if abs(pct) >= self.config["alert_threshold"]:
                        alerts.append(f"{comp_name} 价格变动 {pct:+.1f}%")

                # 更新内存中的价格
                comp["price"] = curr

            # 趋势分析（7天）
            week_trend = None
            if len(history) >= 7:
                old = history[-7]["prices"]
                new = latest
                old_min = min(old.values()) if old else 0
                new_min = min(new.values()) if new else 0
                if old_min > 0:
                    week_trend = round((new_min - old_min) / old_min * 100, 2)

            dashboards.append({
                "product": product_name,
                "lowest_price": {"competitor": lowest[0], "price": lowest[1]},
                "competitor_count": len(comps),
                "recent_changes": changes,
                "alerts": alerts,
                "week_trend": week_trend,
                "last_update": history[-1]["timestamp"],
                "status": "watching",
            })

        return dashboards

    def get_product_detail(self, product_name):
        """获取单个商品详情"""
        if product_name not in self.products:
            return {"error": "商品不存在"}

        data = self.products[product_name]
        history = self.price_history.get(product_name, [])

        # 价格走势
        timeline = []
        for snapshot in history[-14:]:
            timeline.append({
                "time": snapshot["timestamp"],
                "prices": snapshot["prices"],
                "min_price": min(snapshot["prices"].values()),
                "max_price": max(snapshot["prices"].values()),
            })

        latest = history[-1] if history else {}
        comps = data["competitors"]

        # 竞品对比
        comparisons = []
        for comp in comps:
            curr = latest.get("prices", {}).get(comp["name"], comp["price"])
            min_in_history = min([s["prices"].get(comp["name"], curr) for s in history]) if history else curr
            max_in_history = max([s["prices"].get(comp["name"], curr) for s in history]) if history else curr

            if curr <= min_in_history * 1.02:
                signal = "📉 接近历史最低"
            elif curr >= max_in_history * 0.98:
                signal = "📈 接近历史最高"
            else:
                signal = "➡️ 价格适中"

            comparisons.append({
                **comp,
                "current_price": curr,
                "min_price": round(min_in_history, 0),
                "max_price": round(max_in_history, 0),
                "signal": signal,
            })

        all_current = [c["current_price"] for c in comparisons]
        avg_price = sum(all_current) / len(all_current) if all_current else 0
        min_price = min(all_current) if all_current else 0
        recommendation = (
            f"建议关注最低价 ¥{min_price:.0f}，"
            f"当前均价 ¥{avg_price:.0f}，"
            f"如竞品价格低于均价5%可考虑跟价"
        )

        return {
            "product": product_name,
            "competitors": comparisons,
            "timeline": timeline,
            "recommendation": recommendation,
            "last_update": latest.get("timestamp", "未知"),
        }

    def check_alerts(self):
        """检查价格提醒"""
        dashboards = self.get_dashboard()
        all_alerts = []

        for item in dashboards:
            if item["alerts"]:
                all_alerts.append({
                    "product": item["product"],
                    "alerts": item["alerts"],
                    "lowest_price": item["lowest_price"],
                    "week_trend": item["week_trend"],
                    "time": item["last_update"],
                })

        return all_alerts if all_alerts else [{"message": "暂无价格异常提醒", "time": datetime.now().isoformat()}]

    def export_report(self, product_name=None, format="json"):
        """导出分析报告"""
        if product_name:
            data = self.get_product_detail(product_name)
        else:
            data = {
                "dashboard": self.get_dashboard(),
                "alerts": self.check_alerts(),
                "export_time": datetime.now().isoformat(),
            }

        if format == "json":
            output_file = f"price_report_{datetime.now().strftime('%Y%m%d_%H%M')}.json"
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(data, f, ensure_ascii=False, indent=2)
            return {"success": True, "file": output_file, "format": "json"}
        else:
            return {"error": f"不支持格式: {format}"}

    def set_config(self, **kwargs):
        """更新配置"""
        self.config.update(kwargs)
        return {"success": True, "config": self.config}

    def get_status(self):
        """获取系统状态"""
        return {
            "products_count": len([p for p in self.products.values() if p.get("watch")]),
            "total_snapshots": sum(len(h) for h in self.price_history.values()),
            "config": self.config,
            "last_check": datetime.now().isoformat(),
        }


# ============================================================
# CLI 入口
# ============================================================

def main():
    import sys

    monitor = CompetitorMonitor()

    if len(sys.argv) < 2:
        print("=" * 50)
        print("  竞品价格监控系统 v2.0 (MVP)")
        print("=" * 50)
        print("\n📊 命令：")
        print("  dashboard    - 查看监控仪表盘")
        print("  refresh     - 刷新所有价格")
        print("  detail <商品> - 查看商品详情")
        print("  alerts       - 检查价格提醒")
        print("  report [商品] - 导出报告")
        print("  status       - 系统状态")
        print("  remove <商品> - 移除商品")
        print("\n" + "=" * 50)
        print("\n📈 当前监控：")
        dashboards = monitor.get_dashboard()
        for d in dashboards:
            print(f"  • {d['product']} | 最低 ¥{d['lowest_price']['price']:.0f} @ {d['lowest_price']['competitor']}")
            if d['week_trend'] is not None:
                trend_icon = "📈" if d['week_trend'] > 0 else "📉"
                print(f"    {trend_icon} 7日趋势: {d['week_trend']:+.1f}%")
            if d['alerts']:
                print(f"    ⚠️  {', '.join(d['alerts'])}")
        print()
        return

    command = sys.argv[1]

    if command == "dashboard":
        result = monitor.get_dashboard()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "refresh":
        print("🔄 正在刷新价格...")
        result = monitor.refresh_prices()
        for r in result:
            print(f"  ✅ {r['product']} - {len(r['prices'])} 个竞品已更新")
        print("\n📊 刷新后仪表盘：")
        dashboards = monitor.get_dashboard()
        for d in dashboards:
            print(f"  • {d['product']} | 最低 ¥{d['lowest_price']['price']:.0f} @ {d['lowest_price']['competitor']}")
        alerts = monitor.check_alerts()
        if alerts and alerts[0].get("alerts"):
            print("\n⚠️  价格提醒：")
            for a in alerts:
                for alert in a.get("alerts", []):
                    print(f"  • {a['product']}: {alert}")

    elif command == "detail":
        product = sys.argv[2] if len(sys.argv) > 2 else list(monitor.products.keys())[0]
        result = monitor.get_product_detail(product)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "alerts":
        result = monitor.check_alerts()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "report":
        product = sys.argv[2] if len(sys.argv) > 2 else None
        result = monitor.export_report(product)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "status":
        result = monitor.get_status()
        print(json.dumps(result, ensure_ascii=False, indent=2))

    elif command == "remove":
        if len(sys.argv) < 3:
            print("用法: python price_monitor.py remove <商品名称>")
            return
        product = sys.argv[2]
        result = monitor.remove_product(product)
        print(json.dumps(result, ensure_ascii=False, indent=2))

    else:
        print(f"未知命令: {command}")
        print("运行 python price_monitor.py 查看帮助")


if __name__ == "__main__":
    main()
