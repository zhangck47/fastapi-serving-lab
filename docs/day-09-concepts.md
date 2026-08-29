# Day 09 新概念讲义

## 1. 今天为什么要学习这些概念

`fastapi-serving-lab` 最终要成为一个 OpenAI 兼容模型服务网关。网关的工作可以先用一句话描述：**接收客户端发来的 HTTP 请求，调用后端模型，再把 HTTP 响应返回给客户端。**

阶段 1 已经解决了 Python 内部的数据处理问题。从 Day 9 开始，我们要给这些能力增加一个网络入口。今天先做最小的 `/health` 健康检查接口：调用方通过它判断服务是否能够接收请求。

今天只学习三个概念组：

1. HTTP 请求与响应：理解客户端和服务端交换了什么。
2. GET 方法：理解客户端希望执行哪一类操作。
3. FastAPI 路由与 `TestClient`：把一个 URL 交给 Python 函数处理，并用 pytest 验证它。

今天不学习 POST、请求体、Pydantic 模型、异步或真实网络部署。这些内容都有各自的前置依赖，会在后续日期逐步加入。

## 2. 概念一：HTTP 请求与响应

### 它是什么

HTTP 是客户端和服务端之间交换消息的一套规则，也叫“协议”。协议可以理解成双方共同遵守的格式：客户端按格式发送**请求**，服务端处理后按格式返回**响应**。

- 客户端：主动发起请求的一方，例如浏览器、压测脚本或 OpenAI Python SDK。
- 服务端：接收并处理请求的一方，例如我们将要创建的 FastAPI 应用。
- 请求：客户端想让服务端做什么。
- 响应：服务端处理后的结果。

### 它解决什么问题

如果没有共同协议，客户端不知道应该怎样描述“查询健康状态”，服务端也不知道怎样表达“处理成功”。HTTP 规定了请求方法、路径、状态码、Header 和 Body 等组成部分，使不同语言编写的程序也能通信。

今天先关注这些最小组成：

| 位置 | 示例 | 作用 |
| --- | --- | --- |
| 请求方法 | `GET` | 表示希望执行的操作类型 |
| 请求路径 | `/ping` | 表示要访问哪个功能 |
| 响应状态码 | `200` | 表示请求是否成功 |
| 响应体 | `{"message": "pong"}` | 返回给客户端的数据 |

Header 是附加信息，例如内容类型；Body 是主要数据。今天 FastAPI 会自动生成 JSON 响应所需的 Header，所以暂时不用手写。

### 最基础的语法或使用方法

从概念上看，一次最小 HTTP 交换可以写成：

```text
请求：
GET /ping

响应：
状态码 200
Content-Type: application/json

{"message": "pong"}
```

这不是 Python 代码，而是为了看清消息结构。`GET /ping` 表示“使用 GET 方法访问 `/ping` 路径”。

### 一个最小示例

下面先用普通 Python 数据表示一次响应：

```python
status_code: int = 200
response_body: dict[str, str] = {"message": "pong"}
```

### 示例的输入、执行过程和输出

- 输入：客户端提出“访问 `/ping`”的请求。
- 执行：服务端找到负责 `/ping` 的 Python 函数并调用它。
- 输出：状态码是 `200`，响应体是 `{"message": "pong"}`。

`200` 只表达“成功”，真正的数据放在响应体中。这两部分不能混为一谈。

### 它会在今天哪个 TODO 中使用

- TODO 1 会把请求路径和处理函数建立联系。
- TODO 3 会决定响应体中的 JSON 数据。
- 测试会分别检查状态码和响应体，避免只验证“没有报错”。

### 初学者最容易混淆的地方

1. 请求和响应方向相反：请求从客户端到服务端，响应从服务端回到客户端。
2. 状态码不是业务数据。`200` 表示成功，但不会代替 `{"status": "ok"}`。
3. Python 字典不是网络上的最终格式。FastAPI 会把字典序列化成 JSON 文本再发送。

## 3. 概念二：HTTP GET 方法

### 它是什么

HTTP 方法是请求的一部分，用来表达操作意图。`GET` 通常表示“读取或查询资源”。今天的健康检查只读取服务状态，不创建或修改数据，所以使用 GET。

同一个路径配合不同方法，可以代表不同操作。例如 `GET /items` 可以读取列表，而未来的 `POST /items` 可以创建新项目。方法和路径要一起看，不能只看路径。

### 它解决什么问题

如果所有请求都只有路径，服务端很难区分客户端想读取、创建还是删除。GET 等方法为接口提供统一语义，也让测试、文档和调用者更容易理解行为。

### 最基础的语法或使用方法

在 HTTP 概念中：

```text
GET /ping
```

在 FastAPI 中，GET 会写在路由装饰器中：

```python
@example_app.get("/ping")
```

装饰器是放在函数定义上方、以 `@` 开头的语法。今天只需要知道：它把下面的函数登记为某个请求的处理函数，不学习装饰器内部原理。

### 一个最小示例

```python
@example_app.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "pong"}
```

这里的 `get` 对应 HTTP GET，`"/ping"` 是路径，`ping` 是收到请求后运行的函数。

### 示例的输入、执行过程和输出

