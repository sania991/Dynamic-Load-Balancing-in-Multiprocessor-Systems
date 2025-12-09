# How to Adapt This Repository for Other Projects

## 🎯 Overview

This guide shows you how to adapt the Dynamic Workload Distribution algorithm for different use cases like web servers, databases, microservices, etc.

---

## 🌐 Example 1: Web Server Load Balancer

### Step 1: Understand the Mapping

**Current Project (Processors):**
- `Processor` → Represents a CPU processor
- `Task` → Represents a computation task
- `Load` → CPU utilization percentage

**Web Server Adaptation:**
- `Processor` → `WebServer` (represents a web server)
- `Task` → `HTTPRequest` (represents an HTTP request)
- `Load` → Server load (requests, CPU, memory)

### Step 2: Create New Classes

Create `web_server.py`:

```python
"""
Adapted Processor class for Web Servers
"""

import time
import requests
from collections import deque
from threading import Lock

class WebServer:
    """Represents a web server with load tracking"""
    
    def __init__(self, server_id, url, max_connections=100):
        self.server_id = server_id
        self.url = url
        self.max_connections = max_connections
        self.request_queue = deque()  # Queue of HTTP requests
        self.active_connections = 0
        self.current_load = 0
        self.total_requests_handled = 0
        self.error_count = 0
        self.avg_response_time = 0
        self.is_healthy = True
        self.lock = Lock()
    
    def add_request(self, http_request):
        """Add an HTTP request to the server's queue"""
        with self.lock:
            if self.active_connections < self.max_connections:
                self.request_queue.append(http_request)
                self.update_load()
                return True
            return False
    
    def get_queue_length(self):
        """Get current request queue length"""
        with self.lock:
            return len(self.request_queue)
    
    def get_current_load(self):
        """Get current server load percentage"""
        with self.lock:
            return self.current_load
    
    def update_load(self):
        """Update load based on active connections and queue"""
        with self.lock:
            connection_factor = (self.active_connections / self.max_connections) * 50
            queue_factor = min(len(self.request_queue) / 50, 1.0) * 50
            self.current_load = min(connection_factor + queue_factor, 100)
    
    def handle_request(self, request_data):
        """Handle an HTTP request"""
        self.active_connections += 1
        self.total_requests_handled += 1
        self.update_load()
        
        start_time = time.time()
        try:
            # Forward request to actual server
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
        """Check if server is healthy"""
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
                'total_requests': self.total_requests_handled,
                'error_rate': self.error_count / max(self.total_requests_handled, 1),
                'avg_response_time': self.avg_response_time,
                'is_healthy': self.is_healthy
            }
```

### Step 3: Adapt the Load Balancer

Create `web_load_balancer.py`:

```python
"""
Adapted Load Balancer for Web Servers
"""

from typing import List
from web_server import WebServer

class HTTPRequest:
    """Represents an HTTP request"""
    
    def __init__(self, request_id, method='GET', path='/', data=None):
        self.request_id = request_id
        self.method = method
        self.path = path
        self.data = data
        self.assigned_server = None

class WebLoadBalancer:
    """Load balancer for web servers"""
    
    def __init__(self, servers: List[WebServer]):
        self.servers = servers
        self.total_requests = 0
        self.rebalance_count = 0
    
    def assign_request(self, http_request: HTTPRequest) -> bool:
        """Assign request to least loaded server"""
        # Filter healthy servers
        healthy_servers = [s for s in self.servers if s.is_healthy]
        if not healthy_servers:
            return False
        
        # Find least loaded server (same algorithm as original)
        least_loaded = min(healthy_servers, key=lambda s: s.get_current_load())
        
        if least_loaded.add_request(http_request):
            http_request.assigned_server = least_loaded
            self.total_requests += 1
            return True
        return False
    
    def get_least_loaded_server(self):
        """Get server with minimum load"""
        healthy_servers = [s for s in self.servers if s.is_healthy]
        return min(healthy_servers, key=lambda s: s.get_current_load())
```

