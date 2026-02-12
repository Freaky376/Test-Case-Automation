# Windows Installation & Usage Guide

## One-Time Setup (Install the Tool)

1. **Copy the entire "QAUTO" folder to your Windows PC**
   - Example location: `C:\Tools\QAUTO\`

2. **Open Command Prompt**
   - Press `Win + R`, type `cmd`, press Enter

3. **Navigate to the tool folder**
   ```cmd
   cd "C:\Tools\QAUTO"
   ```

4. **Run the installer**
   ```cmd
   install.bat
   ```
   
5. **Add to PATH (recommended)**
   - Follow the instructions shown by the installer
   - This allows you to use `qauto` from anywhere

## Daily Usage (After Installation)

### Option A: If you added the folder to PATH
You can use `qauto` from **any folder**:

```cmd
# Go to your screenshots folder
cd "C:\My Projects\Screenshots"

# Run the tool
qauto prepare
qauto generate
```

### Option B: Without PATH (use full path)
```cmd
# Go to your screenshots folder
cd "C:\My Projects\Screenshots"

# Run the tool using full path
python "C:\Tools\QAUTO\qauto.py" prepare
python "C:\Tools\QAUTO\qauto.py" generate
```

## Complete Workflow Example

```cmd
# 1. Navigate to your project with screenshots
cd "C:\Users\YourName\Desktop\MyApp\Screenshots"

# 2. Prepare batches
qauto prepare

# 3. Process each batch with AI, save response.json files

# 4. Generate Excel report
qauto generate

# 5. Find report in "output" folder
explorer output
```

## Quick Test

After installation, test it works:
```cmd
qauto --version
qauto config show
```

## Key Points

✅ **Install once** in one location (e.g., `C:\Tools\QAUTO\`)
✅ **Use anywhere** - navigate to your screenshots folder and run `qauto`
❌ **Don't reinstall** in every project folder - that's not needed!
