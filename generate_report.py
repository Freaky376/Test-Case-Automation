#!/usr/bin/env python3
import json
import os
import sys
import glob
from datetime import datetime

# Check for required library
try:
    import openpyxl
    from openpyxl.styles import Alignment
    from openpyxl.utils import get_column_letter
except ImportError:
    print("Error: 'openpyxl' is required to work with the Excel template.")
    print("Please install it using your system package manager or pip.")
    print("  Arch/EndeavourOS: sudo pacman -S python-openpyxl")
    print("  Other: pip install openpyxl")
    sys.exit(1)

def merge_batches(base_dir):
    """Merges response.json files from batch directories."""
    all_test_cases = []
    errors = []
    
    # Find all batch folders
    # Check current directory first, then home directory fallback
    search_path = os.path.join(base_dir, "batch_*")
    batch_folders = sorted(glob.glob(search_path))
    
    if not batch_folders:
        # Try home directory if not found in current
        home_path = os.path.expanduser("~/test_batches")
        search_path = os.path.join(home_path, "batch_*")
        batch_folders = sorted(glob.glob(search_path))
        
        if batch_folders:
            print(f"Found batch folders in {home_path}")
        else:
            print("No 'batch_*' folders found in current directory or ~/test_batches.")
            return [], []

    print(f"Found {len(batch_folders)} batch folders.")

    for folder in batch_folders:
        if not os.path.isdir(folder):
            continue
            
        json_path = os.path.join(folder, "response.json")
        folder_name = os.path.basename(folder)
        
        if os.path.exists(json_path):
            # Check if file is empty
            if os.path.getsize(json_path) == 0:
                error_msg = f"{folder_name}: response.json is EMPTY"
                print(f"  ❌ {error_msg}")
                errors.append(error_msg)
                continue
                
            try:
                with open(json_path, 'r') as f:
                    data = json.load(f)
                    if "test_cases" in data:
                        cases = data.get("test_cases", [])
                        print(f"  ✓ {folder_name}: Loaded {len(cases)} test cases.")
                        all_test_cases.extend(cases)
                    else:
                        error_msg = f"{folder_name}: 'test_cases' key not found in JSON"
                        print(f"  ❌ {error_msg}")
                        errors.append(error_msg)
            except json.JSONDecodeError as e:
                error_msg = f"{folder_name}: Invalid JSON - {e}"
                print(f"  ❌ {error_msg}")
                errors.append(error_msg)
            except Exception as e:
                error_msg = f"{folder_name}: Error reading file - {e}"
                print(f"  ❌ {error_msg}")
                errors.append(error_msg)
        else:
            error_msg = f"{folder_name}: response.json not found"
            print(f"  ❌ {error_msg}")
            errors.append(error_msg)
            
    return all_test_cases, errors

