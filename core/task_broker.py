"""
Apeiron-Nexus Asynchronous Distributed Task Broker & Queue.
Manages asynchronous task dispatching, priority queues, and node load balancing.
"""

import time
import uuid
import heapq

class ApeironTaskBroker:
    def __init__(self):
        self.task_queue = []
        self.completed_tasks = {}
        self.active_workers = {}

    def submit_task(self, task_type: str, payload: dict, priority: int = 1) -> str:
        """
        Submits a heavy computation task into the priority queue (lower priority number = higher priority).
        """
        task_id = f"task-{uuid.uuid4().hex[:8]}"
        task_entry = {
            "task_id": task_id,
            "task_type": task_type,
            "payload": payload,
            "submitted_at": time.time(),
            "status": "queued"
        }
        # Using heapq for priority scheduling (priority, timestamp, task_entry)
        heapq.heappush(self.task_queue, (priority, time.time(), task_entry))
        return task_id

    def process_queue(self, worker_node: str) -> dict:
        """
        Worker node pulls and executes the highest priority task from the queue.
        """
        if not self.task_queue:
            return {"status": "queue_empty", "worker": worker_node}

        priority, _, task = heapq.heappop(self.task_queue)
        task["status"] = "processing"
        task["executed_by"] = worker_node
        
        start_time = time.time()
        # Simulate execution based on task type
        time.sleep(0.005) 
        execution_time = round((time.time() - start_time) * 1000, 3)

        task["status"] = "completed"
        task["execution_time_ms"] = execution_time
        self.completed_tasks[task["task_id"]] = task

        return {
            "status": "success",
            "worker": worker_node,
            "task_summary": task
        }
