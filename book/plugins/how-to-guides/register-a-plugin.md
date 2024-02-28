(howto-register-plugin)=
# Register a QIIME 2 plugin

This document will describe how to `register` a plugin, allowing this plugin to interact with the QIIME 2 framework.

## Overview

There are several high-level steps to registering a QIIME 2 plugin:

1. A QIIME 2 plugin must define one or more Python 3 functions that will be accessible through QIIME.
2. The plugin must be a Python 3 package that can be installed with `setuptools`.
3. The plugin must then instantiate a `qiime2.plugin.Plugin` object and define some information including the name of the plugin and its URL. In the plugin package’s `setup.py` file, this instance will be defined as an `entry point`.
4. The plugin must then register its functions as QIIME 2 Actions, which will be accessible to users through any of the QIIME 2 interfaces.
5. Optionally, the plugin could be distributed through [Anaconda](https://anaconda.org/) or [pypi](https://pypi.org/) as that will simplify installation for QIIME 2 users.

These steps are covered in detail below.

Writing a simple QIIME 2 plugin should be a straightforward process.
For example, the [`q2-emperor`](https://github.com/qiime2/q2-emperor) plugin, which connects Emperor to QIIME 2, is written in a little over 100 lines of code (excluding unit tests and assets).
It is a standalone plugin that defines how and which functionality in Emperor should be accessible through QIIME 2.
Plugins will vary in their complexity.
For example, a plugin that defines a lot of new functionality would likely be quite a bit bigger.
[q2-diversity](https://github.com/qiime2/q2-diversity) is a good example of this.
Unlike `q2-emperor`, there is some specific functionality (and associated unit tests) defined in this project, and it depends on several other Python 3 compatible libraries.

Before starting to write a plugin, you should install QIIME 2 and some plugins to familiarize yourself with the system and to provide a means for testing your plugin.

## Instantiating a plugin

The next step is to instantiate a QIIME 2 `Plugin` object.
This might look like the following:

```python
from qiime2.plugin import Plugin
import q2_diversity

plugin = Plugin(
    name='diversity',
    version=q2_diversity.__version__,
    website='https://github.com/qiime2/q2-diversity',
    package='q2_diversity',
    description=('This QIIME 2 plugin supports metrics for calculating '
                'and exploring community alpha and beta diversity through '
                'statistics and visualizations in the context of sample '
                'metadata.'),
    short_description='Plugin for exploring community diversity.',
)
```

This will provide QIIME with essential information about your `Plugin`.

The `name` parameter is the name that users will use to access your plugin from within different QIIME 2 interfaces.
It should be a "command-line-friendly" name, so should not contain spaces or punctuation.
(Avoiding uppercase characters and using dashes (`-`) instead of underscores (`_`) are preferable in the plugin `name`, but not required).

`version` should be the version number of your package (the same that is used in its `setup.py`).

`website` should be the page where you'd like end users to refer for more information about your package.

`package` should be the Python package name for your plugin.

`description` should give a brief description of this plugin's functionality.
This will be displayed when that plugin's help documentation is accessed via the QIIME 2 framework.

`short_description` should give a very brief description of this plugin's functionality.
This will be displayed when the QIIME 2 help documentation is accessed.

While not shown in the previous example, plugin developers can optionally provide the following parameters to `qiime2.plugin.Plugin`:

* `citations`: A list of bibtex-formatted citations.
These are provided in a separate `citations.bib` file, loaded via the `Citations` API, and accessed by using their bibtex indices as keys.
Citations can be listed during plugin or action registration, or both, but will usually only be listed for individual actions unless if a single reference is appropriate for all actions in that plugin.
`q2-diversity` has no such plugin-wide citation listed here.

* `user_support_text`: free text describing how users should get help with the plugin (e.g.
issue tracker, StackOverflow tag, mailing list, etc.).
If not provided, users are referred to the `website` for support.
Plugin developers are free to support their plugins on the QIIME 2 Forum, so you can include that URL as the `user_support_text` for your plugin.
If you do that, you should get in the habit of monitoring the QIIME 2 Forum for technical support questions.

The `Plugin` object can live anywhere in your project, but by convention it will be in a file called `plugin_setup.py`.
You can see a complete working example in q2-dwq2 [here](https://github.com/caporaso-lab/q2-dwq2/blob/e8fe1e5b32bfc2a331d48611b3a70b0fa5b19165/q2_dwq2/plugin_setup.py#L21).


## Defining your plugin object as an entry point

Finally, you need to tell QIIME where to find your instantiated `Plugin` object.
This is done by defining it as an `entry_point` in your project's `setup.py` file.
In `q2-diversity`, this is done as follows:

```python
setup(
    ...
    entry_points={
        'qiime2.plugins': ['q2-diversity=q2_diversity.plugin_setup:plugin']
    }
)
```

The relevant key in the `entry_points` dictionary will be `'qiime2.plugins'`, and the value will be a single element list containing a string formatted as `<distribution-name>=<import-path>:<instance-name>`.
`<distribution-name>` is the name of the Python package distribution (matching the value passed for `name` in this call to `setup`); `<import-path>` is the import path for the `Plugin` instance you created above; and `<instance-name>` is the name for the `Plugin` instance you created above.
