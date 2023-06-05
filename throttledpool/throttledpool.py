import multiprocessing
import os
import threading
import traceback


class ThrottledPool:
    """Wrapper around multiprocessing.Pool that blocks on task submission (`apply_async`) if
    there are already `task_buffer_size` tasks under processing. This can be useful in
    throttling the task producer thread and avoiding too many tasks piling up in the queue and
    eating up too much RAM."""

    def __init__(self, n_processes=None, task_buffer_size=None, initializer=None):
        """Create a new ThrottledPool.

        Args:
            n_processes: the number of processes to use (defaults to the number of cores)
            task_buffer_size: the maximum number of tasks to be processed at once (defaults to 2
            * n_processes)
            initializer: a function to be called in each process at the beginning of its lifetime
        """

        if n_processes is None:
            n_processes = len(os.sched_getaffinity(0))
        if task_buffer_size is None:
            task_buffer_size = 2 * n_processes
        self.pool = multiprocessing.Pool(processes=n_processes, initializer=initializer)
        self.task_semaphore = threading.Semaphore(task_buffer_size)

    def apply_async(self, f, args, kwargs=None, callback=None):
        """Submit a task to the pool. Blocks if there are already `task_buffer_size` tasks under
        processing.

        Args:
            f: the function to be called
            args: a tuple of arguments to be passed to the function
            kwargs: a dictionary of keyword arguments to be passed to the function
            callback: function to be called when the task is completed

        Returns:
            An AsyncResult object as returned by multiprocessing.Pool.apply_async
        """
        self.task_semaphore.acquire()

        def on_task_completion(result):
            if callback is not None:
                callback(result)
            self.task_semaphore.release()

        if kwargs is None:
            kwargs = {}

        return self.pool.apply_async(safe_fun, args=(f, args, kwargs), callback=on_task_completion)

    def close(self):
        self.pool.close()

    def join(self):
        self.pool.join()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.pool.close()
        self.pool.join()
        self.pool.terminate()


class DummyPool:
    """A dummy replacement for BoundedPool, for testing purposes"""

    def __init__(self, n_processes=None, task_buffer_size=None):
        pass

    def apply_async(self, f, args, kwargs=None, callback=None):
        if kwargs is None:
            kwargs = {}
        result = f(*args, **kwargs)
        if callback is not None:
            callback(result)

    def close(self):
        pass

    def join(self):
        pass

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass


def safe_fun(f, args, kwargs):
    try:
        return f(*args, **kwargs)
    except BaseException:
        traceback.print_exc()
        raise
