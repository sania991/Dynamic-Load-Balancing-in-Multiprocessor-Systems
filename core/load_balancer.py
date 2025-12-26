"""
Load Balancer Module
Implements the core load balancing algorithm
"""

from typing import List, Optional
from .processor import Processor
from .monitor import SystemMonitor


class Task:
    """
    Represents a task to be processed
    
    A task is a unit of work that needs to be executed by a processor
    """
    
    def __init__(self, task_id):
        """
        Initialize a task
        
        Args:
            task_id: Unique identifier for this task
        """
        self.task_id = task_id
        self.assigned_processor = None  # Will be set when assigned
    
    def __str__(self):
        return f"Task {self.task_id}"


class LoadBalancer:
    """
    Dynamic load balancer that distributes tasks across processors
    
    Algorithm: "Least Loaded First"
    - Always assigns new tasks to the processor with minimum load
    - Periodically rebalances by moving tasks from overloaded to underloaded processors
    """
    
    def __init__(self, processors: List[Processor], monitor: SystemMonitor):
        """
        Initialize load balancer
        
        Args:
            processors: List of all available processors
            monitor: System monitor for tracking processor states
        """
        self.processors = processors
        self.monitor = monitor
        
        # Statistics
        self.total_tasks_assigned = 0
        self.rebalance_count = 0
        self.migration_count = 0
    
    def assign_task(self, task: Task) -> bool:
        """
        Assign a task to the most suitable processor
        
        Uses "Least Loaded First" strategy:
        1. Find processor with minimum load
        2. Assign task to that processor
        
        Args:
            task: Task to assign
            
        Returns:
            True if task was assigned, False otherwise
        """
        # Find processor with least load
        least_loaded = self.monitor.get_least_loaded_processor()
        
        # Try to add task to that processor
        if least_loaded.add_task(task):
            task.assigned_processor = least_loaded
            self.total_tasks_assigned += 1
            return True
        
        return False
    
    def rebalance_loads(self):
        """
        Rebalance loads by migrating tasks from overloaded to underloaded processors
        
        Process:
        1. Identify overloaded processors (>70% load)
        2. Identify underloaded processors (<40% load)
        3. Migrate tasks from overloaded to underloaded processors
        """
        if not self.monitor.detect_imbalance():
            return  # No need to rebalance
        
        # Get overloaded and underloaded processors
        overloaded = self.monitor.get_overloaded_processors(threshold=70.0)
        underloaded = self.monitor.get_underloaded_processors(threshold=40.0)
        
        if not overloaded or not underloaded:
            return  # Cannot rebalance
        
        migrations = 0
        
        # Migrate tasks from overloaded to underloaded processors
        for overloaded_proc in overloaded:
            if not underloaded:
                break
            
            # Calculate how many tasks to migrate (half of queue)
            queue_length = overloaded_proc.get_queue_length()
            tasks_to_migrate = max(1, queue_length // 2)
            
            for _ in range(tasks_to_migrate):
                if not underloaded:
                    break
                
                # Get a task from overloaded processor
                task = overloaded_proc.get_next_task()
                if task is None:
                    break
                
                # Find least loaded underloaded processor
                target = min(underloaded, key=lambda p: p.get_current_load())
                
                # Migrate task
                if target.add_task(task):
                    task.assigned_processor = target
                    migrations += 1
                    self.migration_count += 1
                    
                    # Update underloaded list if target is no longer underloaded
                    if target.get_current_load() > 40.0:
                        underloaded = [p for p in underloaded if p != target]
        
        if migrations > 0:
            self.rebalance_count += 1
            print(f"[REBALANCING] Migrated {migrations} tasks")
    
    def adaptive_threshold_adjustment(self):
        """
        Adjust rebalancing threshold based on current system load
        
        This makes the system adapt to varying load conditions:
        - High load: More aggressive rebalancing
        - Low load: Less aggressive rebalancing
        """
        state = self.monitor.get_system_state()
        average_load = state['average_load']
        self.monitor.adjust_rebalance_threshold(average_load)
    
    def get_statistics(self) -> dict:
        """
        Get load balancer statistics
        
        Returns:
            Dictionary with statistics
        """
        return {
            'total_tasks_assigned': self.total_tasks_assigned,
            'rebalance_count': self.rebalance_count,
            'migration_count': self.migration_count,
            'processor_count': len(self.processors)
        }

