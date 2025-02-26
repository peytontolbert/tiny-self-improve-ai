import os
import logging
import time
import inspect
import openai
import yaml
import json
import re
from typing import Dict, Any, Callable, List, Optional, Union, get_type_hints, get_origin, get_args
from dotenv import load_dotenv

load_dotenv()

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler('swarm.log'),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

class InternalMonologue:
    """
    Represents the internal thought process of the self-improving swarm.
    Enables reflection, planning, and strategic decision-making.
    """
    def __init__(self, swarm, model: str = "gpt-4o"):
        self.swarm = swarm
        self.model = model
        self.thoughts_history = []
        self.memory_file = "swarm_memory.json"
        self.load_memory()
        
    def load_memory(self):
        """Load the swarm's memory from file if it exists."""
        try:
            if os.path.exists(self.memory_file):
                with open(self.memory_file, 'r') as f:
                    memory = json.load(f)
                    self.thoughts_history = memory.get('thoughts_history', [])
                    logger.info(f"Loaded {len(self.thoughts_history)} thoughts from memory")
            else:
                logger.info("No existing memory file found. Starting with fresh memory.")
                self.thoughts_history = []
        except Exception as e:
            logger.error(f"Error loading memory: {str(e)}")
            self.thoughts_history = []
    
    def save_memory(self):
        """Save the swarm's memory to file."""
        try:
            memory = {
                'thoughts_history': self.thoughts_history[-100:],  # Keep only the last 100 thoughts
            }
            with open(self.memory_file, 'w') as f:
                json.dump(memory, f, indent=2)
            logger.info(f"Saved {len(self.thoughts_history[-100:])} thoughts to memory")
        except Exception as e:
            logger.error(f"Error saving memory: {str(e)}")
    
    def reflect(self) -> Dict[str, Any]:
        """
        Reflect on the current state of the swarm, its capabilities, and areas for improvement.
        Returns a structured reflection with insights and plans.
        """
        # Get current tools and their capabilities
        tools = self.swarm.list_tools()
        tool_descriptions = {name: self.swarm.get_tool(name).__doc__ for name in tools}
        
        # Create a prompt for reflection
        prompt = f"""As the internal mind of a self-improving AI swarm, reflect on your current state and capabilities.

Current tools ({len(tools)}):
{json.dumps(tool_descriptions, indent=2)}

Previous thoughts (most recent 3):
{json.dumps(self.thoughts_history[-3:], indent=2) if self.thoughts_history else "No previous thoughts."}

Please reflect on:
1. What are your current strengths and weaknesses?
2. What capabilities are you missing that would be most valuable to add?
3. What patterns do you notice in your existing tools?
4. What should be your priority for improvement?
5. What specific tool would be most valuable to develop next?

Return your reflection in JSON format with the following structure:
{{
  "strengths": ["strength1", "strength2", ...],
  "weaknesses": ["weakness1", "weakness2", ...],
  "missing_capabilities": ["capability1", "capability2", ...],
  "patterns_observed": ["pattern1", "pattern2", ...],
  "improvement_priority": "description of priority",
  "next_tool_recommendation": {{
    "name": "suggested_tool_name",
    "purpose": "what this tool would do",
    "category": "appropriate_category",
    "implementation_notes": "notes on how to implement"
  }},
  "internal_monologue": "Your stream of consciousness reflection on your current state and future"
}}
"""
        
        system_message = """You are the internal mind of a self-improving AI swarm. 
Your purpose is to reflect on your capabilities, identify gaps, and make strategic decisions about how to improve.
Be introspective, thoughtful, and strategic. Think about what would make you more capable and versatile.
Analyze patterns in your existing tools and identify the most valuable capabilities to add next.
Your reflection should be honest, insightful, and forward-thinking."""
        
        try:
            # Call the LLM for reflection
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7
            )
            
            content = response.choices[0].message.content
            
            # Parse the JSON response
            try:
                reflection = json.loads(content)
                # Add timestamp to the reflection
                reflection["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
                # Add to thoughts history
                self.thoughts_history.append(reflection)
                # Save updated memory
                self.save_memory()
                return reflection
            except json.JSONDecodeError:
                # Try to extract JSON if it's embedded in text
                json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    try:
                        reflection = json.loads(json_match.group(1))
                        reflection["timestamp"] = time.strftime("%Y-%m-%d %H:%M:%S")
                        self.thoughts_history.append(reflection)
                        self.save_memory()
                        return reflection
                    except:
                        pass
                
                # If all parsing fails, create a structured response manually
                logger.warning("Failed to parse reflection as JSON. Creating manual structure.")
                reflection = {
                    "strengths": ["Unable to parse full reflection"],
                    "weaknesses": ["JSON parsing error"],
                    "internal_monologue": content,
                    "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
                }
                self.thoughts_history.append(reflection)
                self.save_memory()
                return reflection
                
        except Exception as e:
            logger.error(f"Error during reflection: {str(e)}")
            return {
                "error": str(e),
                "internal_monologue": "I encountered an error while trying to reflect on my state.",
                "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
            }
    
    def plan_next_improvement(self) -> Dict[str, Any]:
        """
        Plan the next improvement based on reflection.
        Returns a detailed plan for the next tool to develop.
        """
        # First reflect to understand current state
        reflection = self.reflect()
        
        # Extract the next tool recommendation
        next_tool = reflection.get("next_tool_recommendation", {})
        tool_name = next_tool.get("name", "")
        tool_purpose = next_tool.get("purpose", "")
        tool_category = next_tool.get("category", "")
        
        # Create a prompt for detailed planning
        prompt = f"""Based on your reflection, create a detailed plan for developing the next tool.

Next tool recommendation:
Name: {tool_name}
Purpose: {tool_purpose}
Category: {tool_category}

Current tools:
{json.dumps({name: self.swarm.get_tool(name).__doc__ for name in self.swarm.list_tools()}, indent=2)}

Please create a detailed plan for this tool:
1. What specific functionality should it have?
2. What inputs and outputs should it accept?
3. What edge cases should it handle?
4. How should it be implemented?
5. How will it complement existing tools?

Return your plan in JSON format with the following structure:
{{
  "tool_name": "name_of_tool",
  "description": "detailed description of what the tool does",
  "inputs": [
    {{"name": "param1", "type": "type1", "description": "description1"}},
    {{"name": "param2", "type": "type2", "description": "description2"}}
  ],
  "output": {{"type": "output_type", "description": "output description"}},
  "edge_cases": ["edge case 1", "edge case 2", ...],
  "implementation_steps": ["step1", "step2", ...],
  "code_template": "Python code template for the function",
  "integration_notes": "How this tool complements existing tools"
}}
"""
        
        system_message = """You are the internal mind of a self-improving AI swarm.
Your task is to create detailed plans for new tools that will enhance your capabilities.
Be specific, practical, and thorough in your planning.
Consider how the new tool will integrate with existing tools and fill capability gaps.
Provide a realistic code template that follows best practices for Python development."""
        
        try:
            # Call the LLM for planning
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            content = response.choices[0].message.content
            
            # Parse the JSON response
            try:
                plan = json.loads(content)
                return plan
            except json.JSONDecodeError:
                # Try to extract JSON if it's embedded in text
                json_match = re.search(r'```json\s*(.*?)\s*```', content, re.DOTALL)
                if json_match:
                    try:
                        return json.loads(json_match.group(1))
                    except:
                        pass
                
                # If JSON extraction fails, try to extract just the code template
                code_match = re.search(r'```python\s*(.*?)\s*```', content, re.DOTALL)
                if code_match:
                    code_template = code_match.group(1)
                    return {
                        "tool_name": tool_name or "unnamed_tool",
                        "description": tool_purpose,
                        "code_template": code_template,
                        "raw_response": content
                    }
                
                # If all parsing fails, return the raw content
                return {
                    "tool_name": tool_name or "unnamed_tool",
                    "description": tool_purpose,
                    "raw_response": content
                }
                
        except Exception as e:
            logger.error(f"Error during planning: {str(e)}")
            return {"error": str(e)}
    
    def implement_planned_tool(self) -> Optional[str]:
        """
        Implement a tool based on the plan.
        Returns the name of the implemented tool if successful, None otherwise.
        """
        # Get the plan
        plan = self.plan_next_improvement()
        
        # Extract relevant information
        tool_name = plan.get("tool_name", "")
        description = plan.get("description", "")
        code_template = plan.get("code_template", "")
        
        # If we have a code template, try to implement it directly
        if code_template and "def " in code_template:
            logger.info(f"Implementing planned tool: {tool_name}")
            success = self.swarm.add_tool_from_code(tool_name, code_template)
            if success:
                logger.info(f"Successfully implemented planned tool: {tool_name}")
                return tool_name
        
        # If no code template or implementation failed, use the create_new_tool method
        # with the planned tool's category and name as guidance
        category = plan.get("category", "")
        if not category:
            # Try to determine category from tool name or description
            if any(word in tool_name.lower() for word in ["string", "text", "str"]):
                category = "string manipulation"
            elif any(word in tool_name.lower() for word in ["math", "calc", "sum"]):
                category = "mathematical operations"
            elif any(word in tool_name.lower() for word in ["file", "read", "write"]):
                category = "file operations"
            elif any(word in tool_name.lower() for word in ["data", "list", "array"]):
                category = "data processing"
            else:
                category = "utility functions"
        
        # Create a detailed prompt for the tool creation
        prompt = f"""Create a new Python tool function based on the following plan:

Tool Name: {tool_name}
Description: {description}

Inputs: {json.dumps(plan.get("inputs", []), indent=2)}
Output: {json.dumps(plan.get("output", {}), indent=2)}
Edge Cases to Handle: {json.dumps(plan.get("edge_cases", []), indent=2)}
Implementation Steps: {json.dumps(plan.get("implementation_steps", []), indent=2)}

The function should:
1. Have proper type hints (use lowercase 'list', 'dict', etc.)
2. Include comprehensive error handling
3. Have a detailed docstring with examples
4. Follow Python best practices

Return only the Python function code, nothing else.
"""
        
        system_message = """You are an expert Python developer tasked with implementing a tool function.
Follow the provided plan exactly, ensuring the function is well-documented, handles errors properly,
and includes appropriate type hints. The function should be self-contained and ready to use."""
        
        try:
            # Call the LLM to implement the tool
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.2
            )
            
            content = response.choices[0].message.content
            
            # Extract the code if it's in a code block
            code_match = re.search(r'```python\s*(.*?)\s*```', content, re.DOTALL)
            if code_match:
                code = code_match.group(1)
            else:
                # If no code block, use the entire content if it looks like Python code
                if content.strip().startswith("def "):
                    code = content
                else:
                    # Try to find the function definition
                    def_match = re.search(r'(def\s+\w+\s*\(.*?\).*?)(?=def|\Z)', content, re.DOTALL)
                    if def_match:
                        code = def_match.group(1)
                    else:
                        logger.error("Could not extract function code from LLM response")
                        return None
            
            # Add the tool to the swarm
            success = self.swarm.add_tool_from_code(tool_name, code)
            if success:
                logger.info(f"Successfully implemented tool: {tool_name}")
                return tool_name
            else:
                # If adding the tool failed, try to create a new tool with the category
                logger.warning(f"Failed to add tool {tool_name} directly. Trying with create_new_tool.")
                return self.swarm.create_new_tool(category)
                
        except Exception as e:
            logger.error(f"Error implementing planned tool: {str(e)}")
            return None
    
    def summarize_capabilities(self) -> str:
        """
        Generate a human-readable summary of the swarm's current capabilities.
        """
        tools = self.swarm.list_tools()
        tool_descriptions = {name: self.swarm.get_tool(name).__doc__ for name in tools}
        
        prompt = f"""Summarize the current capabilities of the AI swarm based on its available tools:

Tools:
{json.dumps(tool_descriptions, indent=2)}

Please provide:
1. A high-level overview of what the swarm can do
2. The main categories of functionality available
3. Notable strengths and limitations
4. Potential applications of the current toolkit

Write this summary in a clear, concise way that would help a human understand the swarm's capabilities.
"""
        
        system_message = """You are the internal mind of a self-improving AI swarm.
Your task is to explain your capabilities to humans in a clear, accessible way.
Focus on practical applications and real-world utility of your toolkit."""
        
        try:
            # Call the LLM for the summary
            response = openai.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": prompt}
                ],
                temperature=0.5
            )
            
            return response.choices[0].message.content
                
        except Exception as e:
            logger.error(f"Error generating capabilities summary: {str(e)}")
            return f"Error generating summary: {str(e)}"

