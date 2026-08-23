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

第 8 天已通过：用 pytest 参数化测试串联 Python 阶段的完整压测解析流程。

Day 8 的 3 个 TODO 已完成，完整测试结果为 `26 passed`（2026-08-23）。Python 核心基础阶段已通过。

阶段总结见 [PYTHON_STAGE_REVIEW.md](PYTHON_STAGE_REVIEW.md)，当前项目面试题库见 [INTERVIEW_QA.md](INTERVIEW_QA.md)。面试题库只记录已经实现并能用代码证明的能力，后续阶段完成后继续扩充。

当前目录结构：

```text
src/
└── serving_lab/
    ├── __init__.py
    ├── loaders.py
    ├── metrics.py
    ├── models.py
    └── pipeline.py
```

- `metrics.py`：统计、筛选和示例数据。
- `loaders.py`：JSON/JSONL 文件读取。
- `models.py`：压测记录与汇总结果的数据类。
- `pipeline.py`：连接惰性读取、数据转换和指标汇总。
- `__init__.py`：定义调用者能从包顶层使用的公开接口。

## Day 8 学习任务

### 今日目标

1. 使用 `assert` 写清楚可执行的预期结果。
2. 使用 `@pytest.mark.parametrize` 让同一测试覆盖多组输入。
3. 串联并复盘 Python 阶段的完整数据流程。

### 必要知识

pytest 的 `assert` 表达“实际结果必须满足什么条件”。条件不成立时，pytest 会指出实际值与预期值的差异：

```python
assert summary.total_tokens == expected_total_tokens
```

参数化测试把多组输入交给同一个测试函数。每一组参数都会被 pytest 收集成一个独立测试，因此其中一组失败不会隐藏其他组的结果：

```python
@pytest.mark.parametrize(("value", "expected"), [(1, 2), (2, 4)])
def test_double(value: int, expected: int) -> None:
    assert value * 2 == expected
```

今天的流水线不引入新算法，只组合已有能力：JSONL 生成器产出字典，转换函数建立 `BenchmarkRecord`，汇总函数再产出 `BenchmarkSummary`。每层只负责一件事。

### 今天修改的文件

- `src/serving_lab/pipeline.py`：完成端到端惰性流水线实现。
- `tests/test_pipeline.py`：完成参数化边界用例和惰性异常测试。
- `src/serving_lab/__init__.py`：公开 `iter_benchmark_summaries`。
- `tests/test_benchmark_parser.py`：同步验证包公开接口清单。
- `README.md`、`ROADMAP.md`、`LEARNING_LOG.md`：Day 8 学习材料。

### 我的编码任务（已完成）

- 串联 JSONL 惰性读取、字典到数据类转换和指标汇总。
- 为零 completion 与零 prompt 添加参数化边界用例。
- 断言汇总数量、对象类型、总 token 数和生成吞吐量。

### 运行命令

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

这条命令使用项目虚拟环境运行全部测试。参数化的三组数据会显示为三个独立测试。

### 预期结果

完成 TODO 前应看到 2 个 Day 8 测试失败、22 个旧测试通过；完成两个新增参数组后，正确结果应为：

```text
26 passed
```

### 测试

今天的参数化测试覆盖正常数据、零 completion 和零 prompt；另一个测试验证流水线仍保持惰性，并继续报告后续坏行。前七天测试已经覆盖空文件、文件不存在、损坏 JSON 和提前停止。

### 常见错误

1. 参数名称顺序与参数元组中的值顺序不一致，导致输入和预期被传错位置。
2. 只断言 `summaries` 非空，没有检查类型和指标值，测试即使遇到错误计算也可能通过。
3. 完成代码或断言后忘记删除 `raise NotImplementedError(...)`，程序仍会主动失败。

### 复习问题

1. 为什么一个参数化测试函数最终会显示为三个测试？它比复制三份测试函数好在哪里？
2. 请按顺序解释一条 JSONL 记录从文件到 `BenchmarkSummary` 的完整生命周期。
3. 正常场景、边界场景和异常场景分别在防止什么类型的问题？本项目中各举一个例子。

### 通关标准

- 3 个 TODO 均由你完成，且没有修改测试。
- 全部 26 个测试通过。
- 能解释 pytest 断言、参数化和测试用例收集方式。
- 能用自己的话回答 3 道复习题。
- 能口述文件读取、JSON 解码、数据类转换、指标汇总和异常传播的职责边界。
- 完成 `LEARNING_LOG.md` 的 Day 8 记录，达到 Python 阶段通关标准。

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
