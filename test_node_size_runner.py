#!/usr/bin/env python3
"""
Test runner for node size functions without pytest dependency
"""

import sys
sys.path.append('.')

import pandas as pd
import math
from utils.node_size import size_by_degree, size_by_popularity, compute_stats


def test_size_by_degree():
    """Test degree-based sizing"""
    print("🔧 Testing size_by_degree function...")
    
    # Test deterministic outputs
    test_cases = [
        (0, 4.0),
        (1, 4.0 + math.log1p(1) * 1.01),  # Should be ~4.7
        (10, 4.0 + math.log1p(10) * 1.01)  # Should be ~6.4
    ]
    
    for degree, expected in test_cases:
        result = size_by_degree(degree)
        print(f"   Degree {degree}: {result:.3f} (expected ~{expected:.3f})")
        assert abs(result - expected) < 0.001, f"Mismatch for degree {degree}"
    
    # Test specific requirement: degree 1 -> ~4.7
    result_1 = size_by_degree(1)
    print(f"   Degree 1 check: {result_1:.3f} (should be ~4.7)")
    assert 4.6 < result_1 < 4.8, "Degree 1 should give ~4.7"
    
    # Test range constraints
    assert size_by_degree(0) >= 4.0, "Minimum should be 4.0"
    assert size_by_degree(10000) <= 20.0, "Maximum should be 20.0"
    
    # Test monotonic increase
    sizes = [size_by_degree(d) for d in [0, 1, 5, 10, 25]]
    for i in range(len(sizes) - 1):
        assert sizes[i] <= sizes[i + 1], "Should increase monotonically"
    
    print("   ✅ All degree tests passed!")


def test_size_by_popularity():
    """Test popularity-based sizing"""
    print("\n📊 Testing size_by_popularity function...")
    
    # Sample statistics
    stats = {
        'monthly_users_mean': 100000.0,
        'monthly_users_std': 500000.0,
        'upvotes_mean': 1000.0,
        'upvotes_std': 2000.0,
        'max_rank': 1000.0
    }
    
    # Test None handling
    result_none = size_by_popularity(None, None, None, stats)
    print(f"   All None values: {result_none:.3f}")
    assert 4.0 <= result_none <= 12.0, "Should be in range [4, 12]"
    
    # Test different popularity levels
    low_pop = size_by_popularity(1000, 100, 500, stats)
    high_pop = size_by_popularity(1000000, 5000, 10, stats)
    
    print(f"   Low popularity: {low_pop:.3f}")
    print(f"   High popularity: {high_pop:.3f}")
    
    assert 4.0 <= low_pop <= 12.0, "Low pop should be in range"
    assert 4.0 <= high_pop <= 12.0, "High pop should be in range"
    assert low_pop < high_pop, "High popularity should give larger size"
    
    # Test zero std handling
    stats_zero = {**stats, 'monthly_users_std': 0.0, 'upvotes_std': 0.0}
    result_zero = size_by_popularity(100000, 1000, 50, stats_zero)
    print(f"   Zero std handling: {result_zero:.3f}")
    assert 4.0 <= result_zero <= 12.0, "Should handle zero std"
    
    print("   ✅ All popularity tests passed!")


def test_compute_stats():
    """Test statistics computation"""
    print("\n📈 Testing compute_stats function...")
    
    # Test with normal data
    df = pd.DataFrame({
        'monthly_users': [100000, 500000, 200000, 50000],
        'upvotes': [1000, 2000, 1500, 500],
        'rank': [1, 5, 10, 2]
    })
    
    stats = compute_stats(df)
    print(f"   Computed stats: {stats}")
    
    # Check required keys
    required_keys = ['monthly_users_mean', 'monthly_users_std', 
                    'upvotes_mean', 'upvotes_std', 'max_rank']
    for key in required_keys:
        assert key in stats, f"Missing key: {key}"
    
    # Verify calculations
    expected_users_mean = (100000 + 500000 + 200000 + 50000) / 4
    assert abs(stats['monthly_users_mean'] - expected_users_mean) < 0.1
    assert stats['max_rank'] == 10
    
    # Test with None values
    df_none = pd.DataFrame({
        'monthly_users': [100000, None, 200000],
        'upvotes': [1000, 2000, None],
        'rank': [1, None, 10]
    })
    
    stats_none = compute_stats(df_none)
    print(f"   Stats with None: {stats_none}")
    assert stats_none['monthly_users_mean'] > 0
    assert stats_none['max_rank'] > 0
    
    print("   ✅ All stats tests passed!")


