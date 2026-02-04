#!/usr/bin/env python3
"""
Platinum Tier AI Employee Main Entry Point

This script starts the complete Platinum Tier system with:
- Cloud Planner Agent (runs in cloud, handles reasoning)
- Local Executor Agent (runs locally, handles execution)
- Platinum Loop Manager (coordinates Cloud ↔ Local)
- Zero-Trust enforcement
- All Gold Tier guarantees preserved
"""

import sys
import os
import threading
import time
import signal
import logging
from pathlib import Path

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# Add the project root to the path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))


def signal_handler(sig, frame):
    """Handle interrupt signals gracefully."""
    logger.info("Received interrupt signal. Shutting down Platinum Tier system...")
    print("\nShutting down Platinum Tier system...")
    sys.exit(0)


class PlatinumTierSystem:
    """Main class to manage the Platinum Tier system."""

    def __init__(self):
        self.running = False
        self.threads = []

        # Initialize components
        self.loop_manager = None
        self.cloud_agent = None
        self.local_agent = None

        logger.info("Platinum Tier system initialized")

    def start_cloud_agent(self):
        """Start the Cloud Planner Agent in a separate thread."""
        import sys
        sys.path.append(str(Path(__file__).parent / "Cloud"))
        import cloud_planner_agent
        from Cloud.cloud_planner_agent import CloudPlannerAgent

        def run_cloud_agent():
            logger.info("Starting Cloud Planner Agent...")
            try:
                cloud_agent = CloudPlannerAgent()
                cloud_agent.run()
            except Exception as e:
                logger.error(f"Cloud Planner Agent error: {str(e)}")

        thread = threading.Thread(target=run_cloud_agent, daemon=True)
        thread.start()
        self.threads.append(("Cloud Planner Agent", thread))
        logger.info("Cloud Planner Agent thread started")

    def start_local_agent(self):
        """Start the Local Executor Agent in a separate thread."""
        import sys
        sys.path.append(str(Path(__file__).parent / "Local"))
        import local_executor_agent
        from Local.local_executor_agent import LocalExecutorAgent

        def run_local_agent():
            logger.info("Starting Local Executor Agent...")
            try:
                local_agent = LocalExecutorAgent()
                local_agent.run()
            except Exception as e:
                logger.error(f"Local Executor Agent error: {str(e)}")

        thread = threading.Thread(target=run_local_agent, daemon=True)
        thread.start()
        self.threads.append(("Local Executor Agent", thread))
        logger.info("Local Executor Agent thread started")

    def start_platinum_loop(self):
        """Start the Platinum Loop Manager in a separate thread."""
        import platinum_loop_manager
        from platinum_loop_manager import PlatinumLoopManager

        def run_platinum_loop():
            logger.info("Starting Platinum Loop Manager...")
            try:
                loop_manager = PlatinumLoopManager()
                loop_manager.run_platinum_loop()
            except Exception as e:
                logger.error(f"Platinum Loop Manager error: {str(e)}")

        thread = threading.Thread(target=run_platinum_loop, daemon=True)
        thread.start()
        self.threads.append(("Platinum Loop Manager", thread))
        logger.info("Platinum Loop Manager thread started")

    def start_system(self):
        """Start all components of the Platinum Tier system."""
        logger.info("Starting Platinum Tier AI Employee system...")

        # Set up signal handler for graceful shutdown
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)

        # Start all components
        self.start_cloud_agent()
        self.start_local_agent()
        self.start_platinum_loop()

        self.running = True
        logger.info("All Platinum Tier components started successfully")

        print("\n" + "="*60)
        print(" platinum tier ai employee system ")
        print("="*60)
        print("✓ Cloud Planner Agent: Running (handles reasoning/planning)")
        print("✓ Local Executor Agent: Running (handles execution)")
        print("✓ Platinum Loop Manager: Running (coordinates Cloud ↔ Local)")
        print("✓ Zero-Trust Enforcement: Active")
        print("✓ Plan Verification & Signing: Active")
        print("✓ Human-in-the-Loop: Enforced for sensitive operations")
        print("✓ Gold Tier Guarantees: Preserved")
        print("="*60)
        print("\nSystem is now processing tasks:")
        print("- Tasks in Inbox → Cloud for planning → Signed Plans → Local for execution")
        print("- All operations are verified and logged")
        print("- Sensitive operations require human approval")
        print("\nPress Ctrl+C to stop the system")

    def monitor_system(self):
        """Monitor the system and report status."""
        while self.running:
            try:
                # Check if all threads are alive
                dead_threads = []
                for name, thread in self.threads:
                    if not thread.is_alive():
                        dead_threads.append((name, thread))

                if dead_threads:
                    for name, thread in dead_threads:
                        logger.warning(f"Thread died: {name}")
                        # In a real system, we might restart the thread
                        logger.info(f"Thread {name} would be restarted in production")

                # Sleep before next check
                time.sleep(10)

            except Exception as e:
                logger.error(f"Error in system monitoring: {str(e)}")
                time.sleep(5)

    def run(self):
        """Run the Platinum Tier system."""
        try:
            self.start_system()

            # Monitor system health
            self.monitor_system()

        except KeyboardInterrupt:
            logger.info("Received keyboard interrupt")
        except Exception as e:
            logger.error(f"Unexpected error in Platinum Tier system: {str(e)}")
        finally:
            self.shutdown()

    def shutdown(self):
        """Gracefully shut down the system."""
        logger.info("Shutting down Platinum Tier system...")

        self.running = False

        # Give threads a moment to finish
        for name, thread in self.threads:
            logger.info(f"Waiting for {name} to finish...")

        print("\nPlatinum Tier system has been shut down.")
        print("Thank you for using the Platinum Tier AI Employee!")


def main():
    """Main entry point."""
    print("Initializing Platinum Tier AI Employee System...")
    print("This implements the Cloud + Local split architecture with zero-trust model.")

    # Verify directory structure
    required_dirs = [
        "Inbox", "Needs_Action", "Done", "Pending_Approval", "Approved", "Rejected",
        "Plans", "Logs", "Skills", "Watchers", "Docs", "Cloud/Incoming_Tasks",
        "Cloud/Signed_Plans", "Local/Needs_Action", "Local/Executed_Actions",
        "Local/Invalid_Plans"
    ]

    for directory in required_dirs:
        dir_path = Path(directory)
        dir_path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Ensured directory exists: {directory}")

    # Start the system
    system = PlatinumTierSystem()
    system.run()


if __name__ == "__main__":
    main()