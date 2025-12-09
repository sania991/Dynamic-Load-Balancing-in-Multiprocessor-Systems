# Dynamic Workload Distribution Algorithm

## Project Overview

This project implements an algorithm that dynamically distributes workloads across multiple processors to optimize performance and resource utilization. The solution adapts to varying process loads and system states.

### Real-World Applications

This algorithm is used in:
- **Cloud Computing** (AWS, Google Cloud, Azure) - Distributing requests across servers
- **Web Servers** - Load balancing HTTP requests
- **Database Clusters** - Distributing queries across database servers
- **Microservices** - Balancing service requests
- **CDN** - Distributing content delivery
- **Gaming Servers** - Balancing player load

### What This Project Does

This project **simulates a multi-processor computer system** and demonstrates how to intelligently distribute work (tasks) across multiple processors to keep them balanced and efficient.

**Real-World Analogy:**
Imagine you're a manager with 4 workers (processors) and tasks keep coming in. Instead of giving all tasks to one worker (who gets overwhelmed) or randomly assigning them, this system:
- Monitors how busy each worker is
- Assigns new tasks to the least busy worker
- Automatically moves tasks between workers when one gets too busy
- Adapts its strategy based on how much work is coming in

**What It Demonstrates:**
1. **Load Balancing**: Distributes tasks evenly across processors
2. **Dynamic Adaptation**: Adjusts behavior based on current system state
3. **Performance Optimization**: Prevents any single processor from becoming a bottleneck
4. **Real-time Monitoring**: Tracks system performance continuously
5. **Visualization**: Shows what's happening with graphs and metrics

**Practical Applications:**
- **Cloud Computing**: Distributing requests across multiple servers
- **Data Centers**: Balancing workloads across server clusters
- **Operating Systems**: CPU scheduling and process distribution
- **Web Servers**: Load balancing incoming requests
- **Distributed Systems**: Task allocation in parallel computing

## Quick Start

### One-Click Setup

**Windows Users:**
1. Double-click `setup.bat` to install all requirements
2. Run `python main.py` to start the simulation

**Linux/Mac Users:**
1. Run: `chmod +x setup.sh && ./setup.sh`
2. Run `python3 main.py` to start the simulation

For detailed installation instructions, see [INSTALL.md](INSTALL.md)

## Project Structure
```
.
├── Module1_CoreAlgorithm/     # Core load balancing algorithm
├── Module2_SystemMonitor/     # System state monitoring
├── Module3_Visualization/     # Visualization and reporting
├── main.py                    # Main entry point
├── setup.bat                  # One-click setup for Windows
├── setup.sh                   # One-click setup for Linux/Mac
├── requirements.txt           # Python dependencies
├── requirements.txt           # Python dependencies
└── README.md                  # This file
```

## 🚀 Quick Start

**New to this project?** Start here:
- **[WINDOWS_USAGE_GUIDE.md](WINDOWS_USAGE_GUIDE.md)** - ⭐ **Complete Windows guide** (Recommended for Windows users)
- **[QUICK_START.md](QUICK_START.md)** - Simple step-by-step guide
- **[USAGE_GUIDE.md](USAGE_GUIDE.md)** - Detailed usage instructions

**Windows Users - Easiest Method**: 
1. Double-click `setup.bat` to install all requirements (one-click setup!)
2. Then run: `python main.py` to start the simulation
3. Or follow the **[WINDOWS_USAGE_GUIDE.md](WINDOWS_USAGE_GUIDE.md)** for step-by-step instructions

## Installation

### ⚡ One-Click Setup (Recommended)

**Windows Users:**
1. Double-click `setup.bat` - it will automatically install all requirements!
2. Wait for installation to complete
3. Run `python main.py` to start

**Linux/Mac Users:**
```bash
chmod +x setup.sh && ./setup.sh
```

### Manual Installation

1. **Install Python 3.7 or higher**
   - Download from: https://www.python.org/downloads/
   - ⚠️ **Important**: Check "Add Python to PATH" during installation

