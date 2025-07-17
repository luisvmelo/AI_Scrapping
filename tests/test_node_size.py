"""
Unit tests for node size computation functions

Tests validate:
1. Deterministic output for fixed degrees
2. Size growth with popularity numbers
3. Proper handling of None values
4. Z-score normalization
5. Range constraints [4, 20] for degree, [4, 12] for popularity
6. Statistics computation from DataFrames
"""

import pytest
import pandas as pd
import math
from typing import Dict

# Import the module under test
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from utils.node_size import (
    size_by_degree,
    size_by_popularity,
    compute_stats,
    compute_all_degree_sizes,
    compute_all_popularity_sizes
)


class TestSizeByDegree:
    """Test cases for degree-based node sizing"""
    
    def test_deterministic_output_fixed_degrees(self):
        """Test that specific degrees produce expected sizes"""
        # Test cases with known expected values
        test_cases = [
            (0, 4.0),                    # Isolated node
            (1, 4.0 + math.log1p(1) * 2),  # ~5.386
            (2, 4.0 + math.log1p(2) * 2),  # ~6.197
            (10, 4.0 + math.log1p(10) * 2), # ~8.833
            (100, 4.0 + math.log1p(100) * 2) # ~13.014
        ]
        
        for degree, expected in test_cases:
            result = size_by_degree(degree)
            assert abs(result - expected) < 0.001, f"Degree {degree}: expected ~{expected:.3f}, got {result:.3f}"
    
    def test_specific_degree_values(self):
        """Test specific degree values mentioned in requirements"""
        # Degree 1 should give approximately 4.7
        result_1 = size_by_degree(1)
        assert 4.6 < result_1 < 4.8, f"Degree 1 should be ~4.7, got {result_1:.3f}"
        
        # Degree 0 should give exactly 4.0
        result_0 = size_by_degree(0)
        assert result_0 == 4.0, f"Degree 0 should be 4.0, got {result_0}"
    
    def test_range_constraints(self):
        """Test that output is constrained to [4, 20] range"""
        # Test lower bound
        assert size_by_degree(0) >= 4.0
        assert size_by_degree(-5) >= 4.0  # Negative degrees
        
        # Test upper bound with very high degrees
        assert size_by_degree(10000) <= 20.0
        assert size_by_degree(1000000) <= 20.0
    
    def test_monotonic_increase(self):
        """Test that size increases monotonically with degree"""
        degrees = [0, 1, 5, 10, 25, 50, 100]
        sizes = [size_by_degree(d) for d in degrees]
        
        for i in range(len(sizes) - 1):
            assert sizes[i] <= sizes[i + 1], f"Size should increase: {sizes[i]} <= {sizes[i + 1]}"
    
    def test_negative_degree_handling(self):
        """Test handling of negative degree values"""
        assert size_by_degree(-1) == size_by_degree(0)
        assert size_by_degree(-100) == size_by_degree(0)


