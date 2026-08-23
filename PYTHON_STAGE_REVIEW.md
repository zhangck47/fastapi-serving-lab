# Python 核心基础阶段总结

本文总结 `fastapi-serving-lab` Day 1～Day 8 已经实现并通过测试的内容。它既是阶段复习材料，也是后续学习 HTTP、FastAPI、AsyncIO 和 SSE 时的 Python 基础索引。

## 1. 阶段成果

当前项目已经能够：

- 读取一个 UTF-8 JSON 压测记录文件。
- 逐行读取 JSONL 文件，跳过空行并报告准确坏行行号。
- 将宽泛的字典转换成字段明确的 `BenchmarkRecord` 数据类。
- 计算总 token 数和每秒生成 token 数，返回 `BenchmarkSummary`。
- 使用生成器惰性处理大文件，支持提前停止。
- 将读取、转换和汇总串成端到端惰性流水线。
- 使用 pytest 覆盖正常、边界、异常和参数化场景。

阶段通关测试结果：`26 passed`。

## 2. 当前项目结构

```text
fastapi-serving-lab/
├── README.md
├── ROADMAP.md
├── LEARNING_LOG.md
├── PYTHON_STAGE_REVIEW.md
├── INTERVIEW_QA.md
├── pyproject.toml
├── src/
│   └── serving_lab/
│       ├── __init__.py
│       ├── loaders.py
│       ├── metrics.py
│       ├── models.py
│       └── pipeline.py
└── tests/
    ├── conftest.py
    ├── test_benchmark_parser.py
    ├── test_generator_loader.py
    ├── test_models.py
    └── test_pipeline.py
```

模块职责：

| 模块 | 职责 | 不负责什么 |
| --- | --- | --- |
| `loaders.py` | 文件读取、JSON/JSONL 解码、文件与格式异常 | 业务指标计算 |
| `models.py` | 数据结构、字典转对象、单条记录汇总 | 打开文件 |
| `metrics.py` | 早期字典版本的筛选、模型名收集和指标计算 | 文件生命周期 |
| `pipeline.py` | 组合读取、转换和汇总步骤 | 重复实现底层逻辑 |
| `__init__.py` | 提供稳定的包级公开接口 | 业务实现 |

## 3. 一条记录的完整生命周期

```text
JSONL 文件中的一行文本
        ↓
iter_benchmark_records()
        ↓ json.loads()
dict[str, object]
        ↓ benchmark_record_from_dict()
BenchmarkRecord
        ↓ summarize_benchmark_record()
BenchmarkSummary
        ↓ iter_benchmark_summaries() yield
调用者按需取得结果
```

错误传播路径：

- 文件不存在：底层 `FileNotFoundError` 被转换成包含目标路径的清晰错误。
- JSON 损坏：`JSONDecodeError` 被转换成 `ValueError`，并保留真实行号、文件路径和异常链。
- 调用者提前停止：后续行不会被读取，生成器可以通过 `close()` 退出 `with` 并关闭文件。

## 4. Day 1～Day 8 知识地图

| Day | 核心知识 | 项目实践 | 测试重点 |
| --- | --- | --- | --- |
| 1 | 变量、基本类型、`list`/`dict`、函数、类型标注 | 汇总一条已解码记录 | token 总数与吞吐量 |
| 2 | `if`、`for`、`set`、`tuple` | 筛选成功记录、模型名去重排序 | 顺序、重复、空输入 |
| 3 | `Path`、JSON、异常处理 | 读取单个 JSON 文件 | 文件不存在、格式损坏 |
| 4 | `with`、JSONL、逐行处理 | 多记录读取与坏行定位 | 空行、空文件、真实行号 |
| 5 | 模块、包、虚拟环境 | 拆分职责并定义公开接口 | 包级导入与 `__all__` |
| 6 | 类、对象、`dataclass`、可选值 | 建立记录和汇总数据类 | 对象创建、字段转换、`None` |
| 7 | 迭代器、生成器、惰性执行 | 按需逐条读取 JSONL | 延迟打开、提前停止、惰性异常 |
| 8 | pytest 断言、参数化、阶段集成 | 端到端汇总流水线 | 正常、边界、异常回归 |

## 5. Python 数据与控制流

### 5.1 基本类型和变量

项目中实际使用的基本类型包括：

