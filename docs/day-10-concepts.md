# Day 10 新概念讲义

## 1. 今天为什么要学习这些概念

Day 9 的 `/health` 是固定地址：每次请求都访问同一个路径，也不携带额外参数。模型服务网关还需要处理“访问哪个对象”和“使用什么选项”这两类信息，例如：

```text
GET /models/mock-llm?limit=3
```

这里的 `mock-llm` 指定一个模型，`limit=3` 指定一个查询选项。为了看懂并正确处理这类请求，今天学习三个概念：URL、Path 参数和 Query 参数。

它们会逐步用于后续的模型查询和聊天接口。今天只创建一个观察参数来源的练习路由，不提前实现 `/v1/models`、POST 请求体或 Pydantic 模型。

## 2. 概念一：URL

### 它是什么

URL 是 Uniform Resource Locator 的缩写，中文通常叫“统一资源定位符”。它是客户端用来指出“要访问哪里”的地址。

观察下面这个完整 URL：

```text
http://127.0.0.1:8000/products/book?copies=2
```

今天需要认识的组成部分是：

| 部分 | 示例 | 含义 |
| --- | --- | --- |
| 协议 | `http` | 客户端和服务端使用哪套通信规则 |
| 主机 | `127.0.0.1` | 服务运行在哪台主机；这里表示本机 |
| 端口 | `8000` | 主机上由哪个程序接收请求 |
| 路径 | `/products/book` | 要访问服务中的哪个功能或资源 |
| 查询字符串 | `copies=2` | 附加在请求上的查询选项 |

路径和查询字符串之间使用 `?` 分隔。多个查询参数之间通常使用 `&` 分隔，例如：

```text
/products/book?copies=2&language=zh
```

### 它解决什么问题

一个服务可以提供很多接口。URL 让客户端明确指定服务地址、目标路径和查询选项，服务端才能把请求交给正确的处理逻辑。

对于最终模型网关，URL 会区分 `/health`、`/v1/models` 和 `/v1/chat/completions` 等功能。Path 和 Query 参数则让固定路由能够处理不同输入，不必为每个模型写一条新路由。

### 最基础的语法或使用方法

可以先记住这个最小结构：

```text
协议://主机:端口/路径?查询参数名=查询参数值
```

在 `TestClient` 中，不需要写协议、主机和端口，只写应用内部的路径与查询字符串：

```python
response = client.get("/products/book?copies=2")
```

`TestClient` 已经知道请求要发给当前测试的 FastAPI 应用。

### 一个最小示例

```python
request_url: str = "/products/book?copies=2"
response = client.get(request_url)
```

### 示例的输入、执行过程和输出

- 输入 URL：`/products/book?copies=2`。
- FastAPI 读取路径 `/products/book`，用它匹配路由。
- FastAPI 读取查询字符串 `copies=2`，把值交给对应函数参数。
- 处理函数运行后返回响应。

URL 本身只是地址和参数的载体。具体由哪个 Python 函数处理，还要看 FastAPI 路由声明。

### 它会在今天哪个 TODO 中使用

- TODO 1 要在路由中写出包含动态部分的 URL 路径。
- 测试会使用不同 URL，观察路径值和查询值如何进入函数。

### 初学者最容易混淆的地方

1. URL 路径从 `/` 开始；Python 函数名不需要 `/`。
2. `?` 后面是查询字符串，不再属于路径。
3. `TestClient` 中的相对 URL 不写 `http://127.0.0.1:8000`，不代表真实 HTTP URL 没有主机和端口。
4. URL 中的值最初来自文本，FastAPI 会根据类型标注尝试转换。

## 3. 概念二：Path 参数

### 它是什么

Path 参数是 URL 路径中会变化的一段值。FastAPI 使用花括号声明动态位置：

```python
@example_app.get("/products/{product_id}")
```

`{product_id}` 不是固定文字。访问 `/products/book` 时，`product_id` 的值是 `"book"`；访问 `/products/pen` 时，它的值是 `"pen"`。

### 它解决什么问题

没有 Path 参数时，可能需要为每个产品分别写 `/products/book`、`/products/pen` 等路由。使用 `{product_id}` 后，一条路由就能处理不同产品。

模型网关也可能需要通过路径定位具体资源。Path 参数适合表达“请求针对哪个对象”，并且通常是路径不可缺少的一部分。

### 最基础的语法或使用方法

路由中的花括号名称，必须和函数参数名称一致：

```python
@example_app.get("/products/{product_id}")
def read_product(product_id: str) -> dict[str, str]:
    return {"product_id": product_id}
```

这里有两处 `product_id`：

- `"/products/{product_id}"` 告诉 FastAPI 从路径捕获值。
- `product_id: str` 告诉 FastAPI 把捕获的值作为字符串传给函数。

### 一个最小示例

```python
@example_app.get("/products/{product_id}")
def read_product(product_id: str) -> dict[str, str]:
    return {"product_id": product_id}
```

测试请求：

```python
response = client.get("/products/book")
```

### 示例的输入、执行过程和输出

