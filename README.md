# 城市分级查询 MCP Server

## 服务介绍

基于2025新一线城市魅力排行榜的城市分级查询服务，使用 FastMCP 和 SSE 协议。该服务提供了完整的城市分级查询功能，支持按城市名称查询分级、列出指定分级的所有城市、获取统计信息以及关键词搜索等功能。

## 服务描述

这是一个专业的城市分级查询MCP服务，基于最新的2025年城市魅力排行榜数据。服务提供了四个主要功能：根据城市名称查询其所属级别、列出特定级别的所有城市、获取所有级别的统计信息、以及根据关键词搜索城市。服务采用FastMCP框架和SSE协议实现，确保高效稳定的查询体验。

## 类型

数据查询、城市信息、地理服务

## 功能

- 根据城市名称查询城市属于哪一线城市
- 列出指定分级的所有城市
- 获取所有城市分级的统计信息
- 根据关键词搜索城市

## 城市分级

- **一线城市（4个）**：上海、北京、深圳、广州
- **新一线城市（15个）**：成都、杭州、重庆、武汉、苏州、西安、南京、长沙、郑州、天津、合肥、青岛、东莞、宁波、佛山
- **二线城市（30个）**：济南、无锡、沈阳、昆明、福州、厦门、温州、石家庄等
- **三线城市（70个）**：乌鲁木齐、兰州、中山、盐城、海口、扬州等
- **四线城市（90个）**：枣庄、宜宾、榆林、开封、邵阳、运城等
- **五线城市（128个）**：忻州、盘锦、伊犁、丹东、延边、酒泉等

## 安装

```bash
pip install -r requirements.txt
```

## 使用

### 作为 MCP Server 运行（SSE 协议）

```bash
python server.py
```

服务器将在 SSE 模式下运行，默认监听端口。

### 可用工具

1. **get_city_tier** - 查询城市分级
   - 参数：`city_name` (string) - 城市名称
   - 示例：查询"上海"返回"上海 属于 一线城市"

2. **list_cities_by_tier** - 列出指定分级的城市
   - 参数：`tier` (string) - 城市分级
   - 可选值：一线城市、新一线城市、二线城市、三线城市、四线城市、五线城市

3. **get_all_tiers** - 获取所有分级统计
   - 无参数
   - 返回各分级城市数量统计

4. **search_cities** - 搜索城市
   - 参数：`keyword` (string) - 搜索关键词
   - 返回包含关键词的城市列表及其分级

## 服务配置

在 MCP 客户端配置文件中添加：

### SSE 协议配置

```json
{
  "mcpServers": {
    "city-tier": {
      "command": "python",
      "args": ["main.py"],
      "cwd": "/path/to/mcp_server/city",
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "enabled": true,
      "sse": {
        "url": "http://localhost:8080/sse"
      }
    }
  }
}
```

或者使用项目脚本启动：

```json
{
  "mcpServers": {
    "city-tier": {
      "command": "bash",
      "args": ["start_server.sh"],
      "cwd": "/path/to/mcp_server/city",
      "enabled": true,
      "sse": {
        "url": "http://localhost:8080/sse"
      }
    }
  }
}
```

### 使用 uvx 运行

```json
{
  "mcpServers": {
    "city-tier": {
      "command": "uvx",
      "args": ["fastmcp", "run", "main.py"],
      "cwd": "/path/to/mcp_server/city",
      "env": {
        "FASTMCP_LOG_LEVEL": "ERROR"
      },
      "enabled": true,
      "sse": {
        "url": "http://localhost:8080/sse"
      }
    }
  }
}
```

## 环境变量配置

支持的环境变量：

- `FASTMCP_LOG_LEVEL`: 日志级别，可选值为 DEBUG、INFO、WARNING、ERROR，默认为 ERROR