(pipeline-resumption)=
# Pipeline Resumption in QIIME 2

```{note}
This is more of an advanced user or system administrator usage document.
[This is slated to move](https://github.com/caporaso-lab/developing-with-qiime2/issues/29) to the new general-purpose user documentation.

```

If a {term}`Pipeline` fails at some point during its execution, and you rerun it, QIIME 2 can attempt to reuse the results that were calculated by the `Pipeline` before it failed.

## Pipeline resumption through the command line interface (CLI)

By default, when you run a {term}`Pipeline` on the CLI, QIIME 2 will create a pool in its cache (either the default cache, or the cache specified using the `--use-cache` parameter).
This poll will named based on the scheme: `recycle_<plugin>_<action>_<sha1('plugin_action')>`.
This pool will store all intermediate results created by the pipeline.

Should the `Pipeline` run succeed, this pool will be removed.
However, should the `Pipeline` run fail, you can rerun the `Pipeline` and the intermediate results stored in the pool will be reused to avoid doing duplicate work.

If you wish to specify the specific poll that you would like QIIME 2 should use, either on a `Pipeline`'s first run or on a resumption, you can specify the pool using the `--recycle-pool` option, followed by the name of the pool you wish to use.
This pool will be created in the cache if it does not already exist.
The `--no-recycle` flag may be passed if you do not want QIIME 2 to attempt to recycle any past results or to save the results from this run for future reuse.

It is not necessarily possible to reuse prior results if your inputs to the `Pipeline` differ on resumption with respect to what was provided on the initial run.
In this situation, QIIME 2 will still try to reuse any results that are not dependent on the inputs that changed, but there is no guarantee anything will be usable.

## Pipeline resumption through the Python 3 API

When using the Python API, pools are specified using context managers (i.e., using Python's `with` statement).
If you don't want to enable resumption, don't use the context manager. 

```python
from qiime2.core.cache import Cache

cache = Cache('cache_path')
pool = cache.create_pool('pool', reuse=True)

with pool:
    # run your pipeline here
```