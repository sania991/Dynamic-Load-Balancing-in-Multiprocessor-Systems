"""
Example: Complete Web Server Load Balancer Adaptation
This shows a full working example of adapting the code for web servers

IMPORTANT: This example requires the 'requests' library.
Install it with: pip install requests

Note: This is an EXAMPLE file showing how to adapt the code.
The main project (main.py) does NOT require requests.
"""

import time
try:
    import requests
except ImportError:
    print("ERROR: 'requests' module not found!")
    print("Install it with: pip install requests")
    print("\nNote: This is an example file. The main project doesn't need requests.")
    exit(1)
import threading
from collections import deque
from typing import List, Dict
from threading import Lock

# ============================================================================
# STEP 1: Adapt Processor → WebServer
# ============================================================================

class WebServer:
    """Adapted from Processor class for web servers"""
    
    def __init__(self, server_id: int, url: str, max_connections: int = 100):
        self.server_id = server_id
        self.url = url
        self.max_connections = max_connections
        self.request_queue = deque()
        self.active_connections = 0
        self.current_load = 0
        self.total_requests = 0
        self.error_count = 0
        self.avg_response_time = 0.0
        self.is_healthy = True
        self.lock = Lock()
    
    def add_request(self, request):
        """Add request to queue (adapted from add_task)"""
        with self.lock:
            if self.active_connections < self.max_connections:
                self.request_queue.append(request)
                self.update_load()
                return True
            return False
    
    def get_queue_length(self):
        """Get queue length"""
        with self.lock:
            return len(self.request_queue)
    
    def get_current_load(self):
        """Get current load"""
        with self.lock:
            return self.current_load
    
    def update_load(self):
        """Update load calculation (adapted for web servers)"""
        with self.lock:
            # Connection-based load
            connection_factor = (self.active_connections / self.max_connections) * 50
            # Queue-based load
            queue_factor = min(len(self.request_queue) / 50, 1.0) * 50
            self.current_load = min(connection_factor + queue_factor, 100)
    
    def handle_request(self, request_data: Dict):
        """Handle HTTP request (adapted from process_task)"""
        self.active_connections += 1
        self.total_requests += 1
        self.update_load()
        
        start_time = time.time()
        try:
            # Forward to actual server
            response = requests.post(
                f"{self.url}/api/endpoint",
                json=request_data,
                timeout=10
            )
            
            response_time = time.time() - start_time
            self.avg_response_time = (self.avg_response_time * 0.9 + response_time * 0.1)
            
            if response.status_code >= 400:
                self.error_count += 1
            
            self.active_connections -= 1
            self.update_load()
            return {'status': 'success', 'data': response.json()}
            
        except Exception as e:
            self.error_count += 1
            self.active_connections -= 1
            self.update_load()
            return {'status': 'error', 'message': str(e)}
    
    def health_check(self):
        """Check server health"""
        try:
            response = requests.get(f"{self.url}/health", timeout=2)
            self.is_healthy = response.status_code == 200
            return self.is_healthy
        except:
            self.is_healthy = False
            return False
    
    def get_metrics(self):
        """Get server metrics"""
        with self.lock:
            return {
                'server_id': self.server_id,
                'queue_length': len(self.request_queue),
                'current_load': self.current_load,
                'active_connections': self.active_connections,
                'total_requests': self.total_requests,
                'error_rate': self.error_count / max(self.total_requests, 1),
                'avg_response_time': self.avg_response_time,
                'is_healthy': self.is_healthy
            }


# ============================================================================
# STEP 2: Adapt Task → HTTPRequest
# ============================================================================

class HTTPRequest:
    """Adapted from Task class for HTTP requests"""
    
    def __init__(self, request_id: int, method: str = 'GET', path: str = '/', data: Dict = None):
        self.request_id = request_id
        self.method = method
        self.path = path
        self.data = data or {}
        self.assigned_server = None
        self.created_at = time.time()
    
    def __str__(self):
        return f"HTTPRequest {self.request_id} ({self.method} {self.path})"