- `str`：请求 ID、模型名、状态。
- `int`：prompt token、completion token、total token。
- `float`：毫秒延迟、每秒 token 数。
- `bool`：缓存是否命中。
- `None`：缓存状态没有提供。

变量用于给中间结果命名。清晰的变量名比把所有计算塞进一个表达式更适合调试和代码审查。

### 5.2 `list`、`dict`、`set`、`tuple`

- `list`：有序、可变，适合保存按文件顺序得到的记录。
- `dict`：键值映射，适合表示刚从 JSON 解码出的数据。
- `set`：元素唯一，适合模型名去重，但不能承担业务所需的稳定排序。
- `tuple`：有序、不可变，适合返回已经确定的模型名集合。

模型名处理采用“`set` 去重 → `sorted` 排序 → `tuple` 固化”的顺序，使结果可重复、易测试。

### 5.3 条件和循环

- `for` 按输入顺序处理记录。
- `if` 决定记录是否保留、空行是否跳过。
- `continue` 结束当前循环轮次，直接处理下一行。
- `enumerate(file, start=1)` 同时得到内容和与编辑器一致的行号。

## 6. 函数和类型标注

函数把一项职责封装成可复用单元。项目中的典型函数可以分为：

- 输入函数：读取文件、解码 JSON。
- 转换函数：字典转数据类。
- 计算函数：计算汇总指标。
- 组合函数：把多个小函数连接成流水线。

类型标注示例：

```python
def iter_benchmark_summaries(
    file_path: Path,
) -> Iterator[BenchmarkSummary]:
    ...
```

它说明输入和输出意图，帮助编辑器、静态检查器和读代码的人理解接口。Python 默认不会仅凭类型标注自动校验运行时数据；当前项目依赖测试和访问字段时的自然异常，后续 FastAPI 阶段会学习 Pydantic 运行时校验。

## 7. 文件、路径和 JSON

### 7.1 `pathlib.Path`

`Path` 比手工拼接路径字符串更清晰，也提供 `read_text()`、`open()` 等面向对象接口。项目始终明确使用 `encoding="utf-8"`，避免不同 Windows 环境的默认编码差异。

### 7.2 JSON 与 JSONL

- JSON：整个文件构成一个 JSON 值，通常整体读取和解码。
- JSONL：每个非空行是一个独立 JSON 值，适合日志、压测记录和流式处理。

`json.loads()` 接收字符串并返回 Python 对象。它只负责语法解码，不保证返回值一定具有项目要求的全部字段或正确业务类型。

### 7.3 `with` 上下文管理器

`with` 管理文件生命周期。正常完成、JSON 解码失败或生成器被关闭时，离开代码块都会执行文件关闭逻辑。

## 8. 异常处理

项目遵循三个原则：

1. 只捕获能够理解和转换的具体异常。
2. 对外提供包含业务上下文的错误信息。
3. 使用 `raise NewError(...) from exc` 保留原始异常链。

异常类型表达不同失败类别：

- `FileNotFoundError`：目标文件不存在。
- `json.JSONDecodeError`：底层 JSON 语法错误。
- `ValueError`：对调用者表达“压测文件内容不合法”。

坏行行号必须在跳过空行之前由 `enumerate` 生成，否则报告的将是“有效记录序号”，不是文件真实行号。

## 9. 模块、包和虚拟环境

- 一个 `.py` 文件通常是一个模块。
- `serving_lab/` 是包，`__init__.py` 定义包级入口。
- 相对导入中的 `.` 表示当前包。
- `__all__` 声明希望公开的名称，但不会自动导入，也不是访问控制机制。
- `.venv` 隔离解释器和第三方依赖，不会修改 Python 源代码。
- `src` 布局可避免测试意外从仓库根目录导入未安装的同名模块。

## 10. 类、数据类和可选值

类是结构模板，对象是具体实例。`@dataclass` 适合字段为主的数据对象，它自动生成初始化、比较和便于调试的字符串表示。

`BenchmarkRecord.cache_hit: bool | None = None` 有三种语义：

- `True`：明确命中缓存。
- `False`：明确没有命中缓存。
- `None`：没有提供缓存信息。

`False` 与 `None` 不能混用，否则缓存命中率会把“未知”错误统计成“未命中”。有默认值的字段必须放在没有默认值的字段之后。

