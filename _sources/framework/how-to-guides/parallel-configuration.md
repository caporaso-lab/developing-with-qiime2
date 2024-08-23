(parallel-configuration)=
# Parallel configuration and usage in QIIME 2

```{note}
This is more of an advanced user or system administrator usage document.
[This is slated to move](https://github.com/caporaso-lab/developing-with-qiime2/issues/29) to the new general-purpose user documentation.
```

QIIME 2 supports parallelization of pipelines through [Parsl](https://parsl.readthedocs.io/en/stable/1-parsl-introduction.html>).
This allows for faster execution of QIIME 2 pipelines by ensuring that pipeline steps that can run simultaneously do run simultaneously assuming the compute resources are available.

A [Parsl configuration](https://parsl.readthedocs.io/en/stable/userguide/configuring.html) is required to use Parsl.
This configuration tells Parsl what resources are available to it, and how to use them.
How to create and use a Parsl configuration through QIIME 2 depends on which interface you're using and will be detailed on a per-interface basis below.

For basic usage, we have supplied a vendored configuration that we load from a [`.toml`](https://toml.io/en/) file that will be used by default if you instruct QIIME 2 to execute in parallel without a particular configuration.
This configuration file is shown below.
We write this file the first time you attempt to use it, and the `max(psutil.cpu_count() - 1, 1)` is evaluated and written to the file at that time.
An actual number is required there for all user made config files.

```
[parsl]
strategy = "None"

[[parsl.executors]]
class = "ThreadPoolExecutor"
label = "default"
max_threads = max(psutil.cpu_count() - 1, 1)

[[parsl.executors]]
class = "HighThroughputExecutor"
label = "htex"
max_workers = max(psutil.cpu_count() - 1, 1)

[parsl.executors.provider]
class = "LocalProvider"

[parsl.executor_mapping]
some_action = "htex"
```

An actual `parsel.Config` object in Python looks like the following:

```python
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

# This bit is not part of the actual parsel.Config, but rather is used to tell
# QIIME 2 which non-default executors (if any) you want specific actions to run
# on
mapping = {'some_action': 'htex'}
```

The [Parsl documentation](https://parsl.readthedocs.io/en/stable/) provides full detail.
Briefly, we create a [`ThreadPoolExecutor`](https://parsl.readthedocs.io/en/stable/stubs/parsl.executors.ThreadPoolExecutor.html?highlight=Threadpoolexecutor) that parallelizes jobs across multiple threads in a process.
We also create a [`HighThroughputExecutor`](https://parsl.readthedocs.io/en/stable/stubs/parsl.executors.HighThroughputExecutor.html?highlight=HighThroughputExecutor) that parallelizes jobs across multiple processes.

```{note}
Your config MUST contain an executor with the label default.
This is the executor that QIIME 2 will dispatch your jobs to if you do not specify an executor to use.
The default executor in the default config is the ThreadPoolExecutor meaning that unless you specify otherwise all jobs that use the default config will run on the ThreadPoolExecutor.
```

## The Config File

Let's break down that config file further by constructing it from the ground up using 7 as our max threads/workers.

```
[parsl]
strategy = "None"
```

This very first part of the file indicates that this is the parsl section of our config.
That will be the only section we define at the moment, but in the future we expect to expand on this to provide additional QIIME 2 configuration options through this file.
`strategy = 'None'` is a top level Parsl configuration parameter that you can read more about in the Parsl documentation.
This may need to be set differently depending on your system.
If you were to load this into Python using tomlkit you would get the following dictionary:

```python
{
    'parsl': {
        'strategy': 'None'
        }
}
```

Next, let's add an executor:

```
[[parsl.executors]]
class = "ThreadPoolExecutor"
label = "default"
max_threads = 7
```

The `[[ ]]` indicates that this is a list and the `parsl.executors` in the middle indicates that this list is called `executors` and belongs under parsl.
Now our dictionary looks like the following:

```python
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
```

To add another executor, we simply add another list element.
Notice that we also have `parsl.executors.provider` for this one.
Some classes of parsl executor require additional classes to fully configure them.
These classes must be specified beneath the executor they belong to.

```
[[parsl.executors]]
class = "HighThroughputExecutor"
label = "htex"
max_workers = 7

[parsl.executors.provider]
class = "LocalProvider"
```

Now our dictionary looks like the following:

```python
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
```

Finally, we have the executor_mapping, where you can define which actions, if any, you would like to run on which executors.
If an action is unmapped, it will run on the default executor.

```
[parsl.executor_mapping]
some_action = "htex"
```

Our final result looks like the following.
The `executor_mapping` internally to tell Parsl where you want you actions to run, while the rest of the information is used to instantiate the `parsl.Config` object shown above.

```python
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
```

## Using QIIME 2 in parallel through the command line interface (CLI)

There are two flags that allow you to parallelize a pipeline through the CLI.
The first is the `--parallel` flag.
This flag will use the following priority order to load a Parsl configuration.

1. Check the environment variable `$QIIME2_CONFIG` for a filepath to a configuration file.
2. Check the path `<user_config_dir>/qiime2/qiime2_config.toml`
3. Check the path `<site_config_dir>/qiime2/qiime2_config.toml`
4. Check the path `$CONDA_PREFIX/etc/qiime2_config.toml`
5. Write a default configuration to the path in step 4 and use that.

This implies that after your first time running QIIME 2 in parallel without a config in at least one of the first 3 locations, the path referenced in step 4 will exist and contain the default config (unless you remove the file or switch to a different conda environment).

The second flag related to parallelization through the command line interface is the `--parallel-config` flag, which is used to provide path to a configuration file.
This allows you to easily create and use your own custom configuration based on your system, and a value provided using this parameter overrides the above priority order.

````{admonition} user_config_dir
:class: note
On Linux, `user_config_dir` will usually be `$HOME/.config/qiime2/`.
On macOS, it will usually be `$HOME/Library/Application Support/qiime2/`.

You can get find the directory used on your system by running the following command:

```bash
python -c "import appdirs; print(appdirs.user_config_dir('qiime2'))"
```
````

````{admonition} site_config_dir
:class: note
On Linux `site_config_dir` will usually be something like `/etc/xdg/qiime2/`, but it may vary based on Linux distribution.
On macOS it will usually be `/Library/Application Support/qiime2/`.

You can get find the directory used on your system by running the following command:

```bash
python -c "import appdirs; print(appdirs.site_config_dir('qiime2'))"
```
````


## Using QIIME 2 in parallel through the Python 3 API


Parallelization through the Python API is done using `parsl.Config` objects as context managers.
These objects take a `parsl.Config` object and a dictionary mapping action names to executor names.
If no config is provided your default config will be used (found using the same priority order as described for the `--parallel` flag above).

A `parsl.Config` object itself can be created in several different ways.

First, you can just create it using Parsl directly.

```python
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
```

Alternatively, you can create it from a QIIME 2 config file.

```python
from qiime2.sdk.parallel_config import get_config_from_file

config, mapping = get_config_from_file('path to config')

# Or if you have no mapping
config, _ = get_config_from_file('path to config')

# Or if you only have a mapping and are getting the config from elsewhere
_, mapping = get_config_from_file('path_to_config')
```

Once you have your config and/or your mapping, you can use it as follows:

```python
from qiime2.sdk.parallel_config import ParallelConfig


# Note that the mapping can also be a dictionary literal
with ParallelConfig(parallel_config=config, action_executor_mapping=mapping):
    future = # <your_qiime2_action>.parallel(args)
    # Make sure to call _result inside of the context manager
    result = future._result()
```
