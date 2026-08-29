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

## Day 6（2026-08-18）

- 今天学了什么：
  - 类定义对象具有什么字段和行为，对象是按照类创建的一份具体数据
  - `@dataclass` 会自动生成初始化、比较和便于阅读的字符串表示
  - `bool | None` 可以区分 `True`、`False` 和“没有提供这个信息”三种状态
  - 可以在 JSON 解码边界把宽泛字典转换成字段明确的数据对象
- 我独立写了什么：
  - 为 `BenchmarkRecord` 定义八个带类型标注的字段，并为可选的 `cache_hit` 设置 `None` 默认值
  - 为 `BenchmarkSummary` 定义五个汇总字段
  - 实现 `benchmark_record_from_dict()`，将字典字段传入 `BenchmarkRecord`
  - 通关验证：`.\\.venv\\Scripts\\python.exe -m pytest -q` 结果为 `18 passed`
- 遇到了什么错误：
  - 没有运行错误，18 个测试全部通过
  - 代码审查发现类型标注缺少常用空格，并且 `BenchmarkSummary.cache_hit` 设置了不必要的默认值
- 错误原因是什么：
  - Python 允许 `request_id:str` 和 `bool|None` 这样的紧凑语法，因此测试不会失败，但它不符合常用可读性规范
  - `BenchmarkRecord.cache_hit` 可以缺失，所以默认值合理；`BenchmarkSummary` 由汇总函数完整创建，继续提供默认值会让调用者意外漏传字段而不被及时发现
- 明天需要复习什么：
  - 类与对象的关系，以及 `@dataclass` 自动生成了哪些基础能力
  - 为什么有默认值的字段要放在没有默认值的字段之后
  - `False` 与 `None` 的业务含义为什么不同
  - 字典到数据类对象的转换边界有什么价值

### Day 6 复习问题答案

1. 类和对象是什么关系？请用 `BenchmarkRecord` 举例。
   - 类像结构模板，规定数据有哪些字段；对象是按照模板创建的具体实例。`BenchmarkRecord` 是类，而某次请求对应的 `BenchmarkRecord(request_id="req_001", ...)` 是对象。
2. 相比一直传递 `dict[str, object]`，`dataclass` 在可读性和错误发现方面有什么好处？
   - 数据类把字段名和预期类型集中声明出来，阅读代码时能直接看出数据结构；编辑器也更容易提示属性名。访问对象字段时写 `record.model`，如果名称写错更容易暴露，而宽泛字典只能看到值是 `object`。
3. `cache_hit=False` 与 `cache_hit=None` 分别表示什么？为什么不能混为一谈？
   - `False` 表示记录明确说明缓存没有命中，`None` 表示记录没有提供缓存信息。把二者混在一起会让“已知未命中”和“状态未知”无法区分，导致缓存命中率等统计失真。

## Day 7（2026-08-19）

- 今天学了什么：
  - 迭代器通过 `next()` 一次提供一个值，生成器是使用 `yield` 编写的一类迭代器
  - 调用生成器函数只创建生成器对象，第一次 `next()` 才真正开始执行函数和打开文件
  - `yield` 返回一条记录后会暂停并保存执行位置，下一次 `next()` 从暂停处继续
  - 惰性读取不必一次把整个 JSONL 放入内存，并且可以在后续坏行之前提前停止
- 我独立写了什么：
  - 实现 `iter_benchmark_records()`，使用 `with` 和 `enumerate()` 逐行遍历文件
  - 跳过空白行并用 `json.loads()` 解码非空行
  - 使用 `yield` 逐条产出记录，同时保留文件不存在和坏行行号异常
  - 通关验证：`.\\.venv\\Scripts\\python.exe -m pytest -q` 结果为 `22 passed`
- 遇到了什么错误：
  - 第一次实现后出现 `ValueError: I/O operation on closed file`
  - 当时测试结果为 `1 failed, 21 passed`
