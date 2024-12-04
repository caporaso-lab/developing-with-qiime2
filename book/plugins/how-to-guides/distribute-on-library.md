(share-on-qiime2-library)=
# Distribute plugins on QIIME 2 Library

Distributing your plugin on the QIIME 2 Library is a simple process that requires your plugin to conform to the following standards.

## A GitHub repo

Your plugin must exist as a GitHub repo. Please consult the [](share-on-github) documentation if you need help with this.

## A GitHub about section

Your GitHub repo must have an about section.

This will be used as the short description for your plugin in Library. It should be 300 or so characters max and should describe what your plugin is.

## A top level README

Your GitHub repo must contain a top level README. This README must be written in GitHub MarkDown.

This will be rendered as MarkDown on Library and should give a detailed description of your plugin and what it does.

NOTE: If your README references any resources using paths relative to the root of your repository (images for example) these resources WILL NOT LOAD on QIIME 2 Library. Only resources referenced with absolute URLs will load. This is because we are not cloning and rehosting your assets. We need a valid URL to a resource hosted somewhere online.

## Conda environment files for Installation

This is the highest bar to clear to get your plugin hosted on the QIIME 2 Library.

More detailed instructions on how to do this are provided at [](facilitating-installation).

In broad strokes, your repo must include environment.yml files installing your plugin for each QIIME 2 release you support using following naming scheme `<plugin-name>-qiime2-<distro>-<epoch>.yml`. These files must be located in the `/environment-files` folder.

### Additional requirements for environment files

1. Your plugin must be fully installable via these environment files with no extra steps required.
2. Your environment files must NOT contain a `name` field. The end user is expected to provide the name of the environment on the command line when they install.

# How to add a plugin to the QIIME 2 Library
Once you have met the above requirements, open a PR against the [library-plugins](https://github.com/qiime2/library-plugins) GitHub repo adding a `<my-plugin-name>.yml` file to the `plugins` folder. This file must have the following `key: value` pairs:

```
owner: <repo-owner>
name: <repo-name>
branch: <target-branch>
docs: <latest-docs-url>
```

## Example PR

An [example PR](https://github.com/qiime2/library-plugins/pull/3) showing the addition of a plugin to the library in a single atomic commit.

NOTE: Your plugin must be compliant with the above specifications for us to merge your PR.
