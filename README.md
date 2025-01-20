# JWipe: Secure File Wiping Utility

## Description
JWipe is a Python-based utility designed for securely wiping files by overwriting their data multiple times with random and zeroed patterns, ensuring complete data destruction. This utility is useful for security-conscious users who need to ensure files cannot be recovered after deletion.

## Features
- Overwrites file data multiple times with alternating patterns.
- Confirmation prompt to prevent accidental deletion.
- Progress bar to track overwrite progress.
- Secure deletion of files after the wipe process.

## Prerequisites
- Python 3.x installed on your system.
- Sufficient permissions to modify and delete files.

## Installation
```sh
# Clone the repository (if applicable)
git clone <repository-url>
cd JWipe
```

## Usage
### 1. Basic Script (Test Version)
This script performs secure wiping without a confirmation prompt or progress bar.

```python
import os
import random

def secure_wipe(file_path, passes=3):
    if not os.path.exists(file_path):
        print("Error: File does not exist.")
        return
    
    file_size = os.path.getsize(file_path)
    try:
        with open(file_path, "r+b") as file:
            for i in range(passes):
                pattern = os.urandom(4096) if i % 2 else b'\x00' * 4096
                print(f"Pass {i+1}/{passes}: Overwriting file...")
                file.seek(0)
                for _ in range(file_size // len(pattern)):
                    file.write(pattern)
                    file.flush()
                    os.fsync(file.fileno())
        os.remove(file_path)
        print("File securely wiped and deleted.")
    except Exception as e:
        print(f"Error: {e}")

# Usage
# secure_wipe("test_wipe_file.img", passes=3)
```

### 2. Enhanced Script (With Confirmation & Progress Bar)
This script includes a confirmation prompt and displays a progress bar during the wipe process.

```python
import os
import random
import sys
import time

def secure_wipe_with_progress(file_path, passes=3):
    if not os.path.exists(file_path):
        print("Error: File does not exist.")
        return

    file_size = os.path.getsize(file_path)
    confirm = input(f"WARNING: This will permanently delete '{file_path}'. Type 'CONFIRM' to proceed: ")
    if confirm != "CONFIRM":
        print("Operation canceled.")
        return

    try:
        with open(file_path, "r+b") as file:
            for i in range(passes):
                pattern = os.urandom(4096) if i % 2 else b'\x00' * 4096
                print(f"Pass {i+1}/{passes}: Overwriting file...")
                file.seek(0)
                for j in range(file_size // len(pattern)):
                    file.write(pattern)
                    file.flush()
                    os.fsync(file.fileno())
                    progress = (j + 1) / (file_size // len(pattern)) * 100
                    sys.stdout.write(f"\rProgress: [{int(progress)//2 * '='}{(50 - int(progress)//2) * ' '}] {progress:.2f}%")
                    sys.stdout.flush()
                print()
        os.remove(file_path)
        print("File securely wiped and deleted.")
    except Exception as e:
        print(f"Error: {e}")

# Usage
# secure_wipe_with_progress("test_wipe_file.img", passes=3)
```

## License
This project is open-source and available for modification and redistribution.

## Author
Developed by Ningineer.
