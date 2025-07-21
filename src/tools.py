import os
import subprocess
from pathlib import Path
from agents import function_tool

# Base directory for skills
SKILLS_DIR = Path(__file__).parent / "skills"

@function_tool
def create_file(filename: str, content: str = "") -> str:
    print("TOOL CALLED: create_file", filename, content)
    """Create a new file in the skills directory.
    
    Args:
        filename: Name of the file to create
        content: Content to write to the file (optional)
    
    Returns:
        Success message or error description
    """
    try:
        # Ensure skills directory exists
        SKILLS_DIR.mkdir(exist_ok=True)
        
        file_path = SKILLS_DIR / filename
        
        # Check if file already exists
        if file_path.exists():
            return f"Error: File '{filename}' already exists"
        
        # Create the file
        file_path.write_text(content, encoding='utf-8')
        return f"Successfully created '{filename}'"
        
    except Exception as e:
        return f"Error creating file: {str(e)}"

@function_tool
def edit_file(filename: str, content: str) -> str:
    print("TOOL CALLED: edit_file", filename, content)
    """Edit (overwrite) an existing file in the skills directory.
    
    Args:
        filename: Name of the file to edit
        content: New content for the file
    
    Returns:
        Success message or error description
    """
    try:
        file_path = SKILLS_DIR / filename
        
        # Check if file exists
        if not file_path.exists():
            return f"Error: File '{filename}' does not exist"
        
        # Overwrite the file
        file_path.write_text(content, encoding='utf-8')
        return f"Successfully updated '{filename}'"
        
    except Exception as e:
        return f"Error editing file: {str(e)}"

@function_tool
def list_files() -> str:
    print("TOOL CALLED: list_files")
    """List all files in the skills directory.
    
    Returns:
        List of files or error description
    """
    try:
        # Ensure skills directory exists
        if not SKILLS_DIR.exists():
            return "Skills directory does not exist"
        
        # Get all files (not directories)
        files = [f.name for f in SKILLS_DIR.iterdir() if f.is_file()]
        
        if not files:
            return "No files found in skills directory"
        
        return "\n".join(sorted(files))
        
    except Exception as e:
        return f"Error listing files: {str(e)}"

@function_tool
def execute_skill(skill_filename: str, arguments: str = "") -> str:
    print("TOOL CALLED: execute_skill", skill_filename, arguments)
    """Execute a skill from the skills directory with optional arguments.
    
    Args:
        skill_filename: Name of the skill file to execute
        arguments: Arguments to pass to the skill (optional)
    
    Returns:
        Output from the executed skill or error description
    """
    try:
        skill_path = SKILLS_DIR / skill_filename
        
        if not skill_path.exists():
            return f"Error: Skill '{skill_filename}' does not exist"
        
        # Build command to execute the skill
        cmd = ["python", str(skill_path)]
        if arguments.strip():
            cmd.extend(arguments.split())
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return result.stdout if result.stdout else "Skill executed successfully (no output)"
        else:
            return f"Error: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "Error: Skill execution timed out (30 seconds)"
    except Exception as e:
        return f"Error executing skill: {str(e)}"