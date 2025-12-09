"""
Module 3: Visualization and Reporting
Provides visual representation and performance metrics
"""

import matplotlib.pyplot as plt
import matplotlib.animation as animation
from collections import deque
from typing import List, Dict
import time
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Module2_SystemMonitor.system_monitor import SystemMonitor


class SystemVisualizer:
    """Visualizes system state and performance metrics"""
    
    def __init__(self, monitor: SystemMonitor):
        self.monitor = monitor
        self.fig, self.axes = plt.subplots(2, 2, figsize=(15, 10))
        self.fig.suptitle('Dynamic Load Balancing System Monitor', fontsize=16)
        
        # Data storage for plotting
        self.time_history = deque(maxlen=100)
        self.load_history = {i: deque(maxlen=100) for i in range(len(monitor.processors))}
        self.avg_load_history = deque(maxlen=100)
        self.variance_history = deque(maxlen=100)
        
    def update_plot(self, frame):
        """Update plots with current system state"""
        try:
            state = self.monitor.get_system_state()
            metrics = self.monitor.get_all_metrics()
            current_time = time.time()
            
            # Always update history to show trends
            if len(self.time_history) == 0 or abs(self.time_history[-1] - current_time) > 0.1:
                self.time_history.append(current_time)
                self.avg_load_history.append(state['average_load'])
                self.variance_history.append(state['load_variance'])
            
            # Update processor load history
            for metric in metrics:
                proc_id = metric['processor_id']
                if proc_id not in self.load_history:
                    self.load_history[proc_id] = deque(maxlen=100)
                # Always append current load for real-time display
                if len(self.load_history[proc_id]) == 0 or self.load_history[proc_id][-1] != metric['current_load']:
                    self.load_history[proc_id].append(metric['current_load'])
        except Exception as e:
            print(f"Error in update_plot: {e}", flush=True)
            return
        
        # Clear axes
        for ax in self.axes.flat:
            ax.clear()
        
        # Plot 1: Current Processor Loads (Bar Chart)
        ax1 = self.axes[0, 0]
        if metrics and len(metrics) > 0:
            processor_ids = [m['processor_id'] for m in metrics]
            current_loads = [m['current_load'] for m in metrics]
            # Ensure we have valid data
            if len(processor_ids) > 0 and len(current_loads) > 0:
                colors = ['green' if load < 50 else 'orange' if load < 80 else 'red' for load in current_loads]
                bars = ax1.bar(processor_ids, current_loads, color=colors, width=0.6, edgecolor='black', linewidth=1)
                # Add value labels on bars
                for i, (pid, load) in enumerate(zip(processor_ids, current_loads)):
                    if load > 0:
                        ax1.text(pid, load + 1, f'{load:.1f}%', ha='center', va='bottom', fontsize=8)
                ax1.set_title('Current Processor Load (%)', fontsize=12, fontweight='bold')
                ax1.set_xlabel('Processor ID')
                ax1.set_ylabel('Load (%)')
                ax1.set_ylim(0, 100)
                ax1.set_xticks(processor_ids)
                ax1.grid(True, alpha=0.3, linestyle='--')
            else:
                ax1.text(0.5, 0.5, 'No processor data', ha='center', va='center', transform=ax1.transAxes, fontsize=12)
                ax1.set_title('Current Processor Load (%)')
                ax1.set_ylim(0, 100)
        else:
            ax1.text(0.5, 0.5, 'Waiting for data...', ha='center', va='center', transform=ax1.transAxes, fontsize=12)
            ax1.set_title('Current Processor Load (%)')
            ax1.set_ylim(0, 100)
        
        # Plot 2: Queue Lengths
        ax2 = self.axes[0, 1]
        if metrics and len(metrics) > 0:
            processor_ids = [m['processor_id'] for m in metrics]
            queue_lengths = [m['queue_length'] for m in metrics]
            if len(processor_ids) > 0 and len(queue_lengths) > 0:
                bars = ax2.bar(processor_ids, queue_lengths, color='blue', alpha=0.7, width=0.6, edgecolor='black', linewidth=1)
                # Add value labels on bars
                for pid, qlen in zip(processor_ids, queue_lengths):
                    if qlen > 0:
                        ax2.text(pid, qlen + 0.1, f'{qlen}', ha='center', va='bottom', fontsize=8)
                ax2.set_title('Task Queue Lengths', fontsize=12, fontweight='bold')
                ax2.set_xlabel('Processor ID')
                ax2.set_ylabel('Queue Length')
                ax2.set_xticks(processor_ids)
                if max(queue_lengths) > 0:
                    ax2.set_ylim(0, max(queue_lengths) + 1)
                else:
                    ax2.set_ylim(0, 5)
                ax2.grid(True, alpha=0.3, linestyle='--')
            else:
                ax2.text(0.5, 0.5, 'No queue data', ha='center', va='center', transform=ax2.transAxes, fontsize=12)
                ax2.set_title('Task Queue Lengths')
        else:
            ax2.text(0.5, 0.5, 'Waiting for data...', ha='center', va='center', transform=ax2.transAxes, fontsize=12)
            ax2.set_title('Task Queue Lengths')
        
        # Plot 3: Average Load Over Time
        ax3 = self.axes[1, 0]
        if len(self.time_history) > 0 and len(self.avg_load_history) > 0:
            if len(self.time_history) == 1:
                # Single point - show as bar
                ax3.bar([0], [self.avg_load_history[0]], 
                       color='blue', alpha=0.7, label='Average Load', width=0.5)
                ax3.set_xlim(-1, 1)
            else:
                time_diffs = [(t - self.time_history[0]) for t in self.time_history]
                ax3.plot(time_diffs, list(self.avg_load_history), 'b-', label='Average Load', linewidth=2, marker='o', markersize=3)
                if len(time_diffs) > 0:
                    ax3.set_xlim(0, max(time_diffs) + 1)
            ax3.set_title('Average System Load Over Time')
            ax3.set_xlabel('Time (seconds)')
            ax3.set_ylabel('Load (%)')
            ax3.set_ylim(0, 100)
            ax3.legend()
            ax3.grid(True, alpha=0.3)
        else:
            ax3.text(0.5, 0.5, 'Collecting data...', 
                    ha='center', va='center', transform=ax3.transAxes, fontsize=12)
            ax3.set_title('Average System Load Over Time')
            ax3.set_ylim(0, 100)
        
        # Plot 4: Load Variance Over Time
        ax4 = self.axes[1, 1]
        if len(self.time_history) > 0 and len(self.variance_history) > 0:
            if len(self.time_history) == 1:
                # Single point
                ax4.bar([0], [self.variance_history[0]], 
                       color='red', alpha=0.7, label='Load Variance', width=0.5)
                ax4.set_xlim(-1, 1)
            else:
                time_diffs = [(t - self.time_history[0]) for t in self.time_history]
                ax4.plot(time_diffs, list(self.variance_history), 'r-', label='Load Variance', linewidth=2, marker='o', markersize=3)
                if len(time_diffs) > 0:
                    ax4.set_xlim(0, max(time_diffs) + 1)
            ax4.axhline(y=self.monitor.rebalance_threshold * 100, color='g', 
                       linestyle='--', label='Rebalance Threshold', linewidth=2)
            ax4.set_title('Load Variance Over Time')
            ax4.set_xlabel('Time (seconds)')
            ax4.set_ylabel('Variance (%)')
            ax4.set_ylim(0, 50)
            ax4.legend()
            ax4.grid(True, alpha=0.3)
        else:
            ax4.text(0.5, 0.5, 'Collecting data...', 
                    ha='center', va='center', transform=ax4.transAxes, fontsize=12)
            ax4.set_title('Load Variance Over Time')
            ax4.set_ylim(0, 50)
        
        plt.tight_layout()
    
    def start_live_monitoring(self, interval=500):
        """Start live monitoring with animation"""
        ani = animation.FuncAnimation(self.fig, self.update_plot, interval=interval, blit=False)
        plt.show()
    
    def generate_performance_report(self) -> Dict:
        """Generate a performance report"""
        state = self.monitor.get_system_state()
        metrics = self.monitor.get_all_metrics()
        
        total_tasks = sum(m['total_tasks_completed'] for m in metrics)
        avg_processing_time = sum(m['average_processing_time'] for m in metrics) / len(metrics)
        
        # Calculate load balance efficiency
        loads = [m['current_load'] for m in metrics]
        if loads:
            ideal_load = sum(loads) / len(loads)
            variance = sum((l - ideal_load) ** 2 for l in loads) / len(loads)
            efficiency = max(0, 100 - (variance / ideal_load * 100)) if ideal_load > 0 else 0
        else:
            efficiency = 0
        
        return {
            'timestamp': time.strftime('%Y-%m-%d %H:%M:%S'),
            'average_load': state['average_load'],
            'load_variance': state['load_variance'],
            'total_tasks_completed': total_tasks,
            'average_processing_time': avg_processing_time,
            'load_balance_efficiency': efficiency,
            'processor_count': len(metrics),
            'total_queue_length': state['total_queue_length']
        }
    
    def print_report(self):
        """Print performance report to console"""
        report = self.generate_performance_report()
        print("\n" + "="*50)
        print("PERFORMANCE REPORT")
        print("="*50)
        print(f"Timestamp: {report['timestamp']}")
        print(f"Average Load: {report['average_load']:.2f}%")
        print(f"Load Variance: {report['load_variance']:.2f}%")
        print(f"Load Balance Efficiency: {report['load_balance_efficiency']:.2f}%")
        print(f"Total Tasks Completed: {report['total_tasks_completed']}")
        print(f"Average Processing Time: {report['average_processing_time']:.3f}s")
        print(f"Total Queue Length: {report['total_queue_length']}")
        print("="*50 + "\n")