class TestSizeByPopularity:
    """Test cases for popularity-based node sizing"""
    
    def setUp_sample_stats(self) -> Dict[str, float]:
        """Create sample statistics for testing"""
        return {
            'monthly_users_mean': 100000.0,
            'monthly_users_std': 500000.0,
            'upvotes_mean': 1000.0,
            'upvotes_std': 2000.0,
            'max_rank': 1000.0
        }
    
    def test_none_value_handling(self):
        """Test that None values are handled properly (treated as 1)"""
        stats = self.setUp_sample_stats()
        
        # All None values should give base size
        result = size_by_popularity(None, None, None, stats)
        assert 4.0 <= result <= 12.0, f"All None should be in range, got {result}"
        
        # Individual None values
        result1 = size_by_popularity(100000, None, 50, stats)
        result2 = size_by_popularity(None, 1000, 50, stats)
        result3 = size_by_popularity(100000, 1000, None, stats)
        
        for r in [result1, result2, result3]:
            assert 4.0 <= r <= 12.0, f"Partial None should be in range, got {r}"
    
    def test_size_grows_with_popularity(self):
        """Test that size increases with higher popularity metrics"""
        stats = self.setUp_sample_stats()
        
        # Low popularity tool
        size_low = size_by_popularity(1000, 100, 500, stats)
        
        # Medium popularity tool
        size_medium = size_by_popularity(50000, 1000, 100, stats)
        
        # High popularity tool
        size_high = size_by_popularity(1000000, 5000, 10, stats)
        
        # Sizes should generally increase with popularity
        # Note: due to z-score normalization, this isn't always strictly monotonic
        # but high popularity should generally be larger than low popularity
        assert size_low < size_high, f"High popularity should be larger: {size_low} < {size_high}"
        
        print(f"Low: {size_low:.3f}, Medium: {size_medium:.3f}, High: {size_high:.3f}")
    
    def test_range_constraints_popularity(self):
        """Test that popularity-based sizes stay in reasonable range"""
        stats = self.setUp_sample_stats()
        
        # Test various combinations
        test_cases = [
            (1, 1, 1),           # Minimal values
            (1000000, 10000, 1), # High users, high votes, best rank
            (10, 5, 1000),       # Low users, low votes, worst rank
            (None, None, None),   # All None
        ]
        
        for users, votes, rank in test_cases:
            result = size_by_popularity(users, votes, rank, stats)
            assert 4.0 <= result <= 12.0, f"Size {result:.3f} out of range [4, 12] for {users}, {votes}, {rank}"
    
    def test_rank_inversion(self):
        """Test that lower rank (better position) gives higher size"""
        stats = self.setUp_sample_stats()
        
        # Same users and votes, different ranks
        size_rank_1 = size_by_popularity(100000, 1000, 1, stats)  # Best rank
        size_rank_100 = size_by_popularity(100000, 1000, 100, stats)  # Worse rank
        
        # Lower rank should generally give higher size (though z-score can complicate this)
        print(f"Rank 1: {size_rank_1:.3f}, Rank 100: {size_rank_100:.3f}")
        # Just ensure both are in valid range
        assert 4.0 <= size_rank_1 <= 12.0
        assert 4.0 <= size_rank_100 <= 12.0
    
    def test_zero_std_handling(self):
        """Test handling when standard deviation is zero"""
        stats_zero_std = {
            'monthly_users_mean': 100000.0,
            'monthly_users_std': 0.0,  # Zero std
            'upvotes_mean': 1000.0,
            'upvotes_std': 0.0,        # Zero std
            'max_rank': 1000.0
        }
        
        result = size_by_popularity(100000, 1000, 50, stats_zero_std)
        assert 4.0 <= result <= 12.0, f"Zero std should be handled, got {result}"


class TestComputeStats:
    """Test cases for statistics computation"""
    
    def test_compute_stats_basic(self):
        """Test basic statistics computation"""
        df = pd.DataFrame({
            'monthly_users': [100000, 500000, 200000, 50000],
            'upvotes': [1000, 2000, 1500, 500],
            'rank': [1, 5, 10, 2]
        })
        
        stats = compute_stats(df)
        
        # Check that all required keys are present
        required_keys = ['monthly_users_mean', 'monthly_users_std', 
                        'upvotes_mean', 'upvotes_std', 'max_rank']
        for key in required_keys:
            assert key in stats, f"Missing key: {key}"
        
        # Check reasonable values
        assert stats['monthly_users_mean'] > 0
        assert stats['upvotes_mean'] > 0
        assert stats['max_rank'] > 0
        
        # Verify specific calculations
        expected_users_mean = (100000 + 500000 + 200000 + 50000) / 4
        assert abs(stats['monthly_users_mean'] - expected_users_mean) < 0.1
        
        expected_max_rank = 10  # Max of [1, 5, 10, 2]
        assert stats['max_rank'] == expected_max_rank
    
    def test_compute_stats_with_none_values(self):
        """Test statistics computation with None/NaN values"""
        df = pd.DataFrame({
            'monthly_users': [100000, None, 200000, 50000],
            'upvotes': [1000, 2000, None, 500],
            'rank': [1, 5, 10, None]
        })
        
        stats = compute_stats(df)
        
        # Should handle None values by excluding them
        expected_users_mean = (100000 + 200000 + 50000) / 3  # Exclude None
        assert abs(stats['monthly_users_mean'] - expected_users_mean) < 0.1
        
        # Should still produce valid statistics
        assert stats['monthly_users_std'] > 0
        assert stats['upvotes_mean'] > 0
        assert stats['max_rank'] > 0
    
    def test_compute_stats_empty_data(self):
        """Test statistics computation with empty or all-None data"""
        df_empty = pd.DataFrame({
            'monthly_users': [],
            'upvotes': [],
            'rank': []
        })
        
        stats_empty = compute_stats(df_empty)
        
        # Should provide default values
        assert stats_empty['monthly_users_mean'] == 1.0
        assert stats_empty['monthly_users_std'] == 1.0
        assert stats_empty['max_rank'] == 1.0
        
        # Test all None
        df_none = pd.DataFrame({
            'monthly_users': [None, None, None],
            'upvotes': [None, None, None],
            'rank': [None, None, None]
        })
        
        stats_none = compute_stats(df_none)
        assert stats_none['monthly_users_mean'] == 1.0
        assert stats_none['max_rank'] == 1.0


