#!/usr/bin/env python

try:
    import os
    import subprocess
    import signal
    from functools import wraps

except ImportError as e:
    raise ImportError(str(e) + "- required module not found")

def file_create(path, mode=None):
    """
    Checks if a file has been created with the appropriate permissions
    """
    def run_cmd(cmd):
        if os.geteuid() != 0:
            cmd.insert(0, 'sudo')
        subprocess.check_output(cmd)

    file_path = os.path.dirname(path)
    if not os.path.exists(file_path):
        run_cmd(['mkdir', '-p', file_path])
    if not os.path.isfile(path):
        run_cmd(['touch', path])
    if (mode is not None):    
        run_cmd(['chmod', mode, path])

def cancel_on_sigterm(func):
    """
    Wrapper for a function which has to be cancel on SIGTERM
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        def handler(sig, frame):
            if sigterm_handler:
                sigterm_handler(sig, frame)
            raise Exception("Canceling {}() execution...".format(func.__name__))

        sigterm_handler = signal.getsignal(signal.SIGTERM)
        signal.signal(signal.SIGTERM, handler)
        result = None
        try:
            result = func(*args, **kwargs)
        finally:
            signal.signal(signal.SIGTERM, sigterm_handler)
        return result
    return wrapper

def limit_execution_time(execution_time_secs: int):
    """
    Wrapper for a function whose execution time must be limited
    Args:
        execution_time_secs: maximum execution time in seconds,
        after which the function execution will be stopped
    """
    def wrapper(func):
        @wraps(func)
        def execution_func(*args, **kwargs):
            def handler():
                raise

            signal.signal(signal.SIGALRM, handler)
            signal.alarm(execution_time_secs)
            result = None
            try:
                result = func(*args, **kwargs)
            except Exception:
                raise
            finally:
                signal.alarm(0)

            return result
        return execution_func
    return wrapper

