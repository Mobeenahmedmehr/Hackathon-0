import threading
import time
import logging
from Watchers.gmail_watcher import GmailWatcher
from Watchers.whatsapp_watcher import WhatsappWatcher
from Watchers.linkedin_watcher import LinkedinWatcher
from core.orchestrator import Orchestrator
from auditor.scheduler import ReportScheduler
from logging_setup import get_logger

def start_watchers():
    """Start all watcher services"""
    watchers = []

    # Start Gmail watcher
    gmail_watcher = GmailWatcher()
    gmail_thread = threading.Thread(target=gmail_watcher.start_monitoring, daemon=True)
    gmail_thread.start()
    watchers.append(('Gmail', gmail_thread))
    logger = get_logger(__name__)
    logger.info("Gmail watcher started")

    # Start WhatsApp watcher
    whatsapp_watcher = WhatsappWatcher()
    whatsapp_thread = threading.Thread(target=whatsapp_watcher.start_monitoring, daemon=True)
    whatsapp_thread.start()
    watchers.append(('WhatsApp', whatsapp_thread))
    logger.info("WhatsApp watcher started")

    # Start LinkedIn watcher
    linkedin_watcher = LinkedinWatcher()
    linkedin_thread = threading.Thread(target=linkedin_watcher.start_monitoring, daemon=True)
    linkedin_thread.start()
    watchers.append(('LinkedIn', linkedin_thread))
    logger.info("LinkedIn watcher started")

    return watchers

def start_orchestrator():
    """Start the main orchestrator loop"""
    orchestrator = Orchestrator()
    orchestrator_thread = threading.Thread(target=orchestrator.run, daemon=True)
    orchestrator_thread.start()
    logger = get_logger(__name__)
    logger.info("Orchestrator started")
    return orchestrator, orchestrator_thread

def start_scheduler():
    """Start the report scheduler"""
    scheduler = ReportScheduler()
    scheduler_thread = threading.Thread(target=scheduler.start, daemon=True)
    scheduler_thread.start()
    logger = get_logger(__name__)
    logger.info("Report scheduler started")
    return scheduler, scheduler_thread

def main():
    """Main entry point to start the entire AI Employee system"""
    # Initialize logging
    logger = get_logger(__name__)
    logger.info("Starting AI Employee system...")

    try:
        # Start all services
        watchers = start_watchers()
        orchestrator, orchestrator_thread = start_orchestrator()
        scheduler, scheduler_thread = start_scheduler()

        logger.info("All services started successfully")
        logger.info("AI Employee system is now running...")

        # Keep the system running indefinitely
        while True:
            # Check if any threads have died and restart them if needed
            for name, thread in watchers:
                if not thread.is_alive():
                    logger.error(f"{name} watcher thread died, restarting...")
                    # Restart the watcher
                    if name == "Gmail":
                        gmail_watcher = GmailWatcher()
                        new_thread = threading.Thread(target=gmail_watcher.start_monitoring, daemon=True)
                        new_thread.start()
                        watchers[0] = (name, new_thread)
                    elif name == "WhatsApp":
                        whatsapp_watcher = WhatsappWatcher()
                        new_thread = threading.Thread(target=whatsapp_watcher.start_monitoring, daemon=True)
                        new_thread.start()
                        watchers[1] = (name, new_thread)
                    elif name == "LinkedIn":
                        linkedin_watcher = LinkedinWatcher()
                        new_thread = threading.Thread(target=linkedin_watcher.start_monitoring, daemon=True)
                        new_thread.start()
                        watchers[2] = (name, new_thread)

            if not orchestrator_thread.is_alive():
                logger.error("Orchestrator thread died, restarting...")
                orchestrator = Orchestrator()
                new_thread = threading.Thread(target=orchestrator.run, daemon=True)
                new_thread.start()
                orchestrator_thread = new_thread

            if not scheduler_thread.is_alive():
                logger.error("Scheduler thread died, restarting...")
                scheduler = ReportScheduler()
                new_thread = threading.Thread(target=scheduler.start, daemon=True)
                new_thread.start()
                scheduler_thread = new_thread

            # Sleep to prevent excessive CPU usage
            time.sleep(10)

    except KeyboardInterrupt:
        logger.info("Received interrupt signal, shutting down...")
    except Exception as e:
        logger.error(f"Unexpected error in main: {str(e)}", exc_info=True)
    finally:
        logger.info("AI Employee system shutdown complete")

if __name__ == "__main__":
    main()