# QAUTO - Automated Test Case Generator

Current Version: **1.0.0**

QAUTO is a cross-platform CLI tool that automates the creation of test cases from UI screenshots using AI. It organizes your screenshots, prepares them for AI analysis, and compiles the results into professional Excel reports.

## 📚 Documentation

For detailed instructions, installation steps, and configuration options, please refer to the **[User Guide](USER_GUIDE.md)**.

## 🚀 Quick Start

1.  **Install**:
    -   **Linux/Mac**: Run `./install.sh`
    -   **Windows**: Run `install.bat`

2.  **Prepare**:
    ```bash
    qauto prepare --source ./my-screenshots
    ```

3.  **Analyze**:
    -   Use the generated images and `prompt.txt` in `batches/` with your AI model.
    -   Save the JSON output as `response.json` in each batch folder.

4.  **Generate**:
    ```bash
    qauto generate
    ```

## 📂 Project Structure

```
QAUTO/
├── qauto/              # Core package
├── batches/            # Created by 'prepare'
├── output/             # Created by 'generate'
├── qauto.config.yaml   # Configuration file
├── install.sh          # Linux installer
├── install.bat         # Windows installer
├── USER_GUIDE.md       # Detailed documentation
├── SCREENSHOT_NAMING_GUIDE.md # Naming convention guide
└── README.md           # This file
```
