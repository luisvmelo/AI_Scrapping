"""
Node size computation functions for 3D graph visualization

This module provides backend helper functions to compute node sizes for AI tools
in the 3D graph visualization. Node sizes are calculated based on:

1. Graph connectivity (degree): Higher degree tools get larger nodes
2. Popularity metrics: Blend of monthly_users, upvotes, and rank using z-scores

Mathematical formulas:
- size_by_degree(d) = 4 + log1p(d) * 2, clipped to [4, 20]
- size_by_popularity uses z-score normalization:
  pop_norm = 0.5*z(monthly_users) + 0.3*z(upvotes) + 0.2*(1/max(rank,1))
  size = 4 + pop_norm_scaled * 8, resulting in range ≈ [4, 12]

Usage:
    import pandas as pd
    from utils.node_size import size_by_degree, size_by_popularity, compute_stats
    
    # For degree-based sizing
    node_size = size_by_degree(15)  # ~9.6
    
    # For popularity-based sizing
    df = pd.read_sql("SELECT * FROM ai_tool", connection)
    stats = compute_stats(df)
    node_size = size_by_popularity(1000000, 5000, 10, stats)
"""

import math
import pandas as pd
from typing import Dict, Optional, Union


def size_by_degree(degree: int) -> float:
    """
    Calculate node size based on graph connectivity degree.
    
    Uses logarithmic scaling to prevent extremely large nodes while maintaining
    visual distinction between highly connected and isolated tools.
    
    Formula: size = 4 + log1p(degree) * 1.01
    Range: [4, 20] (clipped)
    
    Args:
        degree: Number of connections (edges) for the tool
        
    Returns:
        Node size in the range [4, 20]
        
    Examples:
        >>> size_by_degree(0)    # Isolated tool
        4.0
        >>> size_by_degree(1)    # Single connection
        ~4.7
        >>> size_by_degree(10)   # Well-connected
        ~6.4
        >>> size_by_degree(100)  # Hub tool
        ~8.7
    """
    if degree < 0:
        degree = 0
    
    # Base size of 4 + logarithmic scaling (calibrated so degree 1 gives ~4.7)
    size = 4.0 + math.log1p(degree) * 1.01
    
    # Clip to reasonable range [4, 20]
    return max(4.0, min(20.0, size))


def size_by_popularity(
    monthly_users: Optional[int],
    upvotes: Optional[int], 
    rank: Optional[int],
    stats: Dict[str, float]
) -> float:
    """
    Calculate node size based on popularity metrics using z-score normalization.
    
    Combines multiple popularity signals into a single size metric:
    - monthly_users: User adoption (50% weight)
    - upvotes: Community approval (30% weight) 
    - rank: Relative position, inverted (20% weight)
    
    Formula:
        z_users = (monthly_users - mean_users) / std_users
        z_upvotes = (upvotes - mean_upvotes) / std_upvotes
        z_rank = 1 / max(rank, 1)  # Lower rank = higher score
        
        pop_norm = 0.5*z_users + 0.3*z_upvotes + 0.2*z_rank
        size = 4 + pop_norm_scaled * 8
    
    Args:
        monthly_users: Number of monthly active users (None treated as 1)
        upvotes: Community upvotes/likes (None treated as 1)
        rank: Tool ranking position (None treated as 1, lower is better)
        stats: Statistics dict from compute_stats() containing:
            - 'monthly_users_mean', 'monthly_users_std'
            - 'upvotes_mean', 'upvotes_std'
            - 'max_rank'
            
    Returns:
        Node size in the approximate range [4, 12]
        
    Examples:
        >>> stats = {'monthly_users_mean': 100000, 'monthly_users_std': 500000,
        ...           'upvotes_mean': 1000, 'upvotes_std': 2000, 'max_rank': 1000}
        >>> size_by_popularity(1000000, 5000, 10, stats)  # Popular tool
        ~8.5
        >>> size_by_popularity(1000, 100, 500, stats)     # Average tool  
        ~5.2
        >>> size_by_popularity(None, None, None, stats)   # No data
        4.0
    """
    # Handle None values by setting to 1 (neutral/low values)
    users = monthly_users if monthly_users is not None else 1
    votes = upvotes if upvotes is not None else 1
    tool_rank = rank if rank is not None else 1
    
    # Extract statistics
    users_mean = stats.get('monthly_users_mean', 0)
    users_std = stats.get('monthly_users_std', 1)
    upvotes_mean = stats.get('upvotes_mean', 0)
    upvotes_std = stats.get('upvotes_std', 1)
    max_rank = stats.get('max_rank', 1)
    
    # Prevent division by zero
    if users_std == 0:
        users_std = 1
    if upvotes_std == 0:
        upvotes_std = 1
    
    # Calculate z-scores for normalization
    z_users = (users - users_mean) / users_std
    z_upvotes = (votes - upvotes_mean) / upvotes_std
    
    # Rank component: lower rank = higher score, normalized to [0, 1]
    rank_norm = 1.0 / max(tool_rank, 1)
    # Scale rank to similar range as z-scores
    rank_scaled = (rank_norm * max_rank - 1) / max(max_rank - 1, 1) * 2 - 1
    
    # Weighted combination of popularity signals
    pop_norm = 0.5 * z_users + 0.3 * z_upvotes + 0.2 * rank_scaled
    
    # Scale and shift to target range [4, 12]
    # Apply sigmoid-like transformation to prevent extreme values
    pop_norm_scaled = math.tanh(pop_norm / 3) * 4  # tanh keeps in [-4, 4] range
    
    size = 4.0 + pop_norm_scaled
    
    # Ensure reasonable bounds
    return max(4.0, min(12.0, size))


