"""
Processor Module
Represents a single processor that can process tasks
"""

import time
from collections import deque
from threading import RLock  # Reentrant lock for nested calls


class Processor:
    """
    Represents a single processor with a task queue
    
    A processor:
    - Has a queue of tasks waiting to be processed
    - Processes tasks one at a time
    - Tracks its current load (0-100%)
    - Maintains statistics about completed tasks
    """
    
    def __init__(self, processor_id, max_queue_size=10):
        """
        Initialize a processor
        
        Args:
            processor_id: Unique identifier for this processor
            max_queue_size: Maximum number of tasks in queue
        """
        self.processor_id = processor_id
        self.max_queue_size = max_queue_size
        self.task_queue = deque()  # Queue of tasks
        self.current_load = 0.0  # Current load percentage (0-100)
        self.is_processing = False  # Whether currently processing a task
        self.lock = RLock()  # Reentrant lock for nested calls (thread safety)
        
        # Statistics
        self.total_tasks_completed = 0
        self.total_processing_time = 0.0
    
    def add_task(self, task):
        """
        Add a task to this processor's queue
        
        Args:
            task: Task object to add
            
        Returns:
            True if task was added, False if queue is full
        """
        with self.lock:
            if len(self.task_queue) < self.max_queue_size:
                self.task_queue.append(task)
                self._update_load()
                return True
            return False
    
    def get_next_task(self):
        """
        Get and remove the next task from queue
        
        Returns:
            Task object or None if queue is empty
        """
        with self.lock:
            if self.task_queue:
                task = self.task_queue.popleft()
                self._update_load()
                return task
            return None
    
    def process_task(self, processing_time=0.5):
        """
        Process a task (simulated) - Optimized to reduce lock contention
        
        Args:
            processing_time: How long to process the task (seconds)
        """
        task = self.get_next_task()
        if task is None:
            return None
        
        with self.lock:
            self.is_processing = True
            self._update_load()
        
        # Simulate processing time (simplified - no frequent updates to reduce overhead)
        time.sleep(processing_time)
        
        with self.lock:
            self.is_processing = False
            self.total_tasks_completed += 1
            self.total_processing_time += processing_time
            self._update_load()
        
        return task
    
    def _update_load(self):
        """
        Update the current load based on queue length and processing status
        
        Load = (Queue Factor × 50%) + (Processing Factor × 50%)
        More accurate calculation that shows load even with few tasks
        Uses RLock so it can be called from within locked sections
        """
        with self.lock:  # RLock allows nested calls
            queue_length = len(self.task_queue)
            is_processing = self.is_processing
            
            # Queue factor: based on how full the queue is
            # Use a more sensitive calculation for better visibility
            if queue_length == 0:
                queue_factor = 0
            elif queue_length <= 2:
                # For small queues, show more load (better visibility)
                queue_factor = min(queue_length * 25, 50)  # 25% per task up to 50%
            else:
                # For larger queues, use percentage of max
                queue_factor = min(queue_length / self.max_queue_size, 1.0) * 50
            
            # Processing factor: 50% if processing, 0% if idle
            processing_factor = 50 if is_processing else 0
            
            # Total load (capped at 100%)
            self.current_load = min(queue_factor + processing_factor, 100.0)
    
    def get_current_load(self):
        """Get current load percentage"""
        with self.lock:
            return self.current_load
    
    def get_queue_length(self):
        """Get number of tasks in queue"""
        with self.lock:
            return len(self.task_queue)
    
    def get_metrics(self):
        """
        Get current processor metrics
        
        Returns:
            Dictionary with processor statistics
        """
        with self.lock:
            avg_time = (self.total_processing_time / self.total_tasks_completed 
                       if self.total_tasks_completed > 0 else 0.0)
            
            return {
                'processor_id': self.processor_id,
                'current_load': self.current_load,
                'queue_length': len(self.task_queue),
                'is_processing': self.is_processing,
                'total_tasks_completed': self.total_tasks_completed,
                'average_processing_time': avg_time
            }
    
    def __str__(self):
        """String representation of processor"""
        return f"Processor {self.processor_id}: Load={self.current_load:.1f}%, Queue={len(self.task_queue)}"

