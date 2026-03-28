from config.config_loader import load_config
from logging_setup import get_logger
from config.paths import (
    NEEDS_ACTION_DIR, PLANS_DIR, PENDING_APPROVAL_DIR,
    APPROVED_DIR, DRAFTS_DIR, DONE_DIR, ERRORS_DIR,
    LOGS_DIR, REPORTS_DIR
)


def check_system_health() -> str:
    """
    Perform a comprehensive system health check.

    Returns:
        str: Formatted health check summary
    """
    try:
        # Initialize error variables
        config_error = ""
        logging_error = ""

        # Check if config loads properly
        config_loaded = False
        try:
            load_config()
            config_loaded = True
        except Exception as e:
            config_error = str(e)

        # Check if required directories exist
        required_dirs = [
            NEEDS_ACTION_DIR, PLANS_DIR, PENDING_APPROVAL_DIR,
            APPROVED_DIR, DRAFTS_DIR, DONE_DIR, ERRORS_DIR,
            LOGS_DIR, REPORTS_DIR
        ]

        dir_status = {}
        for directory in required_dirs:
            dir_status[directory.name] = directory.exists()

        all_dirs_present = all(dir_status.values())

        # Check if logging system works
        logging_operational = False
        try:
            logger = get_logger("health_check_test")
            logger.info("Health check test log")
            logging_operational = True
        except Exception as e:
            logging_error = str(e)

        # Format the status summary
        status_lines = ["System Health Check"]

        if config_loaded:
            status_lines.append("OK Config loaded")
        else:
            status_lines.append(f"XX Config failed: {config_error}")

        if all_dirs_present:
            status_lines.append("OK Directories present")
        else:
            missing_dirs = [name for name, exists in dir_status.items() if not exists]
            status_lines.append(f"XX Missing directories: {', '.join(missing_dirs)}")

        if logging_operational:
            status_lines.append("OK Logging operational")
        else:
            status_lines.append(f"XX Logging failed: {logging_error}")

        return "\n".join(status_lines)

    except Exception as e:
        return f"Health check failed with error: {str(e)}"


if __name__ == "__main__":
    print(check_system_health())