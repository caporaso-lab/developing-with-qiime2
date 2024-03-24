(plugin-from-template)=
# Create the plugin from a template

The easiest way to create a new QIIME 2 plugin is using our [Cookiecutter template](https://cookiecutter.readthedocs.io/en/stable/), which can be found at https://github.com/caporaso-lab/cookiecutter-qiime2-plugin.
Here we'll work through building your QIIME 2 plugin from this template.

To start building your new plugin, first install a QIIME 2 development environment (see [](setup-dev-environment)). Then, activate your development environment.

Next, install cookiecutter in your QIIME 2 development environment using the following command:

```shell
pip install cookiecutter
```

Then, use `cookiecutter` to create your plugin from the template using the following command:

```shell
cookiecutter gh:caporaso-lab/cookiecutter-qiime2-plugin
```

During the plugin creation, you'll be prompted for information on your plugin.
Fill this information in as it's requested, or accept the default values - either is fine.
The plugin I'm going to create will be called `q2-dwq2` (for *Developing with QIIME 2*). You can call your plugin `q2-dwq2`, or whatever you prefer.

After the plugin has been created, change into the top-level directory for the plugin.
For me, that's `q2-dwq2/`.
Run the following command to install your plugin in developer mode:

```shell
make dev
```

Then, have the command line interface cache information about your plugin by running:

```shell
qiime dev refresh-cache
```


 To confirm that your plugin is now available, run:

 ```shell
qiime info
```

You should see your new plugin in the list of available plugins. If you request help text on your plugin (e.g., `qiime dwq2 --help`), you should see some of the information you provided when creating the plugin.

The template plugin includes a simple (and silly) action called `duplicate-table`, along with associated unit tests. This provides an example action and example unit tests. You'll ultimately want to delete this action, but for now let's use this action to make sure everything is working as expected.

First, run the unit tests as follows:

```shell
py.test
```

This should produce a bunch of output, ending with text that looks like the following:

```shell
==== 2 passed, 7 warnings in 2.75s ====
```

This tells you that the unit tests for your plugin all passed (we're not concerned about the warnings right now).

Next, if you call your plugin's `duplicate-table` action with the `--help` parameter (e.g., `qiime dwq2 duplicate-table --help`), you should see text that looks like the following:

```shell
Usage: qiime dwq2 duplicate-table [OPTIONS]

  Create a copy of a feature table with a new uuid. This is for demonstration
  purposes only. 🧐

Inputs:
  --i-table ARTIFACT FeatureTable[Frequency]
                          The feature table to be duplicated.       [required]
Outputs:
  --o-new-table ARTIFACT FeatureTable[Frequency]
                          The duplicated feature table.             [required]
Miscellaneous:
  --output-dir PATH       Output unspecified results to a directory
  --verbose / --quiet     Display verbose output to stdout and/or stderr
                          during execution of this action. Or silence output
                          if execution is successful (silence is golden).
  --example-data PATH     Write example data and exit.
  --citations             Show citations and exit.
  --help                  Show this message and exit.
```

After you've confirmed that both of the above commands worked as expected, you're ready to start working on this plugin.
Open the top-level plugin directory in your text editor of choice (I recommend [VS Code](https://code.visualstudio.com/), if you don't already have one that you're comfortable with).
Poke through all of the files to familiarize yourself with the structure of your plugin's Python package.
Don't worry if it's not clear what everything is yet - we'll get to all of that.

Congratulations - you've created a working QIIME 2 plugin from a template!
If you'd like to try the action out, you can call your `duplicate-table` action on any QIIME 2 `FeatureTable[Frequency]` artifact (e.g., you can download one from the [QIIME 2 user documentation](https://docs.qiime2.org)).
Load your duplicated table with [QIIME 2 View](https://view.qiime2.org), and poke through its Provenance to see how data provenance is recorded for your plugin.

Next, we'll [](add-nw-align-method).

```{tip}
You can see my code after following these steps by looking at [the specific commit in my plugin repository on GitHub](https://github.com/caporaso-lab/q2-dwq2/commit/3465ea40b18ae15825411a5930cfd24016f5d872).
```