2. **Install dependencies**:
   ```bash
   py -m pip install -r requirements.txt
   ```
   Or: `python -m pip install -r requirements.txt`

For detailed troubleshooting, see [INSTALL.md](INSTALL.md)

## 📖 How to Use It

### Method 1: Automatic Setup (Windows - Easiest)

1. **Double-click** `setup_and_run.bat`
2. The script will:
   - Check if Python is installed
   - Install required libraries automatically
   - Run the simulation
3. **That's it!** Watch the console and visualization window

---

### Method 2: Manual Setup

#### Step 1: Verify Python Installation

Open terminal/command prompt and check:

```bash
py --version
```

or

```bash
python --version
```

**Expected output:** `Python 3.x.x` (where x is 7 or higher)

**If Python is not installed:**
1. Go to https://www.python.org/downloads/
2. Download Python 3.8 or higher
3. **⚠️ IMPORTANT:** During installation, check ✅ "Add Python to PATH"
4. Click "Install Now"
5. Restart your terminal

#### Step 2: Navigate to Project Folder

Open terminal in the project directory:

**Windows:**
- Right-click in the folder → "Open PowerShell window here"
- Or press `Shift + Right-click` → "Open PowerShell window here"

**Mac/Linux:**
```bash
cd /path/to/project/folder
```

#### Step 3: Install Required Libraries

```bash
py -m pip install -r requirements.txt
```

**Alternative commands if `py` doesn't work:**
```bash
python -m pip install -r requirements.txt
python3 -m pip install -r requirements.txt
```

**Expected output:**
```
Collecting numpy...
Collecting matplotlib...
Collecting plotly...
Successfully installed numpy-x.x.x matplotlib-x.x.x plotly-x.x.x
```

#### Step 4: Run the Simulation

```bash
py main.py
```

**Alternative:**
```bash
python main.py
```

---

### What You'll See When Running

#### 1. Console Output

The terminal will display:

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

**Understanding the output:**
- **Task X assigned to Processor Y**: New task created and assigned
- **[System State]**: Periodic status update (every 5 seconds)
- **[REBALANCING TRIGGERED]**: System detected imbalance and rebalanced
- **Processor X: Load=Y%, Queue=Z**: Current state of each processor

#### 2. Visualization Window

A matplotlib window will open showing **4 real-time graphs**:

**Top Left - Current Processor Loads:**
- Bar chart showing load percentage for each processor
- **Green bars**: Load < 50% (healthy)
- **Orange bars**: Load 50-80% (moderate)
- **Red bars**: Load > 80% (overloaded)

**Top Right - Task Queue Lengths:**
- Number of tasks waiting in each processor's queue
- Helps identify which processors are busiest

**Bottom Left - Average System Load Over Time:**
- Line graph showing overall system utilization
- Updates in real-time as simulation runs

**Bottom Right - Load Variance Over Time:**
- Measures how evenly distributed the load is
- Green dashed line shows rebalancing threshold
- Lower variance = better load balance

#### 3. Final Performance Report

When simulation ends (after 60 seconds or Ctrl+C), you'll see:

```
============================================================
SIMULATION COMPLETE
============================================================

==================================================
PERFORMANCE REPORT
==================================================
Timestamp: 2025-12-09 22:50:30
Average Load: 45.23%
Load Variance: 12.50%
Load Balance Efficiency: 87.50%
Total Tasks Completed: 120
Average Processing Time: 0.185s
Total Queue Length: 8
==================================================

LOAD BALANCER STATISTICS:
  Total Tasks Assigned: 125
  Rebalance Operations: 8
  Task Migrations: 15
============================================================
```

**Understanding the metrics:**
- **Average Load**: Mean CPU utilization across all processors
- **Load Variance**: Difference between most/least loaded processors
- **Load Balance Efficiency**: How evenly distributed (higher = better)
- **Total Tasks Completed**: Number of tasks processed
- **Rebalance Operations**: How many times system rebalanced
- **Task Migrations**: Total tasks moved between processors

---

### Customizing the Simulation

Edit `main.py` to change simulation parameters:

