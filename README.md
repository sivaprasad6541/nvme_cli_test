# C to C++ Conversion Agent

A sophisticated Python-based agent that intelligently converts C projects to modern C++ with AI-powered analysis and validation.

## 🚀 Features

### Core Capabilities
- **Intelligent Code Parsing**: Advanced C code analysis and AST generation
- **Modern C++ Generation**: Converts to C++11/14/17/20/23 standards
- **Smart Memory Management**: Automatic conversion from malloc/free to smart pointers
- **Exception Handling**: Implements modern error handling patterns
- **RAII Implementation**: Resource Acquisition Is Initialization patterns
- **STL Integration**: Replaces C arrays and strings with STL containers

### AI-Powered Analysis
- **LLM Integration**: OpenAI GPT-4 powered suggestions and improvements
- **Code Quality Analysis**: Identifies potential issues and optimizations
- **Best Practices**: Suggests modern C++ idioms and patterns
- **Performance Analysis**: Evaluates conversion impact on performance

### Validation & Quality Assurance
- **Compilation Checking**: Automatic C++ compilation validation
- **Semantic Analysis**: Ensures conversion correctness
- **Performance Comparison**: Analyzes performance implications
- **Best Practices Validation**: Checks adherence to C++ guidelines

### User Experience
- **Interactive Mode**: Guided conversion with user preferences
- **Batch Processing**: Convert entire projects automatically
- **Progress Tracking**: Real-time conversion progress
- **Detailed Reporting**: Comprehensive conversion results and suggestions

## 📦 Installation

### Prerequisites
- Python 3.8 or higher
- C++ compiler (g++, clang++, or MSVC)
- OpenAI API key (optional, for AI features)

### Install from PyPI
```bash
pip install c-to-cpp-converter
```

### Install from Source
```bash
git clone https://github.com/ai-converter/c-to-cpp.git
cd c-to-cpp
pip install -e .
```

## 🛠️ Usage

### Command Line Interface

#### Basic Conversion
```bash
# Convert a single file
python main.py hello.c -o hello_cpp/

# Convert entire project
python main.py ./my_c_project/ -o ./my_cpp_project/
```

#### With AI Analysis
```bash
# Using OpenAI API key
export OPENAI_API_KEY="your-api-key-here"
python main.py ./project/ -o ./converted/ --model gpt-4

# Or pass API key directly
python main.py ./project/ -o ./converted/ --api-key your-key --model gpt-4
```

#### Interactive Mode
```bash
# Interactive conversion with guided setup
python main.py ./project/ --interactive
```

#### Advanced Options
```bash
# Full featured conversion
python main.py ./project/ -o ./converted/ \
  --api-key your-key \
  --model gpt-4 \
  --validate \
  --verbose
```

### Python API

```python
import asyncio
from pathlib import Path
from src.config.settings import Settings
from src.converter.project_converter import ProjectConverter

async def convert_project():
    # Configure settings
    settings = Settings()
    settings.llm_api_key = "your-openai-api-key"
    settings.cpp_standard = "c++17"
    settings.enable_smart_pointers = True
    settings.enable_exceptions = True
    
    # Initialize converter
    converter = ProjectConverter(settings)
    
    # Convert project
    result = await converter.convert_project(
        input_path=Path("./my_c_project"),
        output_path=Path("./my_cpp_project"),
        validate=True
    )
    
    if result.success:
        print(f"✅ Conversion successful!")
        print(f"📁 Output: {result.output_path}")
        for suggestion in result.suggestions:
            print(f"💡 {suggestion}")
    else:
        print("❌ Conversion failed:")
        for error in result.errors:
            print(f"  {error}")

# Run conversion
asyncio.run(convert_project())
```

## ⚙️ Configuration

### Settings File
Create a `settings.json` file for persistent configuration:

```json
{
  "llm_api_key": "your-openai-api-key",
  "llm_model": "gpt-4",
  "cpp_standard": "c++17",
  "enable_smart_pointers": true,
  "enable_exceptions": true,
  "enable_raii": true,
  "compiler_path": "g++",
  "compiler_flags": ["-std=c++17", "-Wall", "-Wextra", "-O2"]
}
```

### Environment Variables
```bash
export OPENAI_API_KEY="your-api-key"
export CPP_COMPILER="g++"
export CPP_STANDARD="c++17"
```

## 🧪 Examples

