(plugin-package-explanation)=
# The structure of QIIME 2 plugin packages

QIIME 2 doesn't put restrictions on how you structure the Python package that contains your plugin, but there are some conventions that experienced developers follow.
This *Explanation* article will discuss these conventions in the context of the plugin developed in [](plugin-tutorial-intro).

````{margin}
```{tip}
`tree` often isn't installed by default, but you should be able to install it with your preferred package manager (e.g., with `apt-get`, `homebrew`, or whatever you use to install software on your system).
```
````

I'm going to use the `tree` command to get a convenient view of all of the files and directories my plugin package after my first commit.
Then we'll start from the top and talk about what each of these are.

```shell
$ tree -a q2-dwq2
q2-dwq2
├── .copier-answers.yml
├── .git # this will exist if you initialized a git repo (a recommended step)
│   └── # many files
├── .gitattributes
├── .github
│   └── workflows
│       └── ci.yml
├── .gitignore
├── LICENSE
├── Makefile
├── README.md
├── ci
│   └── recipe
│       └── meta.yaml
├── pyproject.toml
├── q2_dwq2
│   ├── __init__.py
│   ├── _methods.py
│   ├── citations.bib
│   ├── plugin_setup.py
│   └── tests
│       ├── __init__.py
│       ├── data
│       │   └── table-1.biom
│       └── test_methods.py
```

(plugin-package-explanation-top-level-directory)=
## `q2-dwq2`

`q2-dwq2` is the top-level directory containing all of the files in the Python package.

### `q2-dwq2/.copier-answers.yml`

This file contains answers to the Copier prompts that were presented during plugin templating.
This file is required for [applying updates to your project with Copier](https://copier.readthedocs.io/en/stable/updating/) (which will reduce work needed to keep your plugin current with QIIME 2, as we may occasionally make updates to the environment file, GitHub Actions workflows, etc.).
You should not edit this file directly.

### `q2-dwq2/.git`

The `.git` directory is where [git](https://git-scm.com/book/en/v2) stores all the version control data for your repository, including the complete history of commits, branches, configuration settings, and metadata.
You should never manually edit files in this directory since git manages it automatically.
Deleting it would remove all your project's version history. [^ai-disclosure]

### `q2-dwq2/.gitattributes`

The `.gitattributes` file lets you configure how git handles specific files in your repository, such as defining which files should have their line endings normalized, which files are binary, or how git should merge certain file types.
It's essentially a way to set per-file or per-directory git behavior rules that apply to everyone who works with your repository. [^ai-disclosure]

### `q2-dwq2/.github`

This directory contains information used by GitHub, and is templated based on the assumption that this plugin will be maintained in a GitHub repository.
GitHub will use some files in this directory in special ways if they exist (see [here](https://stackoverflow.com/a/61301254)).

Following templating, this directory contains a single GitHub Action file, `.github/workflows/ci.yml`.
This defines a GitHub Action that builds the plugin and runs the tests when pulls requests or commits are submitted to GitHub.
To learn more about GitHub Actions, see [GitHub's documentation](https://docs.github.com/en/actions) and/or [GitHub Automation for Scientists](https://hutchdatascience.org/GitHub_Automation_for_Scientists/).

### `q2-dwq2/.gitignore`

A file used by git that specifies filename patterns that should be ignored by git (and therefore not included in revision control).
This helps keep your repository neat and clean by excluding things like temporary files created by text editors or operating systems.
There are lots of examples that you can use or build from [here](https://github.com/github/gitignore).

### `q2-dwq2/LICENSE`

File containing the software's license.
Naming the file this way, and storing it in the top-level directory, enables it to be recognized easily by users or systems (such as GitHub).

### `q2-dwq2/Makefile`

[`make`](https://www.gnu.org/software/make/) instructions for building the Python module, running its tests, and more.
When you run a command like `make test` or `make dev`, you are applying instructions defined in this file.
`make` is a powerful tool, to put it lightly, and it has been around since pre-historic times (i.e., 1976).

### `q2-dwq2/README.md`

The project's readme file.
This is often where someone interested in your Python package will first look for information.
If you manage your project on GitHub, this will be displayed on the repository's front page.

### `q2-dwq2/pyproject.toml`

The `pyproject.toml` file is Python's modern standard for defining project metadata, dependencies, and build configuration all in one place, replacing the older `setup.py` approach.
It uses the TOML format and tells tools like pip how to install your package and what other packages it needs to work properly. [^ai-disclosure]

An important component in this file for QIIME 2 is that the `qiime2.plugins` entry point is defined:

```toml
[project.entry-points.'qiime2.plugins']
"q2-dwq2" = "q2_dwq2.plugin_setup:plugin"
```

This allows the QIIME 2 `PluginManager` to load the module and determine if one or more QIIME 2 plugins are defined in the module, and if so where they can be imported from.
In this case, one plugin is registered (`q2-dwq2`) and it can be imported from `q2_dwq2.plugin_setup` through the variable name `plugin`.
If you prefer to not follow the naming convention described above with respect to `plugin_setup.py`, this is where you can let the `PluginManager` know where it should be looking for your plugin(s).

### `q2-dwq2/q2_dwq2`

The top-level module directory.
This is where all of files relevant to the use of this code with `Python` are stored.
All files not included in this directory can be considered metadata about the Python module.

#### `q2-dwq2/q2_dwq2/__init__.py`

A special file whose existance (even if the file is empty) specifies that this directory is a Python module.
This will often contain `import` statements that the developer wants to propagate up to be module-level imports, enabling statements like `from qiime2 import Artifact`.

#### `q2-dwq2/q2_dwq2/_methods.py`

This is not a required file, but in this plugin it's used to store code for functions that will ultimately be registered as {term}`Methods <Method>`.
As a plugin grows, it may make sense to consider reorganization such as creating a `_methods` directory that contains files with code for each individual Method.

By convention in Python, files, functions, or objects (or anything else) whose name starts with an `_` should be treated as private.
In other words, outside of this specific code base, anything named with a leading underscore shouldn't be referenced or used directly.
This leaves the developer free to make interface changes (such as renaming the `_methods.py`) file without breaking other people's code.

#### `q2-dwq2/q2_dwq2/_version.py`

This is a file created by [The Versioneer](https://github.com/python-versioneer/python-versioneer) to assist with creating versions of software from information in the `.git` directory, if it exists.
You shouldn't ever edit this file directly.

#### `q2-dwq2/q2_dwq2/citations.bib`

This file stores any citations that QIIME 2 will reference for this plugin in [BibTeX](https://www.bibtex.org/) format.
The relative filepath is specified when the Plugin object is initialized, so can be called whatever you'd like.

#### `q2-dwq2/q2_dwq2/plugin_setup.py`

By convention, this file is where the QIIME 2 `Plugin` object is instantiated and where actions and other information are registered to the plugin.
Again, this file can be called anything and live in other places, but it's pretty standard across plugins at this stage so it's a good idea to just adopt this naming convention in your plugin.
(For example, the first thing I typically do when someone sends me their plugin for feedback is read their `plugin_setup.py` file.)

#### `q2-dwq2/q2_dwq2/tests`

This directory contains all unit tests for functionality in the plugin.
Any associated test data files are generally nested under this directory.

##### `q2-dwq2/q2_dwq2/tests/__init__.py`

The file initializing `q2_dwq2/tests` as a submodule in this Python package.

##### `q2-dwq2/q2_dwq2/tests/data`

A directory containing any data files that are used in tests.

##### `q2-dwq2/q2_dwq2/tests/test_methods.py`

The file containing unit tests of the functionality in the module's `_methods.py`
By convention, the naming of test files roughly parallels the naming of the files they are testing.

[^ai-disclosure]: Specified explanations on this page were written in consultation with claude.ai (Anthropic) and used under fair use for educational purposes.