### Step 4: Adapt the Monitor

Create `web_server_monitor.py`:

```python
"""
Adapted System Monitor for Web Servers
"""

from typing import List, Dict
import time
from web_server import WebServer

class WebServerMonitor:
    """Monitors web server states"""
    
    def __init__(self, servers: List[WebServer], rebalance_threshold=0.3):
        self.servers = servers
        self.rebalance_threshold = rebalance_threshold
    
    def get_all_metrics(self) -> List[Dict]:
        """Collect metrics from all servers"""
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
        """Detect if load balancing is needed"""
        state = self.get_system_state()
        if 'error' in state:
            return False
        
        load_variance = state['load_variance']
        if load_variance > (self.rebalance_threshold * 100):
            return True
        
        # Check if any server is overloaded
        for server in self.servers:
            if server.get_current_load() > 80:
                return True
        
        return False
    
    def get_overloaded_servers(self, threshold=70):
        """Get overloaded servers"""
        return [s for s in self.servers if s.get_current_load() > threshold and s.is_healthy]
    
    def get_underloaded_servers(self, threshold=40):
        """Get underloaded servers"""
        return [s for s in self.servers if s.get_current_load() < threshold and s.is_healthy]
```

### Step 5: Create Main Application

Create `web_main.py`:

```python
"""
Main application for Web Server Load Balancer
"""

import time
import threading
from web_server import WebServer
from web_load_balancer import WebLoadBalancer, HTTPRequest
from web_server_monitor import WebServerMonitor

def main():
    # Define your web servers
    servers = [
        WebServer(0, "http://server1.example.com:8000"),
        WebServer(1, "http://server2.example.com:8000"),
        WebServer(2, "http://server3.example.com:8000"),
        WebServer(3, "http://server4.example.com:8000"),
    ]
    
    # Initialize monitor and load balancer
    monitor = WebServerMonitor(servers, rebalance_threshold=0.3)
    load_balancer = WebLoadBalancer(servers)
    
    # Health check thread
    def health_check_loop():
        while True:
            for server in servers:
                server.health_check()
            time.sleep(5)
    
    health_thread = threading.Thread(target=health_check_loop)
    health_thread.daemon = True
    health_thread.start()
    
    # Simulate incoming requests
    request_id = 0
    while True:
        # Simulate incoming HTTP request
        request = HTTPRequest(
            request_id=request_id,
            method='POST',
            path='/api/data',
            data={'user_id': request_id}
        )
        
        if load_balancer.assign_request(request):
            print(f"Request {request_id} → Server {request.assigned_server.server_id}")
        
        # Check for rebalancing
        if monitor.detect_imbalance():
            print("[REBALANCING TRIGGERED]")
            # Implement rebalancing logic here
        
        request_id += 1
        time.sleep(0.5)

if __name__ == "__main__":
    main()
```

---

## 🗄️ Example 2: Database Query Router

### Adaptation Steps:

1. **Rename Classes:**
   - `Processor` → `DatabaseServer`
   - `Task` → `DatabaseQuery`
   - `Load` → Query load (active connections, query queue)

2. **Modify Load Calculation:**
```python
def calculate_load(self):
    connection_factor = self.active_connections / self.max_connections * 50
    query_factor = len(self.query_queue) / 100 * 50
    return min(connection_factor + query_factor, 100)
```

3. **Adapt Task Processing:**
```python
def execute_query(self, query):
    self.active_connections += 1
    result = self.connection.execute(query)
    self.active_connections -= 1
    return result
```

---

## 🔄 General Adaptation Pattern

### Step-by-Step Process:

1. **Identify Your Resources**
   - What are you balancing? (servers, databases, workers, etc.)
   - What are your tasks? (requests, queries, jobs, etc.)

