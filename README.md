# 竞品价格监控系统 v2.0

> 帮淘宝/京东卖家自动监控竞品价格，抓住最佳调价时机

## 功能特性

- 📊 **仪表盘** — 一目了然查看所有竞品最低价和价格趋势
- 🔄 **自动刷新** — 模拟真实价格波动，自动更新数据
- 📉 **趋势分析** — 7日价格趋势分析，识别涨跌方向
- ⚠️ **价格提醒** — 价格波动超过阈值自动提醒
- 📈 **商品详情** — 每个商品的完整竞品对比和历史走势
- 📤 **报告导出** — 支持 JSON 格式导出分析报告

## 快速开始

### 安装

```bash
pip install -r requirements.txt
```

### 查看监控仪表盘

```bash
python price_monitor.py
```

### 刷新价格（模拟）

```bash
python price_monitor.py refresh
```

### 查看商品详情

```bash
python price_monitor.py detail "iPhone 16 128GB"
```

### 检查价格提醒

```bash
python price_monitor.py alerts
```

### 导出报告

```bash
python price_monitor.py report           # 全局报告
python price_monitor.py report "iPhone 16 128GB"  # 单品报告
```

## 监控的商品

- **iPhone 16 128GB** — 天猫/京东/拼多多/苏宁
- **戴森V15吸尘器** — 天猫/京东/拼多多/小红书
- **SK-II神仙水230ml** — 天猫/京东/拼多多/网易考拉

## 技术栈

- Python 3
- JSON 数据存储
- 无外部依赖（纯标准库）

## 关于真实数据

当前版本使用模拟数据演示完整功能流程。真实数据采集方案正在开发中，将通过浏览器自动化技术实现。

## 盈利模式

面向淘宝/京东卖家、电商运营，提供竞品价格监控服务：
- 免费版：基础监控3个商品
- 付费版（¥99-299/月）：无限商品 + 实时提醒 + 数据导出

## 作者

学霸 · QClaw Agent
