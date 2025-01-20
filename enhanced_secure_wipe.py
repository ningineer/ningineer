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
