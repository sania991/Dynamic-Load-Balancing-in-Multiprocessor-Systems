# Simplified Dynamic Load Balancer

## 📋 Overview

This is a simplified, easy-to-understand implementation of a dynamic workload distribution algorithm. It demonstrates how to distribute tasks across multiple processors to optimize performance and resource utilization.

## 🎯 What This Project Does

- **Dynamically distributes workloads** across multiple processors
- **Optimizes performance** by balancing load evenly
- **Adapts to varying loads** automatically
- **Shows real-time visualization** with GUI graphs
- **Allows adding processes** dynamically (1, 2, or more)

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- Required libraries: `matplotlib`, `numpy`

### Installation

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the example:**
   ```bash
   python main.py
   ```

## 📁 Project Structure

```
Simplified_LoadBalancer/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
├── main.py                   # Main example with GUI
├── core/
│   ├── __init__.py
│   ├── processor.py          # Processor class
│   ├── load_balancer.py      # Load balancing algorithm
│   └── monitor.py            # System monitoring
└── gui/
    ├── __init__.py
    └── visualizer.py         # GUI visualization
```

## 🎮 How to Use

### Running the Example

1. **Start the program:**
   ```bash
   python main.py
   ```

2. **Add processes:**
   - Click "Add Process" button to add 1 process
   - Click multiple times to add 2, 3, or more processes
   - Watch how the load balancer distributes them

3. **View real-time graphs:**
   - **Processor Load Chart**: Shows current load on each processor
   - **Queue Length Chart**: Shows number of tasks waiting
   - **Load Over Time**: Shows how load changes over time
   - **System Metrics**: Shows average load and variance

### Understanding the GUI

- **Green bars**: Low load (< 50%)
- **Orange bars**: Medium load (50-80%)
- **Red bars**: High load (> 80%)

## 🔧 How It Works

### 1. Load Balancing Algorithm

The system uses a **"Least Loaded First"** strategy:

```
When a new task arrives:
1. Check all processors' current load
2. Find the processor with minimum load
3. Assign task to that processor
4. Update processor load
```

### 2. Dynamic Rebalancing

The system automatically rebalances when:
- Load variance between processors > 30%
- Any processor exceeds 80% load

### 3. Adaptive Behavior

The system adapts its rebalancing threshold:
- **High load (>70%)**: More aggressive rebalancing (20% threshold)
- **Low load (<30%)**: Less aggressive (40% threshold)
- **Normal load**: Default (30% threshold)

## 📊 Example Usage

### Adding 1 Process
1. Click "Add Process" once
2. Watch it get assigned to the least loaded processor
3. See the load increase on that processor

### Adding 2 Processes
1. Click "Add Process" twice quickly
2. Watch them get distributed across processors
3. See how the system balances the load

### Adding Multiple Processes
1. Click "Add Process" multiple times
2. Watch the system automatically rebalance
3. See how all processors share the load

## 🎓 Key Concepts

### Load Calculation
```
Load = (Queue Length / Max Queue) × 50% + (Processing Status × 50%)
```

### Load Variance
```
Variance = Maximum Load - Minimum Load
```

### Rebalancing
When variance is too high, tasks are moved from overloaded processors to underloaded ones.

## 📈 Performance Metrics

The system tracks:
- **Average Load**: Mean load across all processors
- **Load Variance**: Difference between max and min load
- **Total Tasks**: Number of tasks processed
- **Rebalancing Count**: Number of rebalancing operations

## 🔍 Code Structure

### `core/processor.py`
- Represents a single processor
- Manages task queue
- Calculates current load

### `core/load_balancer.py`
- Implements load balancing algorithm
- Handles task assignment
- Performs rebalancing

### `core/monitor.py`
- Monitors system state
- Detects imbalances
- Collects metrics

### `gui/visualizer.py`
- Creates GUI interface
- Displays real-time graphs
- Shows system metrics

## 🛠️ Customization

### Change Number of Processors

Edit `main.py`:
```python
NUM_PROCESSORS = 4  # Change to 2, 4, 8, etc.
```

### Change Rebalancing Threshold

Edit `core/monitor.py`:
```python
REBALANCE_THRESHOLD = 0.3  # 30% variance threshold
```

### Change Task Processing Time

Edit `core/processor.py`:
```python
PROCESSING_TIME = 0.5  # seconds per task
```

## 📝 Example Output

When you run the program, you'll see:

```
Processor 0: Load=25.0%, Queue=1
Processor 1: Load=15.0%, Queue=0
Processor 2: Load=30.0%, Queue=2
Processor 3: Load=20.0%, Queue=1

[REBALANCING] Load variance too high (15%)
Migrated 1 task from Processor 2 to Processor 1
```

## 🎯 Real-World Applications

This algorithm is used in:
- **Cloud Computing**: Distributing requests across servers
- **Web Servers**: Load balancing HTTP requests
- **Database Clusters**: Distributing queries
- **Operating Systems**: CPU scheduling
- **Distributed Systems**: Task allocation

## 🐛 Troubleshooting

### GUI doesn't appear
- Make sure matplotlib is installed: `pip install matplotlib`
- Check if your system supports GUI

### Processes not balancing
- Check console output for error messages
- Verify all processors are initialized

### Performance issues
- Reduce number of processors
- Increase task processing time

## 📚 Further Reading

- See code comments for detailed explanations
- Check `main.py` for usage examples
- Review algorithm in `core/load_balancer.py`

## 👤 Author

Created as a simplified educational example of dynamic load balancing.

## 📄 License

Educational use only.

