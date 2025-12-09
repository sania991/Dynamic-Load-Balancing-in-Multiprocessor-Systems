"""
Main entry point for Dynamic Workload Distribution System
Simulates a multi-processor system with dynamic load balancing
"""

import time
import random
import threading
import sys
import os

# Add current directory to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from Module2_SystemMonitor.processor import Processor
from Module2_SystemMonitor.system_monitor import SystemMonitor
from Module1_CoreAlgorithm.load_balancer import LoadBalancer, Task
from Module3_Visualization.visualizer import SystemVisualizer
import matplotlib.pyplot as plt


def simulate_task_processing(processor: Processor, running: threading.Event):
    """Simulate continuous task processing on a processor"""
    while running.is_set():
        if processor.get_queue_length() > 0:
            processor.process_task(task_duration=random.uniform(0.2, 0.5))  # Slower to see activity
        else:
            time.sleep(0.1)


def main():
    """Main function to run the load balancing simulation"""
    print("="*60, flush=True)
    print("Dynamic Workload Distribution System", flush=True)
    print("="*60, flush=True)
    
    # Configuration
    NUM_PROCESSORS = 4
    TASK_GENERATION_RATE = 3  # Tasks per second
    SIMULATION_DURATION = 30  # seconds
    REBALANCE_INTERVAL = 2
    
    # Initialize processors
    print(f"\nInitializing {NUM_PROCESSORS} processors...", flush=True)
    processors = [Processor(i) for i in range(NUM_PROCESSORS)]
    
    # Initialize system monitor
    monitor = SystemMonitor(processors, rebalance_threshold=0.3)
    
    # Initialize load balancer
    load_balancer = LoadBalancer(processors, monitor)
    
    # Initialize visualizer
    visualizer = SystemVisualizer(monitor)
    
    # Start processing threads for each processor
    running = threading.Event()
    running.set()
    processing_threads = []
    
    print("Starting processor threads...", flush=True)
    for processor in processors:
        thread = threading.Thread(target=simulate_task_processing, args=(processor, running))
        thread.daemon = True
        thread.start()
        processing_threads.append(thread)
    
    # Show visualization window first
    plt.ion()  # Turn on interactive mode
    plt.figure(visualizer.fig.number)  # Ensure we're using the right figure
    visualizer.update_plot(0)  # Initial plot
    plt.show(block=False)  # Show window without blocking
    plt.pause(0.2)  # Give it time to render
    print("Visualization window opened. You should see 4 empty plots that will fill with data.", flush=True)
    
    # Start visualization in separate thread
    viz_running = threading.Event()
    viz_running.set()
    
    def update_visualization():
        """Update visualization continuously"""
        import matplotlib.pyplot as plt
        while viz_running.is_set():
            try:
                visualizer.update_plot(0)
                plt.pause(0.5)  # Update every 0.5 seconds
            except Exception as e:
                print(f"Viz update error: {e}", flush=True)
                break
    
    viz_thread = threading.Thread(target=update_visualization)
    viz_thread.daemon = True
    viz_thread.start()
    
    print(f"\nStarting simulation for {SIMULATION_DURATION} seconds...", flush=True)
    print("Generating tasks and monitoring system...", flush=True)
    print("Visualization window should be open showing live updates.\n", flush=True)
    
    # Wait a moment for visualization to initialize
    time.sleep(0.5)
    
    start_time = time.time()
    last_rebalance = start_time
    last_state_print = start_time
    task_id = 0
    task_interval = 1.0 / TASK_GENERATION_RATE
    
    # Record initial metrics
    monitor.record_metrics()
    
    # Generate first task immediately
    task = Task(task_id)
    task_id += 1
    if load_balancer.assign_task(task):
        proc_id = task.assigned_processor.processor_id
        print(f"Task {task.task_id} assigned to Processor {proc_id}", flush=True)
    last_task_time = time.time()
    
    # Force an immediate visualization update
    visualizer.update_plot(0)
    plt.pause(0.1)
    
    try:
        while time.time() - start_time < SIMULATION_DURATION:
            current_time = time.time()
            elapsed = current_time - start_time
            
            # Generate tasks at specified rate
            if current_time - last_task_time >= task_interval:
                task = Task(task_id)
                task_id += 1
                if load_balancer.assign_task(task):
                    proc_id = task.assigned_processor.processor_id
                    print(f"Task {task.task_id} assigned to Processor {proc_id}", flush=True)
                last_task_time = current_time
            
            # Periodic rebalancing
            if current_time - last_rebalance >= REBALANCE_INTERVAL:
                if monitor.detect_imbalance():
                    print("\n[REBALANCING TRIGGERED]", flush=True)
                    load_balancer.adaptive_threshold_adjustment()
                    load_balancer.rebalance_loads()
                last_rebalance = current_time
            
            # Record metrics
            monitor.record_metrics()
            
            # Force visualization update every second
            if int(elapsed) != int(current_time - start_time - 0.1):
                visualizer.update_plot(0)
                plt.pause(0.01)
            
            # Print current state every 3 seconds
            if current_time - last_state_print >= 3.0:
                state = monitor.get_system_state()
                metrics = monitor.get_all_metrics()
                print(f"\n[{elapsed:.1f}s] Avg Load: {state['average_load']:.1f}%, "
                      f"Variance: {state['load_variance']:.1f}%, "
                      f"Queue: {state['total_queue_length']}", flush=True)
                proc_loads = [f"P{m['processor_id']}:{m['current_load']:.1f}%" for m in metrics]
                print(f"  Processor loads: {proc_loads}", flush=True)
                last_state_print = current_time
            
            time.sleep(0.1)
    
    except KeyboardInterrupt:
        print("\n\nSimulation interrupted by user", flush=True)
    
    finally:
        # Stop processing
        running.clear()
        viz_running.clear()
        time.sleep(1)
        
        # Generate final report
        print("\n" + "="*60, flush=True)
        print("SIMULATION COMPLETE", flush=True)
        print("="*60, flush=True)
        visualizer.print_report()
        
        stats = load_balancer.get_statistics()
        print("LOAD BALANCER STATISTICS:", flush=True)
        print(f"  Total Tasks Assigned: {stats['total_tasks_assigned']}", flush=True)
        print(f"  Rebalance Operations: {stats['rebalance_count']}", flush=True)
        print(f"  Task Migrations: {stats['migration_count']}", flush=True)
        print("="*60, flush=True)
        
        print("\nVisualization window will stay open. Close it to exit.", flush=True)
        plt.show(block=True)


if __name__ == "__main__":
    main()
