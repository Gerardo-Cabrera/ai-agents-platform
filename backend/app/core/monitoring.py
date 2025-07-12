import logging
import time
import json
from datetime import datetime, timedelta
from typing import Dict, Any, Optional
from contextlib import contextmanager
from dataclasses import dataclass, asdict
from prometheus_client import Counter, Histogram, Gauge, generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request, Response
import psutil
import os

# Configuración de métricas Prometheus
REQUEST_COUNT = Counter('http_requests_total', 'Total HTTP requests', ['method', 'endpoint', 'status'])
REQUEST_DURATION = Histogram('http_request_duration_seconds', 'HTTP request duration')
ACTIVE_CONNECTIONS = Gauge('websocket_active_connections', 'Active WebSocket connections', ['channel'])
ERROR_COUNT = Counter('errors_total', 'Total errors', ['type', 'endpoint'])
MEMORY_USAGE = Gauge('memory_usage_bytes', 'Memory usage in bytes')
CPU_USAGE = Gauge('cpu_usage_percent', 'CPU usage percentage')

@dataclass
class RequestMetrics:
    """Métricas de una petición HTTP."""
    method: str
    endpoint: str
    status_code: int
    duration: float
    user_agent: str
    ip_address: str
    timestamp: datetime

@dataclass
class ErrorMetrics:
    """Métricas de errores."""
    error_type: str
    error_message: str
    endpoint: str
    stack_trace: Optional[str]
    timestamp: datetime

class StructuredLogger:
    """Logger estructurado para mejor análisis."""
    
    def __init__(self, name: str):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(logging.INFO)
        
        # Handler para archivo JSON
        file_handler = logging.FileHandler(f'logs/{name}.json')
        file_handler.setFormatter(JsonFormatter())
        self.logger.addHandler(file_handler)
        
        # Handler para consola
        console_handler = logging.StreamHandler()
        console_handler.setFormatter(StructuredFormatter())
        self.logger.addHandler(console_handler)
    
    def info(self, message: str, **kwargs):
        """Log de información estructurado."""
        self.logger.info(message, extra=kwargs)
    
    def error(self, message: str, **kwargs):
        """Log de error estructurado."""
        self.logger.error(message, extra=kwargs)
    
    def warning(self, message: str, **kwargs):
        """Log de advertencia estructurado."""
        self.logger.warning(message, extra=kwargs)
    
    def debug(self, message: str, **kwargs):
        """Log de debug estructurado."""
        self.logger.debug(message, extra=kwargs)

class JsonFormatter(logging.Formatter):
    """Formateador JSON para logs."""
    
    def format(self, record):
        log_entry = {
            'timestamp': datetime.utcnow().isoformat(),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno
        }
        
        # Agregar campos extra
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 
                          'filename', 'module', 'lineno', 'funcName', 'created', 
                          'msecs', 'relativeCreated', 'thread', 'threadName', 
                          'processName', 'process', 'getMessage', 'exc_info', 'exc_text', 'stack_info']:
                log_entry[key] = value
        
        return json.dumps(log_entry)

class StructuredFormatter(logging.Formatter):
    """Formateador estructurado para consola."""
    
    def format(self, record):
        timestamp = datetime.fromtimestamp(record.created).strftime('%Y-%m-%d %H:%M:%S')
        level = record.levelname.ljust(8)
        message = record.getMessage()
        
        # Agregar campos extra si existen
        extra_fields = []
        for key, value in record.__dict__.items():
            if key not in ['name', 'msg', 'args', 'levelname', 'levelno', 'pathname', 
                          'filename', 'module', 'lineno', 'funcName', 'created', 
                          'msecs', 'relativeCreated', 'thread', 'threadName', 
                          'processName', 'process', 'getMessage', 'exc_info', 'exc_text', 'stack_info']:
                extra_fields.append(f"{key}={value}")
        
        extra_str = f" | {' | '.join(extra_fields)}" if extra_fields else ""
        return f"{timestamp} | {level} | {message}{extra_str}"

class PerformanceMonitor:
    """Monitor de rendimiento del sistema."""
    
    def __init__(self):
        self.start_time = time.time()
        self.request_times = []
        self.error_counts = {}
    
    @contextmanager
    def measure_request(self, method: str, endpoint: str):
        """Medir duración de una petición."""
        start_time = time.time()
        try:
            yield
            duration = time.time() - start_time
            REQUEST_DURATION.observe(duration)
            self.request_times.append(duration)
        except Exception as e:
            duration = time.time() - start_time
            REQUEST_DURATION.observe(duration)
            ERROR_COUNT.labels(type=type(e).__name__, endpoint=endpoint).inc()
            raise
    
    def record_request(self, method: str, endpoint: str, status_code: int):
        """Registrar una petición HTTP."""
        REQUEST_COUNT.labels(method=method, endpoint=endpoint, status=status_code).inc()
    
    def record_websocket_connection(self, channel: str, connected: bool):
        """Registrar conexión WebSocket."""
        if connected:
            ACTIVE_CONNECTIONS.labels(channel=channel).inc()
        else:
            ACTIVE_CONNECTIONS.labels(channel=channel).dec()
    
    def update_system_metrics(self):
        """Actualizar métricas del sistema."""
        # Memoria
        memory = psutil.virtual_memory()
        MEMORY_USAGE.set(memory.used)
        
        # CPU
        cpu_percent = psutil.cpu_percent(interval=1)
        CPU_USAGE.set(cpu_percent)
    
    def get_performance_stats(self) -> Dict[str, Any]:
        """Obtener estadísticas de rendimiento."""
        if not self.request_times:
            return {}
        
        return {
            'uptime_seconds': time.time() - self.start_time,
            'total_requests': len(self.request_times),
            'avg_response_time': sum(self.request_times) / len(self.request_times),
            'min_response_time': min(self.request_times),
            'max_response_time': max(self.request_times),
            'p95_response_time': sorted(self.request_times)[int(len(self.request_times) * 0.95)],
            'memory_usage_mb': psutil.virtual_memory().used / 1024 / 1024,
            'cpu_usage_percent': psutil.cpu_percent(),
            'disk_usage_percent': psutil.disk_usage('/').percent
        }

