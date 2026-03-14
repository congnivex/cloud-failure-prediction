#!/usr/bin/env python
"""Test context engine directly"""

import sys
import pandas as pd
import numpy as np

try:
    print("Testing context engine...")
    
    # Create small test dataframe
    data = {
        'time': list(range(100)),
        'task_id': [i // 10 for i in range(100)],
        'job_id': [i // 50 for i in range(100)],
        'cpu_usage_mean': np.random.rand(100),
        'memory_usage_mean': np.random.rand(100),
        'is_failure': np.random.randint(0, 2, 100),
    }
    df = pd.DataFrame(data)
    
    from src.context_engine import ContextEngine
    engine = ContextEngine(n_clusters=3)
    
    print("Generating context...")
    result_df = engine.generate_all_context(df)
    
    print(f"✓ Context engine working! Result shape: {result_df.shape}")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