# ============================================================================
# STEP 3: Adapt SystemMonitor → WebServerMonitor
# ============================================================================

class WebServerMonitor:
    """Adapted from SystemMonitor for web servers"""
    
    def __init__(self, servers: List[WebServer], rebalance_threshold: float = 0.3):
        self.servers = servers
        self.rebalance_threshold = rebalance_threshold
        self.metrics_history = []
    
    def get_all_metrics(self) -> List[Dict]:
        """Get metrics from all servers"""
        return [server.get_metrics() for server in self.servers]
    
    def get_system_state(self) -> Dict:
        """Get overall system state"""
        metrics = self.get_all_metrics()
        healthy_servers = [m for m in metrics if m['is_healthy']]
        
        if not healthy_servers:
            return {'error': 'No healthy servers'}
        
        total_load = sum(m['current_load'] for m in healthy_servers)
        avg_load = total_load / len(healthy_servers)
        max_load = max(m['current_load'] for m in healthy_servers)
        min_load = min(m['current_load'] for m in healthy_servers)
        
        return {
            'average_load': avg_load,
            'max_load': max_load,
            'min_load': min_load,
            'load_variance': max_load - min_load,
            'total_requests': sum(m['total_requests'] for m in metrics),
            'server_count': len(healthy_servers),
            'timestamp': time.time()
        }
    
    def detect_imbalance(self) -> bool:
        """Detect if rebalancing is needed (same algorithm)"""
        state = self.get_system_state()
        if 'error' in state:
            return False
        
        load_variance = state['load_variance']
        if load_variance > (self.rebalance_threshold * 100):
            return True
        
        for server in self.servers:
            if server.get_current_load() > 80:
                return True
        
        return False
    
    def get_least_loaded_server(self) -> WebServer:
        """Get least loaded server (same algorithm)"""
        healthy_servers = [s for s in self.servers if s.is_healthy]
        if not healthy_servers:
            raise Exception("No healthy servers")
        return min(healthy_servers, key=lambda s: s.get_current_load())
    
    def get_overloaded_servers(self, threshold: int = 70) -> List[WebServer]:
        """Get overloaded servers"""
        return [s for s in self.servers if s.get_current_load() > threshold and s.is_healthy]
    
    def get_underloaded_servers(self, threshold: int = 40) -> List[WebServer]:
        """Get underloaded servers"""
        return [s for s in self.servers if s.get_current_load() < threshold and s.is_healthy]


# ============================================================================
# STEP 4: Adapt LoadBalancer → WebLoadBalancer
# ============================================================================

