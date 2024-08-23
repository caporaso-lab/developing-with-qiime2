# Handling exceptions in parallel Pipelines

In developing parallel computing support in QIIME 2, we tried to minimize the edits that are required to existing Pipelines to enable them to run in parallel.
In the code we developed in the [plugin tutorial](plugin-tutorial-parallel-pipeline), for example, the modifications we made were primarily to support the splitting and combining steps - we didn't add anything to explicitly integrate parallel computing.
There is one minor exception to this though.

If you have code that looks like the following in a Pipeline that you want to run in parallel:

```python
try:
    result1, result2 = some_action(*args)
except SomeException:
    do.something()
```

You must call `_result()` on the return value from `some_action` in the try/except block:

```python
try:
    results = some_action(*args)
    result1, result2 = results._result()
except SomeException:
    do.something()
```

If you do not do this, a parallel run of your Pipeline will most likely crash if `SomeException` is raised.

The reason for this is that when the Pipeline is run in parallel, the return value from `some_action` will be a [Future](https://parsl.readthedocs.io/en/stable/userguide/futures.html) that will eventually resolve into your actual results when the parallel processes complete.
Calling `._result()` blocks the main thread and waits for results before proceeding from the try/except block.

If you do not call `_result()` in the try block, the Future will most likely resolve into results after the main Python thread has exited the try/except block.
This will lead to the exception not being caught, because it is now actually being raised outside of the try/except.