class AlertManager:
    """Gestor de alertas del sistema."""
    
    def __init__(self, logger: StructuredLogger):
        self.logger = logger
        self.alert_thresholds = {
            'response_time_ms': 5000,  # 5 segundos
            'error_rate_percent': 5,   # 5%
            'memory_usage_percent': 90, # 90%
            'cpu_usage_percent': 80,   # 80%
            'disk_usage_percent': 85   # 85%
        }
        self.last_alerts = {}
    
    def check_alerts(self, metrics: Dict[str, Any]):
        """Verificar y generar alertas."""
        current_time = datetime.utcnow()
        
        # Alerta de tiempo de respuesta
        if metrics.get('avg_response_time', 0) * 1000 > self.alert_thresholds['response_time_ms']:
            self._send_alert('HIGH_RESPONSE_TIME', 
                           f"Tiempo de respuesta promedio: {metrics['avg_response_time']*1000:.2f}ms")
        
        # Alerta de uso de memoria
        memory_percent = (metrics.get('memory_usage_mb', 0) * 1024 * 1024 / 
                         psutil.virtual_memory().total) * 100
        if memory_percent > self.alert_thresholds['memory_usage_percent']:
            self._send_alert('HIGH_MEMORY_USAGE', 
                           f"Uso de memoria: {memory_percent:.1f}%")
        
        # Alerta de uso de CPU
        if metrics.get('cpu_usage_percent', 0) > self.alert_thresholds['cpu_usage_percent']:
            self._send_alert('HIGH_CPU_USAGE', 
                           f"Uso de CPU: {metrics['cpu_usage_percent']:.1f}%")
        
        # Alerta de uso de disco
        if metrics.get('disk_usage_percent', 0) > self.alert_thresholds['disk_usage_percent']:
            self._send_alert('HIGH_DISK_USAGE', 
                           f"Uso de disco: {metrics['disk_usage_percent']:.1f}%")
    
    def _send_alert(self, alert_type: str, message: str):
        """Enviar alerta."""
        current_time = datetime.utcnow()
        
        # Evitar alertas duplicadas (máximo una por hora)
        if (alert_type in self.last_alerts and 
            current_time - self.last_alerts[alert_type] < timedelta(hours=1)):
            return
        
        self.last_alerts[alert_type] = current_time
        
        alert_data = {
            'alert_type': alert_type,
            'message': message,
            'timestamp': current_time.isoformat(),
            'severity': 'WARNING'
        }
        
        self.logger.warning(f"ALERTA: {message}", **alert_data)
        
        # Aquí se podría integrar con sistemas de alerta externos
        # como Slack, email, PagerDuty, etc.

# Instancias globales
logger = StructuredLogger('agent_ia')
performance_monitor = PerformanceMonitor()
alert_manager = AlertManager(logger)

def get_metrics():
    """Obtener métricas en formato Prometheus."""
    return Response(generate_latest(), media_type=CONTENT_TYPE_LATEST)

def log_request(request: Request, response: Response, duration: float):
    """Log de petición HTTP."""
    metrics = RequestMetrics(
        method=request.method,
        endpoint=request.url.path,
        status_code=response.status_code,
        duration=duration,
        user_agent=request.headers.get('user-agent', ''),
        ip_address=request.client.host if request.client else '',
        timestamp=datetime.utcnow()
    )
    
    logger.info("HTTP Request", **asdict(metrics))
    performance_monitor.record_request(metrics.method, metrics.endpoint, metrics.status_code)

def log_error(error: Exception, endpoint: str = "", context: Dict[str, Any] = None):
    """Log de error."""
    error_metrics = ErrorMetrics(
        error_type=type(error).__name__,
        error_message=str(error),
        endpoint=endpoint,
        stack_trace=getattr(error, '__traceback__', None),
        timestamp=datetime.utcnow()
    )
    
    log_data = asdict(error_metrics)
    if context:
        log_data.update(context)
    
    logger.error(f"Error: {error_metrics.error_message}", **log_data)
    ERROR_COUNT.labels(type=error_metrics.error_type, endpoint=endpoint).inc() 