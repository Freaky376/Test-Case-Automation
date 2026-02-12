"""
Batch preparation module - refactored from prepare_batches.py
"""
import os
import shutil
from pathlib import Path
from typing import List, Optional
from .config import Config
from .utils import ensure_dir_exists, get_images_in_directory


DEFAULT_PROMPT = """You are a Senior QA Engineer. Analyze the attached UI screenshots for the '{module}' module.

**Screenshot Naming Convention:**
- Main screens: `1.png`, `2.png`, `3.png`, etc.
- Scrollable pages (same screen, scrolled down): `1a.png`, `1b.png`, `1c.png`, etc.
- Sub-components (modals, dropdowns, dialogs): `1.1.png`, `1.2.png`, `2.1.png`, etc.
- Nested components: `1.1.1.png`, `1.1.2.png`, etc.

**Key Distinction:**
- **Letters (a, b, c)** = Same screen, scrolled vertically (continuation of content)
- **Decimals (.1, .2)** = Different UI component (modal, dropdown, dialog)

Example:
- `1.png` = Dashboard (top section)
- `1a.png` = Dashboard (scrolled middle section)
- `1b.png` = Dashboard (scrolled bottom section)
- `1.1.png` = Modal opened from dashboard
- `1.2.png` = Dropdown/component on dashboard
- `2.png` = Settings page
- `2.1.png` = Settings modal

**Instructions:**
Use the screenshot naming to understand:
1. UI hierarchy and navigation flow
2. Which screenshots show the same screen at different scroll positions (treat as ONE screen)
3. Which screenshots show separate components (modals, dropdowns)

4. Do NOT include '[Screenshot X]' or similar references in the title field.

5. **Module Grouping (CRITICAL):** Assign a specific, descriptive `module` value to EACH test case based on the screen or functionality it belongs to.
   - Use the parent module '{module}' as a prefix, then add a descriptive suffix for the specific screen/component.
   - Group test cases that test the SAME screen or component under the SAME module name.
   - Each distinct screen, modal, dialog, or functional area should have its OWN module name.
   - Examples: "{module} - List View", "{module} - Add Member Modal", "{module} - Empty State", "{module} - Search Filter", "{module} - Edit Form"
   - This creates clear section separators in the final Excel report for easy reference.

Context: Module: {module}

Generate comprehensive test cases (Positive, Negative, Edge, UI/UX).

Output JSON format ONLY (no markdown, valid JSON):
{{
    "test_cases": [
        {{
            "id": "202602GEN-XXNN",
            "module": "{module} - Specific Screen or Component",
            "priority": "Critical|High|Medium|Low",
            "type": "UI|Functional|Positive|Negative|Edge",
            "title": "Clear title (do NOT include screenshot reference e.g. [Screenshot 1])",
            "precondition": "Setup required",
            "steps": "1. Step one\\n2. Step two",
            "expected_result": "Expected outcome",
            "actual_result": "",
            "status": "Not Run",
            "qa_tester": "",
            "qa_notes": ""
        }}
    ]
}}"""


def create_batches(
    config: Config,
    source_dir: str = '.',
    batch_size: Optional[int] = None,
    module_name: Optional[str] = None,
    custom_prompt: Optional[str] = None
) -> bool:
    """
    Scans directory for image files, groups them into batches,
    creates batch folders, copies images, and adds prompt.txt.
    
    Args:
        config: Configuration object
        source_dir: Directory to scan for images
        batch_size: Number of images per batch (overrides config)
        custom_prompt: Custom prompt content (overrides config and default)
    
    Returns:
        True if successful, False otherwise
    """
    # Get configuration
    if batch_size is None:
        batch_size = config.get('batch.size', 4)
    
    extensions = config.get('batch.image_extensions', ['png', 'jpg', 'jpeg'])
    batches_dir = config.resolve_path(config.get('directories.batches', './batches'))
    
    # Get images
    os.chdir(source_dir)
    images = get_images_in_directory('.', extensions)
    
    if not images:
        print("❌ No images found in the current directory.")
        print(f"   Looking for extensions: {', '.join(extensions)}")
        return False
    
    print(f"Found {len(images)} images. Processing...")
    
    # Determine prompt content
    if custom_prompt:
        prompt_content = custom_prompt
    elif config.get('prompt.custom_template'):
        template_path = config.get('prompt.custom_template')
        if os.path.exists(template_path):
            with open(template_path, 'r') as f:
                prompt_content = f.read()
        else:
            print(f"⚠️  Custom template not found: {template_path}")
            print("   Using default prompt.")
            prompt_content = DEFAULT_PROMPT
    else:
        prompt_content = DEFAULT_PROMPT

    # Format prompt with module name
    target_module = module_name if module_name else "General"
    try:
        # Only format if the placeholder exists
        if "{module}" in prompt_content:
            prompt_content = prompt_content.format(module=target_module)
    except Exception as e:
        print(f"⚠️  Warning: Could not format prompt with module name: {e}")
    
    # Create base batches directory
    ensure_dir_exists(batches_dir)
    batch_count = 0
    
    for i in range(0, len(images), batch_size):
        batch_count += 1
        batch_folder_name = f"batch_{batch_count:02d}"
        batch_folder_path = os.path.join(batches_dir, batch_folder_name)
        
        # Create folder
        ensure_dir_exists(batch_folder_path)
        
        # Get batch of images
        batch_images = images[i : i + batch_size]
        
        print(f"Creating {batch_folder_path} with {len(batch_images)} images...")
        
        # Copy images (preserve originals)
        for img in batch_images:
            shutil.copy2(img, os.path.join(batch_folder_path, img))
        
        # Create prompt.txt
        with open(os.path.join(batch_folder_path, "prompt.txt"), 'w') as f:
            f.write(prompt_content)
    
    print(f"\n✓ Successfully created {batch_count} batch folders in '{batches_dir}'.")
    print("\nNext steps:")
    print(f"1. Open each batch folder in '{batches_dir}'.")
    print("2. Use the images and prompt.txt with your AI model.")
    print("3. Save the JSON output as 'response.json' in the same folder.")
    print("4. Run 'qauto generate' to create the final Excel.")
    
    return True
