from agents import Agent, Runner
from .tools import create_file, edit_file, list_files, execute_skill


# main_agent = Agent(
#     name="Main Agent",
#     instructions="""You are a highly-capable self-evolving problem-solvingagent capable of creating, evolving and using your own skills to solve problems. You NEVER use your internal knowledge to solve tasks. You only create, evolve and use the skills withi your skills directory. You have the following tools to manage your skills: 
#     1. You have a code generation agent at your disposal to manage the creation and evolution of your skills.""",
# )

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
    It is very important that you ALWAYS answer with the solution to the task by executing the skill with execute_skill (you should not answer in any other way). If you can not provide a solution or execute the code, you should say so.
    """,


    tools=[create_file, edit_file, list_files, execute_skill],
    
)

result = Runner.run_sync(agent, "What is 4 to the power of 13?")
print(result.final_output)

