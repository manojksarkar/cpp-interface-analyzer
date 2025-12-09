"""
Main C++ Interface Analyzer
Orchestrates file scanning, parsing, LLM analysis, and table generation.
"""

import argparse
import sys
from pathlib import Path

# Add phase1 directory to path
sys.path.insert(0, str(Path(__file__).parent))

from file_scanner import find_header_files, get_file_content
from basic_parser import parse_header_file
from llm_agent import analyze_interfaces
from table_generator import generate_markdown_table


def analyze_project(project_path: str, 
                   output_file: str = "interfaces_table.md",
                   use_local_llm: bool = True,
                   max_files: int = None,
                   exclude_dirs: list = None):
    """
    Analyze a C++ project and generate an interface table.
    
    Args:
        project_path: Path to the project directory
        output_file: Output markdown file path
        use_local_llm: Use local Ollama (True) or OpenAI (False)
        max_files: Maximum number of files to analyze (None for all)
        exclude_dirs: Additional directories to exclude
    """
    print("=" * 60)
    print("C++ Interface Analyzer - Phase 1")
    print("=" * 60)
    print(f"\nScanning project: {project_path}")
    
    # Step 1: Find header files
    print("\n[1/4] Scanning for header files...")
    header_files = find_header_files(project_path, exclude_dirs=exclude_dirs)
    
    if not header_files:
        print("❌ No header files found!")
        return
    
    print(f"✅ Found {len(header_files)} header files")
    
    if max_files:
        header_files = header_files[:max_files]
        print(f"   Analyzing first {len(header_files)} files")
    
    # Step 2: Parse files
    print("\n[2/4] Parsing header files...")
    parsed_data_list = []
    
    for i, file_info in enumerate(header_files, 1):
        print(f"   [{i}/{len(header_files)}] {file_info['relative_path']}")
        
        content = get_file_content(file_info['path'])
        if not content:
            continue
        
        try:
            parsed = parse_header_file(file_info['relative_path'], content)
            parsed_data_list.append(parsed)
        except Exception as e:
            print(f"      ⚠️  Error parsing: {e}")
            continue
    
    total_interfaces = sum(d['interface_count'] for d in parsed_data_list)
    print(f"✅ Parsed {len(parsed_data_list)} files, found {total_interfaces} interfaces")
    
    # Step 3: LLM enhancement (optional)
    print("\n[3/4] Enhancing descriptions with LLM...")
    if use_local_llm:
        print("   Using local LLM (Ollama)")
    else:
        print("   Using cloud LLM (OpenAI)")
    
    enhanced_data_list = []
    for i, parsed_data in enumerate(parsed_data_list, 1):
        file_path = parsed_data['file_path']
        print(f"   [{i}/{len(parsed_data_list)}] Enhancing {file_path}")
        
        # Get file content again for LLM analysis
        full_path = None
        for file_info in header_files:
            if file_info['relative_path'] == file_path:
                full_path = file_info['path']
                break
        
        if full_path:
            content = get_file_content(full_path)
            try:
                enhanced = analyze_interfaces(parsed_data, content, use_local=use_local_llm)
                enhanced_data_list.append(enhanced)
            except Exception as e:
                print(f"      ⚠️  LLM error: {e}, using basic descriptions")
                enhanced_data_list.append(parsed_data)
        else:
            enhanced_data_list.append(parsed_data)
    
    print("✅ Enhanced descriptions")
    
    # Step 4: Generate table
    print("\n[4/4] Generating markdown table...")
    table_content = generate_markdown_table(enhanced_data_list, output_file)
    
    print(f"✅ Analysis complete!")
    print(f"\n📊 Results written to: {output_file}")
    print(f"   Total interfaces: {total_interfaces}")
    print("\n" + "=" * 60)


def main():
    parser = argparse.ArgumentParser(
        description="Analyze C++ project interfaces and generate a table"
    )
    parser.add_argument(
        "project_path",
        help="Path to the C++ project directory"
    )
    parser.add_argument(
        "-o", "--output",
        default="interfaces_table.md",
        help="Output markdown file (default: interfaces_table.md)"
    )
    parser.add_argument(
        "--cloud",
        action="store_true",
        help="Use cloud LLM (OpenAI) instead of local (Ollama)"
    )
    parser.add_argument(
        "--max-files",
        type=int,
        help="Maximum number of files to analyze"
    )
    parser.add_argument(
        "--exclude",
        nargs="+",
        help="Additional directories to exclude"
    )
    
    args = parser.parse_args()
    
    # Validate project path
    project_path = Path(args.project_path)
    if not project_path.exists():
        print(f"❌ Error: Project path does not exist: {args.project_path}")
        sys.exit(1)
    
    analyze_project(
        project_path=str(project_path),
        output_file=args.output,
        use_local_llm=not args.cloud,
        max_files=args.max_files,
        exclude_dirs=args.exclude
    )


if __name__ == "__main__":
    main()

