import os
import shutil
from datetime import datetime
from pathlib import Path

# Define source and destination paths
needs_action_dir = Path("Needs_Action")
done_dir = Path("Done")
source_file = needs_action_dir / "TEST_TASK_001.md"

if source_file.exists():
    # Create destination filename with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    dest_filename = f"done_{timestamp}_TEST_TASK_001.md"
    dest_path = done_dir / dest_filename

    # Ensure destination directory exists
    done_dir.mkdir(exist_ok=True)

    # Move the file
    shutil.move(str(source_file), str(dest_path))
    print(f"Successfully moved {source_file} to {dest_path}")
else:
    print(f"Source file {source_file} does not exist")