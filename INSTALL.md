# Installation Guide

This guide will help you set up the Dynamic Workload Distribution System on your computer.

## Quick Setup (One-Click)

### Windows Users
1. Double-click `setup.bat`
2. Wait for the installation to complete
3. Run `python main.py` to start the simulation

### Linux/Mac Users
1. Open terminal in the project directory
2. Run: `chmod +x setup.sh && ./setup.sh`
3. Run `python3 main.py` to start the simulation

## Manual Setup

If the one-click setup doesn't work, follow these steps:

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Step 1: Check Python Installation
```bash
# Windows
python --version

# Linux/Mac
python3 --version
```

If Python is not installed, download it from [python.org](https://www.python.org/downloads/)

### Step 2: Install Requirements
```bash
# Windows
python -m pip install --upgrade pip
python -m pip install -r requirements.txt

# Linux/Mac
python3 -m pip install --upgrade pip --user
python3 -m pip install -r requirements.txt --user
```

### Step 3: Verify Installation
Run the test script:
```bash
# Windows
python SIMPLE_TEST.py

# Linux/Mac
python3 SIMPLE_TEST.py
```

If you see "All tests passed!", the installation is successful.

## Required Packages

The following packages are automatically installed:

- **numpy**: Numerical computing library
- **matplotlib**: Plotting and visualization library
- **plotly**: Interactive visualization (optional)
- **requests**: HTTP library (for web server adaptation example)

## Troubleshooting

### "Python is not recognized"
- Make sure Python is installed
- On Windows, check "Add Python to PATH" during installation
- Restart your terminal/command prompt after installation

### "pip is not recognized"
- Try: `python -m pip` instead of just `pip`
- Or: `python3 -m pip` on Linux/Mac

### Permission Errors (Linux/Mac)
- Use `--user` flag: `pip install --user -r requirements.txt`
- Or use `sudo` (not recommended): `sudo pip install -r requirements.txt`

### Package Installation Fails
- Update pip: `python -m pip install --upgrade pip`
- Check your internet connection
- Try installing packages one by one to identify the problematic package

## Next Steps

After installation:
1. Read `README.md` for project overview
2. Run `python main.py` to start the simulation
3. Check `HOW_TO_DEMONSTRATE.md` for presentation tips

## Support

If you encounter any issues, please check:
- Python version (should be 3.7+)
- All files are in the correct directories
- You're running commands from the project root directory

