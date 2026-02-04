"""
Zero-Trust Enforcement Module for Platinum Tier AI Employee

This module enforces zero-trust boundaries between Cloud and Local components:
- Treats Cloud and Local as untrusted peers
- Enforces read-only boundaries
- Enforces write-only ownership
- Logs violations and quarantines problematic content
"""

import logging
from pathlib import Path
from datetime import datetime
import json
from typing import List, Dict, Optional, Tuple
import re

logger = logging.getLogger(__name__)

class ZeroTrustEnforcer:
    """Enforces zero-trust boundaries between Cloud and Local systems."""

    def __init__(self):
        self.cloud_dirs = ["Cloud"]
        self.local_dirs = ["Local", "Inbox", "Needs_Action", "Done", "Pending_Approval", "Approved", "Rejected", "Plans", "Logs", "Skills", "Watchers", "Docs", "In_Progress", "Quarantined"]

        # Log file for violations
        self.violation_log_path = Path("Logs") / f"zero_trust_violations_{datetime.now().strftime('%Y%m%d')}.log"
        Path("Logs").mkdir(exist_ok=True)

    def log_violation(self, operation: str, source: str, dest: str, reason: str) -> None:
        """Log a zero-trust violation."""
        timestamp = datetime.now().isoformat()
        violation_entry = {
            "timestamp": timestamp,
            "operation": operation,
            "source": source,
            "destination": dest,
            "reason": reason,
            "severity": "HIGH"
        }

        # Write to violation log
        with open(self.violation_log_path, 'a', encoding='utf-8') as f:
            f.write(json.dumps(violation_entry) + "\n")

        logger.error(f"ZERO-TRUST VIOLATION: {reason} - {operation} from {source} to {dest}")

    def validate_operation(self, operation: str, source: str, dest: str) -> Tuple[bool, str]:
        """
        Validate that an operation complies with zero-trust principles.

        Args:
            operation: The operation being performed (e.g., "read", "write", "move", "execute")
            source: Source path of the operation
            dest: Destination path of the operation

        Returns:
            Tuple of (is_valid, reason_for_validity_or_violation)
        """
        source_path = Path(source)
        dest_path = Path(dest)

        # Convert to string paths for comparison
        source_str = str(source_path).replace('\\', '/')
        dest_str = str(dest_path).replace('\\', '/')

        # Cloud should not access Local directories directly
        if any(source_str.startswith(cloud_dir) for cloud_dir in self.cloud_dirs):
            if any(dest_str.startswith(local_dir) for local_dir in self.local_dirs):
                reason = f"Cloud component attempted unauthorized access to Local directory: {operation} from {source_str} to {dest_str}"
                self.log_violation(operation, source_str, dest_str, reason)
                return False, reason

        # Local should not modify Cloud plan directories directly
        if any(source_str.startswith(local_dir) for local_dir in self.local_dirs):
            if dest_str.startswith("Cloud/Signed_Plans") or dest_str.startswith("Cloud/Incoming_Tasks"):
                reason = f"Local component attempted unauthorized modification of Cloud directory: {operation} from {source_str} to {dest_str}"
                self.log_violation(operation, source_str, dest_str, reason)
                return False, reason

        # Cloud should not execute files directly
        if any(source_str.startswith(cloud_dir) for cloud_dir in self.cloud_dirs):
            if operation.lower() in ['execute', 'run', 'exec', 'chmod+x']:
                reason = f"Cloud component attempted to execute file: {dest_str} (Cloud should only plan, not execute)"
                self.log_violation(operation, source_str, dest_str, reason)
                return False, reason

        # Cloud should not invoke MCP servers
        if any(source_str.startswith(cloud_dir) for cloud_dir in self.cloud_dirs):
            if 'mcp' in dest_str.lower() or 'server' in dest_str.lower():
                reason = f"Cloud component attempted to invoke MCP server: {dest_str} (Execution should be Local-only)"
                self.log_violation(operation, source_str, dest_str, reason)
                return False, reason

        # Additional checks can be added here

        return True, "Operation complies with zero-trust principles"

    def quarantine_violation(self, file_path: str, reason: str) -> bool:
        """Quarantine a file that caused a violation."""
        try:
            import shutil
            file_path_obj = Path(file_path)

            if not file_path_obj.exists():
                return False

            # Create quarantine directory
            quarantine_dir = Path("Quarantined") / "ZeroTrustViolations"
            quarantine_dir.mkdir(parents=True, exist_ok=True)

            # Create quarantined filename with timestamp and reason
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            quarantined_name = f"zt_violation_{timestamp}_{reason.replace(' ', '_')}_{file_path_obj.name}"
            quarantined_path = quarantine_dir / quarantined_name

            # Move the file
            shutil.move(str(file_path_obj), str(quarantined_path))

            logger.warning(f"Quarantined violating file: {file_path_obj.name} -> {quarantined_path.name}")
            return True

        except Exception as e:
            logger.error(f"Failed to quarantine violating file {file_path}: {str(e)}")
            return False

    def enforce_file_boundary(self, file_path: str, component_type: str) -> Tuple[bool, str]:
        """
        Enforce file access boundaries based on component type.

        Args:
            file_path: Path to the file being accessed
            component_type: Type of component ("Cloud" or "Local")

        Returns:
            Tuple of (is_allowed, reason)
        """
        file_path_str = str(Path(file_path).resolve()).replace('\\', '/')

        if component_type.lower() == "cloud":
            # Cloud should not access Local execution directories
            for local_dir in self.local_dirs:
                if local_dir in file_path_str and local_dir not in ["Plans", "Logs"]:  # Allow some read access for reporting
                    reason = f"Cloud component attempted to access Local directory: {file_path_str}"
                    self.log_violation("access", "Cloud", file_path_str, reason)
                    return False, reason

        elif component_type.lower() == "local":
            # Local should not access Cloud Incoming_Tasks directly (should only read Signed_Plans)
            if "Cloud/Incoming_Tasks" in file_path_str:
                reason = f"Local component attempted unauthorized access to Cloud Incoming_Tasks: {file_path_str}"
                self.log_violation("access", "Local", file_path_str, reason)
                return False, reason

        return True, "File access allowed under zero-trust principles"


# Global instance for convenience
zero_trust_enforcer = ZeroTrustEnforcer()


def validate_operation(operation: str, source: str, dest: str) -> Tuple[bool, str]:
    """Convenience function to validate an operation."""
    return zero_trust_enforcer.validate_operation(operation, source, dest)


def enforce_file_boundary(file_path: str, component_type: str) -> Tuple[bool, str]:
    """Convenience function to enforce file boundary."""
    return zero_trust_enforcer.enforce_file_boundary(file_path, component_type)


def quarantine_violation(file_path: str, reason: str) -> bool:
    """Convenience function to quarantine a violation."""
    return zero_trust_enforcer.quarantine_violation(file_path, reason)


if __name__ == "__main__":
    # Example usage
    print("Testing Zero-Trust Enforcement...")

    # Test valid operation
    is_valid, reason = validate_operation("read", "Cloud/Signed_Plans/plan1.md", "Local/Temp/temp.md")
    print(f"Valid operation test: {is_valid}, Reason: {reason}")

    # Test invalid operation
    is_valid, reason = validate_operation("write", "Cloud/SomeScript.py", "Local/Needs_Action/task.md")
    print(f"Invalid operation test: {is_valid}, Reason: {reason}")

    # Test file boundary enforcement
    is_allowed, reason = enforce_file_boundary("Local/Needs_Action/task.md", "Cloud")
    print(f"Cloud accessing Local test: {is_allowed}, Reason: {reason}")