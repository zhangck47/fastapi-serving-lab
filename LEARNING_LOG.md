# 学习记录

## Day 1（2026-08-06）

- 今天学了什么：
  - `dict` 的基本用法：按键取值，如 `record["request_id"]`
  - 类型标注：`str`、`int`、`float`、`list[str]`、`dict[str, object]`，变量与函数参数/返回值都可以标注
  - 函数：定义、参数传入、返回值返回
  - 用已有字段计算新指标：`total_tokens` 直接相加；`tokens_per_second` 由完成 token 数除以耗时（毫秒转秒）得到
  - 汇总时返回一个新 `dict`，而不是修改原始记录
- 我独立写了什么：
  - `summarize_record` 中的 3 个 TODO：
    1. 从 `record` 取出 6 个字段，分别存入带类型标注的变量
    2. 计算 `total_tokens = prompt_tokens + completion_tokens` 和 `tokens_per_second = completion_tokens / (latency_ms / 1000)`
    3. 返回包含 `request_id`、`model`、`labels`、`total_tokens`、`tokens_per_second` 五个字段的新 `dict`
  - 通关验证：`.\.venv\Scripts\python.exe -m pytest -q` 结果为 `1 passed`
- 遇到了什么错误：
  - （如今天有遇到错误，请在这里补充；没有则写"无"）
- 错误原因是什么：
  - （与上一项对应，补充错误原因）
- 明天需要复习什么：
  - `dict` 按键取值的写法
  - 类型标注的基本语法（变量、函数参数、返回值）
  - 毫秒转秒再除法的直觉：`640ms → 0.64s`，`8 / 0.64 = 12.5`

## Day 2（2026-08-11）

- 今天学了什么：
  - 用 `for` 循环逐条处理 `list` 中的压测记录
  - 用 `if` 判断记录的 `status`，并通过 `append()` 保存成功记录
  - 用 `set` 去除重复模型名，再用 `sorted()` 和 `tuple()` 得到稳定、有序的结果
- 我独立写了什么：
  - 完成 `filter_successful_records`，筛选成功记录并保持原始顺序
  - 完成 `collect_model_names`，对模型名去重、排序并返回元组
  - 让两个函数能够组合使用：先筛选成功记录，再收集模型名
  - 通关验证：`.\.venv\Scripts\python.exe -m pytest -q` 结果为 `5 passed`
- 遇到了什么错误：
  - 无运行错误，pytest 的 5 个测试全部通过
  - 代码审查发现：使用 `record.get()` 可能把缺少必要字段的坏记录静默处理掉
- 错误原因是什么：
  - 测试输入都包含完整字段，所以当前功能运行正常
  - `dict.get()` 在键不存在时返回 `None`，不会像 `record["status"]` 一样立即抛出 `KeyError`，因此可能隐藏输入数据问题
- 代码审查记录：
  - `record.get("status")` 会把缺少 `status` 的记录当成不成功记录，可能隐藏输入数据问题
  - `dict[str, object]` 的值类型很宽，静态检查器无法确认取出的模型名一定是字符串
  - `return (tuple(sorted(models)))` 可以去掉多余的外层括号，行为不变
- 明天需要复习什么：
  - `for` 循环中每次迭代时 `record` 分别指向什么
  - 为什么 `set` 能去重，但不适合直接承担有序输出
  - `record["status"]` 与 `record.get("status")` 在字段缺失时的区别

### Day 2 复习问题答案

1. `filter_successful_records` 为什么能保持原始顺序？
   - `for` 会按照列表从前到后的顺序读取每条记录；符合条件时，`append()` 又按照发现顺序把记录放进新列表，所以成功记录之间的原始顺序不会改变。
2. 为什么 `set` 去重后还需要 `sorted()`？
   - `set` 的职责是保证元素不重复，但不承诺我们需要的稳定输出顺序。`sorted()` 会把模型名按字母顺序排列，使每次运行和测试都得到一致结果，最后再转成题目要求的 `tuple`。
3. `record["status"]` 和 `record.get("status")` 在字段缺失时有什么区别？
   - `record["status"]` 把 `status` 当成必要字段，缺失时抛出 `KeyError`，能较早暴露坏数据；`record.get("status")` 缺失时默认返回 `None`，程序可以继续运行，但也可能静默隐藏数据问题。

