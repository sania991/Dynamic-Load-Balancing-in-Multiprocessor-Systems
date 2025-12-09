"""
Module 1: Core Load Balancing Algorithm
Implements dynamic workload distribution across processors
"""

import time
import random
from typing import List, Optional
import sys
import os

# Add parent directory to path to import from Module2
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from Module2_SystemMonitor.processor import Processor
from Module2_SystemMonitor.system_monitor import SystemMonitor


class Task:
    """Represents a task to be processed"""
    
    def __init__(self, task_id, processing_time=None):
        self.task_id = task_id
        self.processing_time = processing_time or random.uniform(0.05, 0.3)  # Random processing time
        self.assigned_processor = None
        self.created_at = time.time()
    
    def __str__(self):
        return f"Task {self.task_id} (time={self.processing_time:.2f}s)"


class LoadBalancer:
    """Dynamic load balancer that distributes tasks across processors"""
    
    def __init__(self, processors: List[Processor], monitor: SystemMonitor):
        self.processors = processors
        self.monitor = monitor
        self.total_tasks_assigned = 0
        self.rebalance_count = 0
        self.migration_count = 0
        
    def assign_task(self, task: Task) -> bool:
        """
        Assign a task to the most suitable processor
        Uses 'Least Loaded First' strategy
        """
        # Find processor with least load
        least_loaded = self.monitor.get_least_loaded_processor()
        
        if least_loaded.add_task(task):
            task.assigned_processor = least_loaded
            self.total_tasks_assigned += 1
            return True
        return False
    
    def rebalance_loads(self):
        """
        Rebalance loads across processors by migrating tasks
        Moves tasks from overloaded processors to underloaded ones
        """
        if not self.monitor.detect_imbalance():
            return  # No need to rebalance
        
        overloaded = self.monitor.get_overloaded_processors(threshold=70)
        underloaded = self.monitor.get_underloaded_processors(threshold=40)
        
        if not overloaded or not underloaded:
            return  # Cannot rebalance
        
        migrations = 0
        for overloaded_proc in overloaded:
            if not underloaded:
                break
            
            # Get tasks from overloaded processor
            queue_length = overloaded_proc.get_queue_length()
            tasks_to_migrate = max(1, queue_length // 2)  # Migrate half of tasks
            
            for _ in range(tasks_to_migrate):
                if not underloaded:
                    break
                
                # Get a task from overloaded processor (simplified - in real implementation,
                # we'd need to access the queue properly)
                # For now, we'll simulate by reducing queue
                if overloaded_proc.get_queue_length() > 0:
                    # Find least loaded processor
                    target = min(underloaded, key=lambda p: p.get_current_load())
                    
                    # Simulate task migration
                    # In a real implementation, we'd move actual task objects
                    overloaded_proc.task_queue.popleft() if overloaded_proc.task_queue else None
                    # Add to target (simplified - would need actual task object)
                    target.update_load()
                    overloaded_proc.update_load()
                    migrations += 1
                    self.migration_count += 1
                    
                    # Update underloaded list
                    if target.get_current_load() > 40:
                        underloaded.remove(target)
        
        if migrations > 0:
            self.rebalance_count += 1
            print(f"Rebalanced: Migrated {migrations} tasks")
    
    def adaptive_threshold_adjustment(self):
        """
        Dynamically adjust rebalancing threshold based on system state
        """
        state = self.monitor.get_system_state()
        avg_load = state['average_load']
        
        # Adjust threshold based on average load
        if avg_load > 70:
            # High load - be more aggressive with rebalancing
            self.monitor.rebalance_threshold = 0.2
        elif avg_load < 30:
            # Low load - be less aggressive
            self.monitor.rebalance_threshold = 0.4
        else:
            # Normal load - default threshold
            self.monitor.rebalance_threshold = 0.3
    
    def get_statistics(self) -> dict:
        """Get load balancer statistics"""
        return {
            'total_tasks_assigned': self.total_tasks_assigned,
            'rebalance_count': self.rebalance_count,
            'migration_count': self.migration_count,
            'processors_count': len(self.processors)
        }


