# Self-Improve-Swarms

A self-improving AI system that autonomously creates, tests, and refines its own toolkit of Python functions through reflection and continuous learning.

## Overview

Self-Improve-Swarms is an experimental AI system that demonstrates autonomous self-improvement capabilities. The system uses large language models (LLMs) to:

1. **Reflect** on its current capabilities and limitations
2. **Plan** new tools to address identified gaps
3. **Implement** these tools with proper error handling and documentation
4. **Test** the new tools to ensure they work correctly
5. **Integrate** successful tools into its growing toolkit

The system maintains persistent memory of its reflections and continuously expands its capabilities over time without human intervention.

## Features

- **Autonomous Tool Creation**: Creates new Python functions based on identified needs
- **Self-Reflection**: Analyzes its own capabilities to identify gaps and improvement opportunities
- **Persistent Memory**: Maintains a history of reflections and tools across sessions
- **Robust Testing**: Automatically tests new tools with appropriate inputs based on type hints
- **Error Handling**: Attempts to fix implementation errors using LLM-based code correction
- **Documentation Generation**: Creates and maintains documentation for all tools

## Getting Started

### Prerequisites

- Python 3.8+
- OpenAI API key

### Installation

1. Clone the repository:
   ```
   git clone https://github.com/peytontolbert/tiny-self-improve-ai.git
   cd tiny-self-improve-ai
   ```

2. Install dependencies:
   ```
   pip install openai pyyaml python-dotenv
   ```

3. Create a `.env` file with your OpenAI API key:
   ```
   OPENAI_API_KEY=your_api_key_here
   ```

### Usage

Run the main script to start the continuous self-improvement process:

```
python main.py
```

The system will:
1. Load existing tools from `tools.json` (or create initial tools if none exist)
2. Begin cycles of reflection, planning, and implementation
3. Log its progress to `swarm.log` and the console
4. Save new tools to `tools.json` and update `tools_documentation.md`

## System Architecture

The system consists of two main components:

1. **SelfImprovingSwarm**: Manages the toolkit of functions and handles tool creation, testing, and storage
2. **InternalMonologue**: Provides reflection capabilities, allowing the system to analyze its current state and plan improvements

### Key Files

- `main.py`: The main script containing the SelfImprovingSwarm and InternalMonologue classes
- `tools.json`: Persistent storage for all created tools
- `swarm_memory.json`: Storage for the system's reflections and thoughts
- `tools_documentation.md`: Human-readable documentation of all tools
- `swarm.log`: Detailed logging of the system's activities

## How It Works

1. **Reflection Phase**: The system analyzes its current toolkit to identify strengths, weaknesses, and missing capabilities
2. **Planning Phase**: Based on reflection, it creates a detailed plan for a new tool, including functionality, inputs/outputs, and implementation steps
3. **Implementation Phase**: The system generates code for the planned tool using an LLM
4. **Testing Phase**: The new tool is tested with various inputs to ensure it works correctly
5. **Integration Phase**: If tests pass, the tool is added to the toolkit; if not, the system attempts to fix any errors

## Example Tools

The system has created a diverse range of tools across categories including:
- String manipulation
- Mathematical operations
- Data processing
- File operations
- Validation utilities
- Text analysis

## Limitations and Future Work

- Currently relies on OpenAI's API for all LLM interactions
- Limited to creating Python functions without external dependencies
- No ability to modify existing tools, only create new ones
- Future work could include:
  - Support for multiple LLM providers
  - Ability to refactor and improve existing tools
  - Creation of more complex tools with external dependencies
  - Integration with other systems for practical applications

## License

[MIT License](LICENSE)

## Acknowledgments

- This project uses OpenAI's API for language model capabilities
- Inspired by research in autonomous AI systems and self-improving algorithms 