数据类并不自动完成运行时校验。当前转换函数仍可能收到错误类型；这是阶段 1 有意保留的边界，后续由 Pydantic 解决外部请求校验。

## 11. 迭代器、生成器和惰性执行

迭代器支持逐次调用 `next()`。包含 `yield` 的生成器函数在调用时只返回生成器对象，第一次 `next()` 才开始执行函数体。

列表读取和生成器读取的主要区别：

| 维度 | 返回列表 | 返回生成器 |
| --- | --- | --- |
| 执行时机 | 调用时完整读取 | 消费时按需读取 |
| 额外内存 | 随记录数增长 | 主要保留当前记录 |
| 是否可重复遍历 | 可以 | 单次消费 |
| 提前停止 | 已经读取全部 | 可以避免处理后续记录 |
| 错误出现时机 | 调用阶段 | 消费到坏数据时 |

`list(generator)` 会消耗全部生成器，因此会失去提前停止和低内存优势。生成器暂停在 `with` 内时仍持有文件；提前结束且保留生成器引用时，应调用 `close()` 立即释放资源。

## 12. pytest 测试体系

### 12.1 断言

断言应检查真正重要的行为，而不只是“没有抛异常”。当前测试会检查：

- 返回值内容和顺序。
- 返回对象类型。
- 指标计算结果。
- 异常类型和关键信息。
- 惰性执行与提前停止。

### 12.2 参数化

`@pytest.mark.parametrize` 将每组输入收集为独立测试。Day 8 使用同一套测试逻辑覆盖：

- 普通数据。
- completion token 为零。
- prompt token 为零。

### 12.3 临时文件

`tmp_path` 为每个测试提供隔离目录。Windows 上曾出现不同登录身份共用 pytest 临时目录导致的 ACL 冲突；`tests/conftest.py` 使用真实登录身份分配独立 basetemp，从根因上隔离目录。

### 12.4 当前测试分层

- 函数级测试：筛选、统计、数据类转换。
- 文件边界测试：JSON/JSONL 读取与异常。
- 流水线测试：从文件到汇总结果的组合行为。

阶段 1 尚未引入网络接口，因此还没有 FastAPI 接口测试。

## 13. 指标计算

当前项目计算：

```text
total_tokens = prompt_tokens + completion_tokens
tokens_per_second = completion_tokens / (latency_ms / 1000)
```

`tokens_per_second` 只使用 completion token。prompt token 为零不会造成除零；只有 `latency_ms` 为零才会除零。当前数据模型尚未校验延迟必须大于零，这是后续可增强项。

TTFT、TPOT、并发吞吐和缓存收益尚未进入当前代码，不应在面试中声称已经实现。

## 14. 典型错误与经验

1. 使用 `dict.get()` 读取必要字段会静默隐藏字段缺失；必要字段使用 `data["key"]`。
2. 多个身份共用同一个 pytest 临时目录会产生 Windows ACL 冲突；目录应按真实登录身份隔离。
3. 在多个层级重复捕获并转换同一异常会产生不可达分支；异常应在最合适的一层转换一次。
4. 把三个嵌套 TODO 写成三段并列逻辑，会在离开 `with` 后读取已关闭文件。
5. prompt token 不参与生成吞吐量分母；指标期望必须根据真实公式推导。

## 15. 阶段通关自检

进入 HTTP 和 FastAPI 阶段前，应能不用看答案解释：

- JSON 和 JSONL 的结构、读取方式与适用场景。
- `with` 为什么能在异常时关闭文件。
- `raise ... from exc` 为什么有利于调试。
- 模块、包、`__init__.py` 和 `__all__` 的区别。
- 类型标注为什么不等于运行时校验。
- `dataclass` 与普通字典的取舍。
- 调用生成器函数和第一次 `next()` 的执行差异。
- 列表读取与生成器读取的内存和错误时机差异。
- pytest 参数化如何生成多个测试用例。
- 一条 JSONL 记录到 `BenchmarkSummary` 的完整生命周期。

## 16. 下一阶段边界

下一阶段从 HTTP 请求与响应开始，再进入第一个 FastAPI `/health` 接口和 `TestClient` 测试。阶段 1 的解析器不会被丢弃，它会逐步成为模型服务网关内部的数据处理能力。
