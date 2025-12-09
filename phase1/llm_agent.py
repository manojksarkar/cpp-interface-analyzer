"""
LLM Agent for Interface Analysis
Uses LangChain to analyze C++ interfaces with local or cloud LLM.
"""

import os
from typing import Dict, List, Optional
from dotenv import load_dotenv

load_dotenv()

# Try to import LangChain components
try:
    from langchain.llms import Ollama
    from langchain_openai import ChatOpenAI
    from langchain_ollama import ChatOllama
    from langchain.prompts import ChatPromptTemplate
    from langchain.schema import HumanMessage, SystemMessage
    LANGCHAIN_AVAILABLE = True
except ImportError:
    LANGCHAIN_AVAILABLE = False
    print("Warning: LangChain not installed. Install with: pip install langchain langchain-ollama langchain-openai")


def create_llm(local: bool = True, model: str = None):
    """
    Create an LLM instance (local or cloud).
    
    Args:
        local: If True, use Ollama (local). If False, use OpenAI.
        model: Model name (e.g., 'llama3.2' for Ollama, 'gpt-4' for OpenAI)
    
    Returns:
        LLM instance
    """
    if not LANGCHAIN_AVAILABLE:
        raise ImportError("LangChain is required. Install with: pip install langchain langchain-ollama langchain-openai")
    
    if local:
        # Use Ollama (local)
        model_name = model or os.getenv("OLLAMA_MODEL", "llama3.2")
        base_url = os.getenv("OLLAMA_BASE_URL", "http://localhost:11434")
        
        try:
            return ChatOllama(
                model=model_name,
                base_url=base_url,
                temperature=0.1
            )
        except Exception as e:
            print(f"Error connecting to Ollama: {e}")
            print("Make sure Ollama is running: ollama serve")
            raise
    else:
        # Use OpenAI (cloud)
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY not found in environment variables")
        
        model_name = model or os.getenv("OPENAI_MODEL", "gpt-4o-mini")
        return ChatOpenAI(
            model=model_name,
            api_key=api_key,
            temperature=0.1
        )


def enhance_interface_description(interface: Dict, file_content: str, llm) -> str:
    """
    Use LLM to enhance the description of an interface.
    
    Args:
        interface: Dictionary with interface information
        file_content: Full content of the header file
        llm: LLM instance
    
    Returns:
        Enhanced description
    """
    if not LANGCHAIN_AVAILABLE:
        return interface.get('description', 'No description available')
    
    # Extract context around the interface
    start = interface.get('start_pos', 0)
    end = interface.get('end_pos', len(file_content))
    context = file_content[max(0, start - 200):min(len(file_content), end + 200)]
    
    prompt = f"""Analyze this C++ interface and provide a brief, clear description (1-2 sentences).

Interface: {interface['type']} {interface['name']}
Context:
```cpp
{context}
```

Provide a concise description of what this interface does and its purpose. 
If it's a firmware/HAL interface, mention the hardware peripheral or functionality.
Keep it brief (max 100 words)."""

    try:
        response = llm.invoke(prompt)
        if hasattr(response, 'content'):
            return response.content.strip()
        return str(response).strip()
    except Exception as e:
        print(f"Error enhancing description: {e}")
        return interface.get('description', 'No description available')


def analyze_interfaces(parsed_data: Dict, file_content: str, use_local: bool = True) -> Dict:
    """
    Analyze interfaces using LLM to enhance descriptions.
    
    Args:
        parsed_data: Parsed interface data from basic_parser
        file_content: Full content of the header file
        use_local: Whether to use local LLM (Ollama) or cloud (OpenAI)
    
    Returns:
        Enhanced parsed data with improved descriptions
    """
    if not LANGCHAIN_AVAILABLE:
        print("LangChain not available, using basic descriptions only")
        return parsed_data
    
    try:
        llm = create_llm(local=use_local)
    except Exception as e:
        print(f"Could not create LLM: {e}")
        print("Using basic descriptions only")
        return parsed_data
    
    # Enhance descriptions for each interface
    enhanced_interfaces = []
    for interface in parsed_data['interfaces']:
        enhanced_desc = enhance_interface_description(interface, file_content, llm)
        interface['description'] = enhanced_desc or interface.get('description', 'No description')
        enhanced_interfaces.append(interface)
    
    parsed_data['interfaces'] = enhanced_interfaces
    return parsed_data


if __name__ == "__main__":
    # Test the LLM agent
    test_interface = {
        'name': 'UartDriver',
        'type': 'class',
        'public_method_count': 3,
        'description': 'UART driver',
        'start_pos': 0,
        'end_pos': 100
    }
    
    test_content = """
    class UartDriver {
    public:
        void init(uint32_t baudrate);
        void send(uint8_t data);
        bool isReady();
    };
    """
    
    print("Testing LLM agent...")
    try:
        result = analyze_interfaces({
            'interfaces': [test_interface],
            'file_path': 'test.h'
        }, test_content, use_local=True)
        print("Enhanced description:", result['interfaces'][0]['description'])
    except Exception as e:
        print(f"Error: {e}")

