"""
Unit tests for merge and deduplication logic
"""

import unittest
from datetime import datetime
from scrapers.common import AITool
from merge.merge_and_upsert import SupabaseMerger


class TestMergeDeduplication(unittest.TestCase):
    """Test cases for merge and deduplication logic"""
    
    def setUp(self):
        """Set up test environment"""
        # Create a mock merger (without actual Supabase connection)
        self.merger = MockSupabaseMerger()
    
    def test_deduplicate_by_url(self):
        """Test deduplication by identical URLs"""
        tools = [
            AITool(
                ext_id="tool1",
                name="Tool A",
                description="Short description",
                price="Free",
                popularity=50,
                categories=["ai"],
                source="source1",
                url="https://example.com/tool",
                upvotes=10,
                monthly_users=1000
            ),
            AITool(
                ext_id="tool2",
                name="Tool B", 
                description="Much longer and more detailed description",
                price="$10/month",
                popularity=75,
                categories=["productivity"],
                source="source2",
                url="https://example.com/tool",  # Same URL
                upvotes=20,
                monthly_users=2000
            )
        ]
        
        deduplicated = self.merger._deduplicate_tools_batch(tools)
        
        # Should have only 1 tool after deduplication
        self.assertEqual(len(deduplicated), 1)
        
        tool = deduplicated[0]
        
        # Should keep longer description
        self.assertEqual(tool.description, "Much longer and more detailed description")
        
        # Should keep larger numeric values
        self.assertEqual(tool.popularity, 75)
        self.assertEqual(tool.upvotes, 20)
        self.assertEqual(tool.monthly_users, 2000)
        
        # Should combine categories
        self.assertIn("ai", tool.categories)
        self.assertIn("productivity", tool.categories)
    
    def test_deduplicate_by_name(self):
        """Test deduplication by identical names"""
        tools = [
            AITool(
                ext_id="tool1",
                name="ChatGPT",
                description="AI assistant",
                price="Free",
                popularity=80,
                categories=["chatbot"],
                source="source1",
                url="https://chat.openai.com",
                rank=1,
                upvotes=100
            ),
            AITool(
                ext_id="tool2",
                name="chatgpt",  # Same name (case insensitive)
                description="Advanced AI conversational assistant with capabilities",
                price="$20/month",
                popularity=90,
                categories=["ai", "productivity"],
                source="source2",
                url="https://openai.com/chatgpt",
                rank=2,
                upvotes=150
            )
        ]
        
        deduplicated = self.merger._deduplicate_tools_batch(tools)
        
        # Should have only 1 tool after deduplication
        self.assertEqual(len(deduplicated), 1)
        
        tool = deduplicated[0]
        
        # Should keep longer description
        self.assertEqual(tool.description, "Advanced AI conversational assistant with capabilities")
        
        # Should keep larger numeric values
        self.assertEqual(tool.popularity, 90)
        self.assertEqual(tool.upvotes, 150)
        self.assertEqual(tool.rank, 1)  # Should keep smaller rank (better)
        
        # Should combine categories
        self.assertIn("chatbot", tool.categories)
        self.assertIn("ai", tool.categories)
        self.assertIn("productivity", tool.categories)
    
    def test_no_duplicates_remain(self):
        """Test that no duplicates remain after processing"""
        tools = [
            AITool(
                ext_id="tool1",
                name="Tool A",
                description="Description A",
                price="Free",
                popularity=50,
                categories=["ai"],
                source="source1",
                url="https://example.com/a"
            ),
            AITool(
                ext_id="tool2",
                name="Tool B",
                description="Description B", 
                price="$10",
                popularity=60,
                categories=["productivity"],
                source="source2",
                url="https://example.com/b"
            ),
            AITool(
                ext_id="tool3",
                name="Tool A",  # Duplicate name
                description="Better description A",
                price="$5",
                popularity=70,
                categories=["business"],
                source="source3",
                url="https://different.com/a"
            ),
            AITool(
                ext_id="tool4",
                name="Tool C",
                description="Description C",
                price="Free",
                popularity=40,
                categories=["design"],
                source="source4",
                url="https://example.com/b"  # Duplicate URL
            )
        ]
        
        deduplicated = self.merger._deduplicate_tools_batch(tools)
        
        # Should have 2 tools after deduplication (A merged, B merged with C)
        self.assertEqual(len(deduplicated), 2)
        
        # Check no duplicate names
        names = [tool.name.lower() for tool in deduplicated]
        self.assertEqual(len(names), len(set(names)))
        
        # Check no duplicate URLs
        urls = [tool.url.lower() for tool in deduplicated if tool.url]
        self.assertEqual(len(urls), len(set(urls)))
    
    def test_merge_tool_objects(self):
        """Test merging two AITool objects"""
        existing = AITool(
            ext_id="existing",
            name="Existing Tool",
            description="Short desc",
            price="Free",
            popularity=30,
            categories=["ai"],
            source="source1",
            url="https://example.com",
            rank=5,
            upvotes=50,
            monthly_users=500,
            editor_score=6.0,
            platform=["web"],
            features={"free_tier": True}
        )
        
        new = AITool(
            ext_id="new",
            name="New Tool",
            description="Much longer and more detailed description with lots of information",
            price="$20/month",
            popularity=80,
            categories=["productivity", "business"],
            source="source2",
            url="https://example.com",
            rank=2,
            upvotes=100,
            monthly_users=2000,
            editor_score=8.5,
            platform=["web", "mobile"],
            features={"api_available": True}
        )
        
        merged = self.merger._merge_tool_objects(existing, new)
        
        # Should keep existing ext_id and source
        self.assertEqual(merged.ext_id, "existing")
        self.assertEqual(merged.source, "source1")
        
        # Should keep longer description
        self.assertEqual(merged.description, "Much longer and more detailed description with lots of information")
        
        # Should keep larger numeric values
        self.assertEqual(merged.popularity, 80)
        self.assertEqual(merged.rank, 2)  # Smaller rank is better
        self.assertEqual(merged.upvotes, 100)
        self.assertEqual(merged.monthly_users, 2000)
        self.assertEqual(merged.editor_score, 8.5)
        
        # Should combine categories and platforms
        self.assertIn("ai", merged.categories)
        self.assertIn("productivity", merged.categories)
        self.assertIn("business", merged.categories)
        self.assertIn("web", merged.platform)
        self.assertIn("mobile", merged.platform)
        
        # Should combine features
        self.assertTrue(merged.features["free_tier"])
        self.assertTrue(merged.features["api_available"])
    
    def test_max_optional_values(self):
        """Test max_optional utility function"""
        # Both None
        self.assertIsNone(self.merger._max_optional(None, None))
        
        # One None
        self.assertEqual(self.merger._max_optional(None, 10), 10)
        self.assertEqual(self.merger._max_optional(5, None), 5)
        
        # Both have values
        self.assertEqual(self.merger._max_optional(3, 7), 7)
        self.assertEqual(self.merger._max_optional(10, 2), 10)
        
        # Special case: smaller rank is better, but we use max for consistency
        # (the logic should handle rank separately if needed)
        self.assertEqual(self.merger._max_optional(1, 5), 5)


class MockSupabaseMerger(SupabaseMerger):
    """Mock version of SupabaseMerger for testing without DB connection"""
    
    def __init__(self):
        # Skip the parent __init__ to avoid Supabase connection
        pass


if __name__ == '__main__':
    unittest.main()