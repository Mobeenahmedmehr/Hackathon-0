"""
Common paths used throughout the AI Employee system
"""

import os

# Base directories
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Task directories
DONE_DIR = os.path.join(BASE_DIR, "Done")
ERRORS_DIR = os.path.join(BASE_DIR, "Errors")
NEEDS_ACTION_DIR = os.path.join(BASE_DIR, "Needs_Action")
PLANS_DIR = os.path.join(BASE_DIR, "Plans")
PENDING_APPROVAL_DIR = os.path.join(BASE_DIR, "Pending_Approval")
APPROVED_DIR = os.path.join(BASE_DIR, "Approved")
REJECTED_DIR = os.path.join(BASE_DIR, "Rejected")
DRAFTS_DIR = os.path.join(BASE_DIR, "Drafts")
REPORTS_DIR = os.path.join(BASE_DIR, "Reports")

# Log directory
LOGS_DIR = os.path.join(BASE_DIR, "Logs")

# Watchers directory
WATCHERS_DIR = os.path.join(BASE_DIR, "Watchers")

# Config directory
CONFIG_DIR = os.path.join(BASE_DIR, "config")

# Core directory
CORE_DIR = os.path.join(BASE_DIR, "core")

# AI directory
AI_DIR = os.path.join(BASE_DIR, "ai")

# Utils directory
UTILS_DIR = os.path.join(BASE_DIR, "utils")