- 错误原因是什么：
  - 把 TODO 1、TODO 2、TODO 3 误解成三段并列实现，先在 `with` 中完整读取一次，离开 `with` 后又重复遍历 `file`
  - 离开 `with` 时文件已经自动关闭，生成器被 `list()` 继续消耗后运行到第二个循环，因此读取已关闭文件失败
  - 后面的 `json.loads(line)` 还丢弃了返回值，而 `yield record` 会重复使用旧变量
- 明天需要复习什么：
  - 调用生成器函数和调用 `next()` 分别发生了什么
  - `yield` 暂停、继续和结束的执行顺序
  - `list()` 为什么会消耗完整生成器
  - 提前停止时为什么应关闭仍持有文件的生成器

### Day 7 复习问题答案

1. 调用生成器函数时为什么还没有读取文件？第一次 `next()` 时会发生什么？
   - 因为函数体中包含 `yield`，调用函数只会返回生成器对象，不执行函数体。第一次 `next()` 才从函数开头执行，打开文件、读取并解码第一条有效记录，然后在第一个 `yield` 处返回记录并暂停。
2. `load_benchmark_records()` 返回列表，与 `iter_benchmark_records()` 返回生成器相比，各自适合什么场景？
   - 列表适合文件较小、后续需要反复访问全部记录的场景，使用简单但会一次占用与数据量相关的内存。生成器适合大文件、只需单次遍历或可能提前停止的场景，只保留当前处理所需的数据。
3. 文件第二行是坏 JSON 时，为什么只读取第一条可以不报错？错误会在什么时候出现？
   - 生成器是惰性执行的，第一次 `next()` 只运行到第一条记录的 `yield`，还没有读取第二行。再次调用 `next()` 或用 `list()` 继续消耗生成器、真正解码第二行时，才会出现 JSON 错误。

## Day 8（2026-08-23）

- 今天学了什么：
  - pytest 的 `assert` 是可执行预期，失败时会显示实际值与期望值
  - `@pytest.mark.parametrize` 会把每组参数收集成独立测试，减少重复测试代码
  - 可以把文件读取、JSON 解码、数据类转换和指标计算组合成仍保持惰性的流水线
  - 正常、边界和异常用例承担不同职责，三者共同构成回归保护
- 我独立写了什么：
  - 实现 `iter_benchmark_summaries()`，串联三个已有模块并逐条产出 `BenchmarkSummary`
  - 添加普通数据、零 completion 和零 prompt 三组参数化用例
  - 为汇总数量、数据类型、总 token 数和生成吞吐量编写断言
  - 通关验证：`.\\.venv\\Scripts\\python.exe -m pytest -q` 结果为 `26 passed`
- 遇到了什么错误：
  - 零 prompt 用例最初期望 `tokens_per_second` 为 `float("inf")`，实际结果为 `10.0`
  - 当时测试结果为 `1 failed, 25 passed`
- 错误原因是什么：
  - 把零 prompt token 误认为吞吐量公式的分母为零
  - 实际公式是 `completion_tokens / (latency_ms / 1000)`，prompt token 不参与生成吞吐量计算
  - 按原输入 `5 completion tokens / 0.5 seconds`，正确结果应为 `10.0`；最终按题目改成 250ms，对应 `20.0`
- 明天需要复习什么：
  - 参数列表、测试函数参数和期望值的对应关系
  - 一条记录从 JSONL 文件到 `BenchmarkSummary` 的完整生命周期
  - 类型标注说明、运行时校验和自动化测试三者的职责区别
  - Python 阶段各模块的职责边界和异常传播路径

### Day 8 复习问题答案

1. 为什么一个参数化测试函数最终会显示为三个测试？相比复制三份测试有什么好处？
   - `@pytest.mark.parametrize` 会为参数列表中的每个参数组分别调用一次测试函数，所以三组数据会被收集成三个独立用例。它把共同的准备、调用和断言逻辑只写一次，新增边界数据时只添加参数，能够减少复制错误并保持各用例行为一致。
