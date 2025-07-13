from prometheus_client import Counter, Histogram, Gauge, CollectorRegistry
import time

# Create a custom registry for our metrics
registry = CollectorRegistry()

# HTTP request metrics
REQUEST_COUNT = Counter(
    'http_requests_total',
    'Total HTTP requests',
    ['method', 'endpoint', 'status_code'],
    registry=registry
)

REQUEST_TIME = Histogram(
    'http_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint', 'status_code'],
    registry=registry
)

# Task-specific metrics
TASK_COUNT = Gauge(
    'tasks_total',
    'Total number of tasks',
    registry=registry
)

TASK_COMPLETED = Gauge(
    'tasks_completed_total',
    'Total number of completed tasks',
    registry=registry
)

TASK_PENDING = Gauge(
    'tasks_pending_total',
    'Total number of pending tasks',
    registry=registry
)

TASK_COMPLETION_RATE = Gauge(
    'tasks_completion_rate',
    'Task completion rate as percentage',
    registry=registry
)

# Application metrics
APP_INFO = Gauge(
    'app_info',
    'Application information',
    ['version', 'name'],
    registry=registry
)

# Initialize application info
APP_INFO.labels(version='1.0.0', name='tasky').set(1)

def update_task_metrics(task_crud):
    """Update task-related metrics"""
    stats = task_crud.get_stats()
    TASK_COUNT.set(stats['total_tasks'])
    TASK_COMPLETED.set(stats['completed_tasks'])
    TASK_PENDING.set(stats['pending_tasks'])
    TASK_COMPLETION_RATE.set(stats['completion_rate'])

# Export metrics for Prometheus
metrics = registry 