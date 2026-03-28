import os

def get_needs_action_path():
    """Get the path to the Needs_Action directory."""
    return os.path.join(os.getcwd(), "Needs_Action")

def get_plans_path():
    """Get the path to the Plans directory."""
    return os.path.join(os.getcwd(), "Plans")

def get_pending_approval_path():
    """Get the path to the Pending_Approval directory."""
    return os.path.join(os.getcwd(), "Pending_Approval")

def get_approved_path():
    """Get the path to the Approved directory."""
    return os.path.join(os.getcwd(), "Approved")

def get_rejected_path():
    """Get the path to the Rejected directory."""
    return os.path.join(os.getcwd(), "Rejected")

def get_drafts_path():
    """Get the path to the Drafts directory."""
    return os.path.join(os.getcwd(), "Drafts")

def get_done_path():
    """Get the path to the Done directory."""
    return os.path.join(os.getcwd(), "Done")

def get_logs_path():
    """Get the path to the Logs directory."""
    return os.path.join(os.getcwd(), "Logs")

def get_reports_path():
    """Get the path to the Reports directory."""
    return os.path.join(os.getcwd(), "Reports")

def get_errors_path():
    """Get the path to the Errors directory."""
    return os.path.join(os.getcwd(), "Errors")