2. 请按顺序解释一条 JSONL 记录到 `BenchmarkSummary` 的完整生命周期。
   - `iter_benchmark_records()` 打开 UTF-8 JSONL 文件并逐行读取，跳过空行后用 `json.loads()` 得到字典；`benchmark_record_from_dict()` 将字典转换成 `BenchmarkRecord`；`summarize_benchmark_record()` 计算总 token 数和每秒生成 token 数并返回 `BenchmarkSummary`；`iter_benchmark_summaries()` 使用 `yield` 将汇总逐条交给调用者。
3. 正常、边界和异常测试分别防止什么问题？本项目中各举一个例子。
   - 正常测试确认常见输入能够得到正确业务结果，例如 12 个 prompt token 和 8 个 completion token 得到总数 20。边界测试检查合法但极端的数据，例如 completion 为零时吞吐量应为 0.0。异常测试确认错误输入不会被静默接受，例如损坏 JSONL 应报告准确坏行行号。

## Python 核心基础阶段通关（Day 1～Day 8）

- 已能处理 JSON、JSONL、文件不存在和格式损坏等场景
- 已能使用函数、类型标注、模块、包、数据类与可选值组织代码
- 已能使用上下文管理器与生成器进行资源安全的惰性读取
- 已能编写普通、边界、异常和参数化 pytest 测试
- 已能解释当前压测解析流水线的职责、执行顺序和主要设计取舍
- 阶段总结：`PYTHON_STAGE_REVIEW.md`
- 面试题库：`INTERVIEW_QA.md`

## Day 9（2026-08-29）

- 今天学了什么：
  - HTTP 请求由客户端发给服务端，响应由服务端返回客户端；方法和路径描述请求目标，状态码和响应体描述处理结果
  - GET 通常用于读取状态；FastAPI 使用“HTTP 方法 + 路径”匹配处理函数
  - `@app.get("/health")` 把 `health()` 注册为 GET 路由，函数返回的字典会被 FastAPI 转成 JSON
  - `TestClient` 能在 pytest 进程内访问应用，不需要先启动真实网络服务器
- 我独立写了什么：
  - 使用 GET 路由装饰器注册 `/health`
  - 为 `health()` 添加 `dict[str, str]` 返回值类型标注
  - 返回 `{"status": "ok"}`，使接口返回状态码 200 和预期 JSON
  - 通关验证：`.\.venv\Scripts\python.exe -m pytest -q` 结果为 `29 passed`
- 遇到了什么错误：
  - 没有功能错误，三个新增接口测试全部通过
  - 代码审查发现完成实现后仍保留了 TODO 2、TODO 3 注释，并写成了较紧凑的 `dict[str,str]`
- 错误原因是什么：
  - Python 允许 `dict[str,str]`，所以不影响运行；但逗号后保留空格更符合常用风格，也更易读
  - TODO 注释只用于标识未完成任务，功能完成后应删除，否则维护者可能误判代码状态
- 明天需要复习什么：
  - HTTP 方法和路径为什么要一起匹配
  - 200、404、405 三种状态码的区别
  - FastAPI 如何把 Python 字典转换为 JSON 响应
  - `TestClient` 接口测试比直接调用函数多验证了什么

### Day 9 复习问题答案

1. 一次 `client.get("/health")` 从请求产生到断言响应，按顺序发生了什么？
   - `TestClient` 构造 GET 请求并把它交给 FastAPI 应用；FastAPI 使用 GET 方法和 `/health` 路径查找路由，调用 `health()`；函数返回字典后，FastAPI 将其转换为 JSON 响应并使用默认成功状态码 200；测试最后读取 `status_code` 和 `json()` 进行断言。
2. 为什么 `GET /health` 应为 200，而 `POST /health` 应为 405？404 又表示什么？
   - GET 方法和 `/health` 路径都能匹配已注册路由，因此成功返回 200。`/health` 路径存在，但只登记了 GET，使用 POST 时方法不允许，所以返回 405。如果没有任何路由能匹配目标路径，则返回 404。
3. 为什么接口测试既要检查 `response.status_code`，又要检查 `response.json()`？
   - 状态码验证请求是否按预期成功或失败，JSON 验证实际业务数据。只检查 200 可能漏掉错误响应体，只检查 JSON 又可能漏掉错误的 HTTP 语义，因此两者需要分别断言。
