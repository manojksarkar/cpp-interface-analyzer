# C++ Interface Analyzer

An agentic system for analyzing C++ firmware projects and generating comprehensive interface documentation tables.

## 🎯 Overview

This project analyzes C++ header files to extract interface information and generate detailed markdown tables. It's designed with firmware/embedded projects in mind, with plans to add hardware-specific analysis in future phases.

## 📋 Current Status: Phase 1 (MVP)

**Phase 1** provides basic interface extraction:
- ✅ Scans C++ header files
- ✅ Extracts class/struct definitions
- ✅ Counts public methods
- ✅ LLM-enhanced descriptions
- ✅ Markdown table generation

## 🚀 Quick Start

### 1. Install Dependencies

```bash
pip install -r ../requirements.txt
```

### 2. Set Up LLM

**Option A: Local (Ollama) - Recommended**
```bash
ollama pull llama3.2
ollama serve
```

**Option B: Cloud (OpenAI)**
```bash
# Create .env file with:
OPENAI_API_KEY=your_key_here
```

### 3. Run Analyzer

```bash
cd phase1
python analyzer.py /path/to/cpp/project
```

## 📁 Project Structure

```
cpp-interface-analyzer/
├── phase1/                      # Phase 1: Basic MVP
│   ├── analyzer.py             # Main orchestrator
│   ├── file_scanner.py         # Finds header files
│   ├── basic_parser.py         # Extracts interfaces
│   ├── llm_agent.py            # LLM integration
│   ├── table_generator.py      # Markdown generation
│   └── README.md               # Phase 1 documentation
├── CPP_INTERFACE_ANALYZER_PLAN.md  # Full development plan
├── TEST_PROJECTS.md            # Recommended test projects
└── README.md                    # This file
```

## 📊 Phases

### Phase 1: Basic MVP ✅
- Basic interface extraction
- Simple markdown table
- LLM-enhanced descriptions

### Phase 2: Enhanced Analysis (Planned)
- AST parsing (libclang)
- HAL layer detection
- Method signature extraction
- Inheritance detection

### Phase 3: Advanced Features (Planned)
- Real-time analysis
- Interrupt safety
- Resource estimation
- Design pattern detection

See `CPP_INTERFACE_ANALYZER_PLAN.md` for detailed roadmap.

## 🧪 Testing

Recommended test projects:
- **STM32 HAL Examples** (best for Phase 1)
- **Arduino ESP32 Core**
- **ESP-IDF Components**

See `TEST_PROJECTS.md` for full list and setup instructions.

## 📖 Documentation

- **Development Plan:** `CPP_INTERFACE_ANALYZER_PLAN.md`
- **Test Projects:** `TEST_PROJECTS.md`
- **Phase 1 Details:** `phase1/README.md`

## 🔧 Usage Examples

```bash
# Basic usage
python phase1/analyzer.py /path/to/project

# Use cloud LLM
python phase1/analyzer.py /path/to/project --cloud

# Limit files for testing
python phase1/analyzer.py /path/to/project --max-files 20

# Custom output
python phase1/analyzer.py /path/to/project -o report.md
```

## 📝 License

This is an educational project for exploring multi-agent systems and code analysis.

