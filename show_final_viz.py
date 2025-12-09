"""
Quick script to show final visualization with collected data
Run this after main.py completes to see the graphs with data
"""

import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Module2_SystemMonitor.processor import Processor
from Module2_SystemMonitor.system_monitor import SystemMonitor
from Module1_CoreAlgorithm.load_balancer import LoadBalancer, Task
from Module3_Visualization.visualizer import SystemVisualizer
import matplotlib.pyplot as plt

# Create a quick simulation to generate data
print("Running quick simulation to generate visualization data...")

processors = [Processor(i) for i in range(4)]
monitor = SystemMonitor(processors, rebalance_threshold=0.3)
load_balancer = LoadBalancer(processors, monitor)
visualizer = SystemVisualizer(monitor)

# Generate some tasks and record metrics
for i in range(20):
    task = Task(i)
    load_balancer.assign_task(task)
    monitor.record_metrics()
    import time
    time.sleep(0.1)

# Populate visualization history
for state in monitor.metrics_history:
    visualizer.time_history.append(state['timestamp'])
    visualizer.avg_load_history.append(state['average_load'])
    visualizer.variance_history.append(state['load_variance'])

# Get current metrics
current_metrics = monitor.get_all_metrics()
for metric in current_metrics:
    proc_id = metric['processor_id']
    if proc_id not in visualizer.load_history:
        from collections import deque
        visualizer.load_history[proc_id] = deque(maxlen=100)
    visualizer.load_history[proc_id].append(metric['current_load'])

# Update and show plot
print("Generating visualization...")
visualizer.update_plot(0)
plt.show(block=True)

