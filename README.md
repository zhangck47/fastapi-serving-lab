# fastapi-serving-lab

一个从 Python 基础逐步演进到 OpenAI 兼容模型服务网关的连续练习项目。

## 学习方式

- 每天投入 60～90 分钟。
- 每天只增加 2～3 个核心概念。
- Day 9 起先阅读独立的 `docs/day-XX-concepts.md`，理解概念后再开始 TODO。
- 顺序固定为：概念讲义、独立编码、pytest 测试、复盘。
- 当天通关后才进入下一天。
- 不使用真实 API Key、GPU、公司网络或公司文件。

完整安排见 [ROADMAP.md](ROADMAP.md)，每日复盘写入 [LEARNING_LOG.md](LEARNING_LOG.md)。

## 当前进度

第 8 天已通过：用 pytest 参数化测试串联 Python 阶段的完整压测解析流程。第 9 天已通过：完成第一个 FastAPI `GET /health` 接口和 `TestClient` 测试。

Day 9 的 3 个 TODO 已完成，完整测试结果为 `29 passed`（2026-08-29）。Python 核心基础阶段已通过，HTTP、FastAPI 和 pytest 阶段正在进行。

阶段总结见 [PYTHON_STAGE_REVIEW.md](PYTHON_STAGE_REVIEW.md)，当前项目面试题库见 [INTERVIEW_QA.md](INTERVIEW_QA.md)。面试题库只记录已经实现并能用代码证明的能力，后续阶段完成后继续扩充。

当前目录结构：

```text
src/
└── serving_lab/
    ├── __init__.py
    ├── app.py
    ├── loaders.py
    ├── metrics.py
    ├── models.py
    └── pipeline.py
```

Day 9 起的概念讲义保存在 `docs/`，当天讲义与 TODO 代码分开。先阅读讲义中的最小示例和检查问题，再开始修改源码。

- `metrics.py`：统计、筛选和示例数据。
- `loaders.py`：JSON/JSONL 文件读取。
- `models.py`：压测记录与汇总结果的数据类。
- `pipeline.py`：连接惰性读取、数据转换和指标汇总。
- `__init__.py`：定义调用者能从包顶层使用的公开接口。

## Day 9 学习任务

### 今日目标

1. 能说清 HTTP 请求和响应的方向及最小组成。
2. 能解释 GET 方法与 URL 路径如何共同定位一个操作。
3. 能完成 `/health` 路由，并使用 `TestClient` 从 HTTP 入口测试它。

### 必要知识

先完整阅读 [docs/day-09-concepts.md](docs/day-09-concepts.md)。讲义使用不同的 `/ping` 示例介绍 HTTP 请求/响应、GET、FastAPI 路由和 `TestClient`，不会直接给出今天 TODO 的完整答案。

开始编码前，应先能回答讲义末尾的 5 个基础问题。今天暂不学习 POST 请求体、Pydantic 模型、异步或服务器部署。

### 今天修改的文件

- `docs/day-09-concepts.md`：Day 9 独立概念讲义。
- `src/serving_lab/app.py`：FastAPI 应用和 `/health` 的 3 个 TODO。
- `tests/test_health.py`：从 HTTP 入口验证状态码、JSON 和 GET 方法。
- `pyproject.toml`：记录 FastAPI 运行依赖和 httpx 测试依赖。
- `ROADMAP.md`：记录 Day 9 进度和长期“先讲义、后 TODO”规则。
- `LEARNING_LOG.md`：提供 Day 9 学习记录模板。
- `README.md`：提供完整的 Day 9 学习任务和通关标准。

### 我的编码任务（已完成）

- `TODO 1`：使用 GET 路由装饰器，把 `health()` 注册到 `/health`。
- `TODO 2`：为 `health()` 添加准确的返回值类型标注。
- `TODO 3`：返回 `{"status": "ok"}`，让 FastAPI 生成 JSON 响应。

不要修改测试来迎合当前占位实现。三个 TODO 完成后，测试应自然转绿。

### 运行命令

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

这条命令使用项目虚拟环境运行完整测试，既验证 Day 9 的 HTTP 接口，也防止破坏阶段 1 的解析器。

### 预期结果

课程骨架尚未注册 `/health` 时，预期结果为：

```text
3 failed, 26 passed
```

失败分别对应 GET 状态码、JSON 响应体和 POST 方法检查，它们都由当时尚未完成的 TODO 引起。三个 TODO 已完成，当前结果为：

```text
29 passed
```

当前最新依赖组合还可能显示一条 `StarletteDeprecationWarning`。它来自 FastAPI/Starlette 的上游依赖过渡，不是 TODO 失败，也不影响今天的测试结论。

### 测试

`tests/test_health.py` 使用 `TestClient` 覆盖：

1. `GET /health` 返回状态码 `200`。
2. 响应 JSON 为 `{"status": "ok"}`。
3. `POST /health` 返回 `405`，证明路由只允许 GET。

### 常见错误

1. 把路径写成 `"health"`，忘记 URL 路径必须以 `/` 开头。
2. 把装饰器写成 `@app.get`，忘记调用 `.get("/health")`。
3. 返回 JSON 字符串 `'{"status": "ok"}'`，而不是让 FastAPI 转换 Python 字典。

### 复习问题

1. 一次 `client.get("/health")` 从请求产生到断言响应，按顺序发生了什么？
2. 为什么 `GET /health` 应为 `200`，而 `POST /health` 应为 `405`？`404` 又表示什么？
3. 为什么接口测试既要检查 `response.status_code`，又要检查 `response.json()`？

### 通关标准

- 先阅读概念讲义并能回答其中 5 个基础检查问题。
- 独立完成 `app.py` 的 `TODO 1`、`TODO 2`、`TODO 3`，不修改测试预期。
- 完整测试达到 `29 passed`。
- 能用自己的话回答 3 道复习题。
- 按模板完成 `LEARNING_LOG.md` 的 Day 9 记录。

以上通关条件已于 2026-08-29 全部完成。

### 学习记录

把以下内容填写到 `LEARNING_LOG.md` 的 Day 9 部分：

- 今天学了什么
- 我独立写了什么
- 遇到了什么错误
- 错误原因是什么
- 明天需要复习什么

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
- Web 框架：FastAPI 0.141.1
- 接口测试客户端：httpx 0.28.1
- 开发测试：pytest 9.1.1

2026-08-05 已完成本机学习环境配置：

- Python 3.12.10
- 项目虚拟环境：`.venv`
- pytest 9.1.1

当前 Windows 的旧 `py` 启动器尚未识别新解释器，因此在项目目录中使用虚拟环境的解释器运行测试：

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```
