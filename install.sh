#!/bin/bash
# TestGen Installation Script for Linux/Mac
# This script sets up the TestGen CLI tool

set -e

echo "=================================="
echo "TestGen CLI Tool - Linux/Mac Setup"
echo "=================================="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Get the directory where the script is located
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"

echo "Installation directory: $SCRIPT_DIR"
echo ""

# Check Python version
echo "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}❌ Python 3 is not installed. Please install Python 3 first.${NC}"
    exit 1
fi

PYTHON_VERSION=$(python3 --version)
echo -e "${GREEN}✓${NC} Found: $PYTHON_VERSION"
echo ""

# Check for pip via python module
echo "Checking pip installation..."
if ! python3 -m pip --version &> /dev/null; then
    echo -e "${YELLOW}⚠${NC} pip is not installed. Attempting to install via ensurepip..."
    if python3 -m ensurepip --default-pip; then
        echo -e "${GREEN}✓${NC} pip installed successfully"
    else
        echo -e "${RED}❌ Failed to install pip.${NC}"
        echo "Please install python3-pip manually."
        exit 1
    fi
fi
echo -e "${GREEN}✓${NC} pip is available"
echo ""

# Install dependencies
echo "Installing Python dependencies..."
if python3 -m pip install pyyaml openpyxl --user; then
    echo -e "${GREEN}✓${NC} Dependencies installed successfully"
else
    echo -e "${YELLOW}⚠${NC}  Some dependencies may already be installed (this is OK)"
fi
echo ""

# Make testgen.py executable
echo "Making testgen.py executable..."
chmod +x "$SCRIPT_DIR/testgen.py"
echo -e "${GREEN}✓${NC} testgen.py is now executable"
echo ""

# Option to create symlink for global access
echo "Would you like to make 'testgen' available globally? (y/n)"
read -r response

if [[ "$response" =~ ^([yY][eE][sS]|[yY])$ ]]; then
    # Try to create symlink in ~/.local/bin (user-level, no sudo needed)
    LOCAL_BIN="$HOME/.local/bin"
    mkdir -p "$LOCAL_BIN"
    
    SYMLINK="$LOCAL_BIN/testgen"
    
    if [ -L "$SYMLINK" ]; then
        echo -e "${YELLOW}⚠${NC}  Symlink already exists at $SYMLINK"
        echo "Updating symlink..."
        rm "$SYMLINK"
    fi
    
    ln -s "$SCRIPT_DIR/testgen.py" "$SYMLINK"
    echo -e "${GREEN}✓${NC} Created symlink: $SYMLINK -> $SCRIPT_DIR/testgen.py"
    
    # Check if ~/.local/bin is in PATH
    if [[ ":$PATH:" != *":$LOCAL_BIN:"* ]]; then
        echo ""
        echo -e "${YELLOW}⚠${NC}  $LOCAL_BIN is not in your PATH"
        echo "Add this line to your ~/.bashrc or ~/.zshrc:"
        echo ""
        echo "    export PATH=\"\$HOME/.local/bin:\$PATH\""
        echo ""
        echo "Then run: source ~/.bashrc  (or source ~/.zshrc)"
    else
        echo -e "${GREEN}✓${NC} $LOCAL_BIN is in your PATH"
    fi
    
    echo ""
    echo -e "${GREEN}✓${NC} You can now use 'testgen' command from anywhere!"
else
    echo "Skipping global installation."
    echo "You can run the tool using: python3 $SCRIPT_DIR/testgen.py"
fi

echo ""
echo "=================================="
echo -e "${GREEN}Installation Complete!${NC}"
echo "=================================="
echo ""
echo "Quick Start:"
echo "  1. Navigate to a directory with screenshots"
echo "  2. Run: testgen prepare"
echo "  3. Process batches with AI and save JSON"
echo "  4. Run: testgen generate"
echo ""
echo "For help: testgen --help"
echo ""
