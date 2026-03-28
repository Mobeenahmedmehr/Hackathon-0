#!/usr/bin/env python3
"""
Validation script to check if all required libraries are installed.
"""

import sys
import importlib

def validate_library(library_name, import_name=None):
    """
    Attempts to import a library and reports success or failure.
    """
    if import_name is None:
        import_name = library_name

    try:
        importlib.import_module(import_name)
        print(f"✔ {library_name} installed")
        return True
    except ImportError:
        print(f"✖ {library_name} missing")
        return False

def main():
    print("Validating AI Employee System dependencies...\n")

    # List of required libraries to validate
    libraries = [
        # Core dependencies
        ("requests", "requests"),
        ("dotenv", "dotenv"),
        ("psutil", "psutil"),
        ("schedule", "schedule"),

        # Google APIs
        ("google.auth", "google.auth"),
        ("googleapiclient.discovery", "googleapiclient.discovery"),
        ("google.oauth2.credentials", "google.oauth2.credentials"),

        # Web automation
        ("playwright", "playwright"),
        ("selenium", "selenium"),

        # Data processing
        ("pandas", "pandas"),
        ("numpy", "numpy"),

        # Document processing
        ("openpyxl", "openpyxl"),
        ("pypdf", "pypdf"),
        ("docx", "docx"),  # python-docx
        ("pptx", "pptx"),  # python-pptx

        # Image processing
        ("PIL", "PIL"),  # Pillow
        ("pdf2image", "pdf2image"),

        # Web parsing
        ("bs4", "bs4"),  # beautifulsoup4
        ("lxml", "lxml"),

        # Security
        ("defusedxml", "defusedxml"),

        # Type hints and validation
        ("pydantic", "pydantic"),
        ("yaml", "yaml"),  # PyYAML
    ]

    total = len(libraries)
    success = 0

    for import_name, display_name in libraries:
        if validate_library(display_name, import_name):
            success += 1

    print(f"\nValidation complete: {success}/{total} libraries installed")

    if success == total:
        print("✅ All dependencies are installed correctly!")
        return 0
    else:
        missing = total - success
        print(f"❌ {missing} libraries are missing.")
        print("\nPlease run: pip install -r requirements.txt")
        return 1

if __name__ == "__main__":
    sys.exit(main())