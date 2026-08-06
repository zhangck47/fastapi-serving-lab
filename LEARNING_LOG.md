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
