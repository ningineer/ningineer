import os
import random
from datetime import datetime

def get_timestamp():
    """Returns the current timestamp."""
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")

def secure_wipe(file_path, passes=3, log_file="wipe_log.txt"):
    """
    Securely wipes a file by overwriting it multiple times.
    WARNING: This will destroy all data in the specified file!

    :param file_path: The target file (e.g., "test_wipe_file.img")
    :param passes: Number of overwrite passes (default = 3)
    :param log_file: File to log the wiping process.
    """
    try:
        # Get file size
        file_size = os.path.getsize(file_path)

        # Open log file
        with open(log_file, "a") as log:
            log.write(f"\n[{get_timestamp()}] Starting wipe on {file_path} ({file_size} bytes)\n")

            with open(file_path, "wb") as file:
                for i in range(passes):
                    pattern = os.urandom(4096) if i % 2 else b'\x00' * 4096

                    print(f"[{get_timestamp()}] Pass {i+1}/{passes}: Overwriting with {'random data' if i % 2 else 'zeros'}...")
                    log.write(f"[{get_timestamp()}] Pass {i+1}/{passes} - Writing {'random data' if i % 2 else 'zeros'}\n")

                    file.seek(0)
                    for _ in range(file_size // len(pattern)):
                        file.write(pattern)
                    file.flush()
                    os.fsync(file.fileno())

            # Delete the file after wiping
            os.remove(file_path)
            print(f"[{get_timestamp()}] Secure wipe completed. {file_path} deleted.")
            log.write(f"[{get_timestamp()}] Wipe completed. {file_path} deleted.\n")

    except FileNotFoundError:
        print(f"Error: File {file_path} not found.")
    except PermissionError:
        print("Error: Permission denied. Run as root/admin.")
    except Exception as e:
        print(f"An error occurred: {e}")

# --- TEST CASE: Securely wipe a test file ---
test_file = "test_wipe_file.img"

# Step 1: Create a 10MB test file with random data
if not os.path.exists(test_file):
    print(f"[{get_timestamp()}] Creating test file: {test_file}")
    with open(test_file, "wb") as f:
        f.write(os.urandom(10 * 1024 * 1024))  # 10MB

# Step 2: Run the wipe function
secure_wipe(test_file, passes=3)
