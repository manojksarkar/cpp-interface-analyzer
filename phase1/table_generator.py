"""
Table Generator for Interface Analysis Results
Generates markdown tables from parsed interface data.
"""

from typing import List, Dict
from datetime import datetime


def generate_markdown_table(interfaces_data: List[Dict], output_file: str = None) -> str:
    """
    Generate a markdown table from interface analysis results.
    
    Args:
        interfaces_data: List of parsed file data (from basic_parser + llm_agent)
        output_file: Optional file path to write the table
    
    Returns:
        Markdown table as string
    """
    # Collect all interfaces from all files
    all_interfaces = []
    
    for file_data in interfaces_data:
        file_path = file_data.get('file_path', 'unknown')
        namespace = file_data.get('namespace', '')
        
        for interface in file_data.get('interfaces', []):
            all_interfaces.append({
                'name': interface.get('name', 'Unknown'),
                'file': file_path,
                'namespace': namespace or 'global',
                'type': interface.get('type', 'class'),
                'methods': interface.get('public_method_count', 0),
                'description': interface.get('description', 'No description')
            })
    
    # Generate table
    table_lines = []
    
    # Header
    table_lines.append("# C++ Interface Analysis Report")
    table_lines.append(f"\nGenerated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    table_lines.append(f"\nTotal Interfaces Found: {len(all_interfaces)}\n")
    
    # Table header
    table_lines.append("| Interface Name | File | Namespace | Type | Public Methods | Description |")
    table_lines.append("|---------------|------|-----------|------|----------------|-------------|")
    
    # Table rows
    for interface in all_interfaces:
        # Escape pipe characters in description
        desc = interface['description'].replace('|', '\\|')
        # Truncate long descriptions
        if len(desc) > 100:
            desc = desc[:97] + "..."
        
        # Truncate long file paths
        file_path = interface['file']
        if len(file_path) > 50:
            file_path = "..." + file_path[-47:]
        
        table_lines.append(
            f"| {interface['name']} | {file_path} | {interface['namespace']} | "
            f"{interface['type']} | {interface['methods']} | {desc} |"
        )
    
    # Summary section
    table_lines.append("\n## Summary")
    table_lines.append(f"- **Total Interfaces:** {len(all_interfaces)}")
    
    # Count by type
    type_counts = {}
    for interface in all_interfaces:
        interface_type = interface['type']
        type_counts[interface_type] = type_counts.get(interface_type, 0) + 1
    
    table_lines.append("\n### By Type:")
    for interface_type, count in sorted(type_counts.items()):
        table_lines.append(f"- **{interface_type.capitalize()}:** {count}")
    
    # Count by namespace
    namespace_counts = {}
    for interface in all_interfaces:
        namespace = interface['namespace']
        namespace_counts[namespace] = namespace_counts.get(namespace, 0) + 1
    
    if len(namespace_counts) > 1:
        table_lines.append("\n### By Namespace:")
        for namespace, count in sorted(namespace_counts.items()):
            table_lines.append(f"- **{namespace}:** {count}")
    
    markdown_content = '\n'.join(table_lines)
    
    # Write to file if specified
    if output_file:
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(markdown_content)
        print(f"Table written to: {output_file}")
    
    return markdown_content


if __name__ == "__main__":
    # Test the table generator
    test_data = [
        {
            'file_path': 'drivers/uart.h',
            'namespace': 'hal',
            'interfaces': [
                {
                    'name': 'UartDriver',
                    'type': 'class',
                    'public_method_count': 5,
                    'description': 'UART communication driver interface'
                }
            ]
        },
        {
            'file_path': 'hal/spi.h',
            'namespace': 'hal',
            'interfaces': [
                {
                    'name': 'SpiInterface',
                    'type': 'class',
                    'public_method_count': 8,
                    'description': 'SPI interface abstraction layer'
                }
            ]
        }
    ]
    
    table = generate_markdown_table(test_data, 'test_output.md')
    print(table)