### Input C Code
```c
// hello.c
#include <stdio.h>
#include <stdlib.h>
#include <string.h>

typedef struct {
    char* name;
    int age;
} Person;

Person* create_person(const char* name, int age) {
    Person* p = (Person*)malloc(sizeof(Person));
    if (!p) return NULL;
    
    p->name = (char*)malloc(strlen(name) + 1);
    if (!p->name) {
        free(p);
        return NULL;
    }
    
    strcpy(p->name, name);
    p->age = age;
    return p;
}

void destroy_person(Person* p) {
    if (p) {
        free(p->name);
        free(p);
    }
}

int main() {
    Person* p = create_person("John", 30);
    if (p) {
        printf("Name: %s, Age: %d\n", p->name, p->age);
        destroy_person(p);
    }
    return 0;
}
```

### Generated C++ Code
```cpp
/**
 * @file hello.cpp
 * @brief Converted from C to C++ using automated conversion tool
 * 
 * Original file: hello.c
 * C++ Standard: c++17
 * Generated with modern C++ features:
 * - Smart pointers: enabled
 * - Exceptions: enabled
 * - RAII: enabled
 */

#include <iostream>
#include <memory>
#include <stdexcept>
#include <string>

class Person {
public:
    std::string name;
    int age;

    // Default constructor
    Person() = default;
    
    // Parameterized constructor
    Person(const std::string& name, int age) : name(name), age(age) {}
    
    // Destructor
    ~Person() = default;
    
    // Copy constructor and assignment operator
    Person(const Person&) = default;
    Person& operator=(const Person&) = default;
    
    // Move constructor and assignment operator
    Person(Person&&) = default;
    Person& operator=(Person&&) = default;
};

std::unique_ptr<Person> create_person(const std::string& name, int age) {
    try {
        return std::make_unique<Person>(name, age);
    } catch (const std::bad_alloc& e) {
        throw std::runtime_error("Failed to create person: memory allocation error");
    }
}

int main() {
    try {
        auto p = create_person("John", 30);
        std::cout << "Name: " << p->name << ", Age: " << p->age << std::endl;
        // Automatic cleanup with smart pointers - no manual delete needed
    } catch (const std::exception& e) {
        std::cerr << "Error: " << e.what() << std::endl;
        return 1;
    }
    
    return 0;
}
```

## 🔧 Advanced Features

### Custom Conversion Rules
```python
# Define custom conversion patterns
from src.generators.cpp_generator import CppGenerator

class CustomCppGenerator(CppGenerator):
    def convert_custom_pattern(self, code):
        # Your custom conversion logic
        return modernized_code
```

### Plugin System
```python
# Create conversion plugins
class MyConversionPlugin:
    def analyze(self, ast):
        # Custom analysis logic
        return suggestions
    
    def generate(self, ast, context):
        # Custom code generation
        return cpp_code
```

## 📊 Validation Reports

The tool generates comprehensive validation reports:

```
🔍 Validation Report
==================
Status: PASSED_WITH_WARNINGS
Compilation: ✅ SUCCESS
Issues Found: 2

⚠️ Issues:
  • Consider using const references for large parameters
  • Use std::string_view for read-only string parameters

💡 Suggestions:
  • Implement move semantics for better performance
  • Use range-based for loops where applicable
  • Consider using std::optional for optional values

📈 Performance Analysis:
  • Memory usage: Potentially improved with RAII
  • Execution time: Similar to original
  • Binary size: May increase due to C++ runtime
```

## 🤝 Contributing

We welcome contributions! Please see our [Contributing Guide](CONTRIBUTING.md) for details.

### Development Setup
```bash
git clone https://github.com/ai-converter/c-to-cpp.git
cd c-to-cpp
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -e .[dev]
```

### Running Tests
```bash
pytest tests/
```

### Code Quality
```bash
# Linting
flake8 src/
black src/

# Type checking
mypy src/
```

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- OpenAI for GPT-4 API
- The C++ standardization committee
- Open source C++ community
- Contributors and testers

## 📞 Support

- 📖 [Documentation](https://c-to-cpp-converter.readthedocs.io/)
- 🐛 [Bug Reports](https://github.com/ai-converter/c-to-cpp/issues)
- 💬 [Discussions](https://github.com/ai-converter/c-to-cpp/discussions)
- 📧 [Email Support](mailto:support@converter.ai)

---

**Built with ❤️ for the C++ community**