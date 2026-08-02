import os
import subprocess
import atexit

_process = None

def _cpu_workers():
    try:
        n = len(os.sched_getaffinity(0))
    except (AttributeError, OSError):
        n = os.cpu_count()
    return n if n and n > 0 else 1

def stress_start():
    global _process
    if _process is None:
        _process = subprocess.Popen(["stress", "--cpu", str(_cpu_workers())], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

def stress_stop():
    global _process
    if _process:
        _process.terminate()
        _process.wait(timeout=1)
        _process = None

atexit.register(stress_stop)
