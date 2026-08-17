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

第 5 天已通过：把单文件代码拆成职责清晰的 Python 包，并理解虚拟环境如何隔离项目。

Day 5 的 3 个 TODO 已完成，完整测试结果为 `14 passed`（2026-08-17）。

当前目录结构：

```text
src/
└── serving_lab/
    ├── __init__.py
    ├── loaders.py
    └── metrics.py
```

- `metrics.py`：统计、筛选和示例数据。
- `loaders.py`：JSON/JSONL 文件读取。
- `__init__.py`：定义调用者能从包顶层使用的公开接口。

## Day 5 学习任务

### 今日目标

1. 理解模块、包和导入路径的关系。
2. 使用 `__init__.py` 提供稳定的包级公开接口。
3. 理解 `.venv` 如何隔离解释器和依赖。

### 必要知识

一个 `.py` 文件就是一个模块。包含 `__init__.py` 的目录可以作为普通 Python 包：

```python
from serving_lab.metrics import summarize_record
```

包可以在 `__init__.py` 中重新导出常用名称，让调用者使用更稳定的入口：

```python
from serving_lab import summarize_record
```

`__all__` 是公开接口清单，表达“这个包希望外部使用哪些名称”。它不是安全机制，也不会自动导入名称。

虚拟环境 `.venv` 提供独立解释器和依赖目录，避免不同项目的包版本互相污染。当前 editable 安装通过 `.pth` 把项目的 `src` 放入虚拟环境导入路径，拆包后无需安装新依赖。

### 今天修改的文件

- `src/serving_lab/metrics.py`：统计和筛选职责。
- `src/serving_lab/loaders.py`：文件读取职责。
- `src/serving_lab/__init__.py`：需要你完成的包公开接口。
- `tests/test_benchmark_parser.py`：验证原有功能和包公开接口。
- `pyproject.toml`：从单模块打包改为自动发现 `src` 下的包。
- `README.md`、`ROADMAP.md`、`LEARNING_LOG.md`：Day 5 学习材料。

### 我的编码任务（已完成）

- 从 `.metrics` 相对导入五个统计相关名称。
- 从 `.loaders` 相对导入两个读取函数。
- 在 `__all__` 中按测试要求列出七个公开名称。

### 运行命令

```powershell
.\.venv\Scripts\python.exe -m pytest -q
```

这条命令使用项目虚拟环境运行全部测试，验证拆包没有改变前四天的行为。

### 预期结果

完成 TODO 前，原有功能测试仍应通过，新增包接口测试会失败；正确完成后应看到：

```text
14 passed
```

### 测试

今天新增三个测试：包顶层公开统计函数、公开读取函数、声明完整 `__all__`。原有 11 个测试改为从职责模块导入，以证明拆分没有改变功能。

### 常见错误

1. 在包内写 `from metrics import ...`，Python 会寻找顶级模块；应使用 `.metrics` 相对导入。
2. 只填写 `__all__` 却没有真正导入名称；`__all__` 不会自动创建包属性。
3. 使用系统 `python` 而不是 `.venv` 中的解释器，导致导入路径或依赖版本不同。

### 复习问题

1. 模块和包分别是什么？本项目中的例子是什么？
2. 为什么调用者使用 `from serving_lab import ...`，通常比依赖内部模块路径更稳定？
3. 虚拟环境解决了什么问题？它会自动改变你的 Python 源代码吗？

### 通关标准

- 3 个 TODO 均由你完成，且没有修改测试。
- 全部 14 个测试通过。
- 能解释模块、包、`__init__.py`、`__all__` 和虚拟环境的作用。
- 能用自己的话回答 3 道复习题。
- 完成 `LEARNING_LOG.md` 的 Day 5 记录。

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