- 输入：`GET /ping`。
- 执行：FastAPI 根据“方法 + 路径”找到 `ping()`，然后调用函数。
- 输出：函数返回字典，FastAPI 将其转换成 JSON 响应，默认成功状态码是 `200`。

如果客户端改为发送 `POST /ping`，它与已经登记的 GET 路由不匹配。服务端会返回 `405 Method Not Allowed`，意思是路径可能存在，但该方法不允许。

### 它会在今天哪个 TODO 中使用

- TODO 1 要把健康检查函数登记为正确路径上的 GET 路由。
- 对应测试会发送 GET 请求，并额外确认错误的方法不会被当成 GET 处理。

### 初学者最容易混淆的地方

1. `GET` 不是函数名，它是 HTTP 方法；函数可以使用其他清晰名称。
2. `/ping` 与 `ping` 不同：前者是客户端看到的 URL 路径，后者是 Python 函数名。
3. `404 Not Found` 和 `405 Method Not Allowed` 不同：404 表示没有匹配的路径，405 表示路径存在但请求方法不被允许。

## 4. 概念三：FastAPI 路由与 TestClient

### 它是什么

FastAPI 是一个用于构建 Python Web API 的框架。框架提供已经组织好的请求解析、路由查找、响应转换和文档生成能力，我们只需定义应用对象和处理函数。

路由是一条“HTTP 方法 + URL 路径 → Python 处理函数”的映射。

`TestClient` 是接口测试客户端。它能在 pytest 进程内向 FastAPI 应用发送测试请求，不需要先启动服务器，也不会访问外网。

### 它解决什么问题

- FastAPI 路由解决“收到某种请求后应该调用哪个函数”。
- `TestClient` 解决“如何自动验证整个 HTTP 入口，而不只是直接调用 Python 函数”。

直接调用 `ping()` 只能证明函数返回了字典；通过 `TestClient` 访问 `/ping`，还能验证路由是否登记、GET 是否允许、状态码是否正确，以及字典是否真的被转换成 JSON 响应。

### 最基础的语法或使用方法

创建应用和路由：

```python
from fastapi import FastAPI

example_app = FastAPI()


@example_app.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "pong"}
```

创建测试客户端并发送请求：

```python
from fastapi.testclient import TestClient

client = TestClient(example_app)
response = client.get("/ping")
```

读取响应：

```python
assert response.status_code == 200
assert response.json() == {"message": "pong"}
```

### 一个最小示例

```python
from fastapi import FastAPI
from fastapi.testclient import TestClient

example_app = FastAPI()


@example_app.get("/ping")
def ping() -> dict[str, str]:
    return {"message": "pong"}


client = TestClient(example_app)
response = client.get("/ping")

print(response.status_code)
print(response.json())
```

### 示例的输入、执行过程和输出

1. `TestClient(example_app)` 绑定要测试的 FastAPI 应用。
2. `client.get("/ping")` 构造一条 GET 请求。
3. FastAPI 在路由表中找到 `@example_app.get("/ping")`。
4. FastAPI 调用 `ping()`，得到 Python 字典。
5. FastAPI 将字典转换成 JSON 响应。
6. `response.status_code` 得到 `200`，`response.json()` 把响应 JSON 解码回 Python 字典。

输出为：

```text
200
{'message': 'pong'}
```

### 它会在今天哪个 TODO 中使用

- TODO 1：登记正确的 GET 路由。
- TODO 2：为处理函数写清返回值类型。
- TODO 3：返回健康检查所需的数据。
- pytest 文件已经准备 `TestClient`，会从 HTTP 入口验证结果。

### 初学者最容易混淆的地方

1. `FastAPI` 是类，`FastAPI()` 创建的才是应用对象。
2. 装饰器必须紧贴它要登记的函数，中间不能插入另一个函数定义。
3. `response.json()` 是方法，需要括号；它返回解码后的 Python 对象。
4. `TestClient` 不代表真实服务器已经监听端口。它用于快速、隔离的接口测试。
5. 今天使用普通 `def` 是有意的；`async def` 会在 AsyncIO 阶段系统学习。

## 5. 概念之间如何配合

以示例请求 `GET /ping` 为例：

```text
pytest 调用 client.get("/ping")
        ↓
TestClient 构造 HTTP GET 请求
        ↓
FastAPI 同时匹配 GET 方法和 /ping 路径
        ↓
路由调用 ping() 函数
        ↓
函数返回 {"message": "pong"}
        ↓
FastAPI 生成状态码 200 和 JSON 响应
        ↓
pytest 断言 status_code 与 response.json()
```

三组概念在一次请求中缺一不可：HTTP 定义消息结构，GET 表达读取意图，FastAPI 路由负责把请求交给函数，`TestClient` 则从调用者视角验证完整行为。

## 6. 开始 TODO 前应当能够回答的问题

1. HTTP 请求和 HTTP 响应分别由谁发出、发给谁？
2. `GET /ping` 中，`GET` 和 `/ping` 分别表达什么？
3. 为什么测试接口时要同时检查状态码和 JSON 响应体？
4. `@example_app.get("/ping")` 与下面的 `ping()` 函数是什么关系？
5. `TestClient` 测试与直接调用 `ping()` 相比，多验证了哪些行为？

能用自己的话回答这些问题后，再打开 Day 9 的 TODO 文件开始编码。
