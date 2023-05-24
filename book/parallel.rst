Parallelizing QIIME 2 Pipelines
###############################

QIIME 2 supports parallelization of pipelines through `Parsl <https://parsl.readthedocs.io/en/stable/1-parsl-introduction.html>`_. This allows for faster execution of QIIME 2 pipelines by ensuring that pipeline steps that can run simultaneously do run simultaneously assuming the compute resources are available.

A `Parsl configuration <https://parsl.readthedocs.io/en/stable/userguide/configuring.html>`_ is required to use Parsl. This configuration tells Parsl what resources are available to it, and how to use them. How to create and use a Parsl configuration through QIIME 2 depends on which interface you're using and will be detailed on a per-interface basis below.

For basic usage, we have supplied a vendored configuration that we load from a `.toml <https://toml.io/en/>`_ file that will be used by default if you instruct QIIME 2 to execute in parallel without a particular configuration. This configuration file is shown below. We write this file the first time you attempt to use it, and the "X = max(psutil.cpu_count() - 1, 1)" is calculated and written to the file at that time. An actual number is required there for all user made config files.

.. code-block::

    [parsl]
    strategy = "None"

    [[parsl.executors]]
    class = "ThreadPoolExecutor"
    label = "default"
    max_threads = X = max(psutil.cpu_count() - 1, 1)

    [[parsl.executors]]
    class = "HighThroughputExecutor"
    label = "htex"
    max_workers = X = max(psutil.cpu_count() - 1, 1)

    [parsl.executors.provider]
    class = "LocalProvider"

    [parsl.executor_mapping]
    some_action = "htex"

And as an actual Parsl Config object in Python.

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

    # This bit is not part of the actual Parsl Config, this is used to tell
    # QIIME 2 which non-default executors (if any) you want your actions to run
    # on
    mapping = {'some_action': 'htex'}

You can read the Parsl docs for more details, but basically we create a `ThreadPoolExecutor <https://parsl.readthedocs.io/en/stable/stubs/parsl.executors.ThreadPoolExecutor.html?highlight=Threadpoolexecutor>`_ that parallelizes jobs across multiple threads in a process and what Parsl calls a `HighThroughputExecutor <https://parsl.readthedocs.io/en/stable/stubs/parsl.executors.HighThroughputExecutor.html?highlight=HighThroughputExecutor>`_  that parallelizes jobs across multiple processes.

Note: Your config MUST contain an executor with the label default. This is the executor that QIIME 2 will dispatch your jobs to if you do not specify an executor to use. The default executor in the default config is the ThreadPoolExecutor meaning that unless you specify otherwise all jobs that use the default config will run on the ThreadPoolExecutor.

The Config File
---------------

Let's break down that config file further by constructing it from the ground up using 7 as our max threads/workers.

.. code-block::

    [parsl]
    strategy = "None"

This very first part of the file indicates that this is the parsl section of our config. That will be the only section for now, but in the future you may be able to do more with this file! "strategy = 'None'" is a top level Parsl configuration parameter that you can read more about in the Parsl documentation. This may need to be set differently depending on your system. If you were to load this into Python using tomlkit you would get this dictionary.

.. code-block:: Python

    {
        'parsl': {
            'strategy': 'None'
            }
    }

Now let's add an executor.

.. code-block::

    [[parsl.executors]]
    class = "ThreadPoolExecutor"
    label = "default"
    max_threads = 7

The [[ ]] indicates that this is a list and the "parsl.executors" in the middle indicates that this list is called "executors" and belongs under parsl. Now our dictionary looks like the following.

.. code-block:: Python

    {
        'parsl': {
            'strategy': 'None'
            'executors': [
                {'class': 'ThreadPoolExecutor',
                 'label': 'default',
                 'max_threads': 7}
                ]
            }
    }

To add another executor, we simply add another list element. Notice that we also have "parsl.executors.provider" for this one. Some classes of parsl executor require additional classes to fully configure them. These classes must be specified beneath the executor they belong to.

.. code-block::

    [[parsl.executors]]
    class = "HighThroughputExecutor"
    label = "htex"
    max_workers = 7

    [parsl.executors.provider]
    class = "LocalProvider"

Now our dictionary is this.

.. code-block:: Python

    {
        'parsl': {
            'strategy': 'None'
            'executors': [
                {'class': 'ThreadPoolExecutor',
                 'label': 'default',
                 'max_threads': 7},
                {'class': 'HighThroughputExecutor',
                 'label': 'htex',
                 'max_workers': 7,
                 'provider': {'class': 'LocalProvider'}}]
            }
    }

Finally, we have the executor_mapping, this section tells us which actions you would like to run on which executors. If an action is unmapped, it will run on the default executor.

.. code-block::

    [parsl.executor_mapping]
    some_action = "htex"

And our final result is the following. We use the executor mapping internally to tell Parsl where you want you actions to run, the rest of the information is used to instantiate the Parsl Config object shown above.

.. code-block:: Python

    {
        'parsl': {
            'strategy': 'None'
            'executors': [
                {'class': 'ThreadPoolExecutor',
                 'label': 'default',
                 'max_threads': 7},
                {'class': 'HighThroughputExecutor',
                 'label': 'htex',
                 'max_workers': 7,
                 'provider': {'class': 'LocalProvider'}}],
            'executor_mapping': {'some_action': 'htex'}
            }
    }

Parallelization on the CLI
++++++++++++++++++++++++++

There are two flags that allow you to parallelize a pipeline through the CLI. One is the --parallel flag. This flag will use the following process to determine the configuration it loads.

1. Check the environment variable QIIME2_CONFIG for a filepath to a configuration file.

2. Check the path appdirs.user_config_dir('qiime2')/qiime2_config.toml

3. Check the path appdirs.site_config_dir('qiime2')/qiime2_config.toml

4. Check the path CONDA_PREFIX/etc/qiime2_config.toml

5. Write the vendored configuration to the path in step 4 and use that.

Note: this means that after your first time running this without a config in the first 3 locations the path referenced in step 4 will always exist and contain the default config unless you remove the file.

The other flag to use Parsl through the CLI is the --parallel-config flag followed by a path to a configuration file. This allows you to easily create and use your own custom configuration based on your system.

Parallelization in the Python API
+++++++++++++++++++++++++++++++++

Parallelization in the Python API is done using ParallelConfig objects as context managers. These objects take a Parsl Config object and a dictionary mapping action names to executor names. If no config is provided your default config will be used (found following the steps from the --parallel flag above).

The Parsl Config object itself can be created in several different ways.

First, you can just create it using Parsl directly.

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

Or, you can create it from a QIIME 2 config file.

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