2. **Map to Original Structure**
   ```
   Processor → Your Resource Class
   Task → Your Work Unit Class
   Load → Your Load Metric
   ```

3. **Adapt the Classes**
   - Copy `processor.py` → Rename to your resource class
   - Modify load calculation for your metrics
   - Update task processing for your use case

4. **Keep the Algorithm**
   - Load balancing logic stays the same
   - Monitoring logic stays the same
   - Rebalancing logic stays the same

5. **Update Main Application**
   - Change initialization
   - Update task generation
   - Modify output/visualization

---

## 📋 Quick Adaptation Checklist

- [ ] Create new resource class (based on Processor)
- [ ] Create new task class (based on Task)
- [ ] Adapt load calculation formula
- [ ] Update task processing logic
- [ ] Modify monitor for your metrics
- [ ] Update load balancer (algorithm stays same)
- [ ] Create new main application
- [ ] Test with your use case

---

## 🛠️ Code Reuse Strategy

### What to Keep (Algorithm):
- ✅ Load balancing algorithm (Least Loaded First)
- ✅ Imbalance detection logic
- ✅ Rebalancing mechanism
- ✅ Adaptive threshold management
- ✅ Monitoring structure

### What to Change (Implementation):
- ❌ Resource class (Processor → Your Resource)
- ❌ Task class (Task → Your Work Unit)
- ❌ Load calculation (adapt to your metrics)
- ❌ Task processing (adapt to your operations)
- ❌ Main application (adapt to your use case)

---

## 📚 Example Use Cases

### 1. **API Gateway**
- Resource: API endpoints
- Task: API requests
- Load: Request rate, response time

### 2. **Message Queue**
- Resource: Workers/Consumers
- Task: Messages
- Load: Queue length, processing rate

### 3. **Content Delivery**
- Resource: CDN edge servers
- Task: Content requests
- Load: Bandwidth, latency

### 4. **Microservices**
- Resource: Service instances
- Task: Service requests
- Load: Request count, CPU usage

### 5. **Distributed Computing**
- Resource: Compute nodes
- Task: Computation jobs
- Load: CPU, memory, job queue

---

## 🎯 Key Principles

1. **Algorithm is Universal**: The load balancing algorithm works for any distributed system
2. **Adapt the Interface**: Change how you interact with resources, not the algorithm
3. **Metrics Matter**: Define load calculation based on your specific metrics
4. **Keep It Simple**: Start with basic adaptation, then add complexity

---

## 💡 Tips

1. **Start Small**: Adapt one class at a time
2. **Test Incrementally**: Test each adaptation before moving on
3. **Keep Original**: Don't modify original files, create new ones
4. **Document Changes**: Note what you changed and why
5. **Reuse Logic**: The core algorithm doesn't need to change

---

## 🔗 Integration Examples

### Flask Web Application:

```python
from flask import Flask, request
from web_load_balancer import WebLoadBalancer

app = Flask(__name__)
load_balancer = WebLoadBalancer(servers)

@app.route('/api/endpoint', methods=['POST'])
def handle_request():
    http_request = HTTPRequest(
        request_id=generate_id(),
        method=request.method,
        path=request.path,
        data=request.json
    )
    
    result = load_balancer.assign_request(http_request)
    return result
```

### Django Integration:

```python
# middleware.py
from web_load_balancer import WebLoadBalancer

class LoadBalancingMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response
        self.load_balancer = WebLoadBalancer(servers)
    
    def __call__(self, request):
        # Route request through load balancer
        return self.get_response(request)
```

---

## ✅ Summary

**To adapt for web servers or any project:**

1. **Copy** the module structure
2. **Rename** classes to match your domain
3. **Adapt** load calculation and processing
4. **Keep** the core algorithm
5. **Test** with your use case

The beauty of this design is that the **algorithm is universal** - you just need to adapt the **interface** to your specific resources and tasks!

---

**Ready to adapt? Start with one class, test it, then move to the next!** 🚀

