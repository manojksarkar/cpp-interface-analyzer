"""
Phase 2 AST-based Interface Analyzer Orchestrator
Scans provided directory and runs AST extraction to generate documentation table.
"""

import sys
import os
from pathlib import Path
from typing import List
from ast_parser import extract_classes, print_class_table

def find_headers(directory: str, exts=None, exclude_dirs=None) -> List[str]:
    exts = exts or ['.h', '.hpp']
    exclude_dirs = exclude_dirs or {'.git', 'build', 'cmake-build', 'venv', 'output'}
    result = []
    for root, dirs, files in os.walk(directory):
        # Exclude dirs
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        for f in files:
            if any(f.endswith(ext) for ext in exts):
                result.append(os.path.join(root, f))
    return result

def main():
    import argparse
    parser = argparse.ArgumentParser("Phase 2: C++ AST Interface Analyzer")
    parser.add_argument('directory', help="Directory to scan for headers")
    parser.add_argument('-o', '--output', help="Output table file", default="ast_interfaces_table.md")
    parser.add_argument('--max', type=int, default=None, help="Maximum files to analyze")
    args = parser.parse_args()

    files = find_headers(args.directory)
    if args.max:
        files = files[:args.max]
    print(f"Scanning {len(files)} files in {args.directory}")

    all_classes = []
    for i, f in enumerate(files):
        try:
            classes = extract_classes(f)
            print(f"[{i+1}/{len(files)}] {os.path.basename(f)}: found {len(classes)} class/struct")
            all_classes.extend(classes)
        except Exception as e:
            print(f"  Error in {f}: {e}")

    # Print table to stdout
    print_class_table(all_classes)
    # TODO: Call table_generator to save as markdown/csv/json here

if __name__ == "__main__":
    main()