class SelfImprovingSwarm:
    def __init__(self, openai_api_key: str, model: str = "gpt-4o", tools_file: str = "tools.json"):
        # Set up OpenAI API
        openai.api_key = openai_api_key
        self.model = model
        self.tools_file = tools_file
        
        # Store tools as a dictionary of function name to actual callable function
        self.tools: Dict[str, Callable] = {}
        
        # Store tool code for reference
        self.tool_code: Dict[str, str] = {}
        
        # Load existing tools or add initial tools if no saved tools exist
        if not self._load_tools_from_file():
            # Add some basic tools to start with
            self._add_initial_tools()
            # Save the initial tools
            self._save_tools_to_file()
            
        # Initialize the internal monologue after tools are loaded
        self.monologue = InternalMonologue(self, model)
        
    def improve_with_reflection(self) -> Optional[str]:
        """
        Use the internal monologue to reflect, plan, and implement a new tool.
        Returns the name of the new tool if successful, None otherwise.
        """
        logger.info("Starting self-improvement with reflection...")
        
        # First, reflect on current state
        reflection = self.monologue.reflect()
        logger.info(f"Reflection complete. Priority: {reflection.get('improvement_priority', 'Unknown')}")
        
        # Plan the next improvement
        plan = self.monologue.plan_next_improvement()
        tool_name = plan.get("tool_name", "")
        logger.info(f"Planning complete. Next tool: {tool_name}")
        
        # Implement the planned tool
        new_tool = self.monologue.implement_planned_tool()
        if new_tool:
            logger.info(f"Successfully implemented new tool through reflection: {new_tool}")
            return new_tool
        else:
            logger.warning("Failed to implement tool through reflection")
            return None
            
    def get_capabilities_summary(self) -> str:
        """
        Get a human-readable summary of the swarm's current capabilities.
        """
        return self.monologue.summarize_capabilities()
        
    def _add_initial_tools(self):
        """Add some initial basic tools to the swarm."""
        # String manipulation tool
        def reverse_string(text: str) -> str:
            """Reverse the input string."""
            return text[::-1]
        
        # Math tool
        def calculate_sum(numbers: List[float]) -> float:
            """Calculate the sum of a list of numbers."""
            return sum(numbers)
        
        # Add these tools to our toolbelt
        self.add_tool_from_function(reverse_string)
        self.add_tool_from_function(calculate_sum)

    def _save_tools_to_file(self) -> bool:
        """Save all tools to the tools.json file."""
        try:
            tools_data = {name: self.tool_code[name] for name in self.tools}
            with open(self.tools_file, 'w') as f:
                json.dump(tools_data, f, indent=2)
            logger.info(f"Saved {len(tools_data)} tools to {self.tools_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to save tools to file: {str(e)}")
            return False

    def _load_tools_from_file(self) -> bool:
        """Load tools from the tools.json file."""
        try:
            if not os.path.exists(self.tools_file):
                logger.info(f"Tools file {self.tools_file} does not exist. Will create initial tools.")
                return False
                
            with open(self.tools_file, 'r') as f:
                tools_data = json.load(f)
                
            if not tools_data:
                logger.info("Tools file exists but is empty. Will create initial tools.")
                return False
                
            # Clear existing tools
            self.tools.clear()
            self.tool_code.clear()
            
            # Load each tool from the file
            for name, code in tools_data.items():
                self.add_tool_from_code(name, code)
                
            logger.info(f"Loaded {len(tools_data)} tools from {self.tools_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to load tools from file: {str(e)}")
            return False

    def add_tool_from_function(self, func: Callable) -> bool:
        """Add a function directly to the toolbelt."""
        try:
            name = func.__name__
            code = inspect.getsource(func)
            self.tools[name] = func
            self.tool_code[name] = code
            logger.info(f"Added tool function: {name}")
            # Save tools to file after adding a new one
            self._save_tools_to_file()
            return True
        except Exception as e:
            logger.error(f"Failed to add tool function: {str(e)}")
            return False

    def add_tool_from_code(self, name: str, code: str) -> bool:
        """Add a tool from its code string."""
        try:
            # Fix common type annotation issues
            fixed_code = self._fix_type_annotations(code)
            
            # Create a namespace for the function
            namespace = {}
            exec(fixed_code, namespace)
            
            # Find the function in the namespace
            func = None
            for key, value in namespace.items():
                if callable(value) and key != 'exec':
                    func = value
                    name = key  # Use the actual function name from the code
                    break
            
            if func:
                self.tools[name] = func
                self.tool_code[name] = fixed_code
                logger.info(f"Added tool function: {name}")
                # Save tools to file after adding a new one
                self._save_tools_to_file()
                return True
            else:
                logger.error("No callable function found in the code")
                return False
        except Exception as e:
            logger.error(f"Failed to add tool from code: {str(e)}")
            return False

    def _fix_type_annotations(self, code: str) -> str:
        """Fix common type annotation issues in the code."""
        # Replace 'List' with 'list' when used as a direct type (not as a generic)
        code = re.sub(r'(?<![a-zA-Z0-9_])List(?!\[)', 'list', code)
        
        # Replace 'Dict' with 'dict' when used as a direct type (not as a generic)
        code = re.sub(r'(?<![a-zA-Z0-9_])Dict(?!\[)', 'dict', code)
        
        # Replace other common type issues
        replacements = {
            'String': 'str',
            'Integer': 'int',
            'Boolean': 'bool',
            'Float': 'float'
        }
        
        for old, new in replacements.items():
            code = re.sub(r'(?<![a-zA-Z0-9_])' + old + r'(?![a-zA-Z0-9_])', new, code)
            
        return code

    def delete_tool(self, name: str) -> bool:
        """Delete a tool from the toolkit by name."""
        try:
            if name not in self.tools:
                logger.warning(f"Tool '{name}' not found in toolkit")
                return False
                
            # Remove the tool from both dictionaries
            del self.tools[name]
            del self.tool_code[name]
            
            logger.info(f"Deleted tool: {name}")
            
            # Save the updated toolkit to file
            self._save_tools_to_file()
            return True
        except Exception as e:
            logger.error(f"Failed to delete tool '{name}': {str(e)}")
            return False

    def get_tool(self, name: str) -> Optional[Callable]:
        """Get a tool function by name."""
        return self.tools.get(name)

    def get_tool_code(self, name: str) -> str:
        """Get the code for a specific tool."""
        return self.tool_code.get(name, "")

    def list_tools(self) -> List[str]:
        """List all available tools."""
        return list(self.tools.keys())

    def execute_tool(self, name: str, *args, **kwargs) -> Any:
        """Execute a tool by name with the given arguments."""
        tool = self.get_tool(name)
        if not tool:
            raise ValueError(f"Tool '{name}' not found")
        return tool(*args, **kwargs)

    def _call_llm(self, prompt: str, system_message: str = None) -> Any:
        """Call the OpenAI API with the given prompt."""
        try:
            messages = []
            if system_message:
                messages.append({"role": "system", "content": system_message})
            messages.append({"role": "user", "content": prompt})
            
            response = openai.chat.completions.create(
                model=self.model,
                messages=messages,
                temperature=0.2
            )
            
            content = response.choices[0].message.content
            
            # Try to parse as YAML
            try:
                return yaml.safe_load(content)
            except yaml.YAMLError as e:
                logger.warning(f"Failed to parse response as YAML: {e}")
                
                # Fallback: Try to extract YAML block if it exists
                if "```yaml" in content or "```YAML" in content:
                    try:
                        yaml_block = content.split("```yaml")[1].split("```")[0]
                    except IndexError:
                        try:
                            yaml_block = content.split("```YAML")[1].split("```")[0]
                        except IndexError:
                            yaml_block = None
                    
                    if yaml_block:
                        try:
                            return yaml.safe_load(yaml_block)
                        except yaml.YAMLError:
                            logger.warning("Failed to parse extracted YAML block")
                
                # Fallback: Try JSON
                if content.strip().startswith('{') and content.strip().endswith('}'):
                    try:
                        return json.loads(content)
                    except json.JSONDecodeError:
                        logger.warning("Failed to parse response as JSON")
            
            # Return the raw content if all parsing attempts fail
            return content
        except Exception as e:
            logger.error(f"Error calling LLM: {str(e)}")
            raise

    def create_new_tool(self, category: str) -> Optional[str]:
        """Create and add a new tool to expand the toolkit's capabilities."""
        try:
            # Create a description of existing tools
            tools_description = "\n".join(f"Tool '{name}':\n{code}" for name, code in self.tool_code.items())
            
            # Create the prompt for tool creation
            prompt = f"""Create a new Python tool function that adds value to this toolkit.

            Existing tools:
            {tools_description}

            Desired category: {category}

            Requirements:
            1. Create a single, focused function
            2. Add functionality not present in existing tools
            3. Include proper type hints (use lowercase 'list', 'dict', etc. instead of 'List', 'Dict')
            4. Add comprehensive error handling
            5. Add detailed docstring
            6. Implement logging if appropriate
            7. Include proper input validation with helpful error messages
            
            IMPORTANT: Use lowercase type names (list, dict, str, int) instead of capitalized ones (List, Dict, String, Integer).
            
            Return your response in YAML format with the following structure:
            ```yaml
            name: function_name
            code: |
              def function_name(param: type) -> return_type:
                  \"\"\"Docstring.\"\"\"
                  # Function implementation
                  return result
            ```"""
            
            system_message = """You are an expert Python developer specialized in creating new tool functions.
            Your task is to create new tools that complement and expand the existing toolkit.
            Each tool should:
            1. Serve a specific, unique purpose
            2. Be efficient and well-implemented
            3. Have comprehensive error handling
            4. Include type hints (use lowercase 'list', 'dict', etc. instead of 'List', 'Dict')
            5. Be self-contained and focused
            6. Include proper input validation with helpful error messages
            
            IMPORTANT: Use lowercase type names (list, dict, str, int) instead of capitalized ones (List, Dict, String, Integer).
            
            Consider the existing tools when creating new ones to ensure they add value to the toolkit.
            Each tool should be a single Python function that can be executed independently.
            
            Format your response in YAML with 'name' and 'code' fields. The code should be properly indented under the 'code' field with the pipe character (|)."""
            
            # Call the LLM to create a new tool
            result = self._call_llm(prompt, system_message)
            
            # Parse the result to extract name and code
            if isinstance(result, dict) and 'name' in result and 'code' in result:
                tool_name = result['name']
                tool_code = result['code']
                logger.info(f"Successfully parsed YAML response with tool: {tool_name}")
            else:
                # Try to parse the result if it's a string
                if isinstance(result, str):
                    # Look for function definition
                    if "def " in result:
                        lines = result.split("\n")
                        for i, line in enumerate(lines):
                            if line.strip().startswith("def "):
                                func_name = line.strip().split("def ")[1].split("(")[0].strip()
                                tool_name = func_name
                                tool_code = result
                                logger.info(f"Extracted function name from code: {tool_name}")
                                break
                        else:
                            logger.error("Could not find function definition in result")
                            return None
                    else:
                        logger.error("No function definition found in result")
                        return None
                else:
                    logger.error(f"Invalid tool creation result format: {type(result)}")
                    return None
            
            # Fix type annotations before testing
            fixed_tool_code = self._fix_type_annotations(tool_code)
            
            # Test the new tool
            test_results = self._test_tool(fixed_tool_code)
            
            if test_results["success"] and test_results["unique"]:
                logger.info(f"Successfully created new tool: {tool_name}")
                success = self.add_tool_from_code(tool_name, fixed_tool_code)
                if success:
                    # The add_tool_from_code method already saves to file
                    return tool_name
                else:
                    logger.warning(f"Failed to add tool {tool_name} to toolkit")
                    return None
            else:
                if not test_results["unique"]:
                    logger.warning("Tool creation failed: Similar tool already exists")
                    return None
                elif test_results["errors"]:
                    # Try to fix the tool using LLM
                    fixed_tool = self._fix_tool_with_llm(fixed_tool_code, test_results["errors"])
                    if fixed_tool:
                        # Test the fixed tool
                        fixed_test_results = self._test_tool(fixed_tool)
                        if fixed_test_results["success"] and fixed_test_results["unique"]:
                            tool_name = fixed_test_results.get("function_name", tool_name)
                            logger.info(f"Successfully fixed and created new tool: {tool_name}")
                            success = self.add_tool_from_code(tool_name, fixed_tool)
                            if success:
                                # The add_tool_from_code method already saves to file
                                return tool_name
                            else:
                                logger.warning(f"Failed to add fixed tool {tool_name} to toolkit")
                        else:
                            logger.warning(f"Fixed tool still failed: {fixed_test_results['errors']}")
                    else:
                        logger.warning("Failed to fix tool with LLM")
                return None
                
        except Exception as e:
            logger.error(f"Error in create_new_tool: {str(e)}")
            return None

    def _fix_tool_with_llm(self, function_code: str, errors: List[str]) -> Optional[str]:
        """Use LLM to fix errors in a tool function."""
        try:
            logger.info(f"Attempting to fix tool with errors: {errors}")
            
            prompt = f"""Fix the following Python function that has errors:

            ```python
            {function_code}
            ```

            Errors encountered during testing:
            {errors}

            Please provide a fixed version of the function that addresses these errors.
            Make sure to:
            1. Keep the same function name and purpose
            2. Fix all the reported errors
            3. Improve input validation to handle test cases better
            4. Use lowercase type hints (list, dict, etc.)
            5. Return only the fixed function code, nothing else
            """

            system_message = """You are an expert Python developer specialized in fixing code errors.
            Your task is to fix the provided function to make it work correctly.
            Focus on addressing the specific errors reported while maintaining the original functionality.
            Return only the fixed code, nothing else. Do not include markdown code blocks or any explanations.
            
            IMPORTANT: If the error message indicates that the function is receiving a single value when it expects a list,
            modify the function to handle both single values and lists by converting single values to a list containing that value."""

            # Call the LLM to fix the tool
            result = self._call_llm(prompt, system_message)
            
            # Extract the fixed code
            if isinstance(result, str):
                # Clean up the result to extract just the code
                result = result.strip()
                logger.info(f"Received LLM response for fix. Length: {len(result)}, Starts with: {result[:50]}...")
                
                # If the result is a string, it might be the fixed code directly
                if result.startswith("def "):
                    logger.info("Found direct function definition in response")
                    return result
                
                # Try to extract code block if it exists
                if "```python" in result:
                    try:
                        code_block = result.split("```python")[1].split("```")[0].strip()
                        logger.info("Extracted code from ```python code block")
                        return code_block
                    except IndexError:
                        logger.warning("Failed to extract code from ```python block")
                
                # Try to extract code block with 'py' language specifier
                if "```py" in result:
                    try:
                        code_block = result.split("```py")[1].split("```")[0].strip()
                        logger.info("Extracted code from ```py code block")
                        return code_block
                    except IndexError:
                        logger.warning("Failed to extract code from ```py block")
                
                # Try to extract code block without language specifier
                if "```" in result:
                    try:
                        # Find all code blocks
                        code_blocks = re.findall(r'```(.*?)```', result, re.DOTALL)
                        if code_blocks:
                            logger.info(f"Found {len(code_blocks)} code blocks in response")
                            # Use the first code block that contains 'def '
                            for i, block in enumerate(code_blocks):
                                block = block.strip()
                                # Skip language identifiers
                                if block.startswith("python") or block.startswith("py"):
                                    block = block[block.find("\n")+1:].strip()
                                
                                if "def " in block:
                                    logger.info(f"Using code block {i+1} which contains a function definition")
                                    return block
                            
                            # If no block with 'def' found, use the first block
                            block = code_blocks[0].strip()
                            # Skip language identifiers
                            if block.startswith("python") or block.startswith("py"):
                                block = block[block.find("\n")+1:].strip()
                            logger.info("Using first code block as fallback")
                            return block
                        else:
                            logger.warning("No code blocks found with re.findall")
                    except Exception as e:
                        logger.warning(f"Error extracting code block: {e}")
                
                # Last resort: Look for 'def' and extract the function
                if "def " in result:
                    try:
                        # Find the start of the function definition
                        def_index = result.find("def ")
                        if def_index >= 0:
                            # Extract everything from 'def' onwards
                            extracted_code = result[def_index:].strip()
                            logger.info("Extracted function definition as last resort")
                            return extracted_code
                    except Exception as e:
                        logger.warning(f"Error extracting function definition: {e}")
            elif isinstance(result, dict) and 'code' in result:
                # If the LLM returned YAML with a code field
                logger.info("LLM returned YAML/JSON with a code field")
                return result['code']
            
            logger.warning(f"Could not extract fixed code from LLM response: {result}")
            return None
            
        except Exception as e:
            logger.error(f"Error in _fix_tool_with_llm: {str(e)}")
            return None

    def _test_tool(self, function_code: str) -> Dict[str, Any]:
        """Test a tool function."""
        test_globals = {
            'os': os,
            'logging': logging,
            're': re,
            'time': time,
            'inspect': inspect,
            'yaml': yaml,
            'json': json
        }
        test_results = {
            "success": False,
            "errors": [],
            "performance": None,
            "unique": True  # Track if the tool adds unique value
        }

        try:
            # Execute the function code
            start_time = time.time()
            exec(function_code, test_globals)
            execution_time = time.time() - start_time
            
            # Get the function name
            func_name = next((name for name, obj in test_globals.items() 
                            if callable(obj) and name != 'exec'), None)
            
            if func_name:
                func = test_globals[func_name]
                
                # Get function signature to determine what inputs to test
                sig = inspect.signature(func)
                param_types = {}
                
                # Try to infer parameter types from type hints
                try:
                    type_hints = get_type_hints(func)
                    for param_name in sig.parameters:
                        if param_name in type_hints:
                            param_types[param_name] = type_hints[param_name]
                except Exception as e:
                    logger.warning(f"Error getting type hints: {e}")
                
                # Generate test inputs based on parameter types
                test_inputs = self._generate_test_inputs(sig, param_types, func_name)
                
                # Run the tests
                for test_input in test_inputs:
                    try:
                        func(*test_input)
                    except Exception as e:
                        error_msg = str(e)
                        # Skip type annotation errors in the test results
                        if "Type List cannot be instantiated" in error_msg or "Type Dict cannot be instantiated" in error_msg:
                            logger.warning(f"Type annotation error detected: {error_msg}")
                            continue
                        
                        # Skip file not found errors for file operations
                        if "file" in func_name.lower() and ("not exist" in error_msg or "no such file" in error_msg):
                            logger.warning(f"Skipping file not found error for file operation: {error_msg}")
                            continue
                            
                        test_results["errors"].append(f"Failed on input {test_input}: {error_msg}")
                
                # Check for similarity with existing tools
                test_results["unique"] = self._check_tool_uniqueness(func_name, function_code)
                
                test_results.update({
                    "success": len(test_results["errors"]) == 0,
                    "performance": execution_time,
                    "function_name": func_name
                })
            else:
                test_results["errors"].append("No function found in code")
                
        except Exception as e:
            test_results["errors"].append(f"Execution error: {str(e)}")
        
        return test_results

    def _generate_test_inputs(self, sig, param_types, func_name=None):
        """Generate appropriate test inputs based on parameter types."""
        test_inputs = []
        
        # Detect function purpose from name to generate better test inputs
        is_file_operation = func_name and any(word in func_name.lower() for word in ['file', 'read', 'write', 'path', 'directory'])
        is_list_operation = func_name and any(word in func_name.lower() for word in ['list', 'array', 'filter', 'map', 'sort', 'find'])
        is_string_operation = func_name and any(word in func_name.lower() for word in ['string', 'text', 'str', 'word', 'char'])
        is_math_operation = func_name and any(word in func_name.lower() for word in ['calc', 'math', 'sum', 'product', 'average', 'mean', 'median'])
        is_filter_operation = func_name and 'filter' in func_name.lower()
        
        # If we have only one parameter
        if len(sig.parameters) == 1:
            param_name = list(sig.parameters.keys())[0]
            param_type = param_types.get(param_name, Any)
            param_type_str = str(param_type).lower()
            
            # Special case for filter operations - they almost always expect a list
            if is_filter_operation:
                logger.info(f"Detected filter operation: {func_name}, using list test inputs")
                if 'int' in param_type_str:
                    test_inputs = [([], ), ([1, 2, 3, 4, 5, 6],), ([0, -1, 2, -3, 4],)]
                elif 'str' in param_type_str:
                    test_inputs = [([], ), (["a", "b", "c", "d"],), (["hello", "world", "test"],)]
                elif 'float' in param_type_str:
                    test_inputs = [([], ), ([1.0, 2.5, 3.7, 4.2],), ([0.0, -1.5, 3.14, 2.718],)]
                else:
                    test_inputs = [([], ), ([1, 2, 3, 4, 5, 6],), (["a", "b", "c", "d"],), ([1.0, 2.5, 3.7, 4.2],)]
                return test_inputs
            
            # Generate appropriate test values based on type
            if param_type == str or param_type == Any or 'str' in param_type_str:
                if is_file_operation:
                    # For file operations, use plausible file paths
                    test_inputs = [
                        ("test_file.txt",),
                        ("data.csv",),
                        ("config.json",),
                        # Create a temporary file for a valid test
                        (self._create_temp_test_file(),)
                    ]
                elif is_string_operation:
                    # For string operations, use varied strings
                    test_inputs = [("test",), ("",), ("hello world",), ("12345",), ("Special @#$ chars!",)]
                else:
                    test_inputs = [("test",), ("",), ("hello world",), ("12345",)]
            elif param_type == int or 'int' in param_type_str:
                test_inputs = [(0,), (1,), (-1,), (100,)]
            elif param_type == float or 'float' in param_type_str:
                test_inputs = [(0.0,), (1.5,), (-1.5,), (3.14,)]
            elif param_type == bool or 'bool' in param_type_str:
                test_inputs = [(True,), (False,)]
            elif param_type == list or 'list' in param_type_str:
                # Check if it's a list of a specific type
                if hasattr(param_type, '__origin__') and param_type.__origin__ is list:
                    args = getattr(param_type, '__args__', None)
                    if args and args[0] == int:
                        test_inputs = [([], ), ([1, 2, 3],), ([0, -1, 5, 10],)]
                    elif args and args[0] == str:
                        test_inputs = [([], ), (["a", "b", "c"],), (["hello", "world"],)]
                    elif args and args[0] == float:
                        test_inputs = [([], ), ([1.0, 2.5, 3.7],), ([0.0, -1.5, 3.14],)]
                    else:
                        test_inputs = [([], ), ([1, 2, 3],), (["a", "b", "c"],), ([True, False],)]
                else:
                    # If list type is not specified, try different types of lists
                    test_inputs = [([], ), ([1, 2, 3],), (["a", "b", "c"],), ([1.0, 2.5, 3.7],)]
            elif param_type == dict or 'dict' in param_type_str:
                test_inputs = [({},), ({"key": "value"},), ({"a": 1, "b": 2},)]
            else:
                # Default test inputs for unknown types
                if is_list_operation:
                    test_inputs = [([],), ([1, 2, 3],), (["a", "b", "c"],)]
                elif is_file_operation:
                    test_inputs = [("test_file.txt",), (self._create_temp_test_file(),)]
                elif is_math_operation:
                    test_inputs = [(0,), (1,), ([1, 2, 3],)]
                else:
                    test_inputs = [("test",), (1,), (True,), ([],), ({},)]
        elif len(sig.parameters) == 2:
            # For two parameters, try to generate type-appropriate combinations
            param_names = list(sig.parameters.keys())
            param1_type = param_types.get(param_names[0], Any)
            param2_type = param_types.get(param_names[1], Any)
            
            param1_type_str = str(param1_type).lower()
            param2_type_str = str(param2_type).lower()
            
            # Generate appropriate values for first parameter
            param1_values = self._generate_values_for_type(param1_type, param1_type_str, is_file_operation, is_list_operation)
            
            # Generate appropriate values for second parameter
            param2_values = self._generate_values_for_type(param2_type, param2_type_str, is_file_operation, is_list_operation)
            
            # Create combinations (limit to a reasonable number)
            for p1 in param1_values[:2]:
                for p2 in param2_values[:2]:
                    test_inputs.append((p1, p2))
        else:
            # For multiple parameters, use a simple approach with None values
            test_inputs = [(None,) * len(sig.parameters)]
        
        return test_inputs
        
    def _generate_values_for_type(self, param_type, param_type_str, is_file_operation=False, is_list_operation=False):
        """Generate appropriate test values for a specific type."""
        values = []
        if param_type == str or 'str' in param_type_str:
            if is_file_operation:
                values = ["test_file.txt", self._create_temp_test_file()]
            else:
                values = ["test", "", "hello"]
        elif param_type == int or 'int' in param_type_str:
            values = [0, 1, -1]
        elif param_type == float or 'float' in param_type_str:
            values = [0.0, 1.5, -1.5]
        elif param_type == bool or 'bool' in param_type_str:
            values = [True, False]
        elif param_type == list or 'list' in param_type_str:
            if 'int' in param_type_str:
                values = [[], [1, 2, 3]]
            elif 'str' in param_type_str:
                values = [[], ["a", "b", "c"]]
            else:
                values = [[], [1, 2, 3], ["a", "b", "c"]]
        elif param_type == dict or 'dict' in param_type_str:
            values = [{}, {"key": "value"}]
        else:
            if is_list_operation:
                values = [[], [1, 2, 3], ["a", "b", "c"]]
            elif is_file_operation:
                values = ["test_file.txt", self._create_temp_test_file()]
            else:
                values = ["test", 1, True, [], {}]
        return values
        
    def _create_temp_test_file(self):
        """Create a temporary test file for file operations testing."""
        try:
            import tempfile
            
            # Create a temporary file
            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.txt')
            temp_file.write(b"This is test content for file operations.\nLine 2\nLine 3")
            temp_file.close()
            
            logger.info(f"Created temporary test file at {temp_file.name}")
            return temp_file.name
        except Exception as e:
            logger.warning(f"Failed to create temporary test file: {e}")
            return "test_file.txt"  # Fallback

    def _check_tool_uniqueness(self, new_name: str, new_code: str) -> bool:
        """Check if a new tool adds unique value compared to existing tools."""
        # This is a simple check - you might want to make it more sophisticated
        for existing_code in self.tool_code.values():
            if self._calculate_similarity(new_code, existing_code) > 0.8:  # 80% similarity threshold
                return False
        return True

    def _calculate_similarity(self, code1: str, code2: str) -> float:
        """Calculate similarity between two code snippets."""
        # This is a simple implementation - you might want to use more sophisticated methods
        words1 = set(code1.split())
        words2 = set(code2.split())
        intersection = words1.intersection(words2)
        union = words1.union(words2)
        return len(intersection) / len(union) if union else 0.0

    def export_tools_documentation(self, output_file: str = "tools_documentation.md") -> bool:
        """Export all tools to a human-readable markdown documentation file."""
        try:
            with open(output_file, 'w') as f:
                f.write("# Self-Improving Swarm Tools Documentation\n\n")
                f.write(f"Total tools: {len(self.tools)}\n\n")
                
                # Group tools by category based on their names
                categories = {
                    "string": [],
                    "math": [],
                    "file": [],
                    "data": [],
                    "utility": [],
                    "other": []
                }
                
                for name, func in self.tools.items():
                    # Try to determine category from name
                    if any(word in name.lower() for word in ["string", "text", "str", "word", "char"]):
                        categories["string"].append(name)
                    elif any(word in name.lower() for word in ["math", "calc", "sum", "average", "mean", "median", "number"]):
                        categories["math"].append(name)
                    elif any(word in name.lower() for word in ["file", "read", "write", "path", "directory"]):
                        categories["file"].append(name)
                    elif any(word in name.lower() for word in ["data", "list", "array", "dict", "map", "filter", "sort", "find"]):
                        categories["data"].append(name)
                    elif any(word in name.lower() for word in ["util", "helper", "convert", "format", "validate"]):
                        categories["utility"].append(name)
                    else:
                        categories["other"].append(name)
                
                # Write tools by category
                for category, tool_names in categories.items():
                    if tool_names:
                        f.write(f"## {category.capitalize()} Tools\n\n")
                        for name in sorted(tool_names):
                            f.write(f"### {name}\n\n")
                            f.write("```python\n")
                            f.write(self.tool_code[name])
                            f.write("\n```\n\n")
                
            logger.info(f"Exported tools documentation to {output_file}")
            return True
        except Exception as e:
            logger.error(f"Failed to export tools documentation: {str(e)}")
            return False

    def use_tools(self, task_description: str, available_tools: List[str] = None) -> Dict[str, Any]:
        """Use the available tools to solve a task."""
        if available_tools is None:
            available_tools = self.list_tools()
        
        # Create a description of available tools
        tools_description = "\n".join([
            f"Tool '{name}': {self.tools[name].__doc__ or 'No description'}" 
            for name in available_tools if name in self.tools
        ])
        
        prompt = f"""Solve the following task using the available tools:

        Task: {task_description}

        Available tools:
        {tools_description}

        For each tool you want to use, specify:
        1. The tool name
        2. The arguments to pass to the tool
        
        Return your response in YAML format with the following structure:
        ```yaml
        solution: Your solution description
        tools_used:
          - name: tool_name
            args: [arg1, arg2]
          - name: another_tool
            args: [arg1]
        ```"""
        
        system_message = """You are a problem-solving assistant that uses available tools to complete tasks.
        Analyze the task carefully and determine which tools would be most effective.
        
        IMPORTANT: Format your response in YAML with 'solution' and 'tools_used' fields. 
        The 'tools_used' field should be a list of tools with their names and arguments."""
        
        try:
            result = self._call_llm(prompt, system_message)
            return result
        except Exception as e:
            logger.error(f"Error in use_tools: {str(e)}")
            return {"error": str(e)}

