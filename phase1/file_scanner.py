"""
File Scanner for C++ Header Files
Scans a directory and finds all C++ header files (.h, .hpp)
"""

import os
from pathlib import Path
from typing import List, Dict


def find_header_files(directory: str, exclude_dirs: List[str] = None) -> List[Dict[str, str]]:
    """
    Find all C++ header files in the given directory.
    
    Args:
        directory: Root directory to scan
        exclude_dirs: List of directory names to exclude (e.g., ['build', '.git'])
    
    Returns:
        List of dictionaries with 'path' and 'relative_path' for each header file
    """
    if exclude_dirs is None:
        exclude_dirs = ['.git', 'build', 'cmake-build', 'node_modules', 
                       'venv', '__pycache__', '.vscode', '.idea']
    
    header_files = []
    directory_path = Path(directory)
    
    if not directory_path.exists():
        raise ValueError(f"Directory does not exist: {directory}")
    
    # Header file extensions
    header_extensions = {'.h', '.hpp', '.hxx', '.hh'}
    
    for root, dirs, files in os.walk(directory):
        # Skip excluded directories
        dirs[:] = [d for d in dirs if d not in exclude_dirs]
        
        for file in files:
            file_path = Path(root) / file
            if file_path.suffix in header_extensions:
                relative_path = file_path.relative_to(directory_path)
                header_files.append({
                    'path': str(file_path),
                    'relative_path': str(relative_path),
                    'filename': file
                })
    
    return sorted(header_files, key=lambda x: x['relative_path'])


def get_file_content(file_path: str) -> str:
    """Read the content of a file."""
    try:
        with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
            return f.read()
    except Exception as e:
        print(f"Error reading file {file_path}: {e}")
        return ""


if __name__ == "__main__":
    # Test the scanner
    import sys
    
    if len(sys.argv) > 1:
        test_dir = sys.argv[1]
    else:
        test_dir = "."
    
    print(f"Scanning directory: {test_dir}")
    files = find_header_files(test_dir)
    print(f"\nFound {len(files)} header files:")
    for f in files[:10]:  # Show first 10
        print(f"  - {f['relative_path']}")
    if len(files) > 10:
        print(f"  ... and {len(files) - 10} more")