1. 客户端请求 `GET /products/book`。
2. FastAPI 用 `/products/{product_id}` 匹配这个路径。
3. 动态部分 `book` 被赋给 `product_id`。
4. FastAPI 调用 `read_product(product_id="book")`。
5. 函数返回字典，最终 JSON 为：

```json
{"product_id": "book"}
```

### 它会在今天哪个 TODO 中使用

- TODO 1 会声明一个包含 `{model_name}` 的练习路由。
- TODO 2 会在函数签名中接收同名的 `model_name` Path 参数。
- TODO 3 会把该值放进响应，证明参数确实来自 URL 路径。

### 初学者最容易混淆的地方

1. 路由写 `{product_id}`，请求时写真实值 `book`，不会请求字面量 `{product_id}`。
2. 花括号中的名字与函数参数名不一致时，FastAPI 无法按预期传值。
3. Path 参数不能通过函数默认值省略，因为缺少这一段后 URL 路径就不同了。
4. `product_id: str` 既帮助编辑器理解类型，也告诉 FastAPI 怎样解析输入。

## 4. 概念三：Query 参数

### 它是什么

Query 参数是 URL 中 `?` 后面的键值对：

```text
/products/book?copies=2
```

这里 `copies` 是参数名，`2` 是参数值。FastAPI 会把处理函数中“没有出现在路径模板里”的普通参数识别为 Query 参数。

### 它解决什么问题

Query 参数适合表达查询选项，例如返回数量、排序方式或过滤条件。它通常不决定访问哪个资源，而是调整“怎样查询这个资源”。

默认值可以让 Query 参数变成可选项。例如 `copies: int = 1` 表示客户端不提供 `copies` 时使用 1。

### 最基础的语法或使用方法

```python
@example_app.get("/products/{product_id}")
def read_product(
    product_id: str,
    copies: int = 1,
) -> dict[str, object]:
    return {"product_id": product_id, "copies": copies}
```

FastAPI 看到：

- `product_id` 出现在路径模板中，所以它是 Path 参数。
- `copies` 没有出现在路径模板中，所以它是 Query 参数。
- `copies` 标注为 `int`，所以 FastAPI 会尝试把 URL 文本转换成整数。
- `copies` 有默认值 1，所以请求可以省略它。

### 一个最小示例

带 Query 参数：

```python
response = client.get("/products/book?copies=2")
```

省略 Query 参数：

```python
response = client.get("/products/book")
```

错误类型：

```python
response = client.get("/products/book?copies=many")
```

### 示例的输入、执行过程和输出

对于 `?copies=2`：

1. URL 中的 `"2"` 最初是文本。
2. FastAPI 根据 `copies: int` 尝试转换。
3. 转换成功后，函数实际收到整数 `2`。
4. 响应 JSON 为 `{"product_id": "book", "copies": 2}`。

省略 `copies` 时，函数收到默认整数 `1`。

如果传入 `copies=many`，`many` 不能转换成整数。FastAPI 不会调用处理函数，而会直接返回状态码 `422` 和校验错误 JSON。`422 Unprocessable Content` 在这里表示：请求格式能够被 HTTP 服务理解，但参数内容不符合接口声明的类型要求。

### 它会在今天哪个 TODO 中使用

- TODO 2 会声明带整数类型和默认值的 `limit` Query 参数。
- TODO 3 会返回转换后的 `limit`。
- 测试会覆盖显式传值、使用默认值和错误类型返回 422。

### 初学者最容易混淆的地方

1. Query 参数在 `?` 后面，不使用路径花括号。
2. URL 里的数字最初是文本；函数收到整数是 FastAPI 转换后的结果。
3. `limit: int = 1` 中，`int` 是目标类型，`1` 是省略参数时的默认值。
4. 自动校验失败发生在处理函数调用之前，不需要自己写 `try/except ValueError`。
5. 422 与 404 不同：422 表示路由已经匹配，但参数值不合法；404 表示路径没有匹配。

## 5. 概念之间如何配合

以请求 `GET /products/book?copies=2` 为例：

```text
TestClient 构造请求 URL
        ↓
FastAPI 用 /products/book 匹配 /products/{product_id}
        ↓
从 Path 中得到 product_id="book"
        ↓
从 Query 中得到文本 copies="2"
        ↓
根据 int 类型标注转换为 copies=2
        ↓
调用 read_product(product_id="book", copies=2)
        ↓
函数返回字典，FastAPI 生成 JSON 响应
```

URL 是完整地址结构；Path 参数用于定位具体对象；Query 参数用于携带查询选项。FastAPI 根据路由模板和函数类型标注，把 URL 中的文本拆分、转换并交给 Python 函数。

## 6. 开始 TODO 前应当能够回答的问题

1. 在 `/products/book?copies=2` 中，路径和查询字符串分别是哪一部分？
2. 路由中的 `{product_id}` 与函数参数 `product_id` 为什么必须同名？
3. FastAPI 如何判断一个函数参数是 Path 参数还是 Query 参数？
4. `copies: int = 1` 中，类型标注和默认值各有什么作用？
5. 为什么 `copies=many` 会返回 422，而且处理函数不会执行？

能用自己的话回答这些问题后，再打开 Day 10 的 TODO 文件开始编码。
