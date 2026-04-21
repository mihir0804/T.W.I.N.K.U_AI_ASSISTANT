import subprocess
import sys
import time
import os

# You can place this file in your Startup folder or run it manually.
# Wait for 10 seconds to ensure the system is ready
time.sleep(10)

current_dir = os.path.dirname(os.path.abspath(__file__))

# Start Twinku completely hidden
subprocess.Popen(
    [sys.executable, "main.py", "--startup"],
    creationflags=subprocess.CREATE_NO_WINDOW,
    cwd=current_dir
)