```python
# Configuration (around lines 36-40)
NUM_PROCESSORS = 4              # Number of processors (try 2, 4, 8)
TASK_GENERATION_RATE = 2        # Tasks per second (higher = more load)
SIMULATION_DURATION = 60        # How long to run (in seconds)
REBALANCE_INTERVAL = 2          # Rebalancing check frequency (seconds)
```

#### Example Configurations

**Light Load Test:**
```python
NUM_PROCESSORS = 4
TASK_GENERATION_RATE = 1
SIMULATION_DURATION = 30
```

**Heavy Load Test:**
```python
NUM_PROCESSORS = 4
TASK_GENERATION_RATE = 5
SIMULATION_DURATION = 60
```

**More Processors:**
```python
NUM_PROCESSORS = 8
TASK_GENERATION_RATE = 3
SIMULATION_DURATION = 90
```

**Faster Rebalancing:**
```python
REBALANCE_INTERVAL = 1  # Check every second
```

---

### Controlling the Simulation

**Stop the simulation:**
- Press `Ctrl + C` in the terminal
- Or close the visualization window
- The program will show final statistics before exiting

**Pause/Resume:**
- The simulation runs continuously
- You can minimize the window and check back later
- Graphs update in real-time

---

### Troubleshooting

#### ❌ "Python was not found" or "Python is not recognized"

**Solution:**
1. Install Python from https://www.python.org/downloads/
2. Make sure to check "Add Python to PATH" during installation
3. Restart your terminal after installation
4. Try using `py` instead of `python` on Windows

#### ❌ "No module named 'matplotlib'" or "ModuleNotFoundError"

**Solution:**
```bash
py -m pip install matplotlib numpy plotly
```

Or reinstall all requirements:
```bash
py -m pip install --upgrade -r requirements.txt
```

#### ❌ "Permission denied" or "Access is denied"

**Solution (Windows):**
- Run PowerShell/Command Prompt as Administrator
- Or install for current user only:
```bash
py -m pip install --user -r requirements.txt
```

#### ❌ Visualization window doesn't appear

