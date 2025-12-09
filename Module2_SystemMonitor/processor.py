"""
Module 2: System State Monitor
Processor class to represent individual processors and track their state
"""

import time
from collections import deque
from threading import Lock


class Processor:
    """Represents a single processor with state tracking"""
    
    def __init__(self, processor_id, max_queue_size=100):
        self.processor_id = processor_id
        self.max_queue_size = max_queue_size
        self.task_queue = deque()  # Queue of tasks waiting to be processed
        self.current_load = 0  # Current CPU utilization (0-100)
        self.total_tasks_completed = 0
        self.total_processing_time = 0
        self.is_processing = False
        self.lock = Lock()  # Thread safety for concurrent access
        
    def add_task(self, task):
        """Add a task to the processor's queue"""
        with self.lock:
            if len(self.task_queue) < self.max_queue_size:
                self.task_queue.append(task)
                self.update_load()
                return True
            return False
    
    def remove_task(self, task):
        """Remove a task from the queue (for migration)"""
        with self.lock:
            if task in self.task_queue:
                self.task_queue.remove(task)
                self.update_load()
                return True
            return False
    
    def get_queue_length(self):
        """Get current queue length"""
        with self.lock:
            return len(self.task_queue)
    
    def get_current_load(self):
        """Get current CPU load percentage"""
        with self.lock:
            return self.current_load
    
    def update_load(self):
        """Update the current load based on queue length and processing state
        NOTE: This method should be called while holding self.lock
        """
        # Don't acquire lock here - assume caller already has it
        queue_factor = min(len(self.task_queue) / self.max_queue_size, 1.0) * 50
        processing_factor = 50 if self.is_processing else 0
        self.current_load = min(queue_factor + processing_factor, 100)
    
    def process_task(self, task_duration=0.1):
        """Simulate processing a task"""
        with self.lock:
            if self.task_queue:
                task = self.task_queue.popleft()
                self.is_processing = True
                self.update_load()
        
        # Simulate processing time
        time.sleep(task_duration)
        
        with self.lock:
            self.is_processing = False
            self.total_tasks_completed += 1
            self.total_processing_time += task_duration
            self.update_load()
            return task
    
    def get_metrics(self):
        """Get current processor metrics"""
        with self.lock:
            return {
                'processor_id': self.processor_id,
                'queue_length': len(self.task_queue),
                'current_load': self.current_load,
                'is_processing': self.is_processing,
                'total_tasks_completed': self.total_tasks_completed,
                'average_processing_time': (self.total_processing_time / self.total_tasks_completed 
                                            if self.total_tasks_completed > 0 else 0)
            }
    
    def __str__(self):
        return f"Processor {self.processor_id}: Load={self.current_load:.1f}%, Queue={len(self.task_queue)}"


