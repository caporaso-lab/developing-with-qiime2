Parallelizing QIIME 2 Pipelines
###############################

QIIME 2 supports parallelization of pipelines through `Parsl <https://parsl.readthedocs.io/en/stable/1-parsl-introduction.html>`_. This allows for faster execution of QIIME 2 pipelines by ensuring that pipeline steps that can run simultaneously do run simultaneously assuming the compute resources are available.

A `Parsl configuration <https://parsl.readthedocs.io/en/stable/userguide/configuring.html>`_ is required to use Parsl. This configuration tells Parsl what resources are available to it, and how to use them. How to create and use a Parsl configuration through QIIME 2 depends on which interface you're using and will be detailed on a per-interface basis below.

For basic usage, we have supplied a vendored configuration that we load from a .toml file that will be used by default if you instruct QIIME 2 to execute in parallel without a particular configuration. This configuration file is shown below.

.. code-block::

    [parsl]
    strategy = "None"

    [[parsl.executors]]
    class = "ThreadPoolExecutor"
    label = "default"
    max_threads = numCPUs - 1

    [[parsl.executors]]
    class = "HighThroughputExecutor"
    label = "htex"
    max_workers = numCPUs - 1

    [parsl.executors.provider]
    class = "LocalProvider"

And as an actual parsl.Config object in Python

.. code-block:: Python

    config = Config(
        executors=[
            ThreadPoolExecutor(
                label='default',
                max_threads=max(psutil.cpu_count() - 1, 1)
            ),
            HighThroughputExecutor(
                label='htex',
                max_workers=max(psutil.cpu_count() - 1, 1),
                provider=LocalProvider()
            )
        ],
        # AdHoc Clusters should not be setup with scaling strategy.
        strategy=None
    )

You can read the Parsl docs for more details, but basically we seek to parallelize your jobs by splitting them across multiple threads in a `ThreadPoolExecutor <https://parsl.readthedocs.io/en/stable/stubs/parsl.executors.ThreadPoolExecutor.html?highlight=Threadpoolexecutor>`_ by default while also setting up what Parsl calls a `HighThroughputExecutor <https://parsl.readthedocs.io/en/stable/stubs/parsl.executors.HighThroughputExecutor.html?highlight=HighThroughputExecutor>`_  that you can use for bigger jobs. The HighThroughputExecutor splits jobs across multiple processes.

Parallelization on the CLI
++++++++++++++++++++++++++

There are two flags that allow you to parallelize a pipeline through the cli. One is the `--parallel` flag. This flag will use the following process to determine the configuration it loads.

1. Check the environment variable QIIME2_CONFIG for a filepath to a configuration file.

2. Check the path appdirs.user_config_dir('qiime2')/qiime2_config.toml

3. Check the path appdirs.site_config_dir('qiime2')/qiime2_config.toml

4. Check the path CONDA_PREFIX/etc/qiime2_config.toml

5. Write the vendored configuration to the path in step 4 and use that.

Note: this means that after your first time running this without a config in the first 3 locations the path referenced in step 4 will always exist and contain the default config unless you remove the file.

The other flag to use Parsl through the cli is the `--parallel-config` flag followed by a path to a configuration file. This allows you to easily create and use your own custom configuration based on your system.

Parallelization in the Python API
+++++++++++++++++++++++++++++++++

Parallelization in the Python API is done using `ParallelConfig` objects as context managers. These objects take a parsl config object and a dictionary mapping action names to executor names. If no config is provided your vendored config will be used (found following the steps from the `--parallel` flag above).

The Parsl config object itself can be created in several different ways.

First, you can just create it using Parsl directly:

.. code-block:: Python

    import psutil

    from parsl.config import Config
    from parsl.providers import LocalProvider
    from parsl.executors.threads import ThreadPoolExecutor
    from parsl.executors import HighThroughputExecutor


    config = Config(
        executors=[
            ThreadPoolExecutor(
                label='default',
                max_threads=max(psutil.cpu_count() - 1, 1)
            ),
            HighThroughputExecutor(
                label='htex',
                max_workers=max(psutil.cpu_count() - 1, 1),
                provider=LocalProvider()
            )
        ],
        # AdHoc Clusters should not be setup with scaling strategy.
        strategy=None
    )

Or, you can create it from a QIIME 2 config file

.. code-block:: Python

    from qiime2.sdk.parallel_config import get_config, get_mapping


    config = get_config('path to config')
    mapping = get_mapping(config)

Once you have your config and/or your mapping, you do the following

.. code-block:: Python

    from qiime2.sdk.parallel_config import ParallelConfig


    # Note that the mapping can also be a dictionary literal
    with ParallelConfig(parsl_config=config, action_executor_mapping=mapping):
        future = # <your_qiime2_action>.parallel(args)
        # Make sure to call _result inside of the context manager
        result = future._result()

Note for Pipeline Developers
++++++++++++++++++++++++++++

This needs to be noted somewhere in the dev docs for pipelines, if you have something like this in a pipeline

.. code-block:: Python

    try:
        result1, result2 = some_action(*args)
    except SomeException:
        do something

You must now call _result() on the return value from the action in the try/except. This is necessary to allow people to run your pipeline in parallel. If you do not do this, and someone attempts to run your pipeline in parallel, it will most likely fail.

.. code-block:: Python

    try:
        # You can do it like this
        result1, result2 = some_action(*args)._result()
        # Or you can do it like this
        results = some_action(*args)
        result1, result2 = results._result()
    except SomeException:
        do something

The reason this needs to be done is a bit technical. Basically, if the pipeline is being executed in parallel, the return value from the action will be a future that will eventually resolve into your results when the parallel thread returns. Calling ._result() blocks the main thread and waits for results before proceeding.

If you do not call _result() in the try/except, the future will most likely resolve into results after the main Python thread has exited the try/except block. This will lead to the exception not being caught because it is now actually being raised outside of the try/except.

It's a bit confusing as parallelism often is, and we tried hard to make sure developers wouldn't need to change anything about their pipelines to parallelize them, but we did need to make this one concession.
