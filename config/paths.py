from pathlib import Path


# Base directory of the project
BASE_DIR = Path(__file__).resolve().parent.parent

# Define all important project directories
NEEDS_ACTION_DIR = BASE_DIR / "Needs_Action"
PLANS_DIR = BASE_DIR / "Plans"
PENDING_APPROVAL_DIR = BASE_DIR / "Pending_Approval"
APPROVED_DIR = BASE_DIR / "Approved"
DRAFTS_DIR = BASE_DIR / "Drafts"
DONE_DIR = BASE_DIR / "Done"
ERRORS_DIR = BASE_DIR / "Errors"
LOGS_DIR = BASE_DIR / "Logs"
REPORTS_DIR = BASE_DIR / "Reports"


def setup_directories():
    """Create all required directories if they don't exist."""
    directories = [
        NEEDS_ACTION_DIR,
        PLANS_DIR,
        PENDING_APPROVAL_DIR,
        APPROVED_DIR,
        DRAFTS_DIR,
        DONE_DIR,
        ERRORS_DIR,
        LOGS_DIR,
        REPORTS_DIR
    ]

    for directory in directories:
        directory.mkdir(exist_ok=True)


# Setup directories when this module is imported
setup_directories()