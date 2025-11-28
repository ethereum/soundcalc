from __future__ import annotations
import argparse

from .main import main

if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="soundcalc - Analyze zkVM security levels"
    )
    parser.add_argument(
        "--print-only",
        nargs="+",
        help="Only print specified zkVMs to console (e.g., --print-only ZisK Miden)",
        default=None,
    )
    
    args = parser.parse_args()
    main(print_only=args.print_only)



