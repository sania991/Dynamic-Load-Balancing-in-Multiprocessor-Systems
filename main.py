"""
Main Example: Dynamic Load Balancer with GUI

This example demonstrates:
1. Creating multiple processors
2. Setting up load balancing
3. Adding processes dynamically (1, 2, or more)
4. Viewing real-time visualization

Usage:
    python main.py

Then click "Add Process" to add processes and watch them get distributed!
"""

import sys
import os

# Add project root to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from core.processor import Processor
from core.monitor import SystemMonitor
from core.load_balancer import LoadBalancer
from gui.visualizer import LoadBalancerGUI


def main():
    """
    Main function to run the load balancer example
    
    This creates:
    - 4 processors
    - A system monitor
    - A load balancer
    - A GUI for visualization
    """
    print("="*60)
    print("Dynamic Load Balancer - Simplified Example")
    print("="*60)
    print("\nInitializing system...")
    
    # Configuration
    NUM_PROCESSORS = 4  # Number of processors
    
    # Create processors
    print(f"Creating {NUM_PROCESSORS} processors...")
    processors = [Processor(i) for i in range(NUM_PROCESSORS)]
    
    # Create system monitor
    print("Setting up system monitor...")
    monitor = SystemMonitor(processors, rebalance_threshold=0.3)
    
    # Create load balancer
    print("Initializing load balancer...")
    load_balancer = LoadBalancer(processors, monitor)
    
    # Print initial state
    print("\nSystem initialized!")
    print(f"Processors: {NUM_PROCESSORS}")
    print(f"Rebalance threshold: {monitor.rebalance_threshold * 100}%")
    print("\n" + "="*60)
    print("Starting GUI...")
    print("="*60)
    print("\nInstructions:")
    print("  - Click 'Add Process' to add 1 process")
    print("  - Click 'Add 5 Processes' to add multiple processes at once")
    print("  - Tasks will process continuously until queue is empty")
    print("  - Watch the graphs update in real-time")
    print("  - Close the window to exit")
    print("\n")
    
    # Create and run GUI
    gui = LoadBalancerGUI(monitor, load_balancer, processors)
    gui.run()
    
    # Print final statistics
    print("\n" + "="*60)
    print("Final Statistics")
    print("="*60)
    stats = load_balancer.get_statistics()
    print(f"Total Tasks Assigned: {stats['total_tasks_assigned']}")
    print(f"Rebalance Operations: {stats['rebalance_count']}")
    print(f"Task Migrations: {stats['migration_count']}")
    
    state = monitor.get_system_state()
    print(f"\nFinal System State:")
    print(f"  Average Load: {state['average_load']:.1f}%")
    print(f"  Load Variance: {state['load_variance']:.1f}%")
    print(f"  Total Queue Length: {state['total_queue_length']}")
    
    print("\n" + "="*60)
    print("Example completed!")
    print("="*60)


if __name__ == "__main__":
    main()

