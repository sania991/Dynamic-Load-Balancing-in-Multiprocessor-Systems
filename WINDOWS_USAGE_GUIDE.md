# How to Use This Project on Windows - Complete Guide

## 🪟 Windows-Specific Instructions

### Method 1: Easiest Way (Automatic)

1. **Double-click** the file: `setup_and_run.bat`
2. That's it! The script will:
   - Check if Python is installed
   - Install required libraries
   - Run the simulation automatically

---

### Method 2: Step-by-Step Manual Method

#### Step 1: Open PowerShell in Project Folder

**Option A - Right-click method:**
1. Navigate to the project folder: `C:\Users\harry\OneDrive\Desktop\sania rana`
2. Right-click in an empty area of the folder
3. Select **"Open in Terminal"** or **"Open PowerShell window here"**

**Option B - From File Explorer:**
1. Open File Explorer
2. Navigate to: `C:\Users\harry\OneDrive\Desktop\sania rana`
3. Click in the address bar
4. Type `powershell` and press Enter

**Option C - From Start Menu:**
1. Press `Windows Key`
2. Type `PowerShell`
3. Right-click "Windows PowerShell" → "Run as Administrator" (optional)
4. Type: `cd "C:\Users\harry\OneDrive\Desktop\sania rana"`
5. Press Enter

#### Step 2: Check Python Installation

In PowerShell, type:
```powershell
python --version
```

**If you see a version number** (like `Python 3.12.0`):
- ✅ Python is installed! Skip to Step 3

**If you see "Python was not found":**
- You need to install Python first
- See: `INSTALL_PYTHON_WINDOWS.md` for detailed instructions
- Or go to: https://www.python.org/downloads/
- **Important**: Check "Add Python to PATH" during installation

