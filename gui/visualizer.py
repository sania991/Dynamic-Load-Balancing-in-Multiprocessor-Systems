"""
GUI Visualizer Module
Creates a graphical interface with real-time charts
"""

import tkinter as tk
from tkinter import ttk
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from collections import deque
import threading
import time
from typing import List
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from core.monitor import SystemMonitor


class LoadBalancerGUI:
    """
    GUI application for visualizing load balancing
    
    Features:
    - Real-time processor load charts
    - Queue length visualization
    - Load over time graph
    - System metrics display
    - Button to add processes dynamically
    """
    
    def __init__(self, monitor: SystemMonitor, load_balancer, processors: List):
        """
        Initialize GUI
        
        Args:
            monitor: System monitor instance
            load_balancer: Load balancer instance
            processors: List of processors
        """
        self.monitor = monitor
        self.load_balancer = load_balancer
        self.processors = processors
        
        # Create main window
        self.root = tk.Tk()
        self.root.title("Dynamic Load Balancer - Real-time Visualization")
        self.root.geometry("1200x800")
        
        # Data storage for graphs
        self.time_history = deque(maxlen=50)
        self.load_history = {i: deque(maxlen=50) for i in range(len(processors))}
        self.avg_load_history = deque(maxlen=50)
        self.variance_history = deque(maxlen=50)
        
        # Task counter
        self.task_counter = 0
        
        # Setup GUI
        self._setup_gui()
        
        # Start update thread
        self.running = True
        self.update_thread = threading.Thread(target=self._update_loop, daemon=True)
        self.update_thread.start()
    
    def _setup_gui(self):
        """Setup GUI components"""
        # Create main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Configure grid weights
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)
        main_frame.columnconfigure(0, weight=1)
        main_frame.rowconfigure(1, weight=1)
        
        # Control panel
        control_frame = ttk.Frame(main_frame)
        control_frame.grid(row=0, column=0, sticky=(tk.W, tk.E), pady=(0, 10))
        
        # Add Process button
        self.add_process_btn = ttk.Button(
            control_frame,
            text="Add Process",
            command=self._add_process,
            width=20
        )
        self.add_process_btn.pack(side=tk.LEFT, padx=5)
        
        # Add Multiple Processes button
        self.add_multiple_btn = ttk.Button(
            control_frame,
            text="Add 5 Processes",
            command=self._add_multiple_processes,
            width=20
        )
        self.add_multiple_btn.pack(side=tk.LEFT, padx=5)
        
        # Metrics display
        self.metrics_label = ttk.Label(
            control_frame,
            text="Average Load: 0% | Variance: 0% | Total Tasks: 0",
            font=("Arial", 10, "bold")
        )
        self.metrics_label.pack(side=tk.LEFT, padx=20)
        
        # Create matplotlib figure
        self.fig = Figure(figsize=(12, 8), dpi=100)
        
        # Create subplots
        self.ax1 = self.fig.add_subplot(2, 2, 1)  # Processor loads
        self.ax2 = self.fig.add_subplot(2, 2, 2)  # Queue lengths
        self.ax3 = self.fig.add_subplot(2, 2, 3)  # Load over time
        self.ax4 = self.fig.add_subplot(2, 2, 4)  # Variance over time
        
        # Embed in tkinter
        self.canvas = FigureCanvasTkAgg(self.fig, main_frame)
        self.canvas.get_tk_widget().grid(row=1, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
        
        # Initial plot
        self._update_plots()
    
    def _add_process(self):
        """Add a single process"""
        from core.load_balancer import Task
        
        task = Task(self.task_counter)
        self.task_counter += 1
        
        if self.load_balancer.assign_task(task):
            print(f"Task {task.task_id} assigned to Processor {task.assigned_processor.processor_id}")
        else:
            print(f"Failed to assign Task {task.task_id}")
    
    def _add_multiple_processes(self):
        """Add multiple processes at once"""
        for _ in range(5):
            self._add_process()
            time.sleep(0.1)  # Small delay between tasks
    
    def _update_plots(self):
        """Update all plots with current data"""
        try:
            # Get current system state
            state = self.monitor.get_system_state()
            metrics = self.monitor.get_all_metrics()
            
            # Debug: Print metrics to console (can be removed later)
            if len(metrics) > 0:
                debug_info = ", ".join([f"P{m['processor_id']}: L={m['current_load']:.1f}%, Q={m['queue_length']}" 
                                      for m in metrics])
                # Only print occasionally to avoid spam
                if hasattr(self, '_last_debug_print'):
                    if time.time() - self._last_debug_print > 2.0:  # Print every 2 seconds
                        print(f"[DEBUG] Metrics: {debug_info}")
                        self._last_debug_print = time.time()
                else:
                    self._last_debug_print = time.time()
            
            # Update history
            current_time = time.time()
            if not self.time_history:
                self.start_time = current_time
            self.time_history.append(current_time)
            self.avg_load_history.append(state['average_load'])
            self.variance_history.append(state['load_variance'])
            
            for metric in metrics:
                proc_id = metric['processor_id']
                if proc_id not in self.load_history:
                    self.load_history[proc_id] = deque(maxlen=50)
                self.load_history[proc_id].append(metric['current_load'])
        except Exception as e:
            print(f"Error getting metrics: {e}")
            import traceback
            traceback.print_exc()
            return
        
        # Clear all axes
        try:
            self.ax1.clear()
            self.ax2.clear()
            self.ax3.clear()
            self.ax4.clear()
        except Exception as e:
            print(f"Error clearing axes: {e}")
            return
        
        # Get processor IDs once for both plots
        if not metrics:
            processor_ids = []
        else:
            processor_ids = [m['processor_id'] for m in metrics]
        
        # Plot 1: Current Processor Loads - Always show data
        if not metrics or not processor_ids:
            # No processors, show empty graph
            self.ax1.text(0.5, 0.5, 'No Processors', ha='center', va='center', 
                         transform=self.ax1.transAxes, fontsize=14)
            self.ax1.set_title('Current Processor Load (%)', fontsize=12, fontweight='bold')
            self.ax1.set_xlabel('Processor ID')
            self.ax1.set_ylabel('Load (%)')
            self.ax1.set_ylim(0, 100)
        else:
            current_loads = [max(m['current_load'], 0.1) for m in metrics]  # Minimum 0.1% for visibility
            colors = ['green' if load < 50 else 'orange' if load < 80 else 'red' 
                     for load in current_loads]
            
            # Always show bars with minimum height for visibility
            bars = self.ax1.bar(processor_ids, current_loads, color=colors, alpha=0.8, 
                               edgecolor='black', linewidth=1.5, width=0.7)
            self.ax1.set_title('Current Processor Load (%)', fontsize=12, fontweight='bold')
            self.ax1.set_xlabel('Processor ID')
            self.ax1.set_ylabel('Load (%)')
            self.ax1.set_ylim(0, 100)
            self.ax1.grid(True, alpha=0.3, axis='y', linestyle='--')
            self.ax1.set_xticks(processor_ids)
            
            # Add value labels on bars (always show with actual values)
            for proc_id, load, orig_load in zip(processor_ids, current_loads, [m['current_load'] for m in metrics]):
                label_y = max(load + 3, 5)  # At least 5 pixels high for visibility
                # Show actual load value (even if 0)
                self.ax1.text(proc_id, label_y, f'{orig_load:.1f}%', 
                             ha='center', va='bottom', fontsize=10, fontweight='bold',
                             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
        
        # Plot 2: Queue Lengths - Always show data
        if not metrics or not processor_ids:
            # No processors, show empty graph
            self.ax2.text(0.5, 0.5, 'No Processors', ha='center', va='center', 
                         transform=self.ax2.transAxes, fontsize=14)
            self.ax2.set_title('Task Queue Lengths', fontsize=12, fontweight='bold')
            self.ax2.set_xlabel('Processor ID')
            self.ax2.set_ylabel('Queue Length')
            self.ax2.set_ylim(0, 10)
        else:
            queue_lengths = [m['queue_length'] for m in metrics]
            # Use minimum height for visibility (0.1 for empty queues)
            display_lengths = [max(q_len, 0.1) for q_len in queue_lengths]
            max_queue = max(queue_lengths) if queue_lengths else 0
            y_max = max(5, max_queue + 2)  # Ensure minimum range for visibility (at least 5)
            self.ax2.bar(processor_ids, display_lengths, color='blue', alpha=0.8, 
                        edgecolor='black', linewidth=1.5, width=0.7)
            self.ax2.set_title('Task Queue Lengths', fontsize=12, fontweight='bold')
            self.ax2.set_xlabel('Processor ID')
            self.ax2.set_ylabel('Queue Length')
            self.ax2.set_ylim(0, y_max)
            self.ax2.grid(True, alpha=0.3, linestyle='--')
            self.ax2.set_xticks(processor_ids)
            
            # Add value labels on bars (always show with actual values)
            for proc_id, q_len in zip(processor_ids, queue_lengths):
                label_y = max(q_len + 0.3, 0.5)  # At least 0.5 for visibility
                # Show actual queue length (even if 0)
                self.ax2.text(proc_id, label_y, str(q_len), 
                             ha='center', va='bottom', fontsize=10, fontweight='bold',
                             bbox=dict(boxstyle='round,pad=0.3', facecolor='white', alpha=0.7))
        
        # Plot 3: Average Load Over Time
        if len(self.time_history) > 1:
            time_diffs = [(t - self.start_time) for t in self.time_history]
            self.ax3.plot(time_diffs, list(self.avg_load_history), 'b-', linewidth=2, label='Average Load')
            self.ax3.set_title('Average System Load Over Time', fontsize=12, fontweight='bold')
            self.ax3.set_xlabel('Time (seconds)')
            self.ax3.set_ylabel('Load (%)')
            self.ax3.set_ylim(0, 100)
            self.ax3.legend()
            self.ax3.grid(True, alpha=0.3)
        
        # Plot 4: Load Variance Over Time
        if len(self.time_history) > 1:
            time_diffs = [(t - self.start_time) for t in self.time_history]
            self.ax4.plot(time_diffs, list(self.variance_history), 'r-', linewidth=2, label='Load Variance')
            threshold = self.monitor.rebalance_threshold * 100
            self.ax4.axhline(y=threshold, color='g', linestyle='--', linewidth=2, label=f'Threshold ({threshold:.0f}%)')
            self.ax4.set_title('Load Variance Over Time', fontsize=12, fontweight='bold')
            self.ax4.set_xlabel('Time (seconds)')
            self.ax4.set_ylabel('Variance (%)')
            self.ax4.legend()
            self.ax4.grid(True, alpha=0.3)
        
        try:
            self.fig.tight_layout()
            # Use draw_idle for non-blocking updates
            self.canvas.draw_idle()
        except Exception as e:
            print(f"Error drawing canvas: {e}")
        
        # Update metrics label with more details
        try:
            stats = self.load_balancer.get_statistics()
            total_queue = state['total_queue_length']
            metrics_text = (f"Avg Load: {state['average_load']:.1f}% | "
                           f"Variance: {state['load_variance']:.1f}% | "
                           f"Tasks: {stats['total_tasks_assigned']} | "
                           f"Queue: {total_queue} | "
                           f"Rebalances: {stats['rebalance_count']}")
            self.metrics_label.config(text=metrics_text)
        except Exception as e:
            print(f"Error updating metrics label: {e}")
    
    def _update_loop(self):
        """Background thread to update plots and process tasks - Optimized to prevent hanging"""
        last_rebalance = time.time()
        last_plot_update = time.time()
        rebalance_interval = 2.0  # Check every 2 seconds
        plot_update_interval = 0.5  # Update plots every 0.5 seconds (reduced for performance)
        
        # Keep track of processing threads to ensure continuous processing
        processing_threads = {}
        
        while self.running:
            try:
                current_time = time.time()
                
                # Process tasks on all processors continuously
                for processor in self.processors:
                    if processor.get_queue_length() > 0:
                        # Check if processor is already processing (get minimal info)
                        proc_id = processor.processor_id
                        metrics = processor.get_metrics()
                        
                        # Only start a new processing thread if not already processing
                        if not metrics['is_processing']:
                            # Check if we already have a thread for this processor
                            if proc_id not in processing_threads or not processing_threads[proc_id].is_alive():
                                # Start processing in a separate thread
                                thread = threading.Thread(
                                    target=self._process_continuously,
                                    args=(processor,),
                                    daemon=True
                                )
                                thread.start()
                                processing_threads[proc_id] = thread
                
                # Periodic rebalancing
                if current_time - last_rebalance >= rebalance_interval:
                    if self.monitor.detect_imbalance():
                        self.load_balancer.adaptive_threshold_adjustment()
                        self.load_balancer.rebalance_loads()
                    self.monitor.record_metrics()
                    last_rebalance = current_time
                
                # Update plots less frequently to prevent hanging
                if current_time - last_plot_update >= plot_update_interval:
                    # Use after_idle for non-blocking updates
                    self.root.after_idle(self._update_plots)
                    last_plot_update = current_time
                
                time.sleep(0.2)  # Longer sleep to reduce CPU usage
                
            except Exception as e:
                print(f"Error in update loop: {e}")
                time.sleep(0.5)  # Wait a bit before retrying
    
    def _process_continuously(self, processor):
        """Continuously process tasks on a processor until queue is empty - Optimized"""
        while self.running:
            try:
                queue_length = processor.get_queue_length()
                if queue_length > 0:
                    # Check if already processing (get minimal metrics)
                    metrics = processor.get_metrics()
                    if not metrics['is_processing']:
                        # Process task
                        processor.process_task(processing_time=0.5)
                    else:
                        time.sleep(0.1)  # Wait if already processing
                else:
                    # Queue empty, exit this thread (new one will be created if needed)
                    break
            except Exception as e:
                print(f"Error processing task on Processor {processor.processor_id}: {e}")
                break  # Exit thread on error, will be recreated if needed
    
    def run(self):
        """Start the GUI main loop"""
        print("\n" + "="*60)
        print("GUI is running. Add tasks using the buttons.")
        print("The system will process tasks continuously.")
        print("Close the window to exit.")
        print("="*60 + "\n")
        self.root.mainloop()
        self.running = False
        print("\n[GUI Closed] Shutting down...")

