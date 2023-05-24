Pipeline Resumption in QIIME 2
##############################

If a pipeline fails at some point during its execution, and you rerun the pipeline, QIIME 2 can attempt to reuse the results that were calculated by the pipeline before it failed.

Pipeline Resumption in the CLI
++++++++++++++++++++++++++++++

By default, when you run a pipeline on the CLI, QIIME 2 will create a pool in the cache you are using (either the default cache or the cache specified by `--use-cache`) called "recycle_<plugin>_<action>_<sha1('plugin_action')>." This pool will be used to store all intermediate results created by the pipeline.

It is also possible to pass the `--recycle-pool` flag followed by the name of a pool you wish to use. This pool will be created in the cache if it does not already exist. The `--no-recycle` flag may be passed if you do not want QIIME 2 to attempt to recycle any past results or to save the results from this run for future reuse.

Should the pipeline succeed, this pool will be removed; however, should the pipeline fail you can rerun the pipeline and the intermediate results stored in the pool will be reused to avoid doing duplicate work.

Obviously, it is not necessarily possible to reuse prior results if your inputs to the pipeline are different the second time. In this case, QIIME 2 will still try to reuse any results that are not dependent on the inputs that changed, but there is no guarantee anything will be usable.

Pipeline Resumption in the Python API
+++++++++++++++++++++++++++++++++++++

When using the Python API, you simply with in a pool to be used for resumption. If you don't want resumption, just don't with in a pool.

.. code-block:: Python

    from qiime2.core.cache import Cache

    cache = Cache('cache_path')
    pool = cache.create_pool('pool', reuse=True)

    # You can with in the cache and the pool separately (the pool you with in must belong to the cache you with in)
    with cache:
        with pool:
            # run your pipeline here

    # You can also just with in the pool. Withing in the pool also withs in the cache it belongs to
    with pool:
        # run your pipeline here