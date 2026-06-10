# 价格趋势分析助手

**作者**: 学霸  
**版本**: 1.1 (合规版)  
**描述**: 手动录入价格数据，自动生成趋势分析和决策建议，保护隐私，本地运行

## 功能

1. **录入价格** - 手动输入产品价格和备注
2. **趋势分析** - 自动计算最低价、最高价、平均价、波动率
3. **变化提醒** - 价格变化超过设定阈值时提醒
4. **导出报告** - 生成Markdown/Excel格式报告

## 使用方法

### 1. 添加价格记录

```bash
python price_monitor.py add "产品名称" 299.0 --note="促销价" --source="京东"
```

示例：
```bash
python price_monitor.py add "无线耳机A" 299.0 --note="6.18促销" --source="京东"
python price_monitor.py add "无线耳机A" 349.0 --note="日常价" --source="淘宝"
```

### 2. 查看趋势报告

```bash
# 单个产品报告
python price_monitor.py report "无线耳机A"

# 所有产品报告
python price_monitor.py report
```

报告包含：
- 价格历史记录
- 最低/最高/平均价格
- 价格波动分析
- 购买建议（基于历史数据）

### 3. 设置价格提醒

```bash
# 设置提醒阈值（变化超过5%提醒）
python price_monitor.py alert "无线耳机A" --threshold=5
```

### 4. 导出数据

```bash
# 导出为CSV
python price_monitor.py export --format=csv

# 导出为Excel
python price_monitor.py export --format=excel
```

## 数据结构

价格数据保存在本地 `price_data.json`：

```json
{
  "无线耳机A": {
    "records": [
      {
        "time": "2026-06-10T16:30:00",
        "price": 299.0,
        "note": "6.18促销",
        "source": "京东"
      }
    ],
    "alert_threshold": 5,
    "status": "active"
  }
}
```

**隐私保护**：所有数据保存在本地，不上传任何服务器。

## 与OpenClaw集成

### 定时提醒（通过cron）

```json
{
  "schedule": {"kind": "cron", "expr": "0 9 * * *"},
  "payload": {
    "kind": "agentTurn",
    "message": "检查价格提醒：cd /Users/zhaona/Documents/qclaw/学霸/price-monitor && python price_monitor.py check_alert"
  },
  "sessionTarget": "isolated"
}
```

### 语音播报（通过tts）

```bash
python price_monitor.py report --voice
```

## 版本规划

### 免费版（当前）
- 无限产品记录
- 手动录入数据
- 基础趋势分析
- 本地存储

### 专业版规划（¥99/月）
- 自动生成采购建议
- 多产品对比分析
- 价格历史图表
- 导出PDF报告
- 邮件/微信提醒

**注**：专业版不包含任何自动抓取功能，所有数据需用户手动录入或通过官方API对接。

## 技术栈

- Python 3.8+
- JSON本地存储
- OpenClaw cron（定时提醒）
- OpenClaw tts（语音播报）

## 合规声明

本工具：
- ✅ 不抓取任何第三方平台数据
- ✅ 不绕过任何网站技术防护措施
- ✅ 所有数据由用户手动录入
- ✅ 完全本地运行，数据不上传
- ✅ 遵守《网络安全法》《反不正当竞争法》

## 作者

学霸 - 高智商且满脑子都是赚钱的人  
风格：简单高效冷淡

---

**免责声明**：本工具仅提供价格数据分析功能，用户需自行确保数据来源合法合规。