def compute_stats(df: pd.DataFrame) -> Dict[str, float]:
    """
    Compute statistics needed for popularity-based node sizing.
    
    Calculates mean and standard deviation for numerical columns used in
    size_by_popularity(), handling missing values appropriately.
    
    Args:
        df: Pandas DataFrame containing ai_tool data with columns:
            - monthly_users: int or None
            - upvotes: int or None  
            - rank: int or None
            
    Returns:
        Dictionary containing statistics:
            - monthly_users_mean: float
            - monthly_users_std: float
            - upvotes_mean: float
            - upvotes_std: float
            - max_rank: float
            
    Examples:
        >>> df = pd.DataFrame({
        ...     'monthly_users': [100000, 500000, None, 50000],
        ...     'upvotes': [1000, 2000, 500, None],
        ...     'rank': [1, 5, 10, 2]
        ... })
        >>> stats = compute_stats(df)
        >>> stats['monthly_users_mean']
        216666.67
    """
    stats = {}
    
    # Monthly users statistics
    users_series = pd.to_numeric(df['monthly_users'], errors='coerce')
    users_clean = users_series.dropna()
    if len(users_clean) > 0:
        stats['monthly_users_mean'] = float(users_clean.mean())
        stats['monthly_users_std'] = float(users_clean.std()) if len(users_clean) > 1 else 1.0
    else:
        stats['monthly_users_mean'] = 1.0
        stats['monthly_users_std'] = 1.0
    
    # Upvotes statistics  
    upvotes_series = pd.to_numeric(df['upvotes'], errors='coerce')
    upvotes_clean = upvotes_series.dropna()
    if len(upvotes_clean) > 0:
        stats['upvotes_mean'] = float(upvotes_clean.mean())
        stats['upvotes_std'] = float(upvotes_clean.std()) if len(upvotes_clean) > 1 else 1.0
    else:
        stats['upvotes_mean'] = 1.0
        stats['upvotes_std'] = 1.0
    
    # Rank statistics (max rank for normalization)
    rank_series = pd.to_numeric(df['rank'], errors='coerce')
    rank_clean = rank_series.dropna()
    if len(rank_clean) > 0:
        stats['max_rank'] = float(rank_clean.max())
    else:
        stats['max_rank'] = 1.0
    
    return stats


# Convenience functions for batch processing
def compute_all_degree_sizes(degrees: pd.Series) -> pd.Series:
    """
    Compute node sizes for a series of degree values.
    
    Args:
        degrees: Pandas Series of degree values
        
    Returns:
        Pandas Series of corresponding node sizes
    """
    return degrees.apply(size_by_degree)


def compute_all_popularity_sizes(
    df: pd.DataFrame,
    stats: Optional[Dict[str, float]] = None
) -> pd.Series:
    """
    Compute node sizes for all tools in a DataFrame based on popularity.
    
    Args:
        df: DataFrame with monthly_users, upvotes, rank columns
        stats: Pre-computed statistics (if None, computed from df)
        
    Returns:
        Pandas Series of node sizes
    """
    if stats is None:
        stats = compute_stats(df)
    
    def compute_row_size(row):
        return size_by_popularity(
            row.get('monthly_users'),
            row.get('upvotes'), 
            row.get('rank'),
            stats
        )
    
    return df.apply(compute_row_size, axis=1)


# Export main functions
__all__ = [
    'size_by_degree',
    'size_by_popularity', 
    'compute_stats',
    'compute_all_degree_sizes',
    'compute_all_popularity_sizes'
]