(plugin-from-template)=
# Create your plugin from a template

The easiest way to create a new QIIME 2 plugin is using our [Cookiecutter template](https://cookiecutter.readthedocs.io/en/stable/), which can be found at https://github.com/caporaso-lab/cookiecutter-qiime2-plugin.
Here we'll work through building your QIIME 2 plugin from this template.

## Install the tools needed for templating your plugin

To start building your new plugin, first install cookiecutter using [their installation instructions](https://cookiecutter.readthedocs.io/en/stable/README.html#installation). (If you opt to install cookiecutter with `pipx`, which the cookiecutter developers recommend, you can find the `pipx` installation instructions [here](https://pipx.pypa.io/stable/).)

```{admonition} Optionally initialize a git repository during plugin templating
:class: dropdown
If `git` is installed in your environment, at the end of the templating process, a new git repository will be initialized and a first commit will be made.
This facilitates managing your plugin in version control, and is especially good practice if you are templating a plugin that you ultimately plan to distribute to others.

You can check if you have git installed by running `git --version`.
If you get a response with a version number (something like `git version 2.44.0`), git is installed and a new local repository will be initialized.
If you get a response suggesting that `git` is not installed, you can just continue and not have cookiecutter create a git repository for you, or you can install [git](https://git-scm.com/book/en/v2/Getting-Started-Installing-Git) and then continue.

The git repository that is created will be a local git repository, meaning that it only exists on your computer and won't be shared through a site like GitHub.
If you'd like to learn how to share your plugins, see [](share-on-github).
```

## Run `cookiecutter` to create your plugin

Next, run `cookiecutter` to create your plugin from the template using the following command.
If you used `pipx` to install `cookiecutter`, follow the instructions in the *pipx* tab - otherwise follow the instructions in the *Other* tab.

`````{tab-set}
````{tab-item} pipx
```shell
pipx run cookiecutter gh:caporaso-lab/cookiecutter-qiime2-plugin
```
````

````{tab-item} Other
```shell
cookiecutter gh:caporaso-lab/cookiecutter-qiime2-plugin
```
````
`````

During the plugin templating process, you'll be prompted for information on your new plugin.
For the questions about the *Target distribution* and whether you're *targeting the stable or latest development QIIME 2 release*, use the default values unless you have a specific reason not to; these are the last two questions, as of this writing in May 2024.
For all of the other questions, feel free to customize your plugin by providing whatever values you'd like.

The plugin I'm going to create will be called `q2-dwq2` (for *Developing with QIIME 2*). You can call your plugin `q2-dwq2`, or whatever you prefer.
After you've answered all of the questions, your plugin should have been successfully created and be ready to be installed and used.

```{note}
If you'd like to learn more about the files that were created in this process, you can refer to [](plugin-package-explanation).
You don't need to know what all of these files are to continue the tutorial though, so you can also come back to that later.
```

## Install and test your new plugin

After the plugin has been created, change into the top-level directory for the plugin.
For me, that's `q2-dwq2/`.
In that directory, you'll find a file called `README.md`, which has a section on it containing *Installation instructions*.
Follow all of the installation instructions, and then follow the instructions in that file for testing and using your new plugin.

After completing all of those steps, you now have a QIIME 2 deployment on your computer that contains includes your new plugin in it, and when you requested help text on your plugin (e.g., `qiime dwq2 --help`), you should have seen some of the information you provided when creating the plugin.

The template plugin includes a simple (and silly) action called `duplicate-table`, along with associated unit tests.
This provides an example action and example unit tests.
You'll ultimately want to delete this action, but for now let's use this action to make sure everything is working as expected.

Call your plugin's `duplicate-table` action with the `--help` parameter (e.g., `qiime dwq2 duplicate-table --help`), you should see text that looks like the following:

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

After you've confirmed that the commands in the README.md file work, and that the above command worked as expected, you're ready to start working on this plugin.
Open the top-level plugin directory in your text editor of choice (I recommend [VS Code](https://code.visualstudio.com/), if you don't already have one that you're comfortable with).
Poke through all of the files to familiarize yourself with the structure of your plugin's Python package.

Congratulations - you've created a working QIIME 2 plugin from a template!
If you'd like to try the action out, you can call your `duplicate-table` action on any QIIME 2 `FeatureTable[Frequency]` artifact (e.g., you can download one from the [QIIME 2 user documentation](https://docs.qiime2.org)).
Load your duplicated table with [QIIME 2 View](https://view.qiime2.org), and poke through its Provenance to see how data provenance is recorded for your plugin.

Next, we'll [](add-nw-align-method).

```{tip}
You can see my code after following these steps by looking at the specific commit in my plugin repository on GitHub: {{ dwq2_cookiecutter_build_commit_url }}.
```