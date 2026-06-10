#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
价格获取模块 - 使用xbrowser获取真实价格
"""

import subprocess
import json
import re
from pathlib import Path


class PriceFetcher:
    """价格获取器 - 使用xbrowser爬取真实价格"""
    
    def __init__(self, browser="default"):
        self.browser = browser
        self.xb_path = self._find_xb_path()
    
    def _find_xb_path(self):
        """查找xb CLI路径"""
        # 默认路径
        default_path = Path.home() / ".qclaw/skills/xbrowser/scripts/xb.cjs"
        if default_path.exists():
            return str(default_path)
        
        # 尝试 which
        try:
            result = subprocess.run(
                ["which", "xb"],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout.strip()
        except:
            return None
    
    def _run_xb(self, *args):
        """运行xb命令"""
        if not self.xb_path:
            return {"ok": False, "error": "xbrowser未安装"}
        
        cmd = ["node", self.xb_path, "run", "--browser", self.browser] + list(args)
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            return json.loads(result.stdout)
        except subprocess.TimeoutExpired:
            return {"ok": False, "error": "timeout"}
        except Exception as e:
            return {"ok": False, "error": str(e)}
    
    def fetch_taobao_price(self, url):
        """获取淘宝/天猫价格"""
        # 1. 打开页面
        result = self._run_xb("open", url)
        if not result.get("ok"):
            return None
        
        # 2. 等待加载
        self._run_xb("wait", "--load", "networkidle")
        
        # 3. 获取页面快照（含价格信息）
        snapshot = self._run_xb("snapshot", "-i")
        if not snapshot.get("ok"):
            return None
        
        # 4. 解析价格（简化版，实际需要更复杂的解析）
        # 淘宝价格通常在 <span class="price"> 或类似元素中
        snapshot_text = json.dumps(snapshot)
        
        # 使用正则匹配价格（简化）
        price_patterns = [
            r'"price"[:\s]+"?(\d+\.?\d*)"?',  # JSON中的price字段
            r'¥\s*(\d+\.?\d*)',  # ¥ 符号后跟数字
            r'(\d+\.?\d*)\s*元',  # 数字后跟"元"
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, snapshot_text)
            if match:
                try:
                    return float(match.group(1))
                except:
                    continue
        
        # 如果无法解析，返回None
        return None
    
    def fetch_jd_price(self, url):
        """获取京东价格"""
        # 类似淘宝的逻辑
        result = self._run_xb("open", url)
        if not result.get("ok"):
            return None
        
        self._run_xb("wait", "--load", "networkidle")
        
        snapshot = self._run_xb("snapshot", "-i")
        if not snapshot.get("ok"):
            return None
        
        snapshot_text = json.dumps(snapshot)
        
        # 京东价格模式
        price_patterns = [
            r'"p"[:\s]+"(\d+\.?\d*)"',  # JSON中的p字段
            r'¥\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*元',
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, snapshot_text)
            if match:
                try:
                    return float(match.group(1))
                except:
                    continue
        
        return None
    
    def fetch_pinduoduo_price(self, url):
        """获取拼多多价格"""
        # 类似逻辑
        result = self._run_xb("open", url)
        if not result.get("ok"):
            return None
        
        self._run_xb("wait", "--load", "networkidle")
        
        snapshot = self._run_xb("snapshot", "-i")
        if not snapshot.get("ok"):
            return None
        
        snapshot_text = json.dumps(snapshot)
        
        # 拼多多价格模式
        price_patterns = [
            r'"price"[:\s]+"(\d+\.?\d*)"',
            r'¥\s*(\d+\.?\d*)',
            r'(\d+\.?\d*)\s*元',
        ]
        
        for pattern in price_patterns:
            match = re.search(pattern, snapshot_text)
            if match:
                try:
                    return float(match.group(1))
                except:
                    continue
        
        return None
    
    def fetch_price(self, url, platform):
        """统一价格获取接口"""
        if platform == "taobao":
            return self.fetch_taobao_price(url)
        elif platform == "jd":
            return self.fetch_jd_price(url)
        elif platform == "pinduoduo":
            return self.fetch_pinduoduo_price(url)
        else:
            return None


def main():
    """测试"""
    import sys
    
    if len(sys.argv) < 3:
        print("用法: python price_fetcher.py <url> <platform>")
        sys.exit(1)
    
    url = sys.argv[1]
    platform = sys.argv[2]
    
    fetcher = PriceFetcher()
    price = fetcher.fetch_price(url, platform)
    
    if price:
        print(f"成功获取价格: ¥{price}")
    else:
        print("获取价格失败")


if __name__ == "__main__":
    main()
