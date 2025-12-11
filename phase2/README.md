# Phase 2: AST-Based C++ Interface Analyzer

Phase 2 upgrades the analyzer to use true AST parsing via libclang to extract ALL C++ interface details—class names, methods, inheritance, types, etc.—direct from code, not just comments!

---

## 🚀 Quick Start

### 1. **Install dependencies**

```bash
pip install -r ../requirements.txt
# Phase 2 requirements:
pip install libclang tree-sitter tree-sitter-cpp
```

You may also need to install LLVM/Clang system library (so libclang can load). On Ubuntu:
```bash
sudo apt install libclang-16-dev clang-16
```
On Windows, download the "LLVM for Windows" installer.

### 2. **Analyze a project**

```bash
python analyzer.py /path/to/header/files --max 10
```

**Example:** (assuming STM32CubeF4 is cloned next to analyzer)
```bash
python analyzer.py ../../STM32CubeF4/Drivers/STM32F4xx_HAL_Driver/Inc --max 10
```
Output is a table of ALL classes/interfaces found, with public methods, inheritance, file, line, etc.

---

## 📋 What Phase 2 Extracts
- Class/struct/interface names
- Namespace path
- Inheritance (base classes)
- All methods: name, full signature, access (public/protected/private), virtual/pure/static/const
- Source file and line number

**Table Fields:**
| Name | Namespace | Kind | Bases | Methods | Virtual | Pure | File | Line |

---

## 🆚  What’s New vs Phase 1
- ✅ Real C++ parsing (not regex!)
- ✅ Accurate class/method extraction—even without comments
- ✅ Finds inheritance, templates, C++11 features, etc.
- ✅ Output not limited by formatting or missing comments

---

## 🛠️ Troubleshooting libclang
- If you see `libclang cannot be found`, set the env: `export LIBCLANG_PATH=/path/to/libclang.so`
- On Windows, point to `libclang.dll` (in `C:\Program Files\LLVM\bin`)
- You can add more paths to `ast_parser.py` as needed

---

## 💪 Power Moves
- Switch output to CSV/JSON (update `table_generator.py`)
- Add filtering by access (only public API, etc)
- Support export for diagrams, code intelligence tools, etc.

---

## 📚 See Also
- [LLVM/Clang download](https://releases.llvm.org/download.html)
- [libclang Python docs](https://pypi.org/project/libclang/)
