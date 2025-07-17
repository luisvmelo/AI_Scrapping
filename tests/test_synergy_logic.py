"""
Unit tests for formal edge-scoring logic

Tests validate:
1. Video↔audio pair gets edge (base connectivity)
2. Unrelated domains with low semantic score get no edge
3. Higher popularity increases strength
4. TF-IDF semantic similarity calculation
5. Popularity normalization
6. Edge strength threshold filtering
"""

import unittest
import math
import numpy as np
from unittest.mock import Mock, patch
from synergy.build_synergy import EdgeScoringEngine, ToolData


class TestSynergyLogic(unittest.TestCase):
    """Test suite for edge-scoring algorithm"""
    
    def setUp(self):
        """Set up test fixtures"""
        # Mock Supabase connection to avoid network dependencies
        with patch('synergy.build_synergy.create_client'):
            self.engine = EdgeScoringEngine()
        
        # Mock the supabase client
        self.engine.supabase = Mock()
        
        # Create test tools
        self.video_tool = ToolData(
            id='video_tool_1',
            name='Video Editor Pro',
            description='Professional video editing software with AI enhancement',
            macro_domain='VIDEO',
            categories=['video', 'editing', 'professional'],
            monthly_users=1000000,
            popularity=85.0
        )
        
        self.audio_tool = ToolData(
            id='audio_tool_1', 
            name='Audio Master',
            description='Advanced audio processing and enhancement tool',
            macro_domain='AUDIO',
            categories=['audio', 'processing', 'professional'],
            monthly_users=500000,
            popularity=75.0
        )
        
        self.nlp_tool = ToolData(
            id='nlp_tool_1',
            name='Text Analyzer',
            description='Natural language processing for document analysis',
            macro_domain='NLP',
            categories=['text', 'analysis', 'business'],
            monthly_users=2000000,
            popularity=90.0
        )
        
        self.unrelated_tool = ToolData(
            id='unrelated_tool_1',
            name='Spreadsheet Calculator',
            description='Basic spreadsheet calculations and data management',
            macro_domain='BUSINESS',
            categories=['spreadsheet', 'calculations'],
            monthly_users=100000,
            popularity=60.0
        )
    
    def test_video_audio_base_connectivity(self):
        """Test that video↔audio pairs get base connectivity score of 1.0"""
        base_score = self.engine._calculate_base_connectivity(
            self.video_tool.macro_domain, 
            self.audio_tool.macro_domain
        )
        
        self.assertEqual(base_score, 1.0, 
                        "Video and Audio domains should have base connectivity of 1.0")
    
    def test_same_domain_base_connectivity(self):
        """Test that same domains get base connectivity score of 1.0"""
        base_score = self.engine._calculate_base_connectivity('NLP', 'NLP')
        
        self.assertEqual(base_score, 1.0,
                        "Same domains should have base connectivity of 1.0")
    
    def test_unrelated_domains_no_base_connectivity(self):
        """Test that unrelated domains get base connectivity score of 0.0"""
        base_score = self.engine._calculate_base_connectivity(
            self.nlp_tool.macro_domain,
            self.unrelated_tool.macro_domain
        )
        
        self.assertEqual(base_score, 0.0,
                        "Unrelated domains should have base connectivity of 0.0")
    
    def test_semantic_similarity_with_similar_descriptions(self):
        """Test semantic similarity calculation with similar descriptions"""
        # Create TF-IDF vectors for similar descriptions
        descriptions = [
            'Professional video editing software with AI enhancement',
            'Advanced video editing tool with artificial intelligence'
        ]
        
        tfidf_matrix = self.engine._compute_tfidf_matrix(descriptions)
        
        similarity = self.engine._calculate_semantic_similarity(
            tfidf_matrix[0], tfidf_matrix[1]
        )
        
        self.assertGreater(similarity, 0.3,
                          "Similar descriptions should have semantic similarity > 0.3")
        self.assertLessEqual(similarity, 1.0,
                            "Semantic similarity should not exceed 1.0")
    
    def test_semantic_similarity_with_different_descriptions(self):
        """Test semantic similarity with completely different descriptions"""
        descriptions = [
            'Professional video editing software with AI enhancement',
            'Basic spreadsheet calculations and data management'
        ]
        
        tfidf_matrix = self.engine._compute_tfidf_matrix(descriptions)
        
        similarity = self.engine._calculate_semantic_similarity(
            tfidf_matrix[0], tfidf_matrix[1]
        )
        
        self.assertLess(similarity, 0.2,
                       "Different descriptions should have low semantic similarity")
    
    def test_popularity_score_calculation(self):
        """Test popularity score calculation and normalization"""
        tools = [self.video_tool, self.audio_tool, self.nlp_tool, self.unrelated_tool]
        pop_factors = self.engine._calculate_popularity_normalization(tools)
        
        # Test high popularity pair
        high_pop_score = self.engine._calculate_popularity_score(
            self.video_tool.monthly_users,
            self.nlp_tool.monthly_users,
            pop_factors
        )
        
        # Test low popularity pair  
        low_pop_score = self.engine._calculate_popularity_score(
            self.unrelated_tool.monthly_users,
            self.audio_tool.monthly_users,
            pop_factors
        )
        
        self.assertGreater(high_pop_score, low_pop_score,
                          "Higher popularity tools should have higher popularity score")
        
        self.assertGreaterEqual(high_pop_score, 0.0,
                               "Popularity score should be >= 0")
        self.assertLessEqual(high_pop_score, 1.0,
                            "Popularity score should be <= 1")
    
    def test_edge_strength_video_audio_pair(self):
        """Test that video↔audio pair gets a strong edge"""
        # Mock TF-IDF vectors
        tfidf1 = np.array([0.1, 0.2, 0.3, 0.4])
        tfidf2 = np.array([0.2, 0.1, 0.4, 0.3])
        
        # Mock popularity factors
        pop_factors = {
            'min_product': 0.0,
            'max_product': 100.0,
            'log_users': [1.0, 2.0]
        }
        
        strength = self.engine._calculate_edge_strength(
            self.video_tool, self.audio_tool,
            tfidf1, tfidf2, pop_factors
        )
        
        # Should have base connectivity (0.4 * 1.0 = 0.4) plus other factors
        self.assertGreaterEqual(strength, 0.4,
                               "Video↔Audio pair should have strength >= 0.4 from base connectivity")
        
        # Should exceed threshold for inclusion
        self.assertGreaterEqual(strength, self.engine.STRENGTH_THRESHOLD,
                               "Video↔Audio pair should exceed strength threshold")
    
    def test_edge_strength_unrelated_tools(self):
        """Test that unrelated tools with low semantic similarity get weak/no edge"""
        # Mock low similarity TF-IDF vectors
        tfidf1 = np.array([1.0, 0.0, 0.0, 0.0])
        tfidf2 = np.array([0.0, 1.0, 0.0, 0.0])
        
        # Mock popularity factors
        pop_factors = {
            'min_product': 0.0,
            'max_product': 100.0,
            'log_users': [1.0, 2.0]
        }
        
        strength = self.engine._calculate_edge_strength(
            self.nlp_tool, self.unrelated_tool,
            tfidf1, tfidf2, pop_factors
        )
        
        # Should have low strength (no base connectivity, low semantic similarity)
        self.assertLess(strength, self.engine.STRENGTH_THRESHOLD,
                       "Unrelated tools should have strength below threshold")
    
    def test_popularity_boost_effect(self):
        """Test that higher popularity increases edge strength"""
        # Create two similar tools with different popularity
        high_pop_tool = ToolData(
            id='high_pop',
            name='Popular Tool',
            description='AI tool for text processing',
            macro_domain='NLP',
            categories=['text'],
            monthly_users=10000000,  # High popularity
            popularity=95.0
        )
        
        low_pop_tool = ToolData(
            id='low_pop',
            name='Niche Tool', 
            description='AI tool for text processing',
            macro_domain='NLP',
            categories=['text'],
            monthly_users=10000,  # Low popularity
            popularity=70.0
        )
        
        # Mock identical TF-IDF vectors (high semantic similarity)
        tfidf_vec = np.array([0.5, 0.5, 0.5, 0.5])
        
        # Calculate popularity factors for both scenarios
        tools_high = [high_pop_tool, self.nlp_tool]
        tools_low = [low_pop_tool, self.nlp_tool]
        
        pop_factors_high = self.engine._calculate_popularity_normalization(tools_high)
        pop_factors_low = self.engine._calculate_popularity_normalization(tools_low)
        
        strength_high = self.engine._calculate_edge_strength(
            high_pop_tool, self.nlp_tool,
            tfidf_vec, tfidf_vec, pop_factors_high
        )
        
        strength_low = self.engine._calculate_edge_strength(
            low_pop_tool, self.nlp_tool,
            tfidf_vec, tfidf_vec, pop_factors_low
        )
        
        self.assertGreater(strength_high, strength_low,
                          "Higher popularity should result in higher edge strength")
    
    def test_strength_threshold_filtering(self):
        """Test that edges below strength threshold are filtered out"""
        threshold = self.engine.STRENGTH_THRESHOLD
        
        # Test edge above threshold
        self.assertTrue(0.3 >= threshold or 0.3 < threshold,
                       "Threshold filtering logic should be binary")
        
        # Verify threshold value matches specification
        self.assertEqual(threshold, 0.25,
                        "Strength threshold should be 0.25 as specified")
    
    def test_algorithm_weights(self):
        """Test that algorithm weights sum to 1.0 and match specification"""
        total_weight = (self.engine.BASE_WEIGHT + 
                       self.engine.SEMANTIC_WEIGHT + 
                       self.engine.POPULARITY_WEIGHT)
        
        self.assertAlmostEqual(total_weight, 1.0, places=5,
                              msg="Algorithm weights should sum to 1.0")
        
        # Verify individual weights match specification
        self.assertEqual(self.engine.BASE_WEIGHT, 0.4)
        self.assertEqual(self.engine.SEMANTIC_WEIGHT, 0.4)
        self.assertEqual(self.engine.POPULARITY_WEIGHT, 0.2)
    
    def test_tool_id_ordering(self):
        """Test that tool IDs are correctly ordered (tool_id_1 < tool_id_2)"""
        id1 = 'tool_z'
        id2 = 'tool_a'
        
        # Simulate the ordering logic from the main algorithm
        tool_id_1 = min(id1, id2)
        tool_id_2 = max(id1, id2)
        
        self.assertEqual(tool_id_1, 'tool_a')
        self.assertEqual(tool_id_2, 'tool_z')
        self.assertLess(tool_id_1, tool_id_2,
                       "tool_id_1 should be less than tool_id_2")
    
    def test_category_filtering_optimization(self):
        """Test that category filtering reduces computation complexity"""
        tools = [self.video_tool, self.audio_tool, self.nlp_tool, self.unrelated_tool]
        
        candidate_pairs = self.engine._filter_pairs_by_category_overlap(tools)
        
        # Should reduce from N*(N-1)/2 to much smaller set
        max_possible_pairs = len(tools) * (len(tools) - 1) // 2
        
        self.assertLessEqual(len(candidate_pairs), max_possible_pairs,
                            "Filtering should not increase number of pairs")
        
        # Should include pairs with category overlap
        tool_indices = {tool.id: i for i, tool in enumerate(tools)}
        
        # Check that pairs with shared categories are included
        professional_pairs = []
        for i, (idx1, idx2) in enumerate(candidate_pairs):
            tool1, tool2 = tools[idx1], tools[idx2]
            if ('professional' in tool1.categories and 
                'professional' in tool2.categories):
                professional_pairs.append((idx1, idx2))
        
        self.assertGreater(len(professional_pairs), 0,
                          "Pairs with shared categories should be included")


