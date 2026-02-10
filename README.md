# TestGen - Automated Test Case Generator

Current Version: **1.0.0**

TestGen is a cross-platform CLI tool that automates the creation of test cases from UI screenshots using AI. It streamlines the QA process by:
1. Organizing screenshots into batches
2. Using AI to analyze UI and generate test cases
3. Compiling results into a formatted Excel report

## Features

- **Cross-Platform**: Works on Windows, Linux, and macOS
- **Smart Batching**: Automatically groups screenshots
- **AI Integration**: Uses your preferred AI model to generate test cases
- **Excel Reporting**: Creates professional test case documents
- **Dynamic Configuration**: Customizable settings for templates and paths
- **Hierarchical Naming**: Smart screenshot organization

## Installation

### Linux / macOS
```bash
chmod +x install.sh
./install.sh
```
Follow the prompts to install dependencies and make `testgen` available globally.

### Windows
Double-click `install.bat` or run in Command Prompt:
```cmd
install.bat
```
Add the installation folder to your PATH environment variable as instructed.

## Quick Start

1. **Prepare Screenshots**: Place your UI screenshots in a folder.
2. **Run Preparation**:
   ```bash
   testgen prepare
   ```
   This creates a `batches/` folder with organized subfolders.

3. **Generate Test Cases**:
   - Open each batch folder (e.g., `batches/batch_01`).
   - Use the images and `prompt.txt` with your AI tool (ChatGPT, Claude, Gemini, etc.).
   - Save the AI's JSON output as `response.json` in the same batch folder.

4. **Create Report**:
   ```bash
   testgen generate
   ```
   The final Excel report will be saved in the `output/` folder.

## Commands

| Command | Description |
|---------|-------------|
| `testgen prepare` | Organize screenshots into batches |
| `testgen generate` | Compile batches into Excel report |
| `testgen config show` | View current configuration |
| `testgen config set` | Update configuration settings |
| `testgen init` | Create a config file in current directory |

### Options
- `testgen prepare --batch-size 6` (Custom batch size)
- `testgen generate --output-dir ./my-reports` (Custom output location)

## Configuration

You can customize TestGen using `testgen config` or by editing `testgen.config.yaml`.

**Key Settings:**
- `template.primary`: Path to your Excel template
- `batch.size`: Number of images per batch (default: 4)
- `directories.batches`: Where to create batch folders
- `directories.output`: Where to save Excel reports

Example:
```bash
testgen config set batch.size 5
testgen config set template.primary "/path/to/my/template.xlsx"
```

## Screenshot Naming

Use the hierarchical naming convention for better AI analysis:

- **Main Screens**: `1.png`, `2.png`
- **Scrollable Pages**: `1a.png`, `1b.png`
- **Sub-components**: `1.1.png` (Modal), `1.2.png` (Dropdown)

See [SCREENSHOT_NAMING_GUIDE.md](SCREENSHOT_NAMING_GUIDE.md) for details.

## Project Structure

```
Test Case Automation/
├── testgen/            # Core package
├── batches/            # Created by 'prepare'
├── output/             # Created by 'generate'
├── testgen.config.yaml # Configuration file
├── testgen.py          # Entry point
├── install.sh          # Linux installer
├── install.bat         # Windows installer
└── README.md           # Documentation
```
