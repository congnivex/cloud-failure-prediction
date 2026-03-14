#!/usr/bin/env python
"""Quick test with smaller dataset"""

import sys
from pathlib import Path

try:
    print("Starting test with small dataset...")
    
    from src.utils import get_logger, set_seed, get_default_config
    from run import CloudFailurePredictor
    
    set_seed(42)
    config = get_default_config()
    
    # Use much smaller dataset for quick testing
    config.set("n_tasks", 10)
    config.set("n_timestamps", 50)
    
    print("Initializing predictor...")
    predictor = CloudFailurePredictor(config)
    
    print("Running pipeline...")
    predictor.run()
    
    print("✓ Pipeline completed successfully!")
    
except Exception as e:
    print(f"\n{'='*60}")
    print(f"ERROR: {type(e).__name__}: {e}")
    print(f"{'='*60}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
