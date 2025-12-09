# Quick Start: Testing the C++ Interface Analyzer

## 🎯 Best Repository for Phase 1 Testing

### ⭐ Recommended: STM32 HAL Examples

**Why this is best:**
- ✅ Clean, well-structured interfaces
- ✅ Moderate size (~100-200 header files)
- ✅ Well-documented
- ✅ Perfect for learning firmware patterns
- ✅ Not too overwhelming for initial testing

## 🚀 Quick Test Commands

### Step 1: Clone the Repository (OUTSIDE the project)

**📍 Clone OUTSIDE the `cpp-interface-analyzer` directory** - Keep test repos separate from your analyzer code.

**Recommended structure:**
```
cursor-tests/
├── cpp-interface-analyzer/     ← Your analyzer project
├── STM32CubeF4/                ← Clone test repos here (outside)
└── arduino-esp32/              ← Or here
```

**Commands:**
```bash
# From cursor-tests directory (parent of cpp-interface-analyzer)
cd ~/Desktop/cursor-tests

# Clone STM32 HAL (F4 series - popular and well-maintained)
git clone https://github.com/STMicroelectronics/STM32CubeF4.git

# Or clone a smaller variant (F1 series)
git clone https://github.com/STMicroelectronics/STM32CubeF1.git
```

**Why outside?**
- ✅ Keeps test repos separate from your code
- ✅ Won't be included in your git repository
- ✅ Easy to manage multiple test projects
- ✅ Clean project structure

### Step 2: Run the Analyzer

```bash
# Navigate to analyzer
cd cpp-interface-analyzer/phase1

# Analyze the HAL driver headers (recommended target)
python analyzer.py ../../STM32CubeF4/Drivers/STM32F4xx_HAL_Driver/Inc --max-files 20

# Or analyze the entire Inc directory
python analyzer.py ../../STM32CubeF4/Drivers/STM32F4xx_HAL_Driver/Inc
```

### Step 3: View Results

The analyzer will generate `interfaces_table.md` in the current directory.

## 📁 What to Analyze

### STM32 HAL Structure:
```
STM32CubeF4/
└── Drivers/
    └── STM32F4xx_HAL_Driver/
        └── Inc/                    ← ANALYZE THIS DIRECTORY
            ├── stm32f4xx_hal_uart.h
            ├── stm32f4xx_hal_spi.h
            ├── stm32f4xx_hal_gpio.h
            ├── stm32f4xx_hal_i2c.h
            └── ... (many more)
```

**Recommended command:**
```bash
python analyzer.py ../../STM32CubeF4/Drivers/STM32F4xx_HAL_Driver/Inc --max-files 20
```

## 🔄 Alternative Test Projects

### Option 2: Arduino ESP32 Core (Smaller, Simpler)

```bash
# Clone
git clone https://github.com/espressif/arduino-esp32.git

# Analyze
cd cpp-interface-analyzer/phase1
python analyzer.py ../../arduino-esp32/cores/esp32 --max-files 15
```

### Option 3: ESP-IDF Drivers (More Complex)

```bash
# Clone (large repository)
git clone --depth 1 https://github.com/espressif/esp-idf.git

# Analyze just the driver headers
cd cpp-interface-analyzer/phase1
python analyzer.py ../../esp-idf/components/driver/include/driver --max-files 30
```

## 💡 Testing Tips

1. **Start Small:** Use `--max-files 10` first to test quickly
2. **Check Output:** Review `interfaces_table.md` to see if results look correct
3. **Increment:** Gradually increase file count as you refine
4. **Compare:** Try different projects to see how parser handles different styles

## 📊 Expected Results

After running on STM32 HAL, you should see:
- ✅ Interface names (e.g., `UART_HandleTypeDef`, `SPI_HandleTypeDef`)
- ✅ File locations
- ✅ Namespace information
- ✅ Method counts
- ✅ LLM-enhanced descriptions

## 🐛 Troubleshooting

### If no interfaces found:
- Check that you're pointing to a directory with `.h` files
- Verify the path is correct
- Try with `--max-files 1` to debug

### If LLM errors occur:
- Make sure Ollama is running: `ollama serve`
- Or use `--cloud` flag for OpenAI
- Check `.env` file has API keys if using cloud

## 🎯 Full Test Workflow

```bash
# 1. Navigate to parent directory (cursor-tests)
cd ~/Desktop/cursor-tests

# 2. Clone test repository (OUTSIDE cpp-interface-analyzer)
git clone https://github.com/STMicroelectronics/STM32CubeF4.git

# 3. Navigate to analyzer
cd cpp-interface-analyzer/phase1

# 4. Run analyzer with limited files (quick test)
#    Path: ../../ goes up to cursor-tests, then into STM32CubeF4
python analyzer.py ../../STM32CubeF4/Drivers/STM32F4xx_HAL_Driver/Inc --max-files 10

# 5. Check results
cat interfaces_table.md

# 6. If good, run on more files
python analyzer.py ../../STM32CubeF4/Drivers/STM32F4xx_HAL_Driver/Inc --max-files 50
```

**Directory Structure After Cloning:**
```
cursor-tests/
├── cpp-interface-analyzer/          ← Your analyzer project
│   └── phase1/
│       └── analyzer.py              ← You run this
├── STM32CubeF4/                     ← Cloned test repo (outside)
│   └── Drivers/
│       └── STM32F4xx_HAL_Driver/
│           └── Inc/                  ← Analyzer points here
└── examples/
```

## 📚 More Test Projects

See `TEST_PROJECTS.md` for a complete list of recommended repositories.

---

**Ready to test? Start with STM32 HAL!** 🚀

