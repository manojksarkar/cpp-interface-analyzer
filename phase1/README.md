# Phase 1: C++ Interface Analyzer - Basic MVP

## 🎯 Overview

Phase 1 provides a basic interface analyzer that:
- Scans C++ header files (.h, .hpp)
- Extracts basic interface information (class/struct names, method counts)
- Uses LLM to enhance descriptions
- Generates a markdown table

## 📋 Features

✅ **File Scanner** - Finds all C++ header files in a project  
✅ **Basic Parser** - Extracts class/struct definitions and method counts  
✅ **LLM Enhancement** - Uses local (Ollama) or cloud (OpenAI) LLM to improve descriptions  
✅ **Table Generator** - Creates markdown table with interface information  

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r ../requirements.txt
```

### 2. Set Up LLM (Choose One)

#### Option A: Local LLM (Ollama) - Recommended

1. Install Ollama: https://ollama.ai
2. Pull a model:
   ```bash
   ollama pull llama3.2
   ```
3. Start Ollama (if not running):
   ```bash
   ollama serve
   ```

#### Option B: Cloud LLM (OpenAI)

1. Get API key from https://platform.openai.com
2. Create `.env` file:
   ```
   OPENAI_API_KEY=your_key_here
   ```

### 3. Run the Analyzer

```bash
# Analyze a project (using local Ollama)
python analyzer.py /path/to/cpp/project

# Use cloud LLM instead
python analyzer.py /path/to/cpp/project --cloud

# Limit number of files analyzed
python analyzer.py /path/to/cpp/project --max-files 20

# Custom output file
python analyzer.py /path/to/cpp/project -o my_interfaces.md
```

## 📁 Project Structure

```
phase1/
├── analyzer.py          # Main orchestrator script
├── file_scanner.py      # Finds C++ header files
├── basic_parser.py      # Extracts basic interface info
├── llm_agent.py         # LLM integration for descriptions
├── table_generator.py   # Generates markdown table
└── README.md           # This file
```

## 📊 Output Format

The analyzer generates a markdown table with:

| Interface Name | File | Namespace | Type | Public Methods | Description |
|---------------|------|-----------|------|----------------|-------------|

Plus summary statistics by type and namespace.

## 🧪 Testing

### Test with Sample Code

Create a test header file:

```cpp
// test.h
namespace hal {
    /**
     * UART Driver Interface
     */
    class UartDriver {
    public:
        void init();
        void send(uint8_t data);
        bool isReady();
    };
}
```

Run:
```bash
python analyzer.py . --max-files 1
```

### Test with Open Source Projects

See `../TEST_PROJECTS.md` for recommended test projects.

**Recommended for Phase 1:**
- STM32 HAL Examples
- Arduino ESP32 Core

## ⚙️ Configuration

### Environment Variables

Create a `.env` file in the project root:

```bash
# For local LLM (Ollama)
OLLAMA_MODEL=llama3.2
OLLAMA_BASE_URL=http://localhost:11434

# For cloud LLM (OpenAI)
OPENAI_API_KEY=your_key_here
OPENAI_MODEL=gpt-4o-mini
```

### Command Line Options

```bash
python analyzer.py <project_path> [options]

Options:
  -o, --output FILE     Output markdown file (default: interfaces_table.md)
  --cloud              Use cloud LLM (OpenAI) instead of local (Ollama)
  --max-files N        Maximum number of files to analyze
  --exclude DIR ...    Additional directories to exclude
```

## 🔧 Troubleshooting

### Ollama Connection Error

```
Error connecting to Ollama: ...
```

**Solution:**
1. Make sure Ollama is running: `ollama serve`
2. Check if model is installed: `ollama list`
3. Pull the model: `ollama pull llama3.2`

### OpenAI API Error

```
OPENAI_API_KEY not found
```

**Solution:**
1. Create `.env` file with your API key
2. Or set environment variable: `export OPENAI_API_KEY=your_key`

### No Interfaces Found

**Possible causes:**
- No header files in the directory
- Files don't contain class/struct definitions
- Parser couldn't match the code style

**Solution:**
- Check if files are in the scanned directory
- Verify files contain C++ class/struct definitions
- Try with a known good project (STM32 HAL)

## 📈 Limitations (Phase 1)

- ⚠️ Basic parsing (regex-based, not full AST)
- ⚠️ Simple method counting (may not be 100% accurate)
- ⚠️ Limited inheritance detection
- ⚠️ No method signature extraction
- ⚠️ No HAL layer detection

**These will be addressed in Phase 2!**

## 🎯 Next Steps

After Phase 1 works:
1. Test on real firmware projects
2. Refine parser accuracy
3. Move to Phase 2 (AST parsing, HAL detection)

## 📚 See Also

- `../CPP_INTERFACE_ANALYZER_PLAN.md` - Full development plan
- `../TEST_PROJECTS.md` - Recommended test projects
- `../LOCAL_LLM_MULTI_AGENT_GUIDE.md` - LLM setup guide

