#!/usr/bin/env python3
import os
import shutil
import glob

def create_batches():
    """
    Scans the current directory for image files, groups them into batches of 4,
    creates batch_XX folders inside a 'batches' directory, moves the images, 
    and adds a prompt.txt template.
    """
    # Supported image extensions
    image_extensions = ['*.png', '*.jpg', '*.jpeg']
    images = []
    
    for ext in image_extensions:
        images.extend(glob.glob(ext))
    
    # Sort images to ensure consistent grouping
    images.sort()
    
    if not images:
        print("No images found in the current directory.")
        return

    print(f"Found {len(images)} images. Processing...")

    batch_size = 4
    batch_count = 0 
    
    # Default prompt template for test case generation
    prompt_content = """You are a Senior QA Engineer. Analyze the attached UI screenshots for the 'General' module.

Acceptance Criteria Reference: Each test case includes an `acceptance_criteria` field. Use this field to define the specific acceptance criteria that must be met for the test case to pass. This should reference the designer-provided acceptance criteria when available. If no specific acceptance criteria is provided, leave it empty or derive a clear pass/fail criteria from the expected result.

Context: 

Generate comprehensive test cases (Positive, Negative, Edge, UI/UX).

Output JSON format ONLY (no markdown, valid JSON):
{
    "test_cases": [
        {
            "id": "202602GEN-XXNN",
            "priority": "Critical|High|Medium|Low",
            "title": "Clear title (do NOT include screenshot reference e.g. [Screenshot 1])",
            "precondition": "Setup required",
            "steps": "1. Step one\\\\n2. Step two",
            "expected_result": "Expected outcome",
            "actual_result": "",
            "acceptance_criteria": "",
            "status": "Not Run",
            "qa_tester": "",
            "qa_notes": ""
        }
    ]
}"""
    
    # Allow user to override with custom template
    if os.path.exists("prompt_template.txt"):
        with open("prompt_template.txt", 'r') as f:
            prompt_content = f.read()

    # Create base batches directory
    script_dir = os.path.dirname(os.path.abspath(__file__))
    base_batch_dir = os.path.join(script_dir, "batches")
    os.makedirs(base_batch_dir, exist_ok=True)

    for i in range(0, len(images), batch_size):
        batch_count += 1
        # Create batch folder inside 'batches' directory
        batch_folder_name = f"batch_{batch_count:02d}"
        batch_folder_path = os.path.join(base_batch_dir, batch_folder_name)
        
        # Create folder
        os.makedirs(batch_folder_path, exist_ok=True)
        
        # Get batch of images
        batch_images = images[i : i + batch_size]
        
        print(f"Creating {batch_folder_path} with {len(batch_images)} images...")
        
        # Copy images (preserve originals)
        for img in batch_images:
            shutil.copy2(img, os.path.join(batch_folder_path, img))
            
        # Create prompt.txt
        with open(os.path.join(batch_folder_path, "prompt.txt"), 'w') as f:
            f.write(prompt_content)
            
    print(f"\nSuccessfully created {batch_count} batch folders in '{base_batch_dir}'.")
    print("Next steps:")
    print(f"1. Open each batch folder in '{base_batch_dir}'.")
    print("2. Use the images and prompt.txt with your AI model.")
    print("3. Save the JSON output as 'response.json' in the same folder.")
    print("4. Run 'generate_report.py' to create the final Excel.")

if __name__ == "__main__":
    create_batches()