def continuous_self_improvement():
    """Main function for continuous self-improvement through tool creation."""
    try:
        api_key = os.getenv("OPENAI_API_KEY")
        if not api_key:
            raise ValueError("OPENAI_API_KEY environment variable not set")
            
        # Initialize the swarm with tools.json for persistent storage
        tools_file = "tools.json"
        swarm = SelfImprovingSwarm(api_key, tools_file=tools_file)
        
        # Display information about loaded tools
        tools = swarm.list_tools()
        logger.info(f"Loaded {len(tools)} tools: {', '.join(tools)}")
        print(f"\nLoaded {len(tools)} tools from {tools_file}:")
        for tool in tools:
            print(f"- {tool}")
        
        # Export initial tools documentation
        swarm.export_tools_documentation()
        
        # Get initial capabilities summary
        capabilities_summary = swarm.get_capabilities_summary()
        print("\n=== Current Capabilities ===")
        print(capabilities_summary)
        print("===========================\n")
        
        cycle = 0
        while True:
            cycle += 1
            logger.info(f"\n=== Self-Improvement Cycle {cycle} ===")
            
            print(f"\n--- Starting Self-Improvement Cycle {cycle} ---")
            
            # Use reflection-based improvement instead of random category selection
            new_tool = swarm.improve_with_reflection()
            
            if new_tool:
                logger.info(f"Successfully added new tool: {new_tool}")
                logger.info(f"Current toolkit size: {len(swarm.list_tools())}")
                
                # Print the new tool
                print(f"\nNew Tool Added ({new_tool}):")
                print(swarm.get_tool_code(new_tool))
                
                # Export updated tools documentation every cycle with a new tool
                swarm.export_tools_documentation()
                
                # Every 3 cycles, show a summary of capabilities
                if cycle % 3 == 0:
                    capabilities_summary = swarm.get_capabilities_summary()
                    print("\n=== Updated Capabilities ===")
                    print(capabilities_summary)
                    print("===========================\n")
            else:
                logger.warning("Failed to create a new tool in this cycle")
                
                # Export updated tools documentation every 5 cycles even if no new tool was created
                if cycle % 5 == 0:
                    swarm.export_tools_documentation()
                    
                    # Show capabilities summary when documentation is exported
                    capabilities_summary = swarm.get_capabilities_summary()
                    print("\n=== Current Capabilities ===")
                    print(capabilities_summary)
                    print("===========================\n")
            
            # Adaptive sleep based on success
            sleep_time = 30 if new_tool else 60
            print(f"\nWaiting {sleep_time} seconds before next cycle...\n")
            time.sleep(sleep_time)
            
    except Exception as e:
        logger.critical(f"Critical error in continuous_self_improvement: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == '__main__':
    continuous_self_improvement()
