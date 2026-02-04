"""
Platinum Tier Plan Verification and Signing Module

This module provides functionality for:
- Computing deterministic hashes of plan content
- Signing plans with cryptographic signatures
- Verifying plan signatures
- Managing signature validation
"""

import hashlib
import hmac
import json
from datetime import datetime
from typing import Dict, Optional, Tuple
import logging

logger = logging.getLogger(__name__)

class PlanSigner:
    """Handles plan signing and verification for Platinum Tier."""

    def __init__(self, secret_key: Optional[str] = None):
        """
        Initialize the PlanSigner.

        Args:
            secret_key: Secret key for HMAC signing. If None, uses a default.
        """
        self.secret_key = secret_key or "platinum_default_secret_key_change_this_in_production"

    def compute_content_hash(self, content: str) -> str:
        """
        Compute deterministic SHA-256 hash of plan content.

        Args:
            content: The plan content to hash

        Returns:
            Hexadecimal representation of the SHA-256 hash
        """
        return hashlib.sha256(content.encode('utf-8')).hexdigest()

    def sign_plan(self, content: str, additional_metadata: Optional[Dict] = None) -> str:
        """
        Sign a plan by appending a signature block.

        Args:
            content: The plan content to sign
            additional_metadata: Additional metadata to include in signature

        Returns:
            The original content with appended signature block
        """
        # Compute the content hash
        content_hash = self.compute_content_hash(content)

        # Create signature data
        signature_data = {
            "hash": content_hash,
            "signed_at": datetime.now().isoformat(),
            "signer": "Platinum_Cloud_Agent",
            "algorithm": "SHA256-HMAC",
        }

        if additional_metadata:
            signature_data.update(additional_metadata)

        # Create HMAC signature of the hash
        signature = hmac.new(
            self.secret_key.encode('utf-8'),
            content_hash.encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        # Create signature block
        signature_block = (
            "\n\n<!-- PLATINUM_SIGNATURE_START -->\n"
            f"<!-- Content Hash: {content_hash} -->\n"
            f"<!-- HMAC Signature: {signature} -->\n"
            f"<!-- Signed At: {signature_data['signed_at']} -->\n"
            f"<!-- Signer: {signature_data['signer']} -->\n"
            f"<!-- Algorithm: {signature_data['algorithm']} -->\n"
        )

        # Add additional metadata if provided
        if additional_metadata:
            for key, value in additional_metadata.items():
                signature_block += f"<!-- {key.title()}: {value} -->\n"

        signature_block += "<!-- PLATINUM_SIGNATURE_END -->\n"

        return content + signature_block

    def extract_signature_block(self, content: str) -> Tuple[str, Optional[Dict]]:
        """
        Extract signature block from plan content and return content without signature.

        Args:
            content: The plan content containing signature

        Returns:
            Tuple of (content_without_signature, signature_data_dict or None)
        """
        signature_start = content.find("<!-- PLATINUM_SIGNATURE_START -->")
        if signature_start == -1:
            return content, None

        signature_end = content.find("<!-- PLATINUM_SIGNATURE_END -->") + len("<!-- PLATINUM_SIGNATURE_END -->")
        if signature_end == -1:
            return content, None

        # Extract the signature block
        signature_block = content[signature_start:signature_end]
        # Extract content without signature
        content_without_signature = content[:signature_start].rstrip()  # Remove trailing whitespace

        # Parse signature data from comments
        signature_data = {}
        for line in signature_block.split('\n'):
            if 'Content Hash:' in line:
                signature_data['hash'] = line.split('Content Hash:')[1].strip().strip('-->')
            elif 'HMAC Signature:' in line:
                signature_data['hmac_signature'] = line.split('HMAC Signature:')[1].strip().strip('-->')
            elif 'Signed At:' in line:
                signature_data['signed_at'] = line.split('Signed At:')[1].strip().strip('-->')
            elif 'Signer:' in line:
                signature_data['signer'] = line.split('Signer:')[1].strip().strip('-->')
            elif 'Algorithm:' in line:
                signature_data['algorithm'] = line.split('Algorithm:')[1].strip().strip('-->')
            # Look for additional metadata fields
            elif ':' in line and 'Hash:' not in line and 'Signature:' not in line and 'At:' not in line and 'Signer:' not in line and 'Algorithm:' not in line:
                clean_line = line.strip().strip('<!--').strip('-->').strip()
                if ':' in clean_line:
                    parts = clean_line.split(':', 1)
                    if len(parts) == 2:
                        key = parts[0].strip()
                        value = parts[1].strip()
                        signature_data[key.lower()] = value

        return content_without_signature, signature_data

    def verify_signature(self, content_with_signature: str) -> Tuple[bool, str]:
        """
        Verify the signature of a plan.

        Args:
            content_with_signature: The plan content with signature

        Returns:
            Tuple of (is_valid, reason_for_invalidity_or_success_message)
        """
        content_without_signature, signature_data = self.extract_signature_block(content_with_signature)

        if not signature_data or 'hash' not in signature_data or 'hmac_signature' not in signature_data:
            return False, "Plan has no valid signature block"

        # Recompute content hash
        expected_content_hash = self.compute_content_hash(content_without_signature)

        # Check if content hash matches the one in signature
        if expected_content_hash != signature_data['hash']:
            logger.warning(f"Content hash mismatch: expected {expected_content_hash}, got {signature_data['hash']}")
            return False, f"Content hash mismatch - plan may have been tampered with"

        # Verify HMAC signature
        expected_hmac = hmac.new(
            self.secret_key.encode('utf-8'),
            signature_data['hash'].encode('utf-8'),
            hashlib.sha256
        ).hexdigest()

        if expected_hmac != signature_data['hmac_signature']:
            logger.warning(f"HMAC signature mismatch: expected {expected_hmac}, got {signature_data['hmac_signature']}")
            return False, f"HMAC signature verification failed - plan may have been altered"

        return True, "Signature verification successful"

    def quarantine_invalid_plan(self, plan_path: str, reason: str) -> bool:
        """
        Quarantine an invalid plan by moving it to the invalid plans directory.

        Args:
            plan_path: Path to the invalid plan
            reason: Reason for quarantining

        Returns:
            True if successfully quarantined, False otherwise
        """
        try:
            import shutil
            from pathlib import Path

            plan_file = Path(plan_path)
            if not plan_file.exists():
                return False

            # Create invalid plans directory if it doesn't exist
            invalid_dir = plan_file.parent / "Invalid_Plans"
            invalid_dir.mkdir(exist_ok=True)

            # Create a new filename with timestamp and reason
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            quarantined_name = f"quarantined_{timestamp}_{reason.replace(' ', '_')}_{plan_file.name}"
            quarantined_path = invalid_dir / quarantined_name

            # Move the file
            shutil.move(str(plan_file), str(quarantined_path))

            logger.warning(f"Quarantined invalid plan: {plan_file.name} -> {quarantined_path.name} ({reason})")
            return True

        except Exception as e:
            logger.error(f"Failed to quarantine plan {plan_path}: {str(e)}")
            return False


# Global instance for convenience (though it's better to inject this as a dependency)
default_signer = PlanSigner()


def sign_plan(content: str, additional_metadata: Optional[Dict] = None) -> str:
    """Convenience function to sign a plan."""
    return default_signer.sign_plan(content, additional_metadata)


def verify_plan_signature(content: str) -> Tuple[bool, str]:
    """Convenience function to verify a plan signature."""
    return default_signer.verify_signature(content)


def quarantine_invalid_plan(plan_path: str, reason: str) -> bool:
    """Convenience function to quarantine an invalid plan."""
    return default_signer.quarantine_invalid_plan(plan_path, reason)


if __name__ == "__main__":
    # Example usage
    sample_plan = "# Sample Plan\n\nThis is a sample plan for testing."

    print("Original plan:")
    print(sample_plan)
    print("\n" + "="*50 + "\n")

    # Sign the plan
    signed_plan = sign_plan(sample_plan, {"priority": "high", "domain": "operations"})
    print("Plan with signature:")
    print(signed_plan)
    print("\n" + "="*50 + "\n")

    # Verify the plan
    is_valid, message = verify_plan_signature(signed_plan)
    print(f"Verification result: {is_valid}")
    print(f"Message: {message}")

    print("\n" + "="*50 + "\n")

    # Test with tampered content
    tampered_plan = signed_plan.replace("sample plan", "modified plan")
    is_valid_tampered, message_tampered = verify_plan_signature(tampered_plan)
    print(f"Tampered plan verification: {is_valid_tampered}")
    print(f"Tampered plan message: {message_tampered}")