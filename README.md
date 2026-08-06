# fastapi-serving-lab

一个从 Python 基础逐步演进到 OpenAI 兼容模型服务网关的连续练习项目。

## 学习方式

- 每天投入 60～90 分钟。
- 每天只增加 2～3 个核心概念。
- 顺序固定为：最少理论、立即编码、pytest 测试、复盘。
- 当天通关后才进入下一天。
- 不使用真实 API Key、GPU、公司网络或公司文件。

完整安排见 [ROADMAP.md](ROADMAP.md)，每日复盘写入 [LEARNING_LOG.md](LEARNING_LOG.md)。

## 当前进度

第 1 天：用 Python 数据结构表示一条脱敏压测结果，并编写一个带类型标注的汇总函数。

输入记录：

```python
{
    "request_id": "req_demo_001",
    "model": "mock-llm",
    "prompt_tokens": 12,
    "completion_tokens": 8,
    "latency_ms": 640.0,
    "labels": ["mock", "cache-hit"],
}
```

期望汇总：

```python
{
    "request_id": "req_demo_001",
    "model": "mock-llm",
    "labels": ["mock", "cache-hit"],
    "total_tokens": 20,
    "tokens_per_second": 12.5,
}
```

这里的 `tokens_per_second` 定义为：

```text
completion_tokens / (latency_ms / 1000)
```

今天只修改 [src/benchmark_parser.py](src/benchmark_parser.py) 中的 3 个 TODO，不改测试来迁就实现。

## 环境要求

- 目标版本：Python 3.12
- 开发测试：pytest

2026-08-05 已完成本机学习环境配置：

- Python 3.12.10
- 项目虚拟环境：`.venv`
- pytest 9.1.1

当前 Windows 的旧 `py` 启动器尚未识别新解释器，因此在项目目录中使用虚拟环境的解释器运行测试：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```
