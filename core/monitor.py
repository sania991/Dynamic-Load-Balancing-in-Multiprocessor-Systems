"""
System Monitor Module
Monitors system state and detects when rebalancing is needed
"""

import time
from typing import List, Dict
from .processor import Processor


class SystemMonitor:
    """
    Monitors the state of all processors and detects imbalances
    
    Responsibilities:
    - Track all processor states
    - Calculate system-wide metrics
    - Detect when load balancing is needed
    - Identify overloaded and underloaded processors
    """
    
    def __init__(self, processors: List[Processor], rebalance_threshold=0.3):
        """
        Initialize system monitor
        
        Args:
            processors: List of all processors to monitor
            rebalance_threshold: Load variance threshold for rebalancing (0.3 = 30%)
        """
        self.processors = processors
        self.rebalance_threshold = rebalance_threshold
        self.metrics_history = []  # Store historical metrics
    
    def get_system_state(self) -> Dict:
        """
        Get current state of the entire system
        
        Returns:
            Dictionary with system-wide metrics
        """
        # Get metrics from all processors
        processor_loads = [p.get_current_load() for p in self.processors]
        queue_lengths = [p.get_queue_length() for p in self.processors]
        
        if not processor_loads:
            return {
                'average_load': 0.0,
                'max_load': 0.0,
                'min_load': 0.0,
                'load_variance': 0.0,
                'total_queue_length': 0,
                'processor_count': 0,
                'timestamp': time.time()
            }
        
        # Calculate metrics
        average_load = sum(processor_loads) / len(processor_loads)
        max_load = max(processor_loads)
        min_load = min(processor_loads)
        load_variance = max_load - min_load
        total_queue_length = sum(queue_lengths)
        
        return {
            'average_load': average_load,
            'max_load': max_load,
            'min_load': min_load,
            'load_variance': load_variance,
            'total_queue_length': total_queue_length,
            'processor_count': len(self.processors),
            'timestamp': time.time()
        }
    
    def detect_imbalance(self) -> bool:
        """
        Detect if system load is imbalanced and needs rebalancing
        
        Returns:
            True if rebalancing is needed, False otherwise
        """
        state = self.get_system_state()
        load_variance = state['load_variance']
        
        # Check if variance exceeds threshold
        variance_threshold = self.rebalance_threshold * 100  # Convert to percentage
        if load_variance > variance_threshold:
            return True
        
        # Also check if any processor is overloaded (>80%)
        for processor in self.processors:
            if processor.get_current_load() > 80.0:
                return True
        
        return False
    
    def get_least_loaded_processor(self) -> Processor:
        """
        Get the processor with the lowest current load
        
        Returns:
            Processor with minimum load
        """
        return min(self.processors, key=lambda p: p.get_current_load())
    
    def get_most_loaded_processor(self) -> Processor:
        """
        Get the processor with the highest current load
        
        Returns:
            Processor with maximum load
        """
        return max(self.processors, key=lambda p: p.get_current_load())
    
    def get_overloaded_processors(self, threshold=70.0) -> List[Processor]:
        """
        Get list of processors that exceed the load threshold
        
        Args:
            threshold: Load threshold (default 70%)
            
        Returns:
            List of overloaded processors
        """
        return [p for p in self.processors if p.get_current_load() > threshold]
    
    def get_underloaded_processors(self, threshold=40.0) -> List[Processor]:
        """
        Get list of processors below the load threshold
        
        Args:
            threshold: Load threshold (default 40%)
            
        Returns:
            List of underloaded processors
        """
        return [p for p in self.processors if p.get_current_load() < threshold]
    
    def record_metrics(self):
        """Record current system state to history"""
        state = self.get_system_state()
        self.metrics_history.append(state)
        
        # Keep only last 100 records to prevent memory issues
        if len(self.metrics_history) > 100:
            self.metrics_history.pop(0)
    
    def get_metrics_history(self) -> List[Dict]:
        """Get historical metrics"""
        return self.metrics_history
    
    def get_all_metrics(self) -> List[Dict]:
        """
        Get metrics from all processors
        
        Returns:
            List of processor metrics dictionaries
        """
        return [processor.get_metrics() for processor in self.processors]
    
    def adjust_rebalance_threshold(self, average_load: float):
        """
        Dynamically adjust rebalancing threshold based on system load
        
        Args:
            average_load: Current average system load
        """
        if average_load > 70.0:
            # High load: be more aggressive (lower threshold)
            self.rebalance_threshold = 0.2
        elif average_load < 30.0:
            # Low load: be less aggressive (higher threshold)
            self.rebalance_threshold = 0.4
        else:
            # Normal load: default threshold
            self.rebalance_threshold = 0.3

