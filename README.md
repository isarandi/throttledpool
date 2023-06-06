# ThrottledPool
Parallel process pool that throttles the task producer thread to avoid out-of-memory issues.

## Example usage

```python

results = []
with throttledpool.ThrottledPool() as pool:
    for item in items:
        pool.apply_async(process_fn, (item, other_arg), kwargs=dict(a=1), callback=results.append)
