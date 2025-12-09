"""
Module 2: System State Monitor
Monitors and tracks the state of all processors
"""

import time
from typing import List, Dict
import sys
import os

# Add current directory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)

from processor import Processor


class SystemMonitor:
    """Monitors system state and detects when load balancing is needed"""
    
    def __init__(self, processors: List[Processor], rebalance_threshold=0.3):
        self.processors = processors
        self.rebalance_threshold = rebalance_threshold  # Threshold for triggering rebalancing
        self.monitoring_active = False
        self.metrics_history = []
        
    def get_all_metrics(self) -> List[Dict]:
        """Collect metrics from all processors"""
        return [processor.get_metrics() for processor in self.processors]
    
    def get_system_state(self) -> Dict:
        """Get overall system state"""
        metrics = self.get_all_metrics()
        total_load = sum(m['current_load'] for m in metrics)
        avg_load = total_load / len(metrics) if metrics else 0
        max_load = max((m['current_load'] for m in metrics), default=0)
        min_load = min((m['current_load'] for m in metrics), default=0)
        total_queue = sum(m['queue_length'] for m in metrics)
        
        return {
            'average_load': avg_load,
            'max_load': max_load,
            'min_load': min_load,
            'load_variance': max_load - min_load,
            'total_queue_length': total_queue,
            'processor_count': len(metrics),
            'timestamp': time.time()
        }
    
    def detect_imbalance(self) -> bool:
        """Detect if load balancing is needed"""
        state = self.get_system_state()
        load_variance = state['load_variance']
        
        # Trigger rebalancing if variance exceeds threshold
        if load_variance > (self.rebalance_threshold * 100):
            return True
        
        # Also check if any processor is overloaded
        metrics = self.get_all_metrics()
        for metric in metrics:
            if metric['current_load'] > 80:  # 80% threshold
                return True
        
        return False
    
    def get_most_loaded_processor(self) -> Processor:
        """Get the processor with the highest load"""
        return max(self.processors, key=lambda p: p.get_current_load())
    
    def get_least_loaded_processor(self) -> Processor:
        """Get the processor with the lowest load"""
        return min(self.processors, key=lambda p: p.get_current_load())
    
    def get_overloaded_processors(self, threshold=80) -> List[Processor]:
        """Get list of processors exceeding the load threshold"""
        return [p for p in self.processors if p.get_current_load() > threshold]
    
    def get_underloaded_processors(self, threshold=30) -> List[Processor]:
        """Get list of processors below the load threshold"""
        return [p for p in self.processors if p.get_current_load() < threshold]
    
    def record_metrics(self):
        """Record current metrics to history"""
        state = self.get_system_state()
        self.metrics_history.append(state)
        
        # Keep only last 1000 records
        if len(self.metrics_history) > 1000:
            self.metrics_history.pop(0)
    
    def get_metrics_history(self) -> List[Dict]:
        """Get historical metrics"""
        return self.metrics_history