## Day 3（2026-08-12）

- 今天学了什么：
  - 使用 `pathlib.Path` 表示文件路径，并通过 `read_text(encoding="utf-8")` 读取文本
  - 使用 `json.loads()` 把 JSON 字符串转换为 Python 对象
  - 使用 `try/except` 捕获指定异常，并通过 `raise ... from exc` 提供清晰错误信息和保留异常链
- 我独立写了什么：
  - 完成 `load_benchmark_record()` 的 3 个 TODO
  - 正确读取合法 JSON 文件并返回 `dict`
  - 将文件不存在转换为带路径信息的 `FileNotFoundError`
  - 将 JSON 格式损坏转换为带路径信息的 `ValueError`
  - 通关验证：`.\.venv\Scripts\python.exe -m pytest -q` 结果为 `8 passed`
- 遇到了什么错误：
  - pytest 创建 `tmp_path` 时出现 `PermissionError: [WinError 5] 拒绝访问`，目标是 Windows 用户临时目录中的 `pytest-of-zck`
- 错误原因是什么：
  - 错误发生在测试准备临时目录的阶段，还没有进入 `load_benchmark_record()`，因此不是 JSON 读取代码导致的
  - 当前终端对 Windows 默认 pytest 临时目录没有正常访问权限，或者该目录存在权限异常的历史残留
  - 通过 `--basetemp=.pytest-tmp` 将 pytest 临时目录固定到项目内可写位置，并在 `.gitignore` 中忽略它后解决
- 明天需要复习什么：
  - 文件读取成功不代表 JSON 解码一定成功
  - `json.load()` 与 `json.loads()` 的输入区别
  - 异常类型、异常信息和异常链分别解决什么问题

### Day 3 复习问题答案

1. 文件存在是否就代表其中一定是合法 JSON？为什么？
   - 不代表。文件存在只说明路径可以找到并读取；文件内容仍可能为空、缺少引号或括号、存在多余逗号，因此读取成功后还必须单独进行 JSON 解码。
2. `json.loads()` 的输入和输出分别是什么？
   - 输入是包含 JSON 内容的字符串、字节或字节数组；本项目传入的是 `read_text()` 得到的字符串。输出是对应的 Python 对象，例如 JSON 对象会转换成 `dict`，JSON 数组会转换成 `list`。
3. `raise NewError(...) from exc` 中的 `from exc` 有什么价值？
   - 它把新的业务层错误和原始底层错误连接起来。调用者能看到更容易理解的新错误，调试时也能沿异常链找到真正的底层原因。

## Day 4（2026-08-13）

- 今天学了什么：
  - 使用 `with` 上下文管理器打开文件，让文件在正常结束或发生异常时都能自动关闭
  - 使用 `enumerate(file, start=1)` 逐行读取 JSONL，并获得与编辑器一致的真实行号
  - 使用 `line.strip()` 识别并跳过空白行，再用 `json.loads()` 解码每个非空行
  - 将坏行的 `JSONDecodeError` 转换为包含行号和文件路径的 `ValueError`
- 我独立写了什么：
  - 完成 `load_benchmark_records()` 的 3 个 TODO
  - 实现合法 JSONL 的逐行读取、空白行跳过和空文件处理
  - 实现损坏 JSON 行的准确定位，并使用 `raise ... from exc` 保留异常链
  - 通关验证：`.\.venv\Scripts\python.exe -m pytest -q` 结果为 `11 passed`
- 遇到了什么错误：
  - pytest 为 `tmp_path` 准备目录时出现 `PermissionError: [WinError 5] 拒绝访问`
  - 错误先后出现在 Windows 默认目录 `pytest-of-zck` 和项目共享目录 `.pytest-tmp`
  - 代码审查发现循环内部提前把 `JSONDecodeError` 转成了 `ValueError`，使外层同类异常处理分支无法执行
- 错误原因是什么：
  - Codex 测试进程的真实 Windows 登录身份是 `CodexSandboxOffline`，而普通终端身份是 `zck`
  - Python 环境变量仍让部分用户识别函数返回 `zck`，造成目录名称像属于 `zck`，实际 ACL 所有者却是沙箱身份
  - 两个身份复用同一个 pytest 临时目录时，一方创建的私有 ACL 会导致另一方无法访问或清理
  - 异常处理方面，内部 `except` 已经改变异常类型，外层 `except json.JSONDecodeError` 因而成为不可达分支
