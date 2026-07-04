# Hello-Agents Code Wiki

> 本文档为 [Hello-Agents](https://github.com/datawhalechina/Hello-Agents) 项目的结构化代码 Wiki，系统梳理项目整体架构、模块职责、关键类与函数、依赖关系及运行方式，便于学习者与贡献者快速理解全貌。

---

## 一、项目概述

### 1.1 项目定位

Hello-Agents 是 Datawhale 社区推出的**系统性智能体学习教程**，聚焦于 AI Native Agent（AI 原生智能体）的构建。教程从智能体核心原理出发，覆盖经典范式、低代码平台、主流框架、自研框架、记忆与检索、上下文工程、通信协议、Agentic-RL、性能评估及综合案例等主题。

- **目标读者**：具备 Python 基础、对 LLM 有概念性了解的开发者、学生与自学者
- **核心特色**：理论 + 实战并重；最终引导学习者从「使用者」蜕变为「构建者」
- **自研框架**：[HelloAgents](https://github.com/jjyaoao/helloagents)（基于 OpenAI 原生 API 自研）

### 1.2 五大部分结构

| 部分 | 章节 | 主题 |
| ---- | ---- | ---- |
| 第一部分 | 第 1 ~ 3 章 | 智能体与语言模型基础 |
| 第二部分 | 第 4 ~ 7 章 | 构建大语言模型智能体（范式 / 低代码 / 框架 / 自研） |
| 第三部分 | 第 8 ~ 12 章 | 高级知识扩展（记忆 / 上下文 / 协议 / RL / 评估） |
| 第四部分 | 第 13 ~ 15 章 | 综合案例（旅行助手 / DeepResearch / 赛博小镇） |
| 第五部分 | 第 16 章 | 毕业设计与未来展望 |

---

## 二、项目整体架构

### 2.1 顶层目录结构

```
hello-agents/
├── docs/                       # 教程正文章档（Markdown）
├── code/                       # 各章节配套代码
│   ├── chapter1/ ~ chapter16/  # 16 章示例代码
├── Co-creation-projects/       # 社区共创毕业项目（30+）
├── Extra-Chapter/              # 社区扩展文章（13 篇）
├── Additional-Chapter/         # 补充安装指南（N8N / NodeJS）
├── README.md                   # 项目主页（中文）
├── README_EN.md                # 项目主页（英文）
├── LICENSE.txt                 # CC BY-NC-SA 4.0
└── .gitignore
```

### 2.2 核心架构图

```
┌──────────────────────────────────────────────────────────┐
│                       学习者入口                          │
│              在线阅读 / PDF / 本地克隆                    │
└────────────────────────┬─────────────────────────────────┘
                         │
        ┌────────────────┼────────────────────┐
        ▼                ▼                    ▼
   ┌─────────┐     ┌──────────┐         ┌──────────────┐
   │ docs/   │     │  code/   │         │Extra-Chapter │
   │ 教程正文 │     │ 配套代码 │         │ 社区扩展文章 │
   └─────────┘     └─────┬────┘         └──────────────┘
                         │
            ┌────────────┼─────────────────────┐
            ▼            ▼                     ▼
      ┌──────────┐  ┌──────────┐         ┌───────────────┐
      │ 理论基础  │  │ 实战框架  │         │  综合案例     │
      │ ch1~ch3  │  │ ch4~ch7  │         │  ch13~ch15    │
      └──────────┘  └─────┬────┘         └───────────────┘
                          │
                    ┌─────┴─────┐
                    ▼           ▼
              ┌───────────┐  ┌─────────────────┐
              │HelloAgents│  │ 第三方框架       │
              │ 自研框架   │  │AutoGen/LangGraph │
              └─────┬─────┘  │ /AgentScope/CAMEL│
                    │        └─────────────────┘
                    ▼
         ┌──────────────────────────┐
         │  HelloAgents PyPI 包     │
         │  (SimpleAgent / ReAct /  │
         │   ToolAware / Memory /   │
         │   MCPTool / A2ATool /    │
         │   ANPTool / RLTraining) │
         └──────────────────────────┘
```

### 2.3 自研框架 HelloAgents 在项目中的角色

- **依赖关系**：项目各章节代码以 `pip install hello-agents` 的方式复用统一框架
- **版本要求**：`hello-agents>=0.2.4,<=0.2.9`（部分章节使用 `hello-agents[protocols]`、`hello-agents[evaluation]`）
- **核心能力**：
  - LLM 客户端 `HelloAgentsLLM`（兼容任意 OpenAI 协议接口）
  - Agent 基类 `SimpleAgent`、`ReActAgent`、`ToolAwareSimpleAgent`
  - 工具体系：`ToolRegistry`、`MCPTool`、`A2ATool`、`ANPTool`、`MemoryTool`、`NoteTool`、`RLTrainingTool`
  - 上下文工程：`ContextBuilder`、`ContextPacket`
  - 评估：BFCL / GAIA 一键评估工具

---

## 三、各章节模块职责

### 3.1 第一部分：基础理论（chapter1 ~ chapter3）

#### chapter1 初识智能体
- 文件：[FirstAgentTest.py](code/chapter1/FirstAgentTest.py)、[FirstAgentTest.ipynb](code/chapter1/FirstAgentTest.ipynb)
- 职责：演示最小可运行的 Thought-Action 循环智能体
- 关键组件：
  - `OpenAICompatibleClient`：兼容 OpenAI 协议的最简 LLM 客户端
  - `get_weather(city)`：调用 `wttr.in` 真实天气 API
  - `get_attraction(city, weather)`：基于 Tavily Search 的景点搜索工具
  - 主循环：通过正则解析 `Thought:` / `Action:` / `Finish[...]`，最多迭代 5 步

#### chapter2 智能体发展史
- 文件：[ELIZA.py](code/chapter2/ELIZA.py)
- 职责：复现 1966 年 ELIZA 规则匹配对话系统
- 关键函数：
  - `swap_pronouns(phrase)`：第一/第二人称代词转换
  - `respond(user_input)`：基于正则规则库匹配响应模板

#### chapter3 大语言模型基础
- 文件：[BPE.py](code/chapter3/BPE.py)、[N_gram.py](code/chapter3/N_gram.py)、[Transformer.py](code/chapter3/Transformer.py)、[Word_Embedding.py](code/chapter3/Word_Embedding.py)、[Qwen.py](code/chapter3/Qwen.py)
- 职责：从底层实现 LLM 核心组件
- 关键类：
  - `MultiHeadAttention`（Transformer.py）：多头注意力机制，含 `scaled_dot_product_attention`、`split_heads`
  - BPE / N-gram / Word Embedding：分词与表示算法实现

### 3.2 第二部分：构建智能体（chapter4 ~ chapter7）

#### chapter4 智能体经典范式构建
- 文件：[ReAct.py](code/chapter4/ReAct.py)、[Plan_and_solve.py](code/chapter4/Plan_and_solve.py)、[Reflection.py](code/chapter4/Reflection.py)、[llm_client.py](code/chapter4/llm_client.py)、[tools.py](code/chapter4/tools.py)
- 职责：手写实现三大经典范式
- 关键类与函数：

| 文件 | 类 / 函数 | 职责 |
| ---- | ---- | ---- |
| llm_client.py | `HelloAgentsLLM` | 自定义 LLM 客户端，流式响应，从 `.env` 读取 `LLM_MODEL_ID`、`LLM_API_KEY`、`LLM_BASE_URL` |
| tools.py | `search(query)` | 基于 SerpApi 的 Google 搜索工具，智能解析 answer_box / knowledge_graph / organic_results |
| tools.py | `ToolExecutor` | 工具注册与执行管理器，方法 `registerTool`、`getTool`、`getAvailableTools` |
| ReAct.py | `ReActAgent` | Reasoning + Acting 范式，`run(question)` 主循环，`_parse_output` / `_parse_action` 正则解析 |
| Plan_and_solve.py | `Planner` / `Executor` / `PlanAndSolveAgent` | 先规划后执行，通过 `ast.literal_eval` 解析 Python 列表格式的计划 |
| Reflection.py | `Memory` / `ReflectionAgent` | 自我反思迭代优化，含 `add_record`、`get_trajectory`、`get_last_execution`；max_iterations 控制迭代轮数 |

#### chapter5 低代码平台
- 文件：[HelloAgent_cozeCase.zip](code/chapter5/HelloAgent_cozeCase.zip)、[HelloAgent_difyCase.yml](code/chapter5/HelloAgent_difyCase.yml)、[HelloAgent_fastgptCase.json](code/chapter5/HelloAgent_fastgptCase.json)、[HelloAgent_n8nCase.json](code/chapter5/HelloAgent_n8nCase.json)
- 职责：Coze / Dify / FastGPT / n8n 四大低代码平台的案例导入文件
- 安装指南：见 [Additional-Chapter/NODEJS_INSTALL_GUIDE.md](Additional-Chapter/NODEJS_INSTALL_GUIDE.md)、[N8N_INSTALL_GUIDE.md](Additional-Chapter/N8N_INSTALL_GUIDE.md)

#### chapter6 框架开发实践
- 目录：[AgentScopeDemo/](code/chapter6/AgentScopeDemo/)、[AutoGenDemo/](code/chapter6/AutoGenDemo/)、[CAMEL/](code/chapter6/CAMEL/)、[Langgraph/](code/chapter6/Langgraph/)
- 职责：对比主流 Agent 框架
- 子项目示例：
  - AgentScope：`game_roles.py` + `main_cn.py` 角色扮演游戏
  - AutoGen：`autogen_software_team.py` 软件团队多智能体
  - CAMEL：`DigitalBookWriting.py` 数字化写作
  - Langgraph：`Dialogue_System.py` 对话系统

#### chapter7 构建自己的 Agent 框架
- 文件：[my_llm.py](code/chapter7/my_llm.py)、[my_simple_agent.py](code/chapter7/my_simple_agent.py)、[my_react_agent.py](code/chapter7/my_react_agent.py)、[my_calculator_tool.py](code/chapter7/my_calculator_tool.py)、[my_advanced_search.py](code/chapter7/my_advanced_search.py)、[my_main.py](code/chapter7/my_main.py)
- 职责：基于 HelloAgents 框架继承扩展自定义组件
- 关键类：

| 文件 | 类 | 职责 |
| ---- | ---- | ---- |
| my_llm.py | `MyLLM(HelloAgentsLLM)` | 重写 `__init__`，新增 `provider="modelscope"` 分支，自动适配 ModelScope 推理服务 |
| my_simple_agent.py | `MySimpleAgent(SimpleAgent)` | 重写 `run()`，支持 `[TOOL_CALL:tool:params]` 文本协议工具调用；提供 `stream_run`、`add_tool`、`_parse_tool_calls`、`_execute_tool_call`、`_parse_tool_parameters` 等方法 |
| my_react_agent.py | `MyReActAgent(ReActAgent)` | 自定义 ReAct 提示模板，重写循环逻辑 |

### 3.3 第三部分：高级知识扩展（chapter8 ~ chapter12）

#### chapter8 记忆与检索
- 文件：11 个示例（[01_MemoryTool_Basic_Operations.py](code/chapter8/01_MemoryTool_Basic_Operations.py) ~ [11_Q&A_Assistant.py](code/chapter8/11_Q&A_Assistant.py)）
- 职责：演示 `MemoryTool`、`RAGTool` 的完整使用流程
- 核心能力：
  - 4 类记忆：working / episodic / semantic / perceptual
  - 操作：`add` / `search` / `summary` / `stats` / `update` / `remove` / `forget` / `consolidate` / `clear_all`
  - RAG：基于 MarkItDown 的文档解析管道 + 高级检索

#### chapter9 上下文工程
- 文件：[01_context_builder_basic.py](code/chapter9/01_context_builder_basic.py) ~ [06_three_day_workflow.py](code/chapter9/06_three_day_workflow.py)、[codebase_maintainer.py](code/chapter9/codebase_maintainer.py)
- 职责：演示长程智能体的上下文管理
- 关键组件：
  - `ContextBuilder` / `ContextPacket`：上下文包构建与 token 限制管理
  - `NoteTool`：结构化笔记 CRUD，支持标签与导出
  - `TerminalTool`：白名单命令的终端文件访问（ls / cat / grep / find 等）
  - `codebase_maintainer.py`：完整代码库维护助手（集成三大工具 + working 记忆）
- 嵌入模型配置：TF-IDF（默认） / 本地 Transformer（sentence-transformers） / DashScope

#### chapter10 智能体通信协议
- 文件：[01_TestConnect.py](code/chapter10/01_TestConnect.py) ~ [14_weather_agent.py](code/chapter10/14_weather_agent.py)（共 20+ 示例）+ [weather-mcp-server/](code/chapter10/weather-mcp-server/)
- 职责：解析并实践 MCP / A2A / ANP 三大协议
- 关键演示：
  - `01_TestConnect.py`：MCPTool / A2ATool / ANPTool 三工具对比
  - `02_Connect2MCP.py` ~ `05_UseMCPToolInAgent.py`：MCP 工具接入流程
  - `07_SimpleA2AAgent.py` ~ `10_A2ATool_Simple.py`：A2A 协议通信
  - `11_ANPInit.py` ~ `13_ANPLoadBalancing.py`：ANP 服务发现与负载均衡
  - `weather-mcp-server/`：完整 MCP Server 实现（含 Dockerfile、pyproject.toml、smithery.yaml）

#### chapter11 Agentic-RL
- 文件：[00_quick_test.py](code/chapter11/00_quick_test.py) ~ [08_distributed_training.py](code/chapter11/08_distributed_training.py)、[config.json](code/chapter11/config.json)、[accelerate_configs/](code/chapter11/accelerate_configs/)
- 职责：从 SFT 到 GRPO 的完整 LLM 训练流水线
- 关键工具：`hello_agents.tools.RLTrainingTool`
- 配置示例（config.json）：
  - 基础模型：`Qwen/Qwen3-0.6B`
  - SFT / GRPO 参数（epochs、batch_size、output_dir）
  - 监控：TensorBoard / Weights & Biases
- 分布式配置：DeepSpeed Zero2 / Zero3 / 多 GPU DDP

#### chapter12 智能体性能评估
- 文件：[01_basic_agent_example.py](code/chapter12/01_basic_agent_example.py) ~ [09_data_generation_win_rate.py](code/chapter12/09_data_generation_win_rate.py)、[data_generation/](code/chapter12/data_generation/)
- 职责：BFCL / GAIA 基准测试 + 数据生成评估
- 三大评估方法：
  - **BFCL**（Berkeley Function Calling Leaderboard）：函数调用准确性
  - **GAIA**：通用 AI 助手基准（需 HuggingFace 申请权限）
  - **数据生成评估**：LLM Judge + Win Rate + 人工验证
- 安装：`pip install hello-agents[evaluation]==0.2.3`

### 3.4 第四部分：综合案例（chapter13 ~ chapter15）

#### chapter13 智能旅行助手
- 目录：[helloagents-trip-planner/](code/chapter13/helloagents-trip-planner/)
- 架构：全栈应用（FastAPI 后端 + Vue3 前端）
- 后端关键模块（`backend/app/`）：

| 子目录 / 文件 | 模块 | 职责 |
| ---- | ---- | ---- |
| agents/trip_planner_agent.py | `MultiAgentTripPlanner` | 4 Agent 协作（景点搜索 / 天气 / 酒店 / 行程规划），共享 `MCPTool`（amap-mcp-server） |
| api/main.py | FastAPI 入口 | CORS、路由注册、启动校验、`/docs` Swagger |
| api/routes/ | trip.py / poi.py / map.py | 三组 REST 端点 |
| services/ | amap_service.py / llm_service.py / unsplash_service.py | 高德地图 / LLM / Unsplash 图片服务封装 |
| models/schemas.py | Pydantic 模型 | TripRequest / TripPlan / DayPlan / Attraction / Meal / WeatherInfo / Hotel |
| config.py | `Settings(BaseSettings)` | pydantic-settings 配置管理，含 `validate_config`、`print_config` |

- 前端技术栈：Vue 3 + TypeScript + Vite + Ant Design Vue + 高德地图 JS API
- 运行：后端 `uvicorn app.api.main:app --reload --port 8000`；前端 `npm run dev`（端口 5173）

#### chapter14 自动化深度研究智能体
- 目录：[helloagents-deepresearch/](code/chapter14/helloagents-deepresearch/)
- 架构：FastAPI + Vue3，基于 TODO 列表的研究编排
- 后端关键类（`backend/src/`）：

| 文件 | 类 / 模块 | 职责 |
| ---- | ---- | ---- |
| agent.py | `DeepResearchAgent` | 编排器，集成 `ToolAwareSimpleAgent`，协调规划 / 总结 / 报告三类 Agent |
| services/planner.py | `PlanningService` | 任务规划 |
| services/summarizer.py | `SummarizationService` | 任务总结 |
| services/reporter.py | `ReportingService` | 报告撰写 |
| services/search.py | `dispatch_search` / `prepare_research_context` | 搜索调度 |
| services/notes.py | 笔记服务 | 配合 `NoteTool` 持久化研究笔记 |
| services/tool_events.py | `ToolCallTracker` | 工具调用追踪 |
| prompts.py | 提示词模板 | `todo_planner_system_prompt` / `report_writer_instructions` / `task_summarizer_instructions` |

- 安装方式：使用 `uv`（见 `pyproject.toml` + `uv.lock`）

#### chapter15 赛博小镇（AI Town）
- 目录：[Helloagents-AI-Town/](code/chapter15/Helloagents-AI-Town/)
- 架构：Godot 4.x 游戏引擎（前端）+ FastAPI Python 后端
- 后端关键文件（`backend/`）：

| 文件 | 职责 |
| ---- | ---- |
| agents.py | `NPCAgentManager`：管理张三 / 李四 / 王五 3 个 NPC Agent；集成 `MemoryManager`、`RelationshipManager` |
| relationship_manager.py | 好感度系统（5 等级） |
| state_manager.py | NPC 状态机（闲逛 / 工作） |
| models.py | Pydantic 数据模型 |
| batch_generator.py | 批量对话生成 |
| logger.py | 结构化日志（`log_dialogue_start` / `log_affinity` / `log_memory_retrieval` 等） |
| view_logs.py | 日志查看工具 |

- 前端关键脚本（GDScript，`helloagents-ai-town/scripts/`）：
  - `api_client.gd`：HTTP 客户端，与后端通信
  - `main.gd` / `player.gd` / `npc.gd` / `dialogue_ui.gd`：游戏主循环 / 玩家 / NPC / 对话 UI
- 文档：[MEMORY_SYSTEM_GUIDE.md](code/chapter15/Helloagents-AI-Town/MEMORY_SYSTEM_GUIDE.md)、[AFFINITY_SYSTEM_GUIDE.md](code/chapter15/Helloagents-AI-Town/AFFINITY_SYSTEM_GUIDE.md)、[DIALOGUE_LOG_GUIDE.md](code/chapter15/Helloagents-AI-Town/DIALOGUE_LOG_GUIDE.md)、[SETUP_GUIDE.md](code/chapter15/Helloagents-AI-Town/SETUP_GUIDE.md)

### 3.5 第五部分：毕业设计（chapter16）

- 文件：[共创路径.md](code/chapter16/共创路径.md)
- 职责：引导学习者完成完整多智能体应用，参考 [Co-creation-projects/](Co-creation-projects/)

---

## 四、关键类与函数索引

### 4.1 HelloAgents 框架核心 API

```python
from hello_agents import (
    HelloAgentsLLM,            # 兼容 OpenAI 协议的 LLM 客户端
    SimpleAgent,                # 简单对话 Agent 基类
    ReActAgent,                 # ReAct 范式 Agent
    ToolAwareSimpleAgent,       # 支持工具调用的 Agent
    Config,                     # 配置类
    Message,                    # 消息封装
    ToolRegistry,               # 工具注册表
)

from hello_agents.tools import (
    MCPTool,                    # Model Context Protocol 工具
    A2ATool,                    # Agent-to-Agent 通信
    ANPTool,                    # Agent Network Protocol
    MemoryTool,                 # 记忆系统（4 类记忆）
    NoteTool,                   # 结构化笔记
    RLTrainingTool,             # RL 训练流水线
    # 评估工具
    BFCLTool,                   # BFCL 评估
    GAIAAtomTool,                # GAIA 评估
)

from hello_agents.memory import (
    MemoryManager, MemoryConfig, MemoryItem,
)
```

### 4.2 通用 LLM 客户端（chapter4）

```python
# llm_client.py
class HelloAgentsLLM:
    def __init__(self, model=None, apiKey=None, baseUrl=None, timeout=None):
        # 优先参数 → 环境变量 LLM_MODEL_ID / LLM_API_KEY / LLM_BASE_URL
        ...
    def think(self, messages, temperature=0) -> str:
        # 流式调用，返回完整文本
        ...
```

### 4.3 ReAct 范式核心（chapter4）

```python
class ReActAgent:
    def __init__(self, llm_client, tool_executor, max_steps=5): ...
    def run(self, question: str): ...
    def _parse_output(self, text): ...      # Thought / Action 解析
    def _parse_action(self, action_text): ...  # tool_name[input]
    def _parse_action_input(self, action_text): ...  # Finish[answer]
```

### 4.4 工具执行器（chapter4）

```python
class ToolExecutor:
    def registerTool(self, name, description, func): ...
    def getTool(self, name) -> callable: ...
    def getAvailableTools(self) -> str: ...  # 格式化工具描述
```

### 4.5 Plan-and-Solve 范式（chapter4）

```python
class Planner:
    def plan(self, question) -> list[str]: ...  # 输出 Python 列表
class Executor:
    def execute(self, question, plan) -> str: ...  # 逐步执行
class PlanAndSolveAgent:
    def __init__(self, llm_client): ...
    def run(self, question): ...  # plan → execute
```

### 4.6 Reflection 范式（chapter4）

```python
class Memory:
    def add_record(self, record_type, content): ...  # execution / reflection
    def get_trajectory(self) -> str: ...
    def get_last_execution(self) -> str: ...

class ReflectionAgent:
    def __init__(self, llm_client, max_iterations=3): ...
    def run(self, task): ...  # 初始执行 → 反思 → 优化（max_iterations 轮）
```

### 4.7 多智能体旅行规划（chapter13）

```python
class MultiAgentTripPlanner:
    def __init__(self): ...  # 创建 4 个 SimpleAgent + 共享 MCPTool
    def plan_trip(self, request: TripRequest) -> TripPlan: ...
    def _build_attraction_query(self, request) -> str: ...
    def _build_planner_query(self, request, attractions, weather, hotels) -> str: ...
    def _parse_response(self, response, request) -> TripPlan: ...  # JSON 提取
    def _create_fallback_plan(self, request) -> TripPlan: ...  # 失败兜底
```

### 4.8 DeepResearch 编排器（chapter14）

```python
class DeepResearchAgent:
    def __init__(self, config=None):
        # 创建 todo_agent / report_agent / summarizer_factory
        # 集成 NoteTool + ToolRegistry + ToolCallTracker
        ...
```

---

## 五、依赖关系

### 5.1 Python 依赖（核心）

| 包 | 用途 | 涉及章节 |
| ---- | ---- | ---- |
| `hello-agents` | 自研 Agent 框架 | ch7 ~ ch15 |
| `hello-agents[protocols]` | 含 MCP / A2A / ANP 协议支持 | ch10、ch13 |
| `hello-agents[evaluation]` | 含 BFCL / GAIA 评估 | ch12 |
| `openai` | OpenAI 协议 SDK | ch1、ch4、ch7 |
| `python-dotenv` | 环境变量管理 | 全章节 |
| `fastapi` + `uvicorn` | Web 框架 | ch13、ch14、ch15 |
| `pydantic` + `pydantic-settings` | 数据校验与配置 | ch13、ch14 |
| `httpx` / `aiohttp` / `requests` | HTTP 客户端 | 全章节 |
| `serpapi` | Google 搜索工具 | ch4 |
| `tavily-python` | Tavily Search API | ch1 |
| `torch` | LLM 底层实现 | ch3、ch11 |
| `transformers` + `trl` + `peft` | SFT / GRPO 训练 | ch11 |
| `accelerate` | 分布式训练 | ch11 |
| `sentence-transformers` | 本地嵌入模型 | ch9 |
| `qdrant-client` | 向量数据库（可选） | ch8、ch9 |
| `fastmcp` | MCP Server 框架 | ch10、ch13 |

### 5.2 前端依赖（综合案例）

| 包 | 用途 | 涉及章节 |
| ---- | ---- | ---- |
| `vue@3` + `typescript` | 前端框架 | ch13、ch14 |
| `vite` | 构建工具 | ch13、ch14 |
| `ant-design-vue` | UI 组件库 | ch13 |
| `axios` | HTTP 客户端 | ch13、ch14 |
| Godot 4.x | 游戏引擎（GDScript） | ch15 |

### 5.3 章节依赖关系图

```
ch1 (基础) ──┐
              ├─→ ch4 (范式) ──→ ch7 (自研框架) ──┐
ch2 (历史) ──┤                                  │
              ├─→ ch5 (低代码)                   ├─→ ch8 (记忆) ──→ ch13 (旅行)
ch3 (LLM) ──┘                                   │   ch9 (上下文) ──→ ch14 (DeepResearch)
                                                │   ch10 (协议) ──→ ch15 (AI Town)
                                                ↓
                                         ch11 (RL) ────→ ch16 (毕业)
                                         ch12 (评估) ──┘
```

### 5.4 外部服务依赖

- **LLM 服务**：OpenAI / DeepSeek / ModelScope / 任意 OpenAI 兼容接口
- **搜索服务**：SerpApi、Tavily
- **地图服务**：高德地图 Web API + amap-mcp-server（chapter13）
- **图片服务**：Unsplash API（chapter13）
- **模型托管**：HuggingFace（chapter11、chapter12 GAIA）
- **向量数据库**：Qdrant（chapter8、chapter9 可选）

---

## 六、项目运行方式

### 6.1 环境准备

```bash
# 1. 克隆仓库
git clone https://github.com/datawhalechina/Hello-Agents.git
cd Hello-Agents

# 2. 创建虚拟环境
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate

# 3. 安装自研框架（多数章节依赖）
pip install hello-agents                    # 基础
pip install hello-agents[protocols]        # 第 10、13 章
pip install hello-agents[evaluation]       # 第 12 章
```

### 6.2 环境变量配置

每个章节目录下均有 `.env.example`，复制为 `.env` 后填入真实凭证：

```bash
# 通用 LLM 配置（chapter4 .env copy 示例）
LLM_MODEL_ID="your-model-name"
LLM_API_KEY="your-api-key"
LLM_BASE_URL="https://api.openai.com/v1"
LLM_TIMEOUT=60

# 搜索工具（按需）
SERPAPI_API_KEY="your-serpapi-key"
TAVILY_API_KEY="your-tavily-key"

# 高德地图（chapter13）
AMAP_MAPS_API_KEY="your-amap-key"

# 训练相关（chapter11、chapter12）
HF_TOKEN="your-huggingface-token"
OPENAI_API_KEY="your-openai-key"
```

### 6.3 各章节运行示例

#### chapter1 ~ chapter4：单文件脚本
```bash
cd code/chapter4
python ReAct.py
python Plan_and_solve.py
python Reflection.py
```

#### chapter7：自研框架扩展
```bash
cd code/chapter7
python my_main.py
```

#### chapter11：RL 训练（先配置 config.json）
```bash
cd code/chapter11
python 00_quick_test.py           # 快速测试
python 06_complete_pipeline.py    # 完整 SFT + GRPO 流水线
```

#### chapter12：评估
```bash
cd code/chapter12
python 02_bfcl_quick_start.py    # BFCL 一键评估
python 05_gaia_quick_start.py     # GAIA 一键评估
python 07_data_generation_complete_flow.py 30 3.0  # 数据生成评估
```

#### chapter13：旅行助手（全栈）
```bash
# 后端
cd code/chapter13/helloagents-trip-planner/backend
pip install -r requirements.txt
cp .env.example .env
uvicorn app.api.main:app --reload --host 0.0.0.0 --port 8000

# 前端（另开终端）
cd ../frontend
npm install
cp .env.example .env
npm run dev   # http://localhost:5173
```

#### chapter14：DeepResearch（全栈，使用 uv）
```bash
cd code/chapter14/helloagents-deepresearch/backend
uv sync
uv run uvicorn src.main:app --reload --port 8000

cd ../frontend
npm install
npm run dev
```

#### chapter15：赛博小镇（Godot + FastAPI）
```bash
# 后端
cd code/chapter15/Helloagents-AI-Town/backend
pip install -r requirements.txt
cp .env.example .env
python main.py   # 或 uvicorn main:app --reload

# 前端：使用 Godot 4.x 编辑器打开 helloagents-ai-town/project.godot 运行
```

### 6.4 运行 FirstAgentTest.py（chapter1）说明

[FirstAgentTest.py](code/chapter1/FirstAgentTest.py) 的运行需要：
1. 安装依赖：`pip install tavily-python openai`
2. 编辑文件第 145-148 行，填入真实凭证：
   ```python
   API_KEY = "your-actual-api-key"
   BASE_URL = "your-actual-base-url"
   MODEL_ID = "your-actual-model-id"
   os.environ['TAVILY_API_KEY'] = "your-actual-tavily-key"
   ```
3. 运行：`python FirstAgentTest.py`

> 若未配置真实凭证，程序仍可正常启动并执行循环逻辑，但每次 LLM 调用会返回 `Connection error.`，最终因无法解析 `Action:` 字段而循环 5 次后退出。

---

## 七、社区共创与扩展

### 7.1 Co-creation-projects（30+ 共创项目）

目录：[Co-creation-projects/](Co-creation-projects/)

命名规范：`{GitHub用户名}-{项目名称}`，每个项目至少包含 `README.md`、`requirements.txt`、`main.ipynb`。代表项目：

| 项目 | 主题 |
| ---- | ---- |
| [Apricity-InnocoreAI](Co-creation-projects/Apricity-InnocoreAI/) | 论文分析多智能体系统（含 agents/api/core/models/utils 完整结构） |
| [939147533-DatabaseAgent](Co-creation-projects/939147533-DatabaseAgent/) | 数据库 Agent |
| [CC1227871-StockInsightAgent](Co-creation-projects/CC1227871-StockInsightAgent/) | 股票分析 Agent（含 RAG） |
| [tino-chen-HelloClaw](Co-creation-projects/tino-chen-HelloClaw/) | CLI + API 双入口 Agent |
| [melxy1997-ColumnWriter](Co-creation-projects/melxy1997-ColumnWriter/) | 专栏写作 Agent（含 orchestrator + exporter） |
| [lcyting-StockSage-agent](Co-creation-projects/lcyting-StockSage-agent/) | 股票 Agent（含 Docker 部署 + run_exe.py 打包） |
| [pamdla-MindEchoAgent](Co-creation-projects/pamdla-MindEchoAgent/) | 心理 Agent（含 Dockerfile） |

### 7.2 Extra-Chapter（13 篇社区扩展文章）

目录：[Extra-Chapter/](Extra-Chapter/)

| 编号 | 主题 |
| ---- | ---- |
| Extra01 | Agent 面试题总结 + 参考答案 |
| Extra02 | 上下文工程内容补充 |
| Extra03 | Dify 智能体创建保姆级教程 |
| Extra04 | Datawhale 课程常见问题 |
| Extra05 | Agent Skills 与 MCP 对比解读 |
| Extra06 | GUI Agent 科普与实战 |
| Extra07 | 环境配置指南 |
| Extra08 | 如何写出好的 Skill |
| Extra09 | Agent 应用开发踩坑与经验 |
| Extra10 | Agent 自进化（四类闭环） |
| Extra11 | WebAgent 科普与实战 |
| Extra12 | 旅行助手后训练实战 |
| Extra13 | Hello-Agents 视频课录制共创 |

### 7.3 Additional-Chapter

- [NODEJS_INSTALL_GUIDE.md](Additional-Chapter/NODEJS_INSTALL_GUIDE.md)：Node.js 安装指南
- [N8N_INSTALL_GUIDE.md](Additional-Chapter/N8N_INSTALL_GUIDE.md)：n8n 安装指南

---

## 八、配置与工程化约定

### 8.1 .env 配置约定

项目所有章节均使用 `python-dotenv` 加载 `.env`，常见环境变量：

| 变量名 | 用途 | 章节 |
| ---- | ---- | ---- |
| `LLM_MODEL_ID` | 默认模型 ID | ch4、ch7、ch13 |
| `LLM_API_KEY` | LLM 服务密钥 | 全章节 |
| `LLM_BASE_URL` | LLM 服务地址 | 全章节 |
| `LLM_TIMEOUT` | 超时秒数（默认 60） | ch4 |
| `SERPAPI_API_KEY` | SerpApi 密钥 | ch4 |
| `TAVILY_API_KEY` | Tavily 密钥 | ch1 |
| `AMAP_MAPS_API_KEY` | 高德地图密钥 | ch13 |
| `OPENAI_API_KEY` | OpenAI 密钥（评估用） | ch12 |
| `HF_TOKEN` | HuggingFace Token | ch11、ch12 |
| `EMBED_MODEL_TYPE` | 嵌入模型类型（tfidf/local/dashscope） | ch9 |
| `EMBED_MODEL_NAME` | 嵌入模型名 | ch9 |
| `MODELSCOPE_API_KEY` | ModelScope 密钥 | ch7 |

### 8.2 代码风格约定

- Python 3.10+
- 类型注解：`typing` 模块（List / Dict / Optional / Iterator）
- 数据模型：`pydantic` / `pydantic-settings`
- 异步支持：`async / await`（FastAPI 路由）
- 错误处理：try-except 捕获 + 中文友好提示
- 注释风格：模块级 docstring + 函数级中文注释

### 8.3 项目结构规范（共创项目要求）

```
项目名称/
├── README.md              # 必需
├── requirements.txt       # 必需
├── main.ipynb            # 必需
├── .env.example          # 推荐
├── .gitignore            # 推荐
└── src/                  # 可选（复杂项目）
```

---

## 九、版本与许可

- **HelloAgents 框架版本**：0.2.4 ~ 0.2.9（不同章节有细微差异）
- **评估扩展版本**：`hello-agents[evaluation]==0.2.3`
- **开源协议**：[CC BY-NC-SA 4.0](http://creativecommons.org/licenses/by-nc-sa/4.0/)（知识共享 署名-非商业性使用-相同方式共享 4.0 国际）
- **引用方式**：见 [README.md](README.md) 末尾 BibTeX

---

## 十、学习路径建议

### 10.1 初学者路径（按章节顺序）

1. **理论入门**：阅读 docs/chapter1 ~ chapter3 → 运行 chapter1 FirstAgentTest.py
2. **范式实战**：chapter4 ReAct / Plan-and-Solve / Reflection 三大范式逐个跑通
3. **框架上手**：chapter6 对比主流框架 → chapter7 基于 HelloAgents 扩展
4. **进阶能力**：chapter8 记忆 → chapter9 上下文 → chapter10 协议
5. **训练评估**：chapter11 RL 训练 → chapter12 性能评估
6. **综合案例**：任选 chapter13 / chapter14 / chapter15 之一完整复现

### 10.2 实战派路径（直接上手综合案例）

1. 安装 `hello-agents` 框架
2. 直接运行 chapter13 旅行助手（最完整的全栈示例）
3. 遇到不理解的组件回查对应章节

### 10.3 研究派路径（聚焦训练与评估）

1. 直接进入 chapter11（Agentic-RL）
2. 配合 chapter12（性能评估）量化模型效果
3. 参考 Extra12（旅行助手后训练实战）

---

## 附录：核心文件快速导航

| 主题 | 关键文件 |
| ---- | ---- |
| 最小 Agent | [code/chapter1/FirstAgentTest.py](code/chapter1/FirstAgentTest.py) |
| LLM 客户端 | [code/chapter4/llm_client.py](code/chapter4/llm_client.py) |
| ReAct 范式 | [code/chapter4/ReAct.py](code/chapter4/ReAct.py) |
| 工具执行器 | [code/chapter4/tools.py](code/chapter4/tools.py) |
| 自研框架扩展 | [code/chapter7/my_simple_agent.py](code/chapter7/my_simple_agent.py) |
| 多智能体编排 | [code/chapter13/helloagents-trip-planner/backend/app/agents/trip_planner_agent.py](code/chapter13/helloagents-trip-planner/backend/app/agents/trip_planner_agent.py) |
| DeepResearch | [code/chapter14/helloagents-deepresearch/backend/src/agent.py](code/chapter14/helloagents-deepresearch/backend/src/agent.py) |
| AI Town 后端 | [code/chapter15/Helloagents-AI-Town/backend/agents.py](code/chapter15/Helloagents-AI-Town/backend/agents.py) |
| 项目主页 | [README.md](README.md) |

---

*本文档由 Code Wiki 自动生成工具基于仓库实际代码梳理而成，最后更新日期：2026-07-04。*