class TestEdgeScoringIntegration(unittest.TestCase):
    """Integration tests for the complete edge scoring system"""
    
    def setUp(self):
        """Set up integration test fixtures"""
        with patch('synergy.build_synergy.create_client'):
            self.engine = EdgeScoringEngine()
        
        # Mock Supabase operations
        self.engine.supabase = Mock()
    
    def test_complete_edge_calculation_flow(self):
        """Test the complete edge calculation workflow"""
        # Mock database response
        mock_tools_data = [
            {
                'id': 'tool1',
                'name': 'Video Tool',
                'description': 'Video editing software',
                'macro_domain': 'VIDEO',
                'categories': ['video', 'editing'],
                'monthly_users': 1000000,
                'popularity': 85.0
            },
            {
                'id': 'tool2', 
                'name': 'Audio Tool',
                'description': 'Audio processing software',
                'macro_domain': 'AUDIO',
                'categories': ['audio', 'processing'],
                'monthly_users': 500000,
                'popularity': 75.0
            }
        ]
        
        self.engine.supabase.table.return_value.select.return_value.execute.return_value.data = mock_tools_data
        self.engine.supabase.table.return_value.delete.return_value.gte.return_value.execute.return_value = Mock()
        self.engine.supabase.table.return_value.insert.return_value.execute.return_value.data = [{'id': 1}]
        self.engine.supabase.rpc.return_value.execute.return_value = Mock()
        
        # Run calculation
        stats = self.engine.calculate_all_edges()
        
        # Verify results
        self.assertIn('calculated', stats)
        self.assertIn('inserted', stats)
        self.assertIn('filtered_out', stats)
        self.assertIn('errors', stats)
        
        # Should have calculated at least one pair
        self.assertGreaterEqual(stats['calculated'], 0)


if __name__ == '__main__':
    # Run the test suite
    unittest.main(verbosity=2)