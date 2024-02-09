(setup-dev-environment)=
# Set up your development environment

This how-to guide describes how to install and set up a QIIME 2 development environment.
The development environment you create will be suitable for creating new or contributing to existing QIIME 2 plugins or interfaces, or contributing to the development of the QIIME 2 framework.

```{warning}
QIIME 2 support for Windows is restricted to Windows Subsystem for Linux (WSL).
The QIIME 2 development team doesn't have much experience developing QIIME 2 in the context of Windows.
If you're comfortable with creating development environments with WSL, we expect that it should work just fine.
If you expect that you might need help setting up your development environment, we'll be able to provide better assitance if you're developing on a Linux or macOS system.
```

## Install Prerequisites

{{ miniconda_url }} provides the ``conda`` environment and package manager, and is currently the only supported way to install QIIME 2.
Follow the instructions for downloading and installing Miniconda.

After installing Miniconda and opening a new terminal, make sure you're running the latest version of ``conda`` (and get a copy of ``wget``, while you're at it):

```bash
conda update conda
conda install wget
```

## Install the latest development version of the QIIME 2 "Tiny Distribution"

The QIIME 2 "Tiny Distribution" is a minimal set of QIIME 2 functionality for building and using plugins through the QIIME 2 command line, and is intended for use by developers who want a minimal QIIME 2 environment to work in.

```{note}
We recommend starting your development with the "Tiny Distribution", unless you specifically need plugins that are installed in other QIIME 2 distributions, such as the "Amplicon" or "Shotgun" distributions, in which case see [](other-distros).
```

`````{tab-set}
````{tab-item} macOS
```bash
wget https://raw.githubusercontent.com/qiime2/distributions/dev/latest/passed/qiime2-tiny-macos-latest-conda.yml
conda env create -n q2dev-tiny --file qiime2-tiny-macos-latest-conda.yml
rm qiime2-tiny-macos-latest-conda.yml
```
````

````{tab-item} Linux
```bash
wget https://raw.githubusercontent.com/qiime2/distributions/dev/latest/passed/qiime2-tiny-ubuntu-latest-conda.yml
conda env create -n q2dev-tiny --file qiime2-tiny-ubuntu-latest-conda.yml
rm qiime2-tiny-ubuntu-latest-conda.yml
```
````
`````

## Activate the ``conda`` environment

You can now activate the environment you just created as follows.

```bash
conda activate q2dev-tiny
```

To test your QIIME 2 environment, run:

```bash
qiime info
```

You should see something like the following, though the version numbers you'll see will be different:

```
System versions
Python version: 3.8.18
QIIME 2 release: 2023.11
QIIME 2 version: 2023.11.0.dev0+15.g8ac7e3e
q2cli version: 2023.11.0.dev0+12.g7cf7a7a

Installed plugins
types: 2023.11.0.dev0+2.g1827eab

Application config directory
/Users/gregcaporaso/miniconda3/envs/q2dev-tiny/var/q2cli

Getting help
To get help with QIIME 2, visit https://qiime2.org
```

The versions listed here, for QIIME 2, q2cli, and q2-types, are development versions as defined by [versioneer](https://github.com/python-versioneer/python-versioneer), and these indicate that you're working in a QIIME 2 development environment (as opposed to working with a specific release version of QIIME 2).

At this stage you should now have a working development environment - time to start hacking!

## Next steps

### Building a new plugin

If you're creating a new plugin, you can now move on to [](start-plugin-tutorial) or [](start-plugin-explainers), depending on whether you'd like to start with step-by-step instructions, or a narrative overview of how QIIME 2 plugins work (respectively).

### Contributing to existing plugins
If you want to make changes to the QIIME 2 framework, q2cli, or any existing plugins, follow these steps (for the sake of this example, we will focus on the example of contributing to developing ``q2-types``):

```bash
# Grab the package source from the relevant source repository.
git clone https://github.com/qiime2/q2-types
cd q2-types

# Install any additional build-time dependencies needed for this project.
# Check ci/recipe/meta.yaml in any QIIME 2 repository under the QIIME 2 GitHub
# organization for build or test requirements. For example, see
# https://github.com/qiime2/q2-types/blob/dev/ci/recipe/meta.yaml
conda install pytest flake8

# Install local source in "development mode", and build any package assets.
make dev

# Run package tests to ensure that everything is okay.
make test
```

(other-distros)=
## Installing other QIIME 2 distributions

```{note}
If you install a distribution other than the "Tiny Distribution", be sure that the environment name in your `conda activate` command (in the example above this was `q2dev-tiny`) matches the value that you provided to the `conda env create` command through the `-n` parameter.
```

### Amplicon distribution

`````{tab-set}
````{tab-item} macOS
```bash
wget https://raw.githubusercontent.com/qiime2/distributions/dev/latest/passed/qiime2-amplicon-macos-latest-conda.yml
conda env create -n q2dev-amplicon --file qiime2-amplicon-macos-latest-conda.yml
rm qiime2-amplicon-macos-latest-conda.yml
```
````

````{tab-item} Linux
```bash
wget https://raw.githubusercontent.com/qiime2/distributions/dev/latest/passed/qiime2-amplicon-ubuntu-latest-conda.yml
conda env create -n q2dev-amplicon --file qiime2-amplicon-ubuntu-latest-conda.yml
rm qiime2-amplicon-ubuntu-latest-conda.yml
```
````
`````

### Shotgun distribution

`````{tab-set}
````{tab-item} macOS
```bash
wget https://raw.githubusercontent.com/qiime2/distributions/dev/latest/passed/qiime2-shotgun-macos-latest-conda.yml
conda env create -n q2dev-shotgun --file qiime2-shotgun-macos-latest-conda.yml
rm qiime2-shotgun-macos-latest-conda.yml
```
````

````{tab-item} Linux
```bash
wget https://raw.githubusercontent.com/qiime2/distributions/dev/latest/passed/qiime2-shotgun-ubuntu-latest-conda.yml
conda env create -n q2dev-shotgun --file qiime2-shotgun-ubuntu-latest-conda.yml
rm qiime2-shotgun-ubuntu-latest-conda.yml
```
````
`````

