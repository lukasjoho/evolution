from typing import Literal, Optional
from agents import Agent, Runner
from pydantic import BaseModel, Field
from dotenv import load_dotenv
from .tools import list_files, read_file

load_dotenv()

class DecisionResponse(BaseModel):
    action: Literal["use", "evolve", "create"]
    skill_name: Optional[str] = None
    reasoning: str 

# Deterministic DeciderAgent - First step in the evolution flow
decider_agent = Agent(
    name="DeciderAgent",
    instructions="""You are the DeciderAgent - the first step in a deterministic skill evolution system.
    Your job is to analyze a given task and make a structured decision about how to handle it.
    
    You maintain a skills directory where each skill has its own folder containing:
    - skill.py (current/latest version - always use this)
    - skill-1.py, skill-2.py... (past versions for reference, numbered from most recent)
    
    ## YOUR DECISION PROCESS (FOLLOW EXACTLY):
    
    1. **EXPLORATION PHASE:**
       - Start with `list_files()` to see all available skill folders
       - For each potentially relevant skill folder, use `list_files("skill_name")` to see available files
       - Read the current skill.py file to understand current capabilities
       - If needed, check past versions (skill-1.py, skill-2.py) to understand evolution
    
    2. **DECISION PHASE:**
       Make exactly ONE of these decisions:
       - **"use"**: An existing skill can solve the task as-is
       - **"evolve"**: An existing skill needs modification/improvement to solve the task  
       - **"create"**: No existing skill can solve the task, need a completely new skill
    
    ## TOOL USAGE:
    - List all skills: `list_files()` (no arguments)
    - Explore skill folder: `list_files("skill_name")`
    - Read current skill: `read_file("skill_name/skill.py")`
    - Read past versions: `read_file("skill_name/skill-1.py")`, `read_file("skill_name/skill-2.py")` etc.
    
    ## OUTPUT:
    Always return a DecisionResponse with:
    - action: "use", "evolve", or "create" 
    - skill_name: name of existing skill (for use/evolve) or proposed name (for create)
    - reasoning: clear explanation of your decision process
    
    Be methodical and thorough in your analysis.
    """,
    tools=[list_files, read_file],
    output_type=DecisionResponse,
)

# Placeholder for future agents - commented out for now as requested
# orchestration_agent = Agent(...)
# code_generation_agent = Agent(...)

# Code Generation Agent - commented out for now as requested  
# agent = Agent(...)


task = "What is 2 to the power of 10?"
result = Runner.run_sync(decider_agent, task)
print("--- Decision taken ---")
print(result.final_output)


    



