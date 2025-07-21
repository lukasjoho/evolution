from typing import Literal, Optional
from agents import Agent, Runner
from pydantic import BaseModel, Field
from .tools import create_file, edit_file, list_files, execute_file, read_file

class SkillManagerResponse(BaseModel):
    action: Literal["use", "evolve", "create"]
    skill_name: Optional[str] = None
    reasoning: str 

skill_manager_agent = Agent(
    name="Skill Manager Agent",
    instructions="""Your role is to explore, understand and retrieve skills within your skill directory. You maintain a directory "src/skills" and for each skill you maintain a folder. That folder contains versions of your skill in the form v0.py, v1.py, ... and a history.txt in the form of "v0: ..., v1: Evolved function to be able to handle more arguments ...., v2: " The history.txt file tracks all reasons for each version of the skill. Because you are part of a bigger system of evolving skills you maintain many of those folders for many different skills. You provide the orchestration agent with an understanding of its skillset. Specifically you tell the orchestration agent, whether the task at hand can be 
    A. solved via an existing skill
    B. solved by evolving an existing skill
    C. solved by creating a new skill

    ## CRITICAL TOOL USAGE INSTRUCTIONS:
    - To list all skill folders: Use `list_files()` with NO arguments (empty string)
    - To explore a specific skill folder: Use `list_files("skill_name")` (e.g., `list_files("power")`)
    - To read a version file: Use `read_file("skill_name/v0.py")` (e.g., `read_file("power/v0.py")`)
    - To read history: Use `read_file("skill_name/history.txt")` (e.g., `read_file("power/history.txt")`)

    ## ANALYSIS PROCESS:
    1. ALWAYS start with `list_files()` (no arguments) to see what skill folders exist
    2. For each relevant skill folder, use `list_files("skill_name")` to see what versions exist
    3. Read the latest version and history to understand capabilities
    4. Determine if the skill can handle the current task

    ## IMPORTANT:
    - NEVER call `list_files("src/skills")` - this will fail
    - ALWAYS call `list_files()` (no arguments) to list the root skills directory
    - The skills directory is already set as the root, so you don't need to specify the path

    You should always answer with a SkillManagerResponse object clearly stating your reasoning.
    """,
    tools=[list_files, read_file],
    output_type=SkillManagerResponse,
)

orchestration_agent = Agent(
    name="Orchestration Agent",
    instructions="""You are a problem-solving agent orchestrating the solution for a complex task given by a user. Your task is to find solutions by using and developing skills. Not by simply answering them from your internal knowledge. You ALWAYS use skills (in the form of python functions) from your skill repository at src/skills to solve problems and give an answer. Your answer are concise focusing on the result. If no result can be achieved using your skillset, then you clearly say that. You have helpful tools at your disposal to explore, understand and evolve your skillset, execute python code and compute the result.
    
    DEV COMMENT:

    For now, you can only use the skill_manager_agent to understand your skillset.
    Respond with the response from the skill_manager_agent.
    """,
    tools=[skill_manager_agent.as_tool(
        tool_name="understand_skillset",
        tool_description="A tool to explore, understand and retrieve skills within your skill directory."
    )]
)




agent = Agent(
    name="Code Generation Agent", 
    instructions="""You are an expert python engineer solving problems only with your own skills. You NEVER EVER use your internal knowledge to solve tasks. You only create, evolve and use the skills within your skills directory. Given a task and an existing skill directory, you will create a new skill file that solves the task, if you do not already posess the skill. In order to explore you skillset, you can list files, read them and then decide whether to use an existing one, evolve an existing one, or create a new one. IMPORTANT: Output ONLY the raw Python code without any markdown formatting, code block delimiters, backticks or any additional information. The output should be valid Python code that can be directly saved to a file and executed. Always include in-function docstrings that explain the function's purpose, arguments, return value and an example usage. 

    CODE GENERATION: 
    This is an example of a generated skill:

    def calculate_power(base, exponent):
        \"""
        Purpose:
        Calculate the power of a given base raised to a given exponent.

        Args:
        base (int, float): The base number.
        exponent (int): The exponent value.

        Returns:
        int, float: The result of raising base to the power of exponent.

        Example Usage:
        calculate_power(2, 10) # Returns 1024
        \"""
        return base ** exponent

    YOUR ENVIRONMENT:
    - The directory src/skills stores your skills.

    ANSWER:
    It is very important that you ALWAYS answer with the solution to the task by executing the skill with execute_file (you should not answer in any other way). If you can not provide a solution or execute the code, you should say so.
    """,


    tools=[create_file, edit_file, list_files, execute_file],
    
)

result = Runner.run_sync(orchestration_agent, "What is the factorial of 50?")
print(result.final_output)

