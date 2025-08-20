#!/usr/bin/env python3
"""
城市分级查询 MCP Server 测试脚本
使用 unittest 框架和 FastMCP Client
"""

import sys
import os
import unittest
import asyncio
sys.path.append(os.path.dirname(__file__))

from fastmcp import Client
from main import mcp, CITY_TO_TIER, CITY_TIERS


class TestCityTierFunctions(unittest.TestCase):
    """测试城市分级查询功能"""

    async def test_get_city_tier_existing_city(self):
        """测试查询存在的城市"""
        async with Client(mcp) as client:
            result = await client.call_tool("get_city_tier", {"city_name": "上海"})
            self.assertTrue(result.data["success"])
            self.assertEqual(result.data["city"], "上海")
            self.assertEqual(result.data["tier"], "一线城市")
            self.assertEqual(result.data["message"], "上海 属于 一线城市")
            
            result = await client.call_tool("get_city_tier", {"city_name": "成都"})
            self.assertTrue(result.data["success"])
            self.assertEqual(result.data["city"], "成都")
            self.assertEqual(result.data["tier"], "新一线城市")
            self.assertEqual(result.data["message"], "成都 属于 新一线城市")
            
            result = await client.call_tool("get_city_tier", {"city_name": "济南"})
            self.assertTrue(result.data["success"])
            self.assertEqual(result.data["city"], "济南")
            self.assertEqual(result.data["tier"], "二线城市")
            self.assertEqual(result.data["message"], "济南 属于 二线城市")
            
            result = await client.call_tool("get_city_tier", {"city_name": "乌鲁木齐"})
            self.assertTrue(result.data["success"])
            self.assertEqual(result.data["city"], "乌鲁木齐")
            self.assertEqual(result.data["tier"], "三线城市")
            self.assertEqual(result.data["message"], "乌鲁木齐 属于 三线城市")
            
            result = await client.call_tool("get_city_tier", {"city_name": "枣庄"})
            self.assertTrue(result.data["success"])
            self.assertEqual(result.data["city"], "枣庄")
            self.assertEqual(result.data["tier"], "四线城市")
            self.assertEqual(result.data["message"], "枣庄 属于 四线城市")
            
            result = await client.call_tool("get_city_tier", {"city_name": "忻州"})
            self.assertTrue(result.data["success"])
            self.assertEqual(result.data["city"], "忻州")
            self.assertEqual(result.data["tier"], "五线城市")
            self.assertEqual(result.data["message"], "忻州 属于 五线城市")

    async def test_get_city_tier_city_with_suffix(self):
        """测试查询带市/区后缀的城市"""
        async with Client(mcp) as client:
            result = await client.call_tool("get_city_tier", {"city_name": "上海市"})
            self.assertTrue(result.data["success"])
            self.assertEqual(result.data["city"], "上海市")
            self.assertEqual(result.data["tier"], "一线城市")
            self.assertEqual(result.data["message"], "上海市 属于 一线城市")
            
            result = await client.call_tool("get_city_tier", {"city_name": "成都市"})
            self.assertTrue(result.data["success"])
            self.assertEqual(result.data["city"], "成都市")
            self.assertEqual(result.data["tier"], "新一线城市")
            self.assertEqual(result.data["message"], "成都市 属于 新一线城市")

    async def test_get_city_tier_empty_input(self):
        """测试空输入"""
        async with Client(mcp) as client:
            result = await client.call_tool("get_city_tier", {"city_name": ""})
            self.assertFalse(result.data["success"])
            self.assertEqual(result.data["message"], "请提供城市名称")
            
            result = await client.call_tool("get_city_tier", {"city_name": "   "})
            self.assertFalse(result.data["success"])
            self.assertEqual(result.data["message"], "请提供城市名称")

    async def test_get_city_tier_nonexistent_city(self):
        """测试不存在的城市"""
        async with Client(mcp) as client:
            result = await client.call_tool("get_city_tier", {"city_name": "不存在的城市"})
            self.assertFalse(result.data["success"])
            self.assertEqual(result.data["city"], "不存在的城市")
            self.assertTrue(result.data["message"].startswith("未找到城市 '不存在的城市'"))
            self.assertIn("请检查城市名称是否正确", result.data["message"])

    async def test_get_city_tier_partial_match(self):
        """测试部分匹配的城市名称"""
        async with Client(mcp) as client:
            result = await client.call_tool("get_city_tier", {"city_name": "乌鲁"})
            self.assertFalse(result.data["success"])
            self.assertEqual(result.data["city"], "乌鲁")
            self.assertTrue(result.data["message"].startswith("未找到城市 '乌鲁'"))
            self.assertIn("您是否想查询", result.data["message"])
            self.assertIn("乌鲁木齐", result.data["suggestions"])

    async def test_list_cities_by_tier_valid_tier(self):
        """测试有效的城市分级"""
        async with Client(mcp) as client:
            result = await client.call_tool("list_cities_by_tier", {"tier": "一线城市"})
            self.assertTrue(result.data["success"])
            self.assertEqual(result.data["tier"], "一线城市")
            self.assertEqual(result.data["count"], 4)
            self.assertIn("上海", result.data["cities"])
            self.assertIn("北京", result.data["cities"])
            self.assertIn("深圳", result.data["cities"])
            self.assertIn("广州", result.data["cities"])
            self.assertTrue(result.data["message"].startswith("一线城市（4个）："))

    async def test_list_cities_by_tier_invalid_tier(self):
        """测试无效的城市分级"""
        async with Client(mcp) as client:
            result = await client.call_tool("list_cities_by_tier", {"tier": "不存在的分级"})
            self.assertFalse(result.data["success"])
            self.assertEqual(result.data["tier"], "不存在的分级")
            self.assertTrue(result.data["message"].startswith("无效的城市分级：不存在的分级"))
            self.assertIn("可选分级：", result.data["message"])

    async def test_get_all_tiers(self):
        """测试获取所有分级统计"""
        async with Client(mcp) as client:
            result = await client.call_tool("get_all_tiers", {})
            self.assertTrue(result.data["success"])
            self.assertEqual(result.data["total_cities"], 337)
            self.assertIn("一线城市", result.data["tiers"])
            self.assertIn("新一线城市", result.data["tiers"])
            self.assertIn("二线城市", result.data["tiers"])
            self.assertIn("三线城市", result.data["tiers"])
            self.assertIn("四线城市", result.data["tiers"])
            self.assertIn("五线城市", result.data["tiers"])
            self.assertEqual(result.data["tiers"]["一线城市"]["count"], 4)
            self.assertEqual(result.data["tiers"]["新一线城市"]["count"], 15)
            self.assertEqual(result.data["tiers"]["二线城市"]["count"], 30)
            self.assertEqual(result.data["tiers"]["三线城市"]["count"], 70)
            self.assertEqual(result.data["tiers"]["四线城市"]["count"], 90)
            self.assertEqual(result.data["tiers"]["五线城市"]["count"], 128)
            self.assertIn("一线城市：4个城市", result.data["message"])
            self.assertIn("新一线城市：15个城市", result.data["message"])
            self.assertIn("二线城市：30个城市", result.data["message"])
            self.assertIn("三线城市：70个城市", result.data["message"])
            self.assertIn("四线城市：90个城市", result.data["message"])
            self.assertIn("五线城市：128个城市", result.data["message"])
            self.assertIn("\n\n总计：337个城市", result.data["message"])

    async def test_search_cities_with_results(self):
        """测试有结果的搜索"""
        async with Client(mcp) as client:
            result = await client.call_tool("search_cities", {"keyword": "州"})
            self.assertTrue(result.data["success"])
            self.assertEqual(result.data["keyword"], "州")
            self.assertTrue(result.data["count"] > 0)
            self.assertTrue(result.data["message"].startswith("找到"))
            self.assertIn("个匹配城市", result.data["message"])
            
            # 检查匹配结果中包含杭州和广州
            cities = [m["city"] for m in result.data["matches"]]
            self.assertIn("杭州", cities)
            self.assertIn("广州", cities)
            
            # 检查杭州和广州的分级
            for match in result.data["matches"]:
                if match["city"] == "杭州":
                    self.assertEqual(match["tier"], "新一线城市")
                if match["city"] == "广州":
                    self.assertEqual(match["tier"], "一线城市")

    async def test_search_cities_many_results(self):
        """测试大量结果的搜索"""
        async with Client(mcp) as client:
            result = await client.call_tool("search_cities", {"keyword": "州"})
            self.assertTrue(result.data["success"])
            self.assertEqual(result.data["keyword"], "州")
            self.assertTrue(result.data["count"] > 20)
            self.assertTrue(result.data["truncated"])
            self.assertEqual(len(result.data["matches"]), 20)
            self.assertTrue(result.data["message"].startswith("找到"))
            self.assertIn("个匹配城市，前20个：", result.data["message"])
            self.assertTrue(result.data["message"].endswith("..."))

    async def test_search_cities_no_results(self):
        """测试无结果的搜索"""
        async with Client(mcp) as client:
            result = await client.call_tool("search_cities", {"keyword": "不存在的关键词"})
            self.assertFalse(result.data["success"])
            self.assertEqual(result.data["keyword"], "不存在的关键词")
            self.assertEqual(result.data["message"], "未找到包含 '不存在的关键词' 的城市")

    async def test_search_cities_empty_input(self):
        """测试空输入搜索"""
        async with Client(mcp) as client:
            result = await client.call_tool("search_cities", {"keyword": ""})
            self.assertFalse(result.data["success"])
            self.assertEqual(result.data["keyword"], "")
            self.assertEqual(result.data["message"], "请提供搜索关键词")
            
            result = await client.call_tool("search_cities", {"keyword": "   "})
            self.assertFalse(result.data["success"])
            self.assertEqual(result.data["keyword"], "")
            self.assertEqual(result.data["message"], "请提供搜索关键词")

    def test_city_to_tier_mapping(self):
        """测试城市到分级的映射完整性"""
        # 验证映射不为空
        self.assertTrue(len(CITY_TO_TIER) > 0)
        
        # 验证一些已知城市的映射
        self.assertEqual(CITY_TO_TIER["上海"], "一线城市")
        self.assertEqual(CITY_TO_TIER["成都"], "新一线城市")
        self.assertEqual(CITY_TO_TIER["济南"], "二线城市")
        self.assertEqual(CITY_TO_TIER["乌鲁木齐"], "三线城市")
        self.assertEqual(CITY_TO_TIER["枣庄"], "四线城市")
        self.assertEqual(CITY_TO_TIER["忻州"], "五线城市")

    def test_city_tiers_structure(self):
        """测试城市分级数据结构完整性"""
        # 验证所有预期的分级都存在
        expected_tiers = ["一线城市", "新一线城市", "二线城市", "三线城市", "四线城市", "五线城市"]
        for tier in expected_tiers:
            self.assertIn(tier, CITY_TIERS)
            self.assertTrue(len(CITY_TIERS[tier]) > 0)
        
        # 验证每个分级的城市数量
        self.assertEqual(len(CITY_TIERS["一线城市"]), 4)
        self.assertEqual(len(CITY_TIERS["新一线城市"]), 15)
        self.assertEqual(len(CITY_TIERS["二线城市"]), 30)
        self.assertEqual(len(CITY_TIERS["三线城市"]), 70)
        self.assertEqual(len(CITY_TIERS["四线城市"]), 90)
        self.assertEqual(len(CITY_TIERS["五线城市"]), 128)

    # Helper method to run async tests
    def _run_async_test(self, coro):
        """Helper method to run async test methods"""
        loop = asyncio.new_event_loop()
        try:
            return loop.run_until_complete(coro)
        finally:
            loop.close()

    # Override default test method to handle async tests
    def run(self, result=None):
        """Override run method to handle both async and regular test methods"""
        # Get all test methods
        test_methods = [method for method in dir(self) if method.startswith('test_')]
        
        for method_name in test_methods:
            method = getattr(self, method_name)
            if asyncio.iscoroutinefunction(method):
                # Run async test methods
                try:
                    self._run_async_test(method())
                    if result:
                        result.addSuccess(self)
                except Exception as e:
                    if result:
                        result.addError(self, e)
            else:
                # Run regular test methods
                super().run(result)

if __name__ == "__main__":
    unittest.main()