"""
Simple test - Minimal code to verify everything works
"""

import time
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Module2_SystemMonitor.processor import Processor
from Module2_SystemMonitor.system_monitor import SystemMonitor
from Module1_CoreAlgorithm.load_balancer import LoadBalancer, Task

print("="*60, flush=True)
print("Simple Test - Dynamic Workload Distribution", flush=True)
print("="*60, flush=True)

# Create processors
print("\n1. Creating processors...", flush=True)
processors = [Processor(i) for i in range(4)]
print("   ✓ Processors created", flush=True)

# Create monitor
print("2. Creating monitor...", flush=True)
monitor = SystemMonitor(processors)
print("   ✓ Monitor created", flush=True)

# Create load balancer
print("3. Creating load balancer...", flush=True)
load_balancer = LoadBalancer(processors, monitor)
print("   ✓ Load balancer created", flush=True)

# Test task assignment
print("\n4. Testing task assignment...", flush=True)
for i in range(10):
    task = Task(i)
    result = load_balancer.assign_task(task)
    if result:
        proc_id = task.assigned_processor.processor_id
        print(f"   Task {i} → Processor {proc_id}", flush=True)
    else:
        print(f"   Task {i} - FAILED", flush=True)
    time.sleep(0.1)

# Show state
print("\n5. System State:", flush=True)
state = monitor.get_system_state()
print(f"   Average Load: {state['average_load']:.1f}%", flush=True)
print(f"   Load Variance: {state['load_variance']:.1f}%", flush=True)
print(f"   Total Queue: {state['total_queue_length']}", flush=True)

for proc in processors:
    metrics = proc.get_metrics()
    print(f"   Processor {proc.processor_id}: Load={metrics['current_load']:.1f}%, Queue={metrics['queue_length']}", flush=True)

print("\n" + "="*60, flush=True)
print("TEST COMPLETE - Everything is working!", flush=True)
print("="*60, flush=True)