**Solution:**
1. Check if window is behind other windows (minimize others)
2. Make sure matplotlib is installed: `py -m pip install matplotlib`
3. Try closing and reopening the program
4. Check if your system supports GUI (some servers don't)

#### ❌ Program runs too fast/slow

**Solution:**
- Adjust `TASK_GENERATION_RATE` in `main.py`:
  - Lower value (0.5-1) = slower, easier to observe
  - Higher value (3-5) = faster, more load
- Adjust `SIMULATION_DURATION` to run longer/shorter

#### ❌ "pip is not recognized"

**Solution:**
Use Python's module installer instead:
```bash
py -m pip install -r requirements.txt
```

---

### Testing Your Installation

Quick test to verify everything works:

```bash
py -c "import numpy, matplotlib; print('✅ All libraries installed successfully!')"
```

If you see the success message, you're ready to run the simulation!

---

### Next Steps After Running

1. **Observe the behavior**: Watch how tasks are distributed
2. **Experiment**: Try different configurations
3. **Analyze results**: Review the performance report
4. **Modify code**: Add your own features or algorithms
5. **Document**: Record your observations for the project report

---

### Example Usage Session

```bash
# 1. Install dependencies (first time only)
py -m pip install -r requirements.txt

# 2. Run the simulation
py main.py

# 3. Watch the console output and visualization

# 4. After 60 seconds (or press Ctrl+C), see final report

# 5. Modify main.py to try different configurations

# 6. Run again to see different behavior
py main.py
```

## Modules
- **Module 1**: Core Load Balancing Algorithm
- **Module 2**: System State Monitor
- **Module 3**: Visualization and Reporting

---

## 🔧 How It Works

### System Architecture

The system consists of three main modules working together to achieve dynamic workload distribution:

```
┌─────────────────────────────────────────────────────────┐
│                    Task Generator                        │
│              (Creates tasks with varying loads)          │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Module 1: Load Balancer                     │
│  • Receives new tasks                                    │
│  • Queries System Monitor for processor states           │
│  • Assigns tasks using "Least Loaded First" strategy     │
│  • Periodically rebalances loads                         │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│         Module 2: System State Monitor                   │
│  • Continuously monitors all processors                  │
│  • Collects metrics (load, queue length, etc.)           │
│  • Detects load imbalances                               │
│  • Identifies overloaded/underloaded processors          │
└──────┬──────────────────────────────┬───────────────────┘
       │                              │
       ▼                              ▼
┌──────────────┐            ┌──────────────┐
│ Processor 1  │            │ Processor N  │
│ • Task Queue │            │ • Task Queue │
│ • Load %     │            │ • Load %     │
│ • Processing │            │ • Processing │
└──────────────┘            └──────────────┘
       │                              │
       └──────────────┬───────────────┘
                      │
                      ▼
┌─────────────────────────────────────────────────────────┐
│         Module 3: Visualization & Reporting               │
│  • Real-time graphs of processor states                  │
│  • Performance metrics calculation                       │
│  • Historical data tracking                              │
└─────────────────────────────────────────────────────────┘
```

---

### Core Algorithm: Dynamic Load Balancing

#### 1. **Task Assignment Strategy**

When a new task arrives, the system uses the **"Least Loaded First"** algorithm:

```
1. New Task Created
   ↓
2. Query System Monitor for all processor loads
   ↓
3. Find processor with minimum current load
   ↓
4. Check if processor queue has space
   ↓
5. Assign task to selected processor
   ↓
6. Update processor load metrics
```

**Example:**
- Processor 0: 45% load, Queue: 3 tasks
- Processor 1: 30% load, Queue: 1 task
- Processor 2: 60% load, Queue: 5 tasks
- Processor 3: 25% load, Queue: 0 tasks

**Result:** Task assigned to Processor 3 (lowest load)

#### 2. **Load Rebalancing Mechanism**

The system periodically checks for load imbalances and redistributes tasks:

**Rebalancing Trigger Conditions:**
- Load variance > 30% (difference between max and min processor loads)
- Any processor exceeds 80% load threshold
- Periodic check every 2 seconds (configurable)

**Rebalancing Process:**
```
1. Detect Imbalance
   ↓
2. Identify Overloaded Processors (>70% load)
   ↓
3. Identify Underloaded Processors (<40% load)
   ↓
4. Calculate tasks to migrate (half of overloaded queue)
   ↓
5. Migrate tasks from overloaded to underloaded processors
   ↓
6. Update all processor loads
```

**Example Rebalancing:**
- Before: P0=85%, P1=20%, P2=90%, P3=15%
- Action: Migrate 3 tasks from P0 to P1, 4 tasks from P2 to P3
- After: P0=55%, P1=50%, P2=60%, P3=45%

#### 3. **Adaptive Threshold Management**

The system dynamically adjusts rebalancing sensitivity based on overall system load:

```python
if average_load > 70%:
    threshold = 0.2  # More aggressive rebalancing (20% variance)
elif average_load < 30%:
    threshold = 0.4  # Less aggressive (40% variance)
else:
    threshold = 0.3  # Default (30% variance)
```

**Why?** 
- High load: Need quick response to prevent bottlenecks
- Low load: Can tolerate more variance to reduce overhead
- Normal load: Balanced approach

---

### Module 2: System State Monitoring

#### Processor State Tracking

Each processor maintains:
- **Current Load**: 0-100% based on queue length and processing status
- **Task Queue**: FIFO queue of pending tasks
- **Processing Status**: Whether currently executing a task
- **Statistics**: Total tasks completed, average processing time

**Load Calculation:**
```
Load = (Queue Factor × 50%) + (Processing Factor × 50%)
Where:
- Queue Factor = min(queue_length / max_queue_size, 1.0)
- Processing Factor = 50% if processing, 0% if idle
```

#### Imbalance Detection

The monitor continuously evaluates:
1. **Load Variance**: `max_load - min_load`
2. **Individual Thresholds**: Any processor > 80%
3. **System Average**: Overall system utilization

**Detection Logic:**
```python
if (max_load - min_load) > (threshold × 100):
    return True  # Imbalance detected
if any_processor.load > 80:
    return True  # Overload detected
return False
```

---

### Module 3: Visualization & Reporting

#### Real-Time Monitoring

The visualization displays four key metrics:

1. **Current Processor Loads** (Bar Chart)
   - Shows load percentage for each processor
   - Color-coded: Green (<50%), Orange (50-80%), Red (>80%)

2. **Task Queue Lengths** (Bar Chart)
   - Number of tasks waiting in each processor's queue
   - Helps identify bottlenecks

3. **Average System Load Over Time** (Line Graph)
   - Tracks overall system utilization
   - Shows load trends and patterns

4. **Load Variance Over Time** (Line Graph)
   - Measures how evenly distributed the load is
   - Lower variance = better balance
   - Shows rebalancing threshold line

#### Performance Metrics

The system calculates:
- **Average Load**: Mean CPU utilization across all processors
- **Load Variance**: Difference between most and least loaded processors
- **Load Balance Efficiency**: `100 - (variance / ideal_load × 100)`
- **Throughput**: Tasks completed per second
- **Average Response Time**: Mean time to process a task

---

### How the System Adapts to Varying Loads

#### Scenario 1: Sudden Load Spike

```
Initial State:
- P0: 30%, P1: 25%, P2: 35%, P3: 20%

Sudden Spike (many tasks arrive):
- P0: 85%, P1: 20%, P2: 90%, P3: 15%

System Response:
1. Monitor detects variance > 30% threshold
2. Identifies P0 and P2 as overloaded
3. Identifies P1 and P3 as underloaded
4. Migrates tasks: P0→P1, P2→P3
5. Adjusts threshold to 0.2 (more aggressive)

Result:
- P0: 55%, P1: 50%, P2: 60%, P3: 45%
- Load balanced within 2 seconds
```

#### Scenario 2: Gradual Load Increase

```
As load gradually increases:
1. System monitors continuously
2. Threshold adapts: 0.3 → 0.2 (more sensitive)
3. Rebalancing becomes more frequent
4. Prevents any single processor from becoming bottleneck
```

#### Scenario 3: Load Decrease

```
When load decreases:
1. Threshold adapts: 0.2 → 0.4 (less sensitive)
2. Rebalancing becomes less frequent
3. Reduces overhead during low-load periods
```

---

### Technical Implementation Details

#### Concurrency Model

- **Multi-threading**: Each processor runs in its own thread
- **Thread Safety**: Locks protect shared data structures
- **Non-blocking**: Task assignment doesn't block processing

#### Task Processing

```python
# Each processor thread continuously:
while running:
    if queue_not_empty:
        task = queue.popleft()
        process_task(task)  # Simulated processing time
        update_metrics()
    else:
        sleep(0.1)  # Wait for tasks
```

#### Load Calculation Update

Load is recalculated when:
- Task added to queue
- Task removed from queue
- Task processing starts/completes
- Task migration occurs

#### Performance Optimization

- **Efficient Queue Operations**: Using `deque` for O(1) operations
- **Lazy Evaluation**: Metrics calculated on-demand
- **History Limiting**: Only last 1000 records kept in memory
- **Configurable Intervals**: Adjustable monitoring and rebalancing frequency

---

### Algorithm Complexity

- **Task Assignment**: O(n) where n = number of processors
- **Load Rebalancing**: O(n × m) where m = average queue length
- **Imbalance Detection**: O(n)
- **Overall**: Efficient for typical processor counts (4-16 processors)

---

### Key Features

✅ **Dynamic Adaptation**: Adjusts to changing load patterns  
✅ **Real-time Monitoring**: Continuous state tracking  
✅ **Automatic Rebalancing**: No manual intervention needed  
✅ **Thread-safe**: Concurrent task processing  
✅ **Visual Feedback**: Real-time graphs and metrics  
✅ **Configurable**: Adjustable parameters for different scenarios  

---

## GitHub Repository
[Add your GitHub repository link here]

## Author
[Your Name]

## Course
CSE 316 - Operating Systems


