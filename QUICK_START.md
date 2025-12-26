# Quick Start Guide

## 🚀 Get Started in 3 Steps

### Step 1: Install Dependencies

```bash
pip install -r requirements.txt
```

### Step 2: Run the Example

```bash
python main.py
```

### Step 3: Use the GUI

1. **Click "Add Process"** - Adds 1 process
2. **Click "Add 5 Processes"** - Adds 5 processes at once
3. **Watch the graphs** - See real-time load balancing

## 📊 What You'll See

### GUI Window Contains:

1. **Top Left**: Current Processor Loads (Bar Chart)
   - Green: Low load (<50%)
   - Orange: Medium load (50-80%)
   - Red: High load (>80%)

2. **Top Right**: Task Queue Lengths
   - Shows how many tasks are waiting in each processor's queue

3. **Bottom Left**: Average Load Over Time
   - Line graph showing how system load changes

4. **Bottom Right**: Load Variance Over Time
   - Shows how balanced the system is
   - Green line shows rebalancing threshold

### Console Output:

```
Task 0 assigned to Processor 1
Task 1 assigned to Processor 0
[REBALANCING] Migrated 2 tasks
```

## 🎯 Try These Examples

### Example 1: Add 1 Process
- Click "Add Process" once
- Watch it get assigned to the least loaded processor
- See the load increase on that processor

### Example 2: Add 2 Processes
- Click "Add Process" twice
- Watch them get distributed across different processors
- See how the system balances the load

### Example 3: Add Multiple Processes
- Click "Add 5 Processes" button
- Watch the system automatically rebalance
- See how tasks are migrated between processors

## 💡 Understanding the Output

### Processor Load
- **0-50%**: Processor is lightly loaded
- **50-80%**: Processor is moderately loaded
- **80-100%**: Processor is heavily loaded (may trigger rebalancing)

### Load Variance
- **Low variance (<30%)**: Load is well balanced
- **High variance (>30%)**: Load is imbalanced (triggers rebalancing)

### Rebalancing
- When variance is too high, tasks are moved from busy processors to idle ones
- This happens automatically every 2 seconds

## 🐛 Troubleshooting

### GUI doesn't appear
- Make sure matplotlib is installed: `pip install matplotlib`
- Check console for error messages

### Nothing happens when clicking buttons
- Check console output for errors
- Make sure all dependencies are installed

### Graphs not updating
- Wait a few seconds for the update cycle
- Check if processes are being added (look at console)

## 📚 Next Steps

- Read the full README.md for detailed documentation
- Explore the code in `core/` directory
- Modify parameters in `main.py` to experiment
- Try changing number of processors

## 🎓 Learning Points

1. **Load Balancing**: Tasks are distributed to keep processors balanced
2. **Dynamic Adaptation**: System adjusts based on current load
3. **Automatic Rebalancing**: System moves tasks when imbalance is detected
4. **Real-time Monitoring**: All metrics update continuously

Enjoy exploring the load balancer! 🚀