**Alternative command:**
```powershell
py --version
```
(This is the Python launcher - works even if PATH isn't set)

#### Step 3: Install Required Libraries

In PowerShell, type:
```powershell
python -m pip install -r requirements.txt
```

**Or if `python` doesn't work:**
```powershell
py -m pip install -r requirements.txt
```

**Expected output:**
```
Collecting numpy...
Collecting matplotlib...
Collecting plotly...
Successfully installed numpy-x.x.x matplotlib-x.x.x plotly-x.x.x
```

**If you see "Requirement already satisfied":**
- ✅ Libraries are already installed! Skip to Step 4

#### Step 4: Run the Simulation

**Full simulation (60 seconds):**
```powershell
python main.py
```

**Or:**
```powershell
py main.py
```

**Quick test (15 seconds):**
```powershell
python test_run.py
```

---

## 📺 What You'll See

### In PowerShell Window:

```
============================================================
Dynamic Workload Distribution System
============================================================

Initializing 4 processors...
Starting processor threads...

Starting simulation for 60 seconds...
Generating tasks and monitoring system...

Task 0 assigned to Processor 2
Task 1 assigned to Processor 1
Task 2 assigned to Processor 0
Task 3 assigned to Processor 3
...

[System State] Avg Load: 45.2%, Variance: 12.5%, Total Queue: 8
  Processor 0: Load=42.3%, Queue=2
  Processor 1: Load=38.1%, Queue=1
  Processor 2: Load=51.2%, Queue=3
  Processor 3: Load=49.0%, Queue=2

[REBALANCING TRIGGERED]
Rebalanced: Migrated 2 tasks
...
```

### Visualization Window:

A new window will open showing 4 graphs:
- **Top Left**: Current processor loads (bars)
- **Top Right**: Task queue lengths
- **Bottom Left**: Average load over time
- **Bottom Right**: Load variance over time

**Note**: The visualization window appears at the END of the simulation (after 60 seconds)

---

## 🎮 Controlling the Program

### To Stop the Program:
- Press `Ctrl + C` in PowerShell
- Or close the PowerShell window
- Or close the visualization window (if open)

### To Pause:
- The program runs continuously
- You can minimize PowerShell and check back later
- Graphs update in real-time

### To Run Again:
- Just type the command again:
```powershell
python main.py
```

---

## ⚙️ Customizing for Windows

### Change Simulation Settings:

1. **Open `main.py` in Notepad:**
   - Right-click `main.py`
   - Select "Open with" → "Notepad"
   - Or use any text editor

2. **Find these lines** (around line 37-40):
```python
NUM_PROCESSORS = 4
TASK_GENERATION_RATE = 2
SIMULATION_DURATION = 60
REBALANCE_INTERVAL = 2
```

3. **Modify as needed:**
```python
NUM_PROCESSORS = 4              # Number of processors
TASK_GENERATION_RATE = 5         # More tasks = more activity (try 3-10)
SIMULATION_DURATION = 30         # Shorter = faster results (try 20-30)
REBALANCE_INTERVAL = 1           # Check more often (try 1-3)
```

4. **Save the file** (Ctrl+S)
5. **Run again:**
```powershell
python main.py
```

---

## 🔧 Windows-Specific Troubleshooting

### ❌ "Python was not found"

**Solution 1 - Use Python Launcher:**
```powershell
py main.py
```

**Solution 2 - Install Python:**
1. Go to: https://www.python.org/downloads/
2. Download Python 3.8 or higher
3. **IMPORTANT**: Check ✅ "Add Python to PATH"
4. Install
5. Restart PowerShell
6. Try again

**Solution 3 - Add Python to PATH manually:**
1. Find Python installation (usually `C:\Users\YourName\AppData\Local\Programs\Python\Python3xx\`)
2. Press `Windows Key`, type "environment"
3. Click "Edit the system environment variables"
4. Click "Environment Variables"
5. Under "User variables", select "Path" → "Edit"
6. Click "New" and add Python path
7. Click "OK" on all windows
8. **Restart PowerShell**

### ❌ "pip is not recognized"

**Solution:**
Use Python's module installer:
```powershell
python -m pip install -r requirements.txt
```

Or:
```powershell
py -m pip install -r requirements.txt
```

### ❌ "Access is denied" or "Permission denied"

**Solution 1 - Run as Administrator:**
1. Right-click PowerShell icon
2. Select "Run as Administrator"
3. Navigate to project folder
4. Run commands again

**Solution 2 - Install for current user only:**
```powershell
python -m pip install --user -r requirements.txt
```

### ❌ Visualization window doesn't appear

**Possible causes:**
1. Window is behind other windows - minimize others
2. Matplotlib not installed - run: `python -m pip install matplotlib`
3. System doesn't support GUI - some Windows Server versions don't

**Check if matplotlib works:**
```powershell
python -c "import matplotlib; print('Matplotlib installed!')"
```

### ❌ "No module named 'processor'" or import errors

**Solution:**
Make sure you're in the project folder:
```powershell
cd "C:\Users\harry\OneDrive\Desktop\sania rana"
python main.py
```

### ❌ Program runs but no output

**This is normal!** The program:
- Generates tasks every 0.5 seconds
- Shows state updates every 5 seconds
- Final report after 60 seconds

**To see more activity:**
- Use `test_run.py` for faster demo
- Or increase `TASK_GENERATION_RATE` in `main.py`

---

## 📋 Quick Reference Commands

### Check Python:
```powershell
python --version
py --version
```

### Install libraries:
```powershell
python -m pip install -r requirements.txt
```

### Run simulation:
```powershell
python main.py
```

### Quick test:
```powershell
python test_run.py
```

### Stop program:
```
Ctrl + C
```

---

## 🎯 Recommended First Run

For your first time, use the quick test:

```powershell
python test_run.py
```

This will:
- Run for only 15 seconds
- Show more activity
- Give you results faster
- Help you understand what's happening

---

## 📁 File Locations

**Project folder:**
```
C:\Users\harry\OneDrive\Desktop\sania rana
```

**Main files:**
- `main.py` - Main simulation (60 seconds)
- `test_run.py` - Quick test (15 seconds)
- `setup_and_run.bat` - Automatic setup script
- `requirements.txt` - Required libraries

**Documentation:**
- `README.md` - Complete project documentation
- `WINDOWS_USAGE_GUIDE.md` - This file
- `QUICK_START.md` - Quick start guide
- `INSTALL_PYTHON_WINDOWS.md` - Python installation guide

---

## ✅ Success Checklist

Before running, make sure:
- [ ] Python is installed (`python --version` works)
- [ ] Libraries are installed (`pip install -r requirements.txt` completed)
- [ ] You're in the project folder
- [ ] PowerShell is open in the project directory

Then run:
```powershell
python main.py
```

---

## 🆘 Still Having Issues?

1. **Check Python installation:**
   ```powershell
   python --version
   ```

2. **Check libraries:**
   ```powershell
   python -c "import numpy, matplotlib; print('OK')"
   ```

3. **Try Python launcher:**
   ```powershell
   py main.py
   ```

4. **Read error messages** - they usually tell you what's wrong

5. **Check file locations** - make sure you're in the right folder

---

## 🎉 You're Ready!

Once everything is set up, just run:
```powershell
python main.py
```

And watch the load balancing algorithm in action!

The program will show you:
- ✅ How tasks are distributed
- ✅ How processors balance loads
- ✅ When rebalancing happens
- ✅ Performance metrics

Enjoy exploring the dynamic workload distribution system! 🚀

