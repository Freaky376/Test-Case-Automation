# Windows Installation & Usage Guide

## One-Time Setup (Install the Tool)

1. **Copy the entire "Test Case Automation" folder to your Windows PC**
   - Example location: `C:\Tools\Test Case Automation\`

2. **Open Command Prompt**
   - Press `Win + R`, type `cmd`, press Enter

3. **Navigate to the tool folder**
   ```cmd
   cd "C:\Tools\Test Case Automation"
   ```

4. **Run the installer**
   ```cmd
   install.bat
   ```
   
5. **Add to PATH (recommended)**
   - Follow the instructions shown by the installer
   - This allows you to use `testgen` from anywhere

## Daily Usage (After Installation)

### Option A: If you added the folder to PATH
You can use `testgen` from **any folder**:

```cmd
# Go to your screenshots folder
cd "C:\My Projects\Screenshots"

# Run the tool
testgen prepare
testgen generate
```

### Option B: Without PATH (use full path)
```cmd
# Go to your screenshots folder
cd "C:\My Projects\Screenshots"

# Run the tool using full path
python "C:\Tools\Test Case Automation\testgen.py" prepare
python "C:\Tools\Test Case Automation\testgen.py" generate
```

## Complete Workflow Example

```cmd
# 1. Navigate to your project with screenshots
cd "C:\Users\YourName\Desktop\MyApp\Screenshots"

# 2. Prepare batches
testgen prepare

# 3. Process each batch with AI, save response.json files

# 4. Generate Excel report
testgen generate

# 5. Find report in "output" folder
explorer output
```

## Quick Test

After installation, test it works:
```cmd
testgen --version
testgen config show
```

## Key Points

✅ **Install once** in one location (e.g., `C:\Tools\Test Case Automation\`)
✅ **Use anywhere** - navigate to your screenshots folder and run `testgen`
❌ **Don't reinstall** in every project folder - that's not needed!
