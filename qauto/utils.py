"""
Utility functions for QAUTO
"""
import os
from pathlib import Path
from typing import List


def get_script_dir() -> Path:
    """Get the directory where the script is located"""
    return Path(__file__).parent.parent


def ensure_dir_exists(path: str) -> str:
    """Ensure directory exists, create if not"""
    Path(path).mkdir(parents=True, exist_ok=True)
    return path


def get_images_in_directory(directory: str = '.', extensions: List[str] = None) -> List[str]:
    """Get all image files in a directory"""
    if extensions is None:
        extensions = ['png', 'jpg', 'jpeg']
    
    images = []
    for ext in extensions:
        images.extend(Path(directory).glob(f'*.{ext}'))
        images.extend(Path(directory).glob(f'*.{ext.upper()}'))
    
    # Return sorted list of filenames
    return sorted([img.name for img in images])


def validate_file_exists(filepath: str, file_description: str = "File") -> bool:
    """Validate that a file exists"""
    if not os.path.exists(filepath):
        print(f"❌ Error: {file_description} not found: {filepath}")
        return False
    return True


def format_error(message: str) -> str:
    """Format error message with emoji"""
    return f"❌ {message}"


def format_success(message: str) -> str:
    """Format success message with emoji"""
    return f"✓ {message}"


def format_warning(message: str) -> str:
    """Format warning message with emoji"""
    return f"⚠️  {message}"
