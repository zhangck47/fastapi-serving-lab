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

第 3 天：从 JSON 文件读取一条压测记录，并为文件不存在和 JSON 格式损坏提供清晰异常。

今天只修改 [src/benchmark_parser.py](src/benchmark_parser.py) 中 `load_benchmark_record()` 的 3 个 TODO，不修改测试来迁就实现。

当前状态（2026-08-12）：Day 3 代码、异常处理、复习和自动化测试均已完成，结果为 `8 passed`。

期望读取的文件内容：

```json
{
  "request_id": "req_file_001",
  "model": "mock-llm"
}
```

期望行为：

- 文件存在且 JSON 合法：返回 Python `dict`。
- 文件不存在：抛出带清晰路径信息的 `FileNotFoundError`。
- JSON 损坏：抛出带清晰路径信息的 `ValueError`。

今天暂时假设 JSON 顶层一定是对象，不做字段结构验证；这会在后续数据模型课程中处理。

## Day 3 学习任务

### 今日目标

1. 使用 `Path` 表示并读取文件路径。
2. 使用 `json.loads()` 把 JSON 文本转换成 Python 字典。
3. 捕获底层异常并提供清晰的错误信息。

### 必要知识

`Path` 是 Python 对文件路径的表示。`read_text()` 会读取整个文本文件：

```python
text: str = file_path.read_text(encoding="utf-8")
```

JSON 是文本格式，`json.loads(text)` 才会把文本转换成 Python 对象。文件读取和 JSON 解码是两个独立步骤，因此也可能发生两种不同错误。

`try` 中放可能失败的代码，`except` 处理指定异常：

```python
try:
    ...
except FileNotFoundError as exc:
    raise FileNotFoundError("更清楚的消息") from exc
```

`from exc` 会保留原始错误链，排查问题时既能看到友好说明，也能看到底层原因。

### 今天修改的文件

- `src/benchmark_parser.py`：增加读取单个 JSON 压测记录的函数。
- `tests/test_benchmark_parser.py`：覆盖成功、文件不存在和 JSON 损坏。
- `README.md`：记录 Day 3 的任务说明。
- `ROADMAP.md`：更新当前学习进度。
- `LEARNING_LOG.md`：提供 Day 3 复盘模板。

### 我的编码任务

- `TODO 1`：以 UTF-8 读取文件文本。
- `TODO 2`：把文件不存在错误转换成包含路径的清晰错误。
- `TODO 3`：解码 JSON，并把格式损坏错误转换成清晰的 `ValueError`。

### 运行命令

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

这条命令使用项目虚拟环境运行全部测试，确保 Day 3 没有破坏前两天功能。

### 预期结果

完成 TODO 前，Day 3 测试会失败；正确完成后应看到：

```text
8 passed
```

### 测试

今天新增三个 pytest 测试：合法 JSON 能读取、文件缺失有明确异常、损坏 JSON 有明确异常。测试使用 `tmp_path` 创建临时文件，不会在项目中遗留测试数据。

### 常见错误

1. 忘记指定 `encoding="utf-8"`，可能在不同系统得到不同编码行为。
2. 把 `json.load()` 和 `json.loads()` 混淆；这里输入是字符串，所以使用 `loads()`。
3. 在 `except` 中只写 `raise`，会原样抛出底层异常，无法通过今天对清晰错误信息的测试。

### 复习问题

1. 文件存在是否就代表其中一定是合法 JSON？为什么？
2. `json.loads()` 的输入和输出分别是什么？
3. `raise NewError(...) from exc` 中的 `from exc` 有什么价值？

### 通关标准

- 3 个 TODO 均由你完成，且没有修改测试。
- 全部 8 个测试通过。
- 能解释文件读取与 JSON 解码为什么是两个步骤。
- 能用自己的话回答 3 道复习题。
- 完成 `LEARNING_LOG.md` 的 Day 3 记录。

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
