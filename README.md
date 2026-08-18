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

第 6 天已通过：用 `dataclass` 把压测记录从宽泛字典转换成字段明确的对象。

Day 6 的 3 个 TODO 已完成，完整测试结果为 `18 passed`（2026-08-18）。

当前目录结构：

```text
src/
└── serving_lab/
    ├── __init__.py
    ├── loaders.py
    ├── metrics.py
    └── models.py
```

- `metrics.py`：统计、筛选和示例数据。
- `loaders.py`：JSON/JSONL 文件读取。
- `models.py`：压测记录与汇总结果的数据类。
- `__init__.py`：定义调用者能从包顶层使用的公开接口。

## Day 6 学习任务

### 今日目标

1. 理解类是对象的结构说明，对象是一份具体数据。
2. 使用 `@dataclass` 简化只负责保存数据的类。
3. 使用 `bool | None` 表达“布尔值可能缺失”。

### 必要知识

类像一张字段模板，对象是按照模板创建的一条具体记录：

```python
record = BenchmarkRecord(request_id="req_001", ...)
print(record.request_id)
```

`@dataclass` 会根据字段标注自动生成初始化和比较等基础代码。你只需要声明数据应有哪些字段：

```python
@dataclass
class Example:
    name: str
    cache_hit: bool | None = None
```

`bool | None` 表示值可以是 `True`、`False` 或 `None`。这里的 `None` 不是“缓存未命中”，而是“原始记录没有提供缓存信息”。有默认值的字段必须写在无默认值字段之后。

### 今天修改的文件

- `src/serving_lab/models.py`：包含 3 个待完成 TODO，以及已经写好的对象汇总函数。
- `src/serving_lab/__init__.py`：将四个新名称加入包公开接口。
- `tests/test_models.py`：覆盖对象创建、字典转换、可选默认值和汇总结果。
- `tests/test_benchmark_parser.py`：同步验证新的包公开接口清单。
- `README.md`、`ROADMAP.md`、`LEARNING_LOG.md`：Day 6 学习材料。

### 我的编码任务（已完成）

- 为 `BenchmarkRecord` 定义八个字段，并让 `cache_hit` 默认等于 `None`。
- 为 `BenchmarkSummary` 定义五个字段。
- 在 `benchmark_record_from_dict()` 中把解码后的字典转换成 `BenchmarkRecord`。

### 运行命令

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

这条命令使用项目虚拟环境运行全部测试，同时验证 Day 6 新功能和前五天的回归行为。

### 预期结果

完成 TODO 前应看到 4 个 Day 6 测试失败、14 个旧测试通过；正确完成后应看到：

```text
18 passed
```

### 测试

今天新增四个测试：数据类对象和可选字段默认值、字典转换保留缓存状态、缺少缓存字段时得到 `None`、汇总结果的类型和值。

### 常见错误

1. 把 `cache_hit` 默认值字段写在必要字段之前，会出现 `TypeError: non-default argument ... follows default argument`。
2. 忘记删除类中的 `pass` 虽然通常不影响运行，但会留下已经失去意义的占位代码。
3. 用 `data["cache_hit"]` 读取可选字段，字段缺失时会抛出 `KeyError`；这里应使用 `data.get("cache_hit")`。

### 复习问题

1. 类和对象是什么关系？请用 `BenchmarkRecord` 举例。
2. 相比一直传递 `dict[str, object]`，`dataclass` 在可读性和错误发现方面有什么好处？
3. `cache_hit=False` 与 `cache_hit=None` 分别表示什么？为什么不能混为一谈？

### 通关标准

- 3 个 TODO 均由你完成，且没有修改测试。
- 全部 18 个测试通过。
- 能解释类、对象、`dataclass` 和可选值的作用。
- 能用自己的话回答 3 道复习题。
- 完成 `LEARNING_LOG.md` 的 Day 6 记录。

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
