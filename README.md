# ThrottledPool
Parallel process pool that throttles the task producer thread to avoid out-of-memory issues.

## Examples usage

```python

results = []
with throttledpool.ThrottledPool() as pool:
    for item in items:
        pool.apply_async(process_fn, (item, other_arg), kwargs=dict(a=1), callback=results.append)

examples.sort(key=lambda ex: ex.image_path)
return p3ds.Pose3DDataset(joint_info, examples)
