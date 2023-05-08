Parallelizing QIIME 2 Pipelines
###############################

QIIME 2 supports parallelization of pipelines through `Parsl <https://parsl.readthedocs.io/en/stable/1-parsl-introduction.html>`_.
This allows for faster execution of QIIME 2 pipelines by ensuring that pipeline steps that can run simultaneously do run simultaneously assuming the compute resources are available.

From a user perspective, a Parsl configuration is required to use Parsl. This configuration tells Parsl what resources are available to it, and how to use them. How to create and use a Parsl configuration through QIIME 2 depends on which interface you're using and will be detailed on a per-interface basis below.

For basic usage, we have supplied a vendored configuration that we load from a .toml file that will be loaded by default if you instruct QIIME 2 to execute in parallel without a particular configuration. This configuration is shown below.

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

You can read the Parsl docs for more details, but basically we seek to parallelize your jobs by splitting them across multiple threads in a `ThreadPoolExecutor <https://parsl.readthedocs.io/en/stable/stubs/parsl.executors.ThreadPoolExecutor.html?highlight=Threadpoolexecutor>`_ by default while also setting up what Parsl calls a `HighThroughputExecutor <https://parsl.readthedocs.io/en/stable/stubs/parsl.executors.HighThroughputExecutor.html?highlight=HighThroughputExecutor>`_  for bigger jobs.

Parallelization Through the CLI
+++++++++++++++++++++++++++++++

There are two flags that allow you to parallelize a pipeline through the cli. One is the `--parallel` flag. This flag will use the following process to determine the configuration it loads.

1. Check the environment variable QIIME2_CONFIG for a filepath to a configuration file.

2. Check the path appdirs.user_config_dir('qiime2')/qiime2_config.toml

3. Check the path appdirs.site_config_dir('qiime2')/qiime2_config.toml

4. Check the path CONDA_PREFIX/etc/qiime2_config.toml

5. Write the vendored configuration to the path in step 4 and use that.

Note: this means that after your first time running this without a config in the first 3 locations the path referenced in step 4 will always exist and contain the default config unless you remove the file.

The other flag to use Parsl through the cli is the `--parallel-config` flag followed by a path to a configuration file. This allows you to easily create and use your own custom configuration based on your system.

Parallelization Through the Python API
++++++++++++++++++++++++++++++++++++++


