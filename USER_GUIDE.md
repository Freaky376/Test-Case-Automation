# QAUTO User Guide

QAUTO is a cross-platform Command Line Interface (CLI) tool designed to automate the process of generating detailed test cases from UI screenshots using AI. It bridges the gap between visual design and Quality Assurance by:

1.  **Organizing** your raw screenshots into logical batches.
2.  **Preparing** prompts for AI analysis.
3.  **Generating** professional Excel test case reports from AI outputs.

This tool works with your preferred AI model (ChatGPT, Claude, Gemini, etc.) to convert visual UI elements into structured test scenarios.

---

## 🚀 Installation

### Prerequisites

-   **Python 3.8+** must be installed.
    -   Verify with `python3 --version` or `python --version`.

### Linux / macOS

1.  Open your terminal in the `QAUTO/Test-Case-Automation` directory.
2.  Run the installation script:
    ```bash
    chmod +x install.sh
    ./install.sh
    ```
3.  Follow the prompts. You will be asked if you want to make `qauto` available globally.
    -   **Yes (Recommended):** The script creates a symlink in `~/.local/bin`. Ensure this directory is in your `PATH`.
    -   **No:** You will run the tool using `python3 qauto.py`.

### Windows

1.  Open Command Prompt or PowerShell in the `QAUTO\Test-Case-Automation` directory.
2.  Run the batch installer:
    ```cmd
    install.bat
    ```
3.  Add the installation directory to your system's `PATH` environment variable if you want to run `qauto` from anywhere.

---

## 📖 Usage Workflow

The process consists of three main phases: **Prepare**, **Analyze**, and **Generate**.

### Phase 1: Preparation

1.  **Collect Screenshots**: Place all your UI screenshots in a single source folder.
2.  **Naming Convention**: Rename your screenshots to help the AI understand the flow.
    -   **Main Screens**: `1.png`, `2.png`
    -   **Scrollable Content** (Same screen, further down): `1a.png`, `1b.png`
    -   **Sub-components** (Modals, Dropdowns): `1.1.png`, `1.2.png`
    -   *See [SCREENSHOT_NAMING_GUIDE.md](SCREENSHOT_NAMING_GUIDE.md) for full details.*
3.  **Run Prepare Command**:
    ```bash
    qauto prepare --source ./my-screenshots
    ```
    -   This creates a `batches/` directory.
    -   Inside, you will find subfolders like `batch_01`, `batch_02`, etc.
    -   Each batch folder contains a set of images and a `prompt.txt`.

### Phase 2: AI Analysis (Manual Step)

1.  Open a batch folder (e.g., `batches/batch_01`).
2.  Open `prompt.txt` and copy its content.
3.  Go to your AI tool (ChatGPT, Claude, etc.).
4.  **Upload the images** from that batch folder.
5.  **Paste the prompt** and send.
6.  The AI will generate a JSON response. **Copy only the JSON code block.**
7.  Create a new file named `response.json` in the `batch_01` folder and paste the JSON there.
8.  Repeat for all batch folders.

### Phase 3: Reporting

1.  Once all batches have a `response.json`, run:
    ```bash
    qauto generate
    ```
2.  The tool merges all JSON files and creates a formatted Excel report.
3.  Find your report in the `output/` directory (e.g., `Generated_Test_Cases_2026-02-12.xlsx`).

---

## ⚙️ Configuration

You can customize QAUTO options permanently using the config command or by editing `qauto.config.yaml`.

### View Configuration
```bash
qauto config show
```

### Common Settings

| Key | Description | Default |
| :--- | :--- | :--- |
| `batch.size` | Number of images per batch | `4` |
| `template.primary` | Path to the Excel template | `./actual excel template/Test Cases Template.xlsx` |
| `directories.batches` | Where batches are created | `./batches` |
| `directories.output` | Where reports are saved | `./output` |

### Changing Settings
To change the batch size to 6:
```bash
qauto config set batch.size 6
```

To set a custom template path:
```bash
qauto config set template.primary "/abs/path/to/my_template.xlsx"
```

---

## ❓ Troubleshooting

### "Command not found: qauto"
-   Ensure `~/.local/bin` is in your `PATH`.
-   Try running `source ~/.bashrc` or `source ~/.zshrc` to refresh your shell.
-   Alternatively, use `python3 /path/to/qauto.py` directly.

### "response.json is EMPTY"
-   You created the file but didn't save the content. Open it and paste the JSON.

### "Invalid JSON" error
-   Ensure you only pasted the JSON object (starting with `{` and ending with `}`).
-   Remove any markdown code block markers like ```json.

### "Template file not found"
-   Check your configuration with `qauto config show`.
-   Verify the path to your Excel template exists.
