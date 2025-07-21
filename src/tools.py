import os
import subprocess
from pathlib import Path
from agents import function_tool

# Base directory for skills
ROOT_DIR = Path(__file__).parent / "skills"

@function_tool
def create_folder(foldername: str) -> str:
    print("TOOL CALLED: create_folder", foldername)
    """Create a new folder in the skills directory.
    
    Args:
        foldername: Name of the folder to create
    """
    try:
        ROOT_DIR.mkdir(exist_ok=True)
        folder_path = ROOT_DIR / foldername
        folder_path.mkdir(exist_ok=True)
        return f"Successfully created folder '{foldername}'"
    except Exception as e:
        return f"Error creating folder: {str(e)}"

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
        ROOT_DIR.mkdir(exist_ok=True)
        
        file_path = ROOT_DIR / filename
        
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
        file_path = ROOT_DIR / filename
        
        # Check if file exists
        if not file_path.exists():
            return f"Error: File '{filename}' does not exist"
        
        # Overwrite the file
        file_path.write_text(content, encoding='utf-8')
        return f"Successfully updated '{filename}'"
        
    except Exception as e:
        return f"Error editing file: {str(e)}"

@function_tool
def list_files(path: str = "") -> str:
    print("TOOL CALLED: list_files", path)
    """List all files and directories in the specified path within the skills directory.
    
    Args:
        path: Relative path within the skills directory (optional, defaults to root skills directory)
    
    Returns:
        List of files and directories or error description
    """
    try:
        # Ensure skills directory exists
        ROOT_DIR.mkdir(exist_ok=True)
        
        # Determine target path
        if path:
            target_path = ROOT_DIR / path
        else:
            target_path = ROOT_DIR
        
        if not target_path.exists():
            return f"Error: Path '{path}' does not exist"
        
        # Get all files and directories
        items = []
        for item in target_path.iterdir():
            if item.is_dir():
                items.append(f"[DIR] {item.name}/")
            else:
                items.append(f"[FILE] {item.name}")
        
        if not items:
            return "No files or directories found"
        
        return "\n".join(sorted(items))
        
    except Exception as e:
        return f"Error listing files: {str(e)}"

@function_tool
def read_file(filepath: str) -> str:
    print("TOOL CALLED: read_file", filepath)
    """Read the contents of a file within the skills directory.
    
    Args:
        filepath: Relative path to the file within the skills directory (e.g., 'add/v0.py' or 'power/history.txt')
    
    Returns:
        File contents or error description
    """
    try:
        file_path = ROOT_DIR / filepath
        
        if not file_path.exists():
            return f"Error: File '{filepath}' does not exist"
        
        if not file_path.is_file():
            return f"Error: '{filepath}' is not a file"
        
        return file_path.read_text(encoding='utf-8')
        
    except Exception as e:
        return f"Error reading file: {str(e)}"

@function_tool
def execute_file(filepath: str, arguments: str = "") -> str:
    print("TOOL CALLED: execute_file", filepath, arguments)
    """Execute a Python file from the skills directory with optional arguments.
    
    Args:
        filepath: Relative path to the Python file within the skills directory
        arguments: Arguments to pass to the file (optional)
    
    Returns:
        Output from the executed file or error description
    """
    try:
        file_path = ROOT_DIR / filepath
        
        if not file_path.exists():
            return f"Error: File '{filepath}' does not exist"
        
        if not file_path.is_file():
            return f"Error: '{filepath}' is not a file"
        
        # Build command to execute the file
        cmd = ["python", str(file_path)]
        if arguments.strip():
            cmd.extend(arguments.split())
        
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=30
        )
        
        if result.returncode == 0:
            return result.stdout if result.stdout else "File executed successfully (no output)"
        else:
            return f"Error: {result.stderr}"
            
    except subprocess.TimeoutExpired:
        return "Error: File execution timed out (30 seconds)"
    except Exception as e:
        return f"Error executing file: {str(e)}"

