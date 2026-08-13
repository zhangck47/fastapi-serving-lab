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

第 4 天：从 JSONL 文件逐行读取多条压测记录，并在坏行出现时报告准确行号。

今天只修改 [src/benchmark_parser.py](src/benchmark_parser.py) 中 `load_benchmark_records()` 的 3 个 TODO，不修改测试来迁就实现。

当前状态（2026-08-13）：Day 4 代码、异常处理、权限问题复盘和自动化测试均已完成，结果为 `11 passed`。

JSONL 不是一个大 JSON 数组，而是“一行一个独立 JSON 对象”：

```text
{"request_id": "req_001", "model": "mock-llm"}
{"request_id": "req_002", "model": "fast-llm"}
```

期望行为：

- 每个非空行解码为一条 `dict`，并按照文件顺序加入列表。
- 空白行跳过；空文件返回 `[]`。
- 某一行 JSON 损坏时，错误信息指出真实文件行号。

## Day 4 学习任务

### 今日目标

1. 使用 `with` 管理文件打开与关闭。
2. 使用 `enumerate(..., start=1)` 逐行读取并记录行号。
3. 在 JSONL 损坏时报告准确坏行。

### 必要知识

`with` 是上下文管理器语法。离开缩进块时，无论正常结束还是发生异常，文件都会自动关闭：

```python
with file_path.open("r", encoding="utf-8") as file:
    ...
```

直接遍历文件会一行一行读取，不必先把整个文件装入内存。`enumerate` 同时提供行号和内容：

```python
for line_number, line in enumerate(file, start=1):
    ...
```

`start=1` 让行号与编辑器里看到的行号一致。空白行也占用真实文件行号，即使它被跳过。

### 今天修改的文件

- `src/benchmark_parser.py`：增加 JSONL 多记录读取函数。
- `tests/test_benchmark_parser.py`：覆盖合法多行、空文件和坏行行号。
- `README.md`：记录 Day 4 的任务说明。
- `ROADMAP.md`：更新 Day 4 进度。
- `LEARNING_LOG.md`：提供 Day 4 复盘模板。

### 我的编码任务

- `TODO 1`：用 `with` 打开 UTF-8 JSONL 文件。
- `TODO 2`：逐行读取，跳过空行，解码并收集记录。
- `TODO 3`：把坏行异常转换成包含真实行号和路径的 `ValueError`。

### 运行命令

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

这条命令使用项目虚拟环境运行全部测试，确保 Day 3 没有破坏前两天功能。

### 预期结果

完成 TODO 前，Day 4 测试会失败；正确完成后应看到：

```text
11 passed
```

### 测试

今天新增三个 pytest 测试：合法 JSONL 与空白行、空文件、第二行损坏。测试继续使用 `tmp_path`，不会遗留测试数据。

### 常见错误

1. 忘记缩进：文件操作必须放在 `with` 代码块中。
2. 用单独的“有效记录计数”作为行号，导致存在空白行时报告错误位置不准确。
3. 对空白行直接执行 `json.loads()`，会把空行误报为坏 JSON。

### 复习问题

1. `with` 如何保证发生异常时文件仍然会被关闭？
2. 为什么要使用 `enumerate(file, start=1)`，而不是自己只在成功解码后把计数器加一？
3. JSON 与 JSONL 在文件结构和读取方式上有什么区别？

### 通关标准

- 3 个 TODO 均由你完成，且没有修改测试。
- 全部 11 个测试通过。
- 能解释 `with`、逐行读取和真实文件行号。
- 能用自己的话回答 3 道复习题。
- 完成 `LEARNING_LOG.md` 的 Day 4 记录。

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
