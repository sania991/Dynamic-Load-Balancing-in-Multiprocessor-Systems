# How It Works - Visual Guide

## 🔄 System Flow

```
┌─────────────────────────────────────────────────────────┐
│                    User Clicks Button                    │
│              "Add Process" or "Add 5 Processes"          │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│                  Task Created (Task ID)                   │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Load Balancer: Assign Task                    │
│  Algorithm: "Least Loaded First"                         │
│  1. Check all processors' current load                    │
│  2. Find processor with minimum load                      │
│  3. Assign task to that processor                        │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Processor: Add to Queue                      │
│  - Task added to processor's queue                       │
│  - Load updated: Load = (Queue × 50%) + (Processing × 50%)│
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│              Processor: Process Task                      │
│  - Remove task from queue                                │
│  - Simulate processing (0.5 seconds)                      │
│  - Update statistics                                     │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
┌─────────────────────────────────────────────────────────┐
│            System Monitor: Check Balance                  │
│  Every 2 seconds:                                        │
│  - Calculate load variance                                │
│  - Detect if rebalancing needed                           │
└──────────────────────┬──────────────────────────────────┘
                       │
                       ▼
         ┌─────────────┴─────────────┐
         │                            │
    Balanced?                    Imbalanced?
         │                            │
         ▼                            ▼
    Continue              ┌──────────────────────┐
                          │   Rebalancing         │
                          │  - Find overloaded    │
                          │  - Find underloaded   │
                          │  - Migrate tasks      │
                          └──────────┬────────────┘
                                     │
                                     ▼
                          ┌──────────────────────┐
                          │   Load Balanced      │
                          └──────────────────────┘
```

## 📊 Load Calculation

### Formula:
```
Load = (Queue Factor × 50%) + (Processing Factor × 50%)

Where:
- Queue Factor = min(queue_length / max_queue_size, 1.0) × 50
- Processing Factor = 50 if processing, 0 if idle
```

### Example:
```
Processor with:
- Queue: 3 tasks (max 10) → Queue Factor = (3/10) × 50 = 15%
- Currently processing → Processing Factor = 50%
- Total Load = 15% + 50% = 65%
```

## ⚖️ Rebalancing Logic

### When Rebalancing Occurs:

1. **Load Variance > 30%**
   ```
   Example:
   Processor 0: 85% load
   Processor 1: 20% load
   Processor 2: 90% load
   Processor 3: 15% load
   
   Variance = 90% - 15% = 75% > 30% → REBALANCE!
   ```

2. **Any Processor > 80% Load**
   ```
   Example:
   Processor 2: 85% load → REBALANCE!
   ```

### Rebalancing Process:

```
1. Identify Overloaded Processors (>70% load)
   → Processor 0: 85%, Processor 2: 90%

2. Identify Underloaded Processors (<40% load)
   → Processor 1: 20%, Processor 3: 15%

3. Migrate Tasks
   - Take half of tasks from overloaded processors
   - Move to underloaded processors
   - Update loads

4. Result
   → Processor 0: 55%
   → Processor 1: 50%
   → Processor 2: 60%
   → Processor 3: 45%
   → Variance: 15% < 30% ✓
```

## 🎯 Adaptive Thresholds

The system adjusts rebalancing sensitivity based on overall load:

```
High Load (>70% average):
  → Threshold = 20% (more aggressive)
  → Rebalances more frequently
  → Prevents bottlenecks

Normal Load (30-70% average):
  → Threshold = 30% (default)
  → Balanced approach

Low Load (<30% average):
  → Threshold = 40% (less aggressive)
  → Rebalances less frequently
  → Reduces overhead
```

## 📈 GUI Update Cycle

```
Every 0.5 seconds:
  1. Process tasks on all processors
  2. Update processor loads
  3. Record metrics
  4. Update graphs
  5. Update metrics display

Every 2 seconds:
  1. Check for imbalance
  2. Perform rebalancing if needed
  3. Adjust threshold if needed
```

## 🔍 Example Scenario

### Scenario: Adding 5 Processes

```
Initial State:
  Processor 0: 20% load, Queue: 1
  Processor 1: 15% load, Queue: 0
  Processor 2: 25% load, Queue: 2
  Processor 3: 10% load, Queue: 0

User clicks "Add 5 Processes"

Step 1: Task 0 assigned
  → Processor 3 (lowest: 10%)
  → Processor 3: 25% load, Queue: 1

Step 2: Task 1 assigned
  → Processor 1 (lowest: 15%)
  → Processor 1: 30% load, Queue: 1

Step 3: Task 2 assigned
  → Processor 0 (lowest: 20%)
  → Processor 0: 35% load, Queue: 2

Step 4: Task 3 assigned
  → Processor 1 (lowest: 15%, but now 30%)
  → Actually Processor 3 (lowest: 25%)
  → Processor 3: 40% load, Queue: 2

Step 5: Task 4 assigned
  → Processor 1 (lowest: 30%)
  → Processor 1: 45% load, Queue: 2

After 2 seconds: Rebalancing Check
  → Variance = 45% - 35% = 10% < 30%
  → No rebalancing needed ✓

Final State:
  Processor 0: 35% load, Queue: 2
  Processor 1: 45% load, Queue: 2
  Processor 2: 25% load, Queue: 2
  Processor 3: 40% load, Queue: 2
  → Well balanced!
```

## 🎨 Graph Colors Explained

### Processor Load Chart:
- **🟢 Green**: Load < 50% (Healthy)
- **🟠 Orange**: Load 50-80% (Moderate)
- **🔴 Red**: Load > 80% (High - may trigger rebalancing)

### Variance Chart:
- **Blue Line**: Current variance
- **Green Dashed Line**: Rebalancing threshold (30%)
- When blue line crosses green line → Rebalancing occurs

## 🔄 Task Lifecycle

```
1. CREATED
   → Task object created with unique ID

2. ASSIGNED
   → Load balancer assigns to least loaded processor
   → Task added to processor's queue

3. QUEUED
   → Task waits in queue
   → Processor load increases

4. PROCESSING
   → Processor removes task from queue
   → Task is processed (simulated 0.5 seconds)
   → Processor load remains high

5. COMPLETED
   → Task processing finished
   → Statistics updated
   → Processor load decreases
```

## 📊 Metrics Explained

### Average Load
- Mean load across all processors
- Shows overall system utilization
- Higher = more work being done

### Load Variance
- Difference between max and min processor loads
- Lower = better balance
- When > 30%, triggers rebalancing

### Queue Length
- Number of tasks waiting in each processor
- Should be distributed evenly
- High queue = backlog

### Rebalance Count
- Number of times system rebalanced
- Shows how dynamic the load is
- Higher = more adaptation needed

## 🎓 Key Takeaways

1. **Tasks go to least loaded processor** - Simple but effective
2. **System monitors continuously** - Detects imbalances quickly
3. **Rebalancing is automatic** - No manual intervention needed
4. **System adapts** - Thresholds adjust based on load
5. **Visualization helps** - Graphs show what's happening

---

**Want to see it in action?** Run `python main.py` and click "Add Process"!

