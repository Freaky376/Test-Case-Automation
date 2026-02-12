# QAUTO Command Quick Fix

## The Issue
There's an old `qauto` (or `testgen`) script in `/usr/local/bin` that points to the wrong location. Since we can't remove it without sudo, we've created an alias workaround.

## The Solution
An alias has been added to your `~/.zshrc` file that points to the correct qauto CLI.

## How to Use

**Option 1: Reload your shell (RECOMMENDED)**
```bash
source ~/.zshrc
```

After this, you can use `qauto` normally:
```bash
# Basic usage
qauto prepare
qauto generate

# Using the NEW module feature
qauto prepare --module "Committee"
qauto generate
```

## New Excel Layout
The generated Excel report now features:
- **Grouped Rows**: Test cases are automatically grouped by module.
- **Separator Headers**: A bold blue header row (e.g., `[Committee]`) separates each module section.
- **Clean Titles**: Titles only show `[UI]` or `[FUNCTION]`, while the module name is in the section header.

**Option 2: Open a new terminal**
The alias will be automatically loaded in any new terminal session.

**Option 3: Use the full path (temporary workaround)**
If you don't want to reload your shell:
```bash
~/.local/bin/qauto prepare
~/.local/bin/qauto generate
```

## Verification
To verify the correct qauto is being used:
```bash
which qauto
# Should show: qauto: aliased to /home/jhoncb/.local/bin/qauto
```

## What Works Now
✅ `qauto prepare` - Prepare batches from screenshots  
✅ `qauto generate` - Generate Excel report  
✅ `qauto config show` - Show configuration  
✅ `qauto --help` - Get help  
✅ **Test type prefixes** - Titles now show [UI] or [FUNCTION] tags
