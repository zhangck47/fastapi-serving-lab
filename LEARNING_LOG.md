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
  - 请补充你编码或运行测试时实际遇到的错误；如果没有，请写“无”
- 错误原因是什么：
  - 请与上一项对应填写；如果没有错误，请写“不适用”
- 代码审查记录：
  - `record.get("status")` 会把缺少 `status` 的记录当成不成功记录，可能隐藏输入数据问题
  - `dict[str, object]` 的值类型很宽，静态检查器无法确认取出的模型名一定是字符串
  - `return (tuple(sorted(models)))` 可以去掉多余的外层括号，行为不变
- 明天需要复习什么：
  - `for` 循环中每次迭代时 `record` 分别指向什么
  - 为什么 `set` 能去重，但不适合直接承担有序输出
  - `record["status"]` 与 `record.get("status")` 在字段缺失时的区别