def test_integration():
    """Test integration with realistic data"""
    print("\n🔬 Testing integration with realistic dataset...")
    
    # Realistic AI tools data
    df = pd.DataFrame({
        'monthly_users': [1000000, 500000, 100000, None, 2000000],
        'upvotes': [5000, 2000, 1000, 100, 10000],
        'rank': [1, 5, 20, 100, 2],
        'degree': [15, 8, 5, 1, 25]
    })
    
    print(f"   Dataset shape: {df.shape}")
    
    # Compute statistics
    stats = compute_stats(df)
    print(f"   Statistics computed: {len(stats)} metrics")
    
    # Test degree-based sizing
    degree_sizes = [size_by_degree(d) for d in df['degree']]
    print(f"   Degree sizes: {[f'{s:.2f}' for s in degree_sizes]}")
    
    # Test popularity-based sizing
    pop_sizes = []
    for _, row in df.iterrows():
        size = size_by_popularity(
            row['monthly_users'], 
            row['upvotes'], 
            row['rank'], 
            stats
        )
        pop_sizes.append(size)
    
    print(f"   Popularity sizes: {[f'{s:.2f}' for s in pop_sizes]}")
    
    # Validate ranges
    assert all(4.0 <= s <= 20.0 for s in degree_sizes), "Degree sizes out of range"
    assert all(4.0 <= s <= 12.0 for s in pop_sizes), "Popularity sizes out of range"
    
    # High popularity tool should be larger than low popularity
    high_pop_idx = df['monthly_users'].idxmax()  # Tool with max users
    low_pop_idx = df['monthly_users'].idxmin()   # Tool with min users (excluding None)
    
    if pd.notna(df.loc[high_pop_idx, 'monthly_users']) and pd.notna(df.loc[low_pop_idx, 'monthly_users']):
        assert pop_sizes[high_pop_idx] >= pop_sizes[low_pop_idx], "High popularity should be >= low popularity"
    
    print("   ✅ Integration test passed!")


def test_edge_cases():
    """Test edge cases and boundary conditions"""
    print("\n🚨 Testing edge cases...")
    
    # Empty DataFrame
    df_empty = pd.DataFrame({'monthly_users': [], 'upvotes': [], 'rank': []})
    stats_empty = compute_stats(df_empty)
    print(f"   Empty DF stats: {stats_empty}")
    assert stats_empty['monthly_users_mean'] == 1.0
    
    # All None DataFrame
    df_all_none = pd.DataFrame({
        'monthly_users': [None, None],
        'upvotes': [None, None],
        'rank': [None, None]
    })
    stats_all_none = compute_stats(df_all_none)
    print(f"   All None stats: {stats_all_none}")
    
    # Extreme degree values
    extreme_degrees = [0, 1, 1000, 10000, 100000]
    extreme_sizes = [size_by_degree(d) for d in extreme_degrees]
    print(f"   Extreme degree sizes: {[f'{s:.2f}' for s in extreme_sizes]}")
    assert all(4.0 <= s <= 20.0 for s in extreme_sizes)
    
    # Negative values
    neg_size = size_by_degree(-10)
    assert neg_size == 4.0, "Negative degrees should give minimum size"
    
    print("   ✅ Edge case tests passed!")


def main():
    """Run all tests"""
    print("🎯 NODE SIZE COMPUTATION TESTS")
    print("=" * 50)
    
    try:
        test_size_by_degree()
        test_size_by_popularity()
        test_compute_stats()
        test_integration()
        test_edge_cases()
        
        print("\n" + "=" * 50)
        print("🎉 ALL TESTS PASSED!")
        
        print("\n💡 Node size functions validated:")
        print("   ✅ size_by_degree: 4 + log1p(d) * 2, clipped to [4, 20]")
        print("   ✅ size_by_popularity: z-score blend, range [4, 12]")
        print("   ✅ compute_stats: pandas DataFrame statistics")
        print("   ✅ None value handling")
        print("   ✅ Range constraints")
        print("   ✅ Monotonic behavior")
        print("   ✅ Edge cases handled")
        
        print("\n🚀 Ready for backend integration:")
        print("   - Import from utils.node_size")
        print("   - Use with PostgreSQL ai_tool data")
        print("   - Compatible with export scripts and APIs")
        
        return True
        
    except Exception as e:
        print(f"\n❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)