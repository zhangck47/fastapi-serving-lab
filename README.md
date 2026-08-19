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

第 7 天已通过：使用生成器逐条读取 JSONL，避免一次把整个文件放入内存。

Day 7 的 3 个 TODO 已完成，完整测试结果为 `22 passed`（2026-08-19）。

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

## Day 7 学习任务

### 今日目标

1. 理解迭代器如何通过 `next()` 一次提供一个值。
2. 使用 `yield` 编写生成器函数。
3. 理解惰性执行如何节省内存并支持提前停止。

### 必要知识

迭代器像一个“下一条数据”按钮。每次调用 `next()` 才请求一个值：

```python
records = iter_benchmark_records(path)
first_record = next(records)
```

只要函数体里出现 `yield`，调用函数时就会先返回生成器对象，不会立刻执行文件读取。第一次 `next()` 才从函数开头运行到第一个 `yield`，之后会记住暂停位置：

```python
def count_two():
    yield 1
    yield 2
```

`list(generator)` 会把生成器全部消耗并重新收集成列表；只调用一次 `next()` 则只处理第一条。提前停止后，可以调用生成器的 `close()` 让它离开 `with` 并立即关闭文件。

### 今天修改的文件

- `src/serving_lab/loaders.py`：新增惰性 JSONL 生成器，包含 3 个 TODO。
- `src/serving_lab/__init__.py`：公开 `iter_benchmark_records`。
- `tests/test_generator_loader.py`：验证延迟打开、顺序、提前停止和坏行定位。
- `tests/test_benchmark_parser.py`：同步验证包公开接口清单。
- `README.md`、`ROADMAP.md`、`LEARNING_LOG.md`：Day 7 学习材料。

### 我的编码任务（已完成）

- 使用 `with` 和 `enumerate(..., start=1)` 逐行遍历 UTF-8 JSONL 文件。
- 清理当前行并跳过空白行。
- 解码非空行，并通过 `yield` 逐条产出记录。

### 运行命令

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

这条命令使用项目虚拟环境运行全部测试，同时验证 Day 7 生成器和前六天的回归行为。

### 预期结果

完成 TODO 前应看到 4 个 Day 7 测试失败、18 个旧测试通过；正确完成后应看到：

```text
22 passed
```

### 测试

今天新增四个测试：调用时不打开文件、按顺序产出并跳过空行、在后续坏行前提前停止、真正读取坏行时报告准确行号。

### 常见错误

1. 使用 `return record` 而不是 `yield record`，函数会在第一条记录后直接结束，也不会成为生成器。
2. 在判断空白行之前调用 `json.loads()`，空白行会被误报为损坏 JSON。
3. 为了查看结果立刻调用 `list(generator)`，会一次性消耗全部数据，无法体现提前停止的惰性行为。

### 复习问题

1. 调用生成器函数时为什么还没有读取文件？第一次 `next()` 时会发生什么？
2. `load_benchmark_records()` 返回列表，与 `iter_benchmark_records()` 返回生成器相比，各自适合什么场景？
3. 文件第二行是坏 JSON 时，为什么只读取第一条可以不报错？错误会在什么时候出现？

### 通关标准

- 3 个 TODO 均由你完成，且没有修改测试。
- 全部 22 个测试通过。
- 能解释迭代器、生成器、`yield` 和惰性执行过程。
- 能用自己的话回答 3 道复习题。
- 完成 `LEARNING_LOG.md` 的 Day 7 记录。

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
