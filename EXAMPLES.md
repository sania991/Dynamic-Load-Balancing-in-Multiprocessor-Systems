# Usage Examples

## Example 1: Adding a Single Process

**Goal**: Add 1 process and see how it gets assigned

**Steps**:
1. Run `python main.py`
2. Click "Add Process" button once
3. Observe:
   - Console shows: `Task 0 assigned to Processor X`
   - Top-left graph shows load increase on that processor
   - Queue length graph shows 1 task in that processor's queue

**Expected Result**:
- Task is assigned to the processor with lowest current load
- That processor's load increases
- Other processors remain unchanged

---

## Example 2: Adding Two Processes

**Goal**: Add 2 processes and see load distribution

**Steps**:
1. Run `python main.py`
2. Click "Add Process" twice (quickly)
3. Observe:
   - Two tasks are created
   - They may be assigned to different processors
   - Load is distributed across processors

**Expected Result**:
- Tasks are distributed to keep load balanced
- If one processor is less loaded, both might go there
- If processors are balanced, tasks go to different processors

---

## Example 3: Adding Multiple Processes

**Goal**: Add 5 processes at once and watch rebalancing

**Steps**:
1. Run `python main.py`
2. Click "Add 5 Processes" button
3. Observe:
   - 5 tasks are created quickly
   - System distributes them across processors
   - If imbalance occurs, rebalancing happens automatically
   - Console may show: `[REBALANCING] Migrated X tasks`

**Expected Result**:
- Tasks are initially distributed
- If load variance > 30%, rebalancing occurs
- Tasks are migrated from overloaded to underloaded processors
- System becomes balanced

---

## Example 4: Observing Load Balancing Over Time

**Goal**: Watch how the system adapts to varying loads

**Steps**:
1. Run `python main.py`
2. Add processes gradually:
   - Click "Add Process" once
   - Wait 3 seconds
   - Click "Add Process" again
   - Wait 3 seconds
   - Click "Add 5 Processes"
3. Watch the graphs:
   - **Bottom-left**: Average load increases over time
   - **Bottom-right**: Variance spikes when processes are added, then decreases after rebalancing
   - **Top graphs**: Show current state

**Expected Result**:
- Average load graph shows gradual increase
- Variance graph shows spikes that get smoothed out
- System automatically rebalances every 2 seconds if needed

---

## Example 5: Understanding Rebalancing

**Goal**: See rebalancing in action

**Steps**:
1. Run `python main.py`
2. Click "Add 5 Processes" multiple times quickly
3. Watch console output for rebalancing messages
4. Observe variance graph (bottom-right)

**Expected Result**:
- When variance exceeds 30% threshold (green line), rebalancing triggers
- Console shows: `[REBALANCING] Migrated X tasks`
- Variance decreases after rebalancing
- Load becomes more evenly distributed

---

## Example 6: Processor Load States

**Goal**: Understand different load states

**Steps**:
1. Run `python main.py`
2. Add processes until you see different colors in the load chart:
   - **Green**: < 50% load (healthy)
   - **Orange**: 50-80% load (moderate)
   - **Red**: > 80% load (high, may trigger rebalancing)

**Expected Result**:
- Processors change color as load increases
- Red processors trigger rebalancing
- System tries to keep all processors in green/orange range

---

## Understanding the Metrics

### Average Load
- Shows overall system utilization
- Higher = more work being done
- Ideal: 50-70% for good balance

### Load Variance
- Measures how evenly distributed the load is
- Lower = better balance
- When > 30%, rebalancing occurs

### Queue Length
- Number of tasks waiting to be processed
- Higher = more backlog
- Should be distributed evenly

### Rebalance Count
- Number of times system rebalanced
- Higher = more dynamic load changes
- Shows system is adapting

---

## Tips for Best Results

1. **Add processes gradually** to see step-by-step distribution
2. **Add many processes quickly** to see rebalancing in action
3. **Watch the variance graph** to understand when rebalancing occurs
4. **Check console output** for detailed information
5. **Let it run for a while** to see long-term behavior

---

## Common Patterns

### Pattern 1: Initial Distribution
- New tasks go to least loaded processor
- Load increases on that processor
- Other processors remain idle

### Pattern 2: Rebalancing
- Load variance increases
- System detects imbalance
- Tasks migrate from busy to idle processors
- Variance decreases

### Pattern 3: Steady State
- Load is balanced
- New tasks distributed evenly
- Minimal rebalancing needed

---

## Experiment Ideas

1. **Change number of processors** in `main.py`:
   ```python
   NUM_PROCESSORS = 2  # Try 2, 4, 8
   ```

2. **Change rebalance threshold** in `core/monitor.py`:
   ```python
   rebalance_threshold=0.2  # More aggressive (20%)
   ```

3. **Change processing time** in `gui/visualizer.py`:
   ```python
   args=(1.0,)  # Slower processing (1 second)
   ```

4. **Add processes programmatically** by modifying `main.py` to add tasks automatically

---

## Questions to Explore

- What happens when you add 10 processes at once?
- How does the system handle a sudden spike in load?
- What's the optimal number of processors for your workload?
- How does rebalancing threshold affect performance?
- What happens if one processor is much faster than others?

Happy experimenting! 🚀

