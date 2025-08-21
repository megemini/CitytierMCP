# City Tier Query MCP Server

## Service Introduction

A city tier query service based on the 2025 New First-tier Cities Charm Ranking, using FastMCP and SSE protocols. This service provides comprehensive city tier query functionality, supporting queries by city name, listing cities by tier, obtaining statistical information, and keyword-based search.

## Service Description

This is a professional city tier query MCP service based on the latest 2025 city charm ranking data. The service provides four main functions: querying the tier of a city by name, listing all cities in a specific tier, obtaining statistical information for all tiers, and searching for cities by keywords. The service is implemented using the FastMCP framework and SSE protocol, ensuring efficient and stable query experience.

## Type

Data Query, City Information, Geographic Service

## Features

- Query which tier a city belongs to by city name
- List all cities in a specified tier
- Get statistical information for all city tiers
- Search for cities by keywords

## City Tiers

- **First-tier Cities (4)**: Shanghai, Beijing, Shenzhen, Guangzhou
- **New First-tier Cities (15)**: Chengdu, Hangzhou, Chongqing, Wuhan, Suzhou, Xi'an, Nanjing, Changsha, Zhengzhou, Tianjin, Hefei, Qingdao, Dongguan, Ningbo, Foshan
- **Second-tier Cities (30)**: Jinan, Wuxi, Shenyang, Kunming, Fuzhou, Xiamen, Wenzhou, Shijiazhuang, etc.
- **Third-tier Cities (70)**: Urumqi, Lanzhou, Zhongshan, Yancheng, Haikou, Yangzhou, etc.
- **Fourth-tier Cities (90)**: Zaozhuang, Yibin, Yulin, Kaifeng, Shaoyang, Yuncheng, etc.
- **Fifth-tier Cities (128)**: Xinzhou, Panjin, Ili, Dandong, Yanbian, Jiuquan, etc.

## Installation

```bash
pip install -r requirements.txt
```

## Usage

### Running as MCP Server (SSE Protocol)

```bash
python server.py
```

The server will run in SSE mode, listening on the default port.

### Available Tools

1. **get_city_tier** - Query city tier
   - Parameter: `city_name` (string) - City name
   - Example: Querying "Shanghai" returns "Shanghai belongs to First-tier City"

2. **list_cities_by_tier** - List cities by tier
   - Parameter: `tier` (string) - City tier
   - Optional values: First-tier City, New First-tier City, Second-tier City, Third-tier City, Fourth-tier City, Fifth-tier City

3. **get_all_tiers** - Get all tier statistics
   - No parameters
   - Returns city count statistics for each tier

4. **search_cities** - Search cities
   - Parameter: `keyword` (string) - Search keyword
   - Returns a list of cities containing the keyword and their tiers

## Service Configuration

Add to MCP client configuration file:

### SSE Protocol Configuration

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

Or use the project script to start:

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

### Using uvx to run

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

## Environment Variable Configuration

Supported environment variables:

- `FASTMCP_LOG_LEVEL`: Log level, optional values are DEBUG, INFO, WARNING, ERROR, default is ERROR