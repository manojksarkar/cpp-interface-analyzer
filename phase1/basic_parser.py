"""
Basic Parser for C++ Interfaces
Extracts basic information from C++ header files using simple parsing.
"""

import re
from typing import List, Dict, Optional


def extract_namespace(content: str) -> Optional[str]:
    """Extract namespace from file content."""
    # Look for namespace declarations
    namespace_pattern = r'namespace\s+([a-zA-Z_][a-zA-Z0-9_]*(?:::[a-zA-Z_][a-zA-Z0-9_]*)*)'
    matches = re.findall(namespace_pattern, content)
    if matches:
        return '::'.join(matches)  # Return nested namespaces
    return None


def extract_classes_and_structs(content: str) -> List[Dict[str, any]]:
    """
    Extract class and struct definitions from C++ code.
    Returns basic information about each interface.
    """
    interfaces = []
    
    # Pattern to match class/struct definitions
    # Matches: class/struct name, inheritance, and basic structure
    pattern = r'(?:class|struct)\s+([a-zA-Z_][a-zA-Z0-9_]*)\s*(?::\s*[^{]*)?\{'
    
    matches = re.finditer(pattern, content, re.MULTILINE)
    
    for match in matches:
        interface_name = match.group(1)
        
        # Count public methods (simple heuristic: count function declarations)
        # Look for public: section and count methods after it
        start_pos = match.end()
        
        # Find the matching closing brace
        brace_count = 1
        end_pos = start_pos
        while end_pos < len(content) and brace_count > 0:
            if content[end_pos] == '{':
                brace_count += 1
            elif content[end_pos] == '}':
                brace_count -= 1
            end_pos += 1
        
        # Extract the class body
        class_body = content[start_pos:end_pos] if end_pos < len(content) else ""
        
        # Count public methods (functions ending with ; or {)
        # This is a simple heuristic - counts function-like declarations
        method_pattern = r'[a-zA-Z_][a-zA-Z0-9_]*\s*\([^)]*\)\s*(?:const)?\s*(?:;|\{)'
        methods = re.findall(method_pattern, class_body)
        public_method_count = len(methods)
        
        # Extract description from comments before the class
        description = extract_description_before_class(content, match.start())
        
        interfaces.append({
            'name': interface_name,
            'type': 'class' if 'class' in match.group(0) else 'struct',
            'public_method_count': public_method_count,
            'description': description,
            'start_pos': match.start(),
            'end_pos': end_pos
        })
    
    return interfaces


def extract_description_before_class(content: str, class_pos: int) -> str:
    """Extract comment-based description before a class definition."""
    # Look backwards from class position for comments
    before_class = content[max(0, class_pos - 500):class_pos]
    
    # Look for Doxygen-style comments or regular comments
    # Pattern for /** ... */ or /// comments
    doxygen_pattern = r'/\*\*\s*(.*?)\s*\*/'
    single_line_pattern = r'///\s*(.*?)(?:\n|$)'
    
    # Try to find the most recent comment block
    doxygen_match = list(re.finditer(doxygen_pattern, before_class, re.DOTALL))
    single_line_matches = list(re.finditer(single_line_pattern, before_class))
    
    description = ""
    
    if doxygen_match:
        # Get the last (most recent) match
        last_match = doxygen_match[-1]
        desc_text = last_match.group(1)
        # Clean up the description
        description = ' '.join(line.strip().lstrip('*').strip() 
                              for line in desc_text.split('\n') 
                              if line.strip())
    elif single_line_matches:
        # Get consecutive single-line comments
        last_match = single_line_matches[-1]
        desc_lines = []
        for match in reversed(single_line_matches):
            if match.end() <= last_match.end():
                line = match.group(1).strip()
                if line:
                    desc_lines.insert(0, line)
        description = ' '.join(desc_lines)
    
    # Limit description length
    if len(description) > 200:
        description = description[:197] + "..."
    
    return description


def parse_header_file(file_path: str, content: str) -> Dict[str, any]:
    """
    Parse a C++ header file and extract interface information.
    
    Returns:
        Dictionary with file info and extracted interfaces
    """
    namespace = extract_namespace(content)
    interfaces = extract_classes_and_structs(content)
    
    return {
        'file_path': file_path,
        'namespace': namespace,
        'interfaces': interfaces,
        'interface_count': len(interfaces)
    }


if __name__ == "__main__":
    # Test the parser
    test_code = """
    /**
     * UART Driver Interface
     * Provides UART communication functionality
     */
    namespace hal {
        class UartDriver {
        public:
            void init();
            void send(uint8_t data);
            bool isReady();
        private:
            void configure();
        };
    }
    """
    
    result = parse_header_file("test.h", test_code)
    print("Parsed result:")
    print(f"Namespace: {result['namespace']}")
    print(f"Interfaces found: {result['interface_count']}")
    for interface in result['interfaces']:
        print(f"\n  {interface['type']} {interface['name']}:")
        print(f"    Methods: {interface['public_method_count']}")
        print(f"    Description: {interface['description']}")

