# Installation Guide

## Prerequisites

- **Python 3.7 or higher**
- **pip** (Python package installer)

## Step-by-Step Installation

### Step 1: Check Python Installation

Open a terminal/command prompt and run:

```bash
python --version
```

or

```bash
python3 --version
```

You should see something like: `Python 3.8.0` or higher.

**If Python is not installed:**
1. Download from: https://www.python.org/downloads/
2. During installation, **check "Add Python to PATH"**
3. Restart your terminal after installation

### Step 2: Navigate to Project Directory

```bash
cd Simplified_LoadBalancer
```

### Step 3: Install Dependencies

```bash
pip install -r requirements.txt
```

**Alternative commands if `pip` doesn't work:**
```bash
python -m pip install -r requirements.txt
python3 -m pip install -r requirements.txt
```

### Step 4: Verify Installation

Run this to check if all libraries are installed:

```bash
python -c "import matplotlib, numpy; print('✅ All libraries installed!')"
```

If you see the success message, you're ready to go!

## Running the Program

```bash
python main.py
```

## Troubleshooting

### "Python was not found"

**Solution:**
1. Install Python from https://www.python.org/downloads/
2. Make sure to check "Add Python to PATH" during installation
3. Restart your terminal

### "No module named 'matplotlib'"

**Solution:**
```bash
pip install matplotlib numpy
```

### "Permission denied" (Windows)

**Solution:**
Run terminal as Administrator, or use:
```bash
pip install --user -r requirements.txt
```

### GUI doesn't appear

**Solution:**
1. Make sure matplotlib is installed: `pip install matplotlib`
2. Check if your system supports GUI (some servers don't)
3. Look for error messages in the console

## What Gets Installed

- **matplotlib**: For creating graphs and visualizations
- **numpy**: For numerical operations (used by matplotlib)

That's it! The project uses only standard libraries plus these two.

## Next Steps

After installation, see [QUICK_START.md](QUICK_START.md) to learn how to use the program.