class WebLoadBalancer:
    """Adapted from LoadBalancer for web servers (algorithm stays same)"""
    
    def __init__(self, servers: List[WebServer], monitor: WebServerMonitor):
        self.servers = servers
        self.monitor = monitor
        self.total_requests_assigned = 0
        self.rebalance_count = 0
        self.migration_count = 0
    
    def assign_request(self, request: HTTPRequest) -> bool:
        """Assign request to least loaded server (same algorithm)"""
        try:
            least_loaded = self.monitor.get_least_loaded_server()
            
            if least_loaded.add_request(request):
                request.assigned_server = least_loaded
                self.total_requests_assigned += 1
                return True
            return False
        except:
            return False
    
    def rebalance_loads(self):
        """Rebalance loads (same algorithm)"""
        if not self.monitor.detect_imbalance():
            return
        
        overloaded = self.monitor.get_overloaded_servers(threshold=70)
        underloaded = self.monitor.get_underloaded_servers(threshold=40)
        
        if not overloaded or not underloaded:
            return
        
        migrations = 0
        for overloaded_server in overloaded:
            if not underloaded:
                break
            
            queue_length = overloaded_server.get_queue_length()
            requests_to_migrate = max(1, queue_length // 2)
            
            for _ in range(requests_to_migrate):
                if not underloaded or overloaded_server.get_queue_length() == 0:
                    break
                
                target = min(underloaded, key=lambda s: s.get_current_load())
                
                # Migrate request (simplified - in real implementation, 
                # you'd need to handle actual request objects)
                if overloaded_server.request_queue:
                    overloaded_server.request_queue.popleft()
                target.update_load()
                overloaded_server.update_load()
                migrations += 1
                self.migration_count += 1
                
                if target.get_current_load() > 40:
                    underloaded.remove(target)
        
        if migrations > 0:
            self.rebalance_count += 1
            print(f"Rebalanced: Migrated {migrations} requests")
    
    def adaptive_threshold_adjustment(self):
        """Adaptive threshold (same algorithm)"""
        state = self.monitor.get_system_state()
        if 'error' in state:
            return
        
        avg_load = state['average_load']
        
        if avg_load > 70:
            self.monitor.rebalance_threshold = 0.2
        elif avg_load < 30:
            self.monitor.rebalance_threshold = 0.4
        else:
            self.monitor.rebalance_threshold = 0.3
    
    def get_statistics(self) -> Dict:
        """Get statistics"""
        return {
            'total_requests_assigned': self.total_requests_assigned,
            'rebalance_count': self.rebalance_count,
            'migration_count': self.migration_count,
            'server_count': len(self.servers)
        }


# ============================================================================
# STEP 5: Main Application
# ============================================================================

def main():
    """Main application for web server load balancer"""
    print("="*60)
    print("Web Server Load Balancer")
    print("="*60)
    
    # Define web servers (replace with your actual server URLs)
    servers = [
        WebServer(0, "http://server1.example.com:8000"),
        WebServer(1, "http://server2.example.com:8000"),
        WebServer(2, "http://server3.example.com:8000"),
        WebServer(3, "http://server4.example.com:8000"),
    ]
    
    # Initialize monitor and load balancer
    monitor = WebServerMonitor(servers, rebalance_threshold=0.3)
    load_balancer = WebLoadBalancer(servers, monitor)
    
    # Health check thread
    running = threading.Event()
    running.set()
    
    def health_check_loop():
        while running.is_set():
            for server in servers:
                server.health_check()
            time.sleep(5)
    
    health_thread = threading.Thread(target=health_check_loop)
    health_thread.daemon = True
    health_thread.start()
    
    # Simulate incoming requests
    print("\nStarting request simulation...")
    request_id = 0
    
    try:
        while True:
            # Create HTTP request
            request = HTTPRequest(
                request_id=request_id,
                method='POST',
                path='/api/data',
                data={'user_id': request_id, 'action': 'process'}
            )
            
            # Assign through load balancer
            if load_balancer.assign_request(request):
                server_id = request.assigned_server.server_id
                load = request.assigned_server.get_current_load()
                print(f"Request {request_id} → Server {server_id} (Load: {load:.1f}%)")
            
            # Periodic rebalancing
            if request_id % 10 == 0:
                if monitor.detect_imbalance():
                    print("\n[REBALANCING TRIGGERED]")
                    load_balancer.adaptive_threshold_adjustment()
                    load_balancer.rebalance_loads()
            
            # Print state every 20 requests
            if request_id % 20 == 0 and request_id > 0:
                state = monitor.get_system_state()
                if 'error' not in state:
                    print(f"\n[System State] Avg Load: {state['average_load']:.1f}%, "
                          f"Variance: {state['load_variance']:.1f}%")
                    for server in servers:
                        metrics = server.get_metrics()
                        print(f"  Server {server.server_id}: "
                              f"Load={metrics['current_load']:.1f}%, "
                              f"Queue={metrics['queue_length']}, "
                              f"Requests={metrics['total_requests']}")
            
            request_id += 1
            time.sleep(0.5)
    
    except KeyboardInterrupt:
        print("\n\nStopping...")
        running.clear()
        
        # Final statistics
        stats = load_balancer.get_statistics()
        print("\n" + "="*60)
        print("FINAL STATISTICS")
        print("="*60)
        print(f"Total Requests Assigned: {stats['total_requests_assigned']}")
        print(f"Rebalance Operations: {stats['rebalance_count']}")
        print(f"Request Migrations: {stats['migration_count']}")
        print("="*60)


if __name__ == "__main__":
    main()

