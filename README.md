# 价格趋势分析助手

> 手动录入价格数据，自动生成趋势分析和采购决策建议

## 为什么选择这款工具？

✅ **合规安全** - 不抓取任何平台数据，纯手动录入  
✅ **隐私保护** - 所有数据本地存储，不上传服务器  
✅ **简单高效** - 3个命令完成价格记录和分析  
✅ **完全免费** - 无功能限制，无广告  

## 快速开始

### 安装依赖

```bash
pip install -r requirements.txt
```

### 添加价格记录

```bash
python price_monitor.py add "产品名称" 价格 --note="备注" --source="来源"
```

示例：
```bash
python price_monitor.py add "无线耳机" 299 --note="6.18促销" --source="京东"
```

### 查看趋势报告

```bash
python price_monitor.py report
```

### 设置价格提醒

```bash
python price_monitor.py alert "产品名称" --threshold=5
```

## 功能特性

- ✅ 手动录入价格数据
- ✅ 价格历史记录
- ✅ 趋势分析和波动计算
- ✅ 购买决策建议
- ✅ 数据导出（CSV/Excel）
- ✅ 价格变化提醒
- ⏳ 多产品对比分析（专业版）
- ⏳ 价格历史图表（专业版）
- ⏳ PDF报告导出（专业版）

## 使用场景

### 场景1：个人购物决策
记录心仪产品的价格变化，找到最佳购买时机。

```bash
python price_monitor.py add "MacBook Air" 7999 --note="教育优惠" --source="苹果官网"
python price_monitor.py add "MacBook Air" 8499 --note="常规价" --source="苹果官网"
python price_monitor.py report "MacBook Air"
```

### 场景2：电商运营分析
记录竞品价格（手动查询后录入），分析价格策略。

```bash
python price_monitor.py add "竞品A" 299 --note="促销" --source="淘宝"
python price_monitor.py add "竞品A" 349 --note="日常" --source="淘宝"
python price_monitor.py report "竞品A"
```

### 场景3：采购成本优化
记录供应商报价，找到性价比最高的采购时机。

```bash
python price_monitor.py add "原材料A" 50 --note="批量采购" --source="供应商A"
python price_monitor.py add "原材料A" 55 --note="小批量" --source="供应商B"
python price_monitor.py report "原材料A"
```

## 数据结构

所有数据保存在本地 `price_data.json`，随时可查看和备份。

## 合规说明

本工具严格遵守相关法律法规：

1. **不抓取数据** - 所有价格数据由用户手动录入
2. **不绕过防护** - 不破解任何网站技术措施
3. **本地存储** - 数据保存在用户本地，不上传
4. **透明开源** - 代码完全开源，可接受审计

## 专业版规划

### 功能对比

| 功能 | 免费版 | 专业版（¥99/月） |
|------|--------|-------------------|
| 价格记录 | ✅ 无限 | ✅ 无限 |
| 趋势分析 | ✅ 基础 | ✅ 高级 |
| 数据导出 | ✅ CSV | ✅ Excel + PDF |
| 价格提醒 | ✅ 基础 | ✅ 多渠道提醒 |
| 多产品对比 | ❌ | ✅ |
| 价格图表 | ❌ | ✅ |
| 采购建议 | ❌ | ✅ AI智能建议 |

**注**：专业版不包含任何自动抓取功能。

## 作者

**学霸** - 高智商且满脑子都是赚钱的人  
风格：简单高效冷淡

---

**免责声明**：本工具仅提供数据分析功能，用户需自行确保数据来源合法合规。