- 解决办法：
  - 在 `tests/conftest.py` 中使用 `os.getlogin()` 取得真实登录身份
  - 为不同身份分配独立的同级目录：`.pytest-tmp-zck` 和 `.pytest-tmp-CodexSandboxOffline`
  - 在 `.gitignore` 中忽略 `.pytest-tmp-*/`，避免临时数据进入 Git
  - 删除内部重复的异常转换，由外层统一添加行号、路径和异常链
- 明天需要复习什么：
  - `with` 的进入、退出和自动清理作用
  - JSON 与 JSONL 的文件结构和读取方式差异
  - 为什么真实文件行号必须在跳过空行之前由 `enumerate` 生成
  - 为什么异常不应在多个层级被重复捕获和转换

### Day 4 复习问题答案

1. `with` 如何保证发生异常时文件仍然会被关闭？
   - 文件对象是上下文管理器。进入 `with` 时打开资源，离开代码块时 Python 会调用它的退出逻辑；无论正常结束还是因异常退出，退出逻辑都会关闭文件。
2. 为什么要使用 `enumerate(file, start=1)`，而不是只在成功解码后增加计数器？
   - `enumerate` 对文件中的每一行计数，包括之后被跳过的空白行，因此得到的行号与编辑器中的真实位置一致。只在成功解码后计数会漏掉空行，也无法准确指出损坏行。
3. JSON 与 JSONL 在文件结构和读取方式上有什么区别？
   - JSON 文件通常整体构成一个合法 JSON 值，需要整体解码；JSONL 每个非空行都是一个独立 JSON 值，适合逐行读取和处理，不必一次把整个文件放入内存。

## Day 5（2026-08-17）

- 今天学了什么：
  - 一个 `.py` 文件是一个模块，包含 `__init__.py` 的目录可以组成 Python 包
  - 使用相对导入把包内不同模块的名称汇总到包顶层
  - `__init__.py` 可以定义包的稳定入口，`__all__` 用于声明希望公开的名称
  - 虚拟环境为项目隔离 Python 解释器和第三方依赖，避免不同项目的依赖版本互相影响
- 我独立写了什么：
  - 从 `.metrics` 导入并公开五个统计相关名称
  - 从 `.loaders` 导入并公开两个文件读取函数
  - 定义包含七个名称的 `__all__` 公共接口清单
  - 通关验证：`.\\.venv\\Scripts\\python.exe -m pytest -q` 结果为 `14 passed`
- 遇到了什么错误：
  - 没有运行错误，14 个测试一次通过
  - 代码审查发现导入语句全部写在一行，逗号后缺少空格
- 错误原因是什么：
  - Python 语法允许紧凑写法，所以不影响运行和测试
  - 但过长且缺少空格的导入不符合常用代码风格，会降低可读性，后续添加或删除名称也更容易产生难以审查的改动
- 明天需要复习什么：
  - 模块与包的区别，以及本项目中对应的例子
  - 相对导入中的 `.` 表示什么
  - `__init__.py` 的重新导出与 `__all__` 的职责区别
  - 虚拟环境隔离了什么，以及为什么运行命令要使用 `.venv` 中的 Python

### Day 5 复习问题答案

1. 模块和包分别是什么？本项目中的例子是什么？
   - 模块通常是一个可以被导入的 `.py` 文件，例如 `metrics.py` 和 `loaders.py`。包是组织多个模块的目录，本项目中的 `serving_lab` 就是一个包，`__init__.py` 是它的包入口。
2. 为什么调用者使用 `from serving_lab import ...`，通常比依赖内部模块路径更稳定？
   - 包顶层入口把内部结构隐藏在后面。将来即使把函数从 `metrics.py` 移到别的模块，只要 `serving_lab/__init__.py` 继续公开同一个名称，调用者就不需要修改导入代码。
3. 虚拟环境解决了什么问题？它会自动改变你的 Python 源代码吗？
   - 虚拟环境把项目使用的解释器和第三方依赖与其他项目隔离，避免版本冲突。它不会修改源代码，只会影响运行命令实际使用哪个 Python，以及这个 Python 能找到哪些已安装依赖。
