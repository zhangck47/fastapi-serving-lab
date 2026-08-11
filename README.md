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

第 2 天：用 `if` 条件判断和 `for` 循环筛选多条压测记录中的成功项，再用 `set` 去重、以 `tuple` 汇总模型名。

当前状态（2026-08-11）：第 2 天代码审查和自动化测试已通过，结果为 `5 passed`；复习问题和个人学习记录仍待完成，尚未进入第 3 天。

输入记录（每条比第 1 天多一个 `status` 字段）：

```python
{
    "request_id": "req_demo_001",
    "model": "mock-llm",
    "status": "success",
    "prompt_tokens": 12,
    "completion_tokens": 8,
    "latency_ms": 640.0,
    "labels": ["mock", "cache-hit"],
}
```

今天只修改 [src/benchmark_parser.py](src/benchmark_parser.py) 中的 4 个 TODO，不改测试来迁就实现：

1. `filter_successful_records(records)`：用 `for` + `if` 筛选出 `status == "success"` 的记录，保持原顺序。
2. `collect_model_names(records)`：把所有 `model` 放入 `set` 去重，用 `sorted()` 排序后转为 `tuple` 返回。

期望行为（测试已给出）：

- 成功记录被保留，失败记录被过滤；
- 重复模型只出现一次，且结果按字母序；
- 空列表返回空元组 `()`。

代码审查提醒：

- `record.get("status")` 在合法输入下工作正确，但字段缺失时会返回 `None`，从而把坏记录静默过滤。第 3 天学习异常处理时会重新讨论这种取舍。
- `dict[str, object]` 表示值可能是任意对象，类型标注暂时无法证明取出的 `model` 一定是 `str`。后续会逐步使用更清晰的数据模型解决这个问题。
- `return (tuple(sorted(models)))` 外层括号不影响结果，但可以简化为 `return tuple(sorted(models))`。

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