def generate_excel(test_cases, output_dir, template_path):
    """Generates the Excel report from test cases."""
    if not test_cases:
        print("No test cases to write.")
        return

    # Generate filename with current date
    current_date = datetime.now().strftime("%Y-%m-%d")
    output_filename = f"Generated_Test_Cases_{current_date}.xlsx"
    output_file = os.path.join(output_dir, output_filename)

    if not os.path.exists(template_path):
        print(f"Error: Template file '{template_path}' not found.")
        return

    # Ensure output directory exists
    os.makedirs(output_dir, exist_ok=True)

    try:
        print(f"Generating report: {output_file}...")
        
        # Load Excel Template
        wb = openpyxl.load_workbook(template_path)
        
        if "Page1" in wb.sheetnames:
            ws = wb["Page1"]
        else:
            ws = wb.active

        # Clear existing data rows (keep header at row 1)
        max_row = ws.max_row
        if max_row > 1:
            for row in ws.iter_rows(min_row=2, max_row=max_row):
                for cell in row:
                    cell.value = None
                    cell.style = 'Normal' 

        # Write new data starting at row 2
        start_row = 2
        
        # Define column widths
        col_widths = {
            1: 15,  # ID
            2: 10,  # Priority
            3: 30,  # Title
            4: 25,  # Precondition
            5: 50,  # Steps
            6: 40,  # Expected
            7: 30,  # Actual
            8: 40,  # Acceptance Criteria
            9: 10,  # Status
            10: 15, # Tester
            11: 20  # Notes
        }

        # Apply column widths
        for col_idx, width in col_widths.items():
            col_letter = get_column_letter(col_idx)
            ws.column_dimensions[col_letter].width = width

        # Group by module while preserving original JSON order within each group.
        # Modules appear in the order they are first encountered (batch 1 first).
        for case in test_cases:
            if "module" not in case or not case["module"]:
                case["module"] = "General"
        
        seen_modules = {}  # module -> list of cases
        module_order = []  # preserves first-seen order of modules
        for case in test_cases:
            mod = case.get("module", "General")
            if mod not in seen_modules:
                seen_modules[mod] = []
                module_order.append(mod)
            seen_modules[mod].append(case)
        
        ordered_cases = []
        for mod in module_order:
            ordered_cases.extend(seen_modules[mod])
        test_cases = ordered_cases
        
        current_module = None
        
        for i, case in enumerate(test_cases):
            # Check if module changed
            module = case.get("module", "General")
            
            if module != current_module:
                # Insert Separator Row
                current_module = module
                row_num = ws.max_row + 1
                
                # Create styled header cell
                cell = ws.cell(row=row_num, column=1)
                cell.value = f"[{module}]"
                cell.font = openpyxl.styles.Font(bold=True, size=12, color="0000FF") # Blue, Bold
                cell.alignment = Alignment(horizontal='left', vertical='center')
                
                # Merge row for cleaner look
                ws.merge_cells(start_row=row_num, start_column=1, end_row=row_num, end_column=11)
                
                # Add background color
                fill = openpyxl.styles.PatternFill(start_color="E0E0E0", end_color="E0E0E0", fill_type="solid")
                for col in range(1, 12):
                     ws.cell(row=row_num, column=col).fill = fill
                
                ws.row_dimensions[row_num].height = 25

            row_num = ws.max_row + 1
            
            def get_val(key):
                val = case.get(key, "")
                if val is None: return ""
                return str(val)

            # Add test type prefix to title
            title = get_val("title")
            raw_type = get_val("type").upper()
            
            # Helper to determine type
            def determine_type(type_str, title_str):
                # 1. Use explicit type if available
                if type_str:
                    mapping = {
                        "UI": "UI",
                        "UI/UX": "UI",
                        "UIUX": "UI",
                        "POSITIVE": "FUNCTION",
                        "NEGATIVE": "FUNCTION",
                        "EDGE": "FUNCTION",
                        "FUNCTIONAL": "FUNCTION",
                        "FUNCTION": "FUNCTION"
                    }
                    return mapping.get(type_str, type_str)
                
                # 2. Infer from title keywords if no type
                title_lower = title_str.lower()
                ui_keywords = ["ui", "design", "layout", "color", "font", "align", "spelling", "text", "appearance", "style", "display", "appear", "icon", "button", "logo", "image"]
                if any(k in title_lower for k in ui_keywords):
                    return "UI"
                
                # Default to FUNCTION for logic/behavior tests
                return "FUNCTION"

            display_type = determine_type(raw_type, title)
            
            # Get module name
            module_name = get_val("module")
            
            # Format prefixes: [Type] Title (Module removed from prefix as it's now a header)
            prefix = f"[{display_type}]"
            
            # Avoid double prefixing
            clean_title = title.strip()
            # Remove module prefix if it was there from previous run
            if clean_title.startswith(f"[{module}]"):
                 clean_title = clean_title[len(f"[{module}]"):].strip()
                 
            if clean_title.startswith(prefix):
                 formatted_title = clean_title
            else:
                formatted_title = f"{prefix} {clean_title}"

            # Map data to columns (1-based index)
            columns_data = [
                (1, "id"), 
                (2, "priority"), 
                (3, "title"), 
                (4, "precondition"), 
                (5, "steps"), 
                (6, "expected_result"), 
                (7, "actual_result"), 
                (8, "acceptance_criteria"),
                (9, "status"), 
                (10, "qa_tester"), 
                (11, "qa_notes")
            ]

            max_lines_in_row = 1

            for col_idx, key in columns_data:
                cell = ws.cell(row=row_num, column=col_idx)
                # Use formatted title for title column, otherwise use regular value
                if key == "title":
                    value = formatted_title
                else:
                    value = get_val(key)
                cell.value = value
                
                # Apply text wrapping for long fields
                if col_idx in [3, 4, 5, 6, 7, 8, 11]:
                    cell.alignment = Alignment(wrap_text=True, vertical='top')
                    
                    # Estimate row height
                    newlines = value.count('\n')
                    char_limit = col_widths.get(col_idx, 20)
                    
                    if len(value) > char_limit:
                        wrapped_lines = (len(value) / char_limit) 
                        lines = newlines + wrapped_lines + 1
                    else:
                        lines = newlines + 1
                        
                    if lines > max_lines_in_row:
                        max_lines_in_row = lines
                else:
                     cell.alignment = Alignment(vertical='top')

            # Adjust Row Height
            if max_lines_in_row > 1:
                height = min(max_lines_in_row * 15, 409) 
                ws.row_dimensions[row_num].height = height

        # Save output
        wb.save(output_file)
        print(f"Successfully generated report at: {output_file}")

    except Exception as e:
        print(f"An error occurred during Excel generation: {e}")
        import traceback
        traceback.print_exc()

def main():
    # Configuration
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Adjusted to look in the 'batches' folder relative to script location
    base_search_dir = os.path.join(script_dir, "batches")
    
    # Template paths (Primary and Fallback)
    template_path_primary = os.path.join(script_dir, "actual excel template", "Test_Case_Template.xlsx")
    template_path_fallback = os.path.join(script_dir, "Test_Case_Template.xlsx")
    
    # Check template
    if os.path.exists(template_path_primary):
        template_path = template_path_primary
    elif os.path.exists(template_path_fallback):
        template_path = template_path_fallback
    else:
        print("Error: Excel template not found in expected locations.")
        return

    # Output directory - explicitly "output" folder relative to script location
    output_dir = os.path.join(script_dir, "output")
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    print("--- Starting Test Case Report Generation ---")
    print(f"Searching for batches in: {base_search_dir}")
    
    # Step 1: Merge
    test_cases, errors = merge_batches(base_search_dir)
    
    # Stop if there are any errors
    if errors:
        print("\n" + "="*60)
        print("⚠️  ERROR: Cannot generate report due to batch issues:")
        print("="*60)
        for i, error in enumerate(errors, 1):
            print(f"{i}. {error}")
        print("\nPlease fix the above issues and run the script again.")
        print("="*60)
        return
    
    if not test_cases:
        print("No test cases found. Exiting.")
        return

    print(f"\nTotal merged test cases: {len(test_cases)}")

    # Step 2: Generate Excel
    generate_excel(test_cases, output_dir, template_path)
    
    print("--- Done ---")

if __name__ == "__main__":
    main()
