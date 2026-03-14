#!/usr/bin/env python
"""Test pipeline initialization"""

try:
    print("Initializing config...")
    from src.utils import get_logger, set_seed, get_default_config
    
    set_seed(42)
    config = get_default_config()
    print(f"✓ Config initialized: {type(config)}")
    
    print("\nImporting CloudFailurePredictor...")
    from run import CloudFailurePredictor
    
    print("Initializing CloudFailurePredictor...")
    predictor = CloudFailurePredictor(config)
    print("✓ CloudFailurePredictor initialized successfully!")
    
    print("\nStarting pipeline...")
    predictor.run()
    print("✓ Pipeline completed successfully!")
    
except Exception as e:
    print(f"\n✗ Error: {e}")
    import traceback
    traceback.print_exc()
