#!/usr/bin/env python
"""Run the full pipeline with error catching"""

import sys
import traceback

if __name__ == "__main__":
    try:
        from run import main
        main()
    except Exception as e:
        print(f"\n{'='*60}")
        print(f"ERROR: {type(e).__name__}: {e}")
        print(f"{'='*60}")
        traceback.print_exc()
        sys.exit(1)