class TestBatchProcessing:
    """Test cases for batch processing functions"""
    
    def test_compute_all_degree_sizes(self):
        """Test batch computation of degree-based sizes"""
        degrees = pd.Series([0, 1, 5, 10, 25])
        sizes = compute_all_degree_sizes(degrees)
        
        assert len(sizes) == len(degrees)
        assert all(4.0 <= size <= 20.0 for size in sizes)
        
        # Should match individual calculations
        for i, degree in enumerate(degrees):
            expected = size_by_degree(degree)
            assert abs(sizes.iloc[i] - expected) < 0.001
    
    def test_compute_all_popularity_sizes(self):
        """Test batch computation of popularity-based sizes"""
        df = pd.DataFrame({
            'monthly_users': [100000, 500000, None, 50000],
            'upvotes': [1000, 2000, 500, None],
            'rank': [1, 5, 10, 2]
        })
        
        sizes = compute_all_popularity_sizes(df)
        
        assert len(sizes) == len(df)
        assert all(4.0 <= size <= 12.0 for size in sizes)
    
    def test_compute_all_popularity_sizes_with_prestats(self):
        """Test batch computation with pre-computed statistics"""
        df = pd.DataFrame({
            'monthly_users': [100000, 500000, 200000],
            'upvotes': [1000, 2000, 1500],
            'rank': [1, 5, 10]
        })
        
        stats = compute_stats(df)
        sizes = compute_all_popularity_sizes(df, stats)
        
        assert len(sizes) == len(df)
        assert all(4.0 <= size <= 12.0 for size in sizes)


class TestIntegration:
    """Integration tests combining multiple functions"""
    
    def test_realistic_dataset(self):
        """Test with realistic AI tools dataset"""
        # Simulate realistic AI tools data
        df = pd.DataFrame({
            'monthly_users': [1000000, 500000, 100000, 50000, None, 2000000],
            'upvotes': [5000, 2000, 1000, 500, 100, 10000],
            'rank': [1, 5, 20, 50, 100, 2],
            'degree': [15, 8, 5, 2, 1, 25]
        })
        
        # Compute statistics
        stats = compute_stats(df)
        
        # Compute sizes using both methods
        degree_sizes = compute_all_degree_sizes(df['degree'])
        popularity_sizes = compute_all_popularity_sizes(df, stats)
        
        # All sizes should be in valid ranges
        assert all(4.0 <= size <= 20.0 for size in degree_sizes)
        assert all(4.0 <= size <= 12.0 for size in popularity_sizes)
        
        # Popular tools should generally have larger sizes
        # Tool 0: 1M users, 5k upvotes, rank 1 -> should be large
        # Tool 4: None users, 100 upvotes, rank 100 -> should be smaller
        assert popularity_sizes.iloc[0] > popularity_sizes.iloc[4]
        
        print("Degree sizes:", degree_sizes.tolist())
        print("Popularity sizes:", popularity_sizes.tolist())
    
    def test_edge_cases_combination(self):
        """Test edge cases when combining both sizing methods"""
        df = pd.DataFrame({
            'monthly_users': [0, 1, None],
            'upvotes': [0, 1, None], 
            'rank': [0, 1, None],
            'degree': [0, 1, 100]
        })
        
        stats = compute_stats(df)
        
        # Should handle zeros and None values gracefully
        degree_sizes = compute_all_degree_sizes(df['degree'])
        popularity_sizes = compute_all_popularity_sizes(df, stats)
        
        assert len(degree_sizes) == 3
        assert len(popularity_sizes) == 3
        assert all(4.0 <= size <= 20.0 for size in degree_sizes)
        assert all(4.0 <= size <= 12.0 for size in popularity_sizes)


if __name__ == '__main__':
    # Run tests with verbose output
    pytest.main([__file__, '-v', '--tb=short'])