"""
AST Parser for C++ Interface Extraction using libclang

Parse C++ files to extract class, struct, interface information for documentation and analysis.
"""

import os
import sys
from clang.cindex import Index, CursorKind, Config, AccessSpecifier
from typing import List, Dict

# Attempt to configure libclang location if needed (common defaults)
def try_configure_libclang():
    import platform
    from clang.cindex import Config
    if Config.loaded:
        return
    possible = [
        '/usr/lib/llvm-16/lib/libclang.so', # Ubuntu default
        '/usr/lib/llvm-15/lib/libclang.so',
        '/usr/lib/llvm-14/lib/libclang.so',
        '/usr/local/opt/llvm/lib/libclang.dylib', # Mac
        'C:/Program Files/LLVM/bin/libclang.dll' # Windows LLVM
    ]
    for p in possible:
        if os.path.exists(p):
            Config.set_library_file(p)
            return
try:
    Config.set_library_file(os.environ.get('LIBCLANG_PATH', ''))
except Exception:
    try_configure_libclang()

# Helper for access specifier
ACCESS = {
    AccessSpecifier.PUBLIC: 'public',
    AccessSpecifier.PRIVATE: 'private',
    AccessSpecifier.PROTECTED: 'protected',
    AccessSpecifier.INVALID: 'public',
}


def extract_classes(filename: str, extra_args=None) -> List[Dict]:
    """Parse a header file and return all C++ class/struct/interface info."""
    index = Index.create()
    extra_args = extra_args or ['-std=c++14']  # Add include dirs if needed

    tu = index.parse(filename, args=extra_args)
    results = []

    def visit(node, namespace=''):
        # Only care about classes and structs
        if node.kind in (CursorKind.CLASS_DECL, CursorKind.STRUCT_DECL):
            class_info = {
                'name': node.spelling,
                'namespace': namespace,
                'kind': 'class' if node.kind == CursorKind.CLASS_DECL else 'struct',
                'bases': [],
                'methods': [],
                'file': node.location.file.name if node.location.file else '',
                'line': node.location.line,
            }
            # Inheritance
            for c in node.get_children():
                if c.kind == CursorKind.CXX_BASE_SPECIFIER:
                    class_info['bases'].append(c.spelling)
            # Methods
            for c in node.get_children():
                if c.kind in (CursorKind.CXX_METHOD, CursorKind.CONSTRUCTOR, CursorKind.DESTRUCTOR):
                    method_info = {
                        'name': c.spelling,
                        'signature': c.type.spelling,
                        'access': ACCESS.get(c.access_specifier, 'public'),
                        'is_virtual': c.is_virtual_method(),
                        'is_pure': c.is_pure_virtual_method() if hasattr(c, 'is_pure_virtual_method') else False,
                        'is_static': c.is_static_method() if hasattr(c, 'is_static_method') else False,
                        'is_const': c.type.is_const_qualified() if hasattr(c.type, 'is_const_qualified') else False,
                    }
                    class_info['methods'].append(method_info)
            results.append(class_info)
        # Namespaces
        elif node.kind == CursorKind.NAMESPACE:
            ns = node.spelling if not namespace else namespace + '::' + node.spelling
            for c in node.get_children():
                visit(c, ns)
        # Nested classes
        else:
            for c in node.get_children():
                visit(c, namespace)
    visit(tu.cursor)
    return results


def print_class_table(classes: List[Dict]):
    print("| Name | Namespace | Kind | Bases | Public Methods | Virtual | Pure | File | Line |")
    print("|------|-----------|------|-------|---------------|---------|------|------|------|")
    for cl in classes:
        pub_methods = [m for m in cl['methods'] if m['access'] == 'public']
        is_virtual = any(m['is_virtual'] for m in pub_methods)
        is_pure = any(m['is_pure'] for m in pub_methods)
        bases = ', '.join(cl['bases']) if cl['bases'] else '-'
        pub_sig = '; '.join(f"{m['name']}()" for m in pub_methods)[:60]
        print(f"| {cl['name']} | {cl['namespace'] or '-'} | {cl['kind']} | {bases} | {pub_sig} | {is_virtual} | {is_pure} | {os.path.basename(cl['file'])} | {cl['line']} |")

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser("C++ AST Class Extractor (Phase 2)")
    parser.add_argument('filename', help="Input C++ header file")
    args = parser.parse_args()
    results = extract_classes(args.filename)
    print_class_table(results)
