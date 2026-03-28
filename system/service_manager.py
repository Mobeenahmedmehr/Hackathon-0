import time
import psutil
import threading
from datetime import datetime
from logging_setup import get_logger

class ServiceManager:
    """
    Monitor and restart system components.
    Features:
    • check if watchers are running
    • restart failed services
    • log system health
    """

    def __init__(self, watchers=None, orchestrator=None):
        self.watchers = watchers or []
        self.orchestrator = orchestrator
        self.logger = get_logger(__name__)
        self.running = False

    def check_watcher_status(self):
        """Check if watcher threads are running"""
        statuses = {}

        for i, watcher in enumerate(self.watchers):
            # Since we're passing thread objects, we check if they're alive
            if hasattr(watcher, '__class__') and 'Thread' in str(type(watcher)):
                # If it's a thread object
                statuses[f'watcher_{i}'] = watcher.is_alive()
            else:
                # If it's a watcher instance, we'd need to implement a status check
                # For now, we'll assume it has a status method or property
                if hasattr(watcher, 'is_running'):
                    statuses[f'watcher_{i}'] = watcher.is_running()
                else:
                    # Assume running if no status method exists
                    statuses[f'watcher_{i}'] = True

        return statuses

    def check_orchestrator_status(self):
        """Check if orchestrator is running"""
        if self.orchestrator is None:
            return False

        # Check if orchestrator has a status method
        if hasattr(self.orchestrator, 'is_running'):
            return self.orchestrator.is_running()
        else:
            # If we don't have a specific status method, assume it's running
            return True

    def restart_failed_services(self):
        """Restart any failed services"""
        watcher_statuses = self.check_watcher_status()

        for name, is_running in watcher_statuses.items():
            if not is_running:
                self.logger.error(f"Service {name} is not running, attempting restart...")
                # Logic to restart the service would go here
                # This would depend on the specific implementation of each watcher

        orchestrator_running = self.check_orchestrator_status()
        if not orchestrator_running:
            self.logger.error("Orchestrator is not running, attempting restart...")
            # Logic to restart orchestrator would go here

    def get_system_health(self):
        """Get overall system health metrics"""
        health_metrics = {
            'timestamp': datetime.now().isoformat(),
            'cpu_percent': psutil.cpu_percent(interval=1),
            'memory_percent': psutil.virtual_memory().percent,
            'disk_usage': psutil.disk_usage('/').percent,
            'watcher_statuses': self.check_watcher_status(),
            'orchestrator_status': self.check_orchestrator_status(),
            'uptime_seconds': time.time() if hasattr(self, '_start_time') else 0
        }

        return health_metrics

    def monitor_services(self):
        """Main monitoring loop"""
        self._start_time = time.time()
        self.running = True

        self.logger.info("Service Manager started")

        while self.running:
            try:
                # Get system health
                health = self.get_system_health()

                # Log health metrics
                self.logger.info(f"System Health: CPU={health['cpu_percent']}%, "
                               f"Memory={health['memory_percent']}%, "
                               f"Watchers={[f'{k}:{v}' for k, v in health['watcher_statuses'].items()]}, "
                               f"Orchestrator={health['orchestrator_status']}")

                # Check for failed services and restart them
                self.restart_failed_services()

                # Wait before next check
                time.sleep(30)  # Check every 30 seconds

            except Exception as e:
                self.logger.error(f"Error in service monitoring: {str(e)}")
                time.sleep(10)  # Wait before retrying after error

    def stop(self):
        """Stop the service manager"""
        self.running = False
        self.logger.info("Service Manager stopped")


if __name__ == "__main__":
    # Example usage
    logger = get_logger(__name__)
    manager = ServiceManager()

    # Run in a separate thread
    monitor_thread = threading.Thread(target=manager.monitor_services)
    monitor_thread.daemon = True
    monitor_thread.start()

    try:
        # Keep the main thread alive
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        manager.stop()
        print("Service manager stopped by user")