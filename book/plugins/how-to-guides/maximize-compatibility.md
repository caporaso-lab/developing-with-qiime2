(plugin-how-to-maximize-compatibility)=
# Maximize compatibility between your plugin(s) and existing QIIME 2 distribution(s)

You can build your QIIME 2 tools in your own way.
Your new tool doesn't need to live in the [QIIME 2 GitHub organization](https://github.com/qiime2) or be part of one of the QIIME 2 distributions developed and maintained in the [Caporaso Lab](https://cap-lab.bio).

If you want your QIIME 2 plugin(s) or other tools to work with existing QIIME 2 {term}`distribution(s) <Distribution>`, your focus should be on maximizing compatibility between your plugin(s) and the relevant QIIME 2 distribution(s).
To do this, you can observe the {term}`artifact classes <Artifact class>` that are used in the target distribution(s), and make your functionality compatible with those.
Avoid defining new artifact classes when you can reuse existing ones, to maximize compatibility and interoperability (as well as reducing your own software development time!).
A complete list of artifact classes and formats available in a deployment of QIIME 2 can be accessed with the `qiime tools list-types` and `qiime tools list-formats` commands.
(Some are missing documentation - we'd [love your help addressing that](https://github.com/caporaso-lab/developing-with-qiime2/issues/97).)
If you do need to create new artifact classes, you can add these in your own plugin(s).

The Caporaso Lab is not taking on new responsibility for distributing plugins right now (i.e., integrating them in the distributions they develop and maintain), but we are currently (23 April 2024) developing new mechanisms for helping you share your plugin or other tools (see [](plugin-how-to-publicize)) that will ultimately replace the [QIIME 2 Library](https://library.qiime2.org).

You can consider the existing distributions to be foundations that you can build on, or you can create and distribute your own conda metapackages.
Some guidance on each of these approaches:
   - Your install instructions can indicate that a user should install whichever distribution you depend on (e.g., `tiny`, `amplicon`, or `metagenome`) and then illustrate how to install your plugin(s) in that environment however it makes sense (e.g., `conda` or `pip`). Complete install instructions are drafted for you in the `README.md` of plugins that you build using our template (see [](plugin-from-template)).
   - Alternatively, you can compose and share your own distribution of plugins (e.g., building from the `tiny` distribution) that captures the set of functionality you’d like to share.

Either of these approaches is totally fine, with the following caveat.
The former is an easier starting point, and will allow us to provide more troubleshooting assistance for any installation issues that users may encounter.
While the latter provides you with more flexibility in your environment construction, our assistance with any install issues or environment conflicts that users may run into will be more limited (and will ultimately be your responsibility to troubleshoot and resolve).

With the above information in mind, below are examples of how we recommend constructing installation instructions for users for both of the discussed pathways.

## Installing your plugin on top of an existing QIIME 2 Distribution (recommended)

The easiest way to instruct users to install your plugin in the context of an existing QIIME 2 Distribution is to create an environment file that they will use to install the relevant distribution along with the correct version of your plugin, all while using a single command.

In the top-level directory of your plugin, create the following directory:

```
environment-files/
```

Within this directory, you'll create environment file(s) for current and/or past installable versions of your plugin. You can name them with a pattern like `YYYY.MM-<module-name>-environment.yml` (for example, `2024.05-q2-dwq2-environment.yml`).

The contents of your environment file should look something like this:

```
channels:
- https://packages.qiime2.org/qiime2/20XX.REL/<target-distribution>/released
- conda-forge
- bioconda
- defaults
dependencies:
  - qiime2-<target-distribution>
  - pip
  - pip:
    - <module_name>@git+https://github.com/<your-github-org>/<module-name>.git@<target-branch>
```

With the following terms defined:
- 20XX.REL epoch corresponding to the QIIME 2 release version that your plugin is compatible with
- `<target-distribution>` being the distribution your plugin should be utilized with (i.e. amplicon, metagenome)
- `<module_name>` being the name of your plugin
- <your-github-org> either being the github organization your plugin is hosted under, or your personal github account name
- <module-name> being the name for your plugin on github
- <target-branch> being the relevant branch that users should be utilizing to install your plugin

Using the above guidelines, you can include the following example installation instructions for your users on your Github README page:
```
conda env create -n my-plugin-env -f https://raw.githubusercontent.com/<your-github-org>/<module-name>/<env-file-branch>/environment-files/20XX.REL-<module-name>-environment.yml
```

With <env-file-branch> being defined as the branch of your plugin's github repository where the environment files are located (we recommend the main branch for this, just to keep things simple).

This method also provides an easy way for users to update their environment any time you create a new release for your plugin on Github.
Using different branches on your repository as release locations, you can create a new environment file for each release with your plugin's install location reflecting the new target (i.e. release) branch.

As an example, your branch structure could look like the following:

```
release-2024.5
release-2024.10
```
Which would result in the following environment files (with amplicon as the target distribution):

2024.5
- Environment file name:
`2024.5-my-plugin-environment.yml`

- Contents:
```
channels:
- https://packages.qiime2.org/qiime2/2024.5/amplicon/released
- conda-forge
- bioconda
- defaults
dependencies:
  - qiime2-amplicon
  - pip
  - pip:
    - my_plugin@git+https://github.com/my-plugin-org/my-plugin.git@release-2024.5
```

2024.10
- Environment file name:
`2024.10-my-plugin-environment.yml`

- Contents:
```
channels:
- https://packages.qiime2.org/qiime2/2024.10/amplicon/released
- conda-forge
- bioconda
- defaults
dependencies:
  - qiime2-amplicon
  - pip
  - pip:
    - my_plugin@git+https://github.com/my-plugin-org/my-plugin.git@release-2024.10
```

Users' initial install command would look like this:

```
conda env create -n my-plugin -f https://raw.githubusercontent.com/my-plugin-org/my-plugin/main/environment-files/2024.5-my-plugin-environment.yml
```

With the next release file looking identical aside from the branch name and target release (2024.10), users would then run the following command to update their existing 2024.5 environment:

```
conda env update -n my-plugin -f https://raw.githubusercontent.com/my-plugin-org/my-plugin/main/environment-files/2024.10-my-plugin-environment.yml
```

Note that you may want to utilize a different branch location for your environment files than for each of your package releases (i.e. main branch on the repo vs. a specific release branch).
This will allow for all of your environment files to live in a singular location, for ease of reference.

2. Installing your plugin using the Tiny Distribution and any custom required plugins (not recommended)

If you are working on a unique plugin that is not compatible with one of our existing distributions (amplicon, metagenome) that has a few specific q2 plugin dependencies, you'll utilize a similar approach to install option 1 - just with a more customized environment file.
As a reminder, while this approach is fairly straightforward to implement, we don't recommend this (if at all possible) because this will be more difficult for us to assist with and help users to troubleshoot.
As long as you are aware of these limitations and wish to proceed in this way, please follow the steps below.

You'll follow the same steps above for creating an `environment-files/` directory and for the naming structure of your environment file, but the contents of your environment file(s) will look a bit different.
We'll explore an example plugin below that requires q2-feature-table and q2-composition.

```
channels:
- https://packages.qiime2.org/qiime2/2024.5/tiny/released
- https://packages.qiime2.org/qiime2/2024.5/amplicon/released
- conda-forge
- bioconda
- defaults
dependencies:
  - qiime2-tiny
  - q2-feature-table
  - q2-composition
  - pip
  - pip:
    - my_plugin@git+https://github.com/my-plugin-org/my-plugin.git@release-2024.5
```

In this example, the plugin being developed requires q2-feature-table and q2-composition but is not compatible with the entire amplicon distribution.
In order for this plugin to still work with a basic QIIME 2 environment, the tiny distribution must be included in addition to the two QIIME 2 plugin dependencies.
The tiny distribution's metapackage will be installed from the first channel that includes tiny, and because the two plugin dependencies are a part of the amplicon distribution, this is why the second conda channel provided is from amplicon.

As a general rule, this will be the structure of your customized environment files:
```
channels:
- https://packages.qiime2.org/qiime2/20XX.REL/tiny/released
- https://packages.qiime2.org/qiime2/20XX.REL/<my-plugin-deps-distro>/released
- conda-forge
- bioconda
- defaults
dependencies:
  - qiime2-tiny
  - <my-plugin-dep-1>
  - pip
  - pip:
    - my_plugin@git+https://github.com/my-plugin-org/my-plugin.git@release-2024.5
```

With <my-plugin-deps-distro> corresponding to the distribution where the QIIME 2 dependencies for your plugin live, and <my-plugin-dep-1> being the QIIME 2 dependenc(ies) needed.
Note that if you have plugin dependencies spanning multiple distributions, you'll need to include each distribution's channel in your environment file.

The weekly development builds of the QIIME 2 distributions can help you make sure your code stays current with the distribution(s) you are targeting as you can automate your testing against them.
[](setup-dev-environment) will help you install the most recent successful development metapackage build (again, usually weekly, but sometimes the builds fail and take time to debug).

There are a couple of things that we recommend implementing to help you ensure that your plugin remains compatible within the QIIME 2 ecosystem:

1. Continuous Integration (CI) to regularly run your plugin's unit tests within the type of QIIME 2 environment where it should be used (i.e. Amplicon, Metagenome, Tiny plus custom selections).

To implement this, you'll need to create a Github Action (GHA) that will be triggered each time you make a commit to your repository - either through a pull request (PR) or a direct commit to one of your remote branches.
Github Actions can be a bit confusing to set up, so we'd recommend familiarizing yourself with [this GHA guide](https://hutchdatascience.org/GitHub_Automation_for_Scientists) before moving forward.
Once you've read through this (and hopefully played around with a few of the toy examples provided therein), you can start to put one together based on a re-usable workflow we've created for community plugins.

Here is what the basic structure of your action will look like:
```
name: ci-my-plugin
on:
  pull_request:
    branches: ["<target>"]
  push:
    branches: ["<target>"]
jobs:
  ci:
    uses: qiime2/distributions/.github/workflows/lib-community-ci.yaml@dev
    with:
      github-repo: q2-my-plugin
      env-file-name: 20XX.REL-my-plugin-environment.yml
```
With the following terms defined:
- <target> being the branch where this action should be run.
This will typically be your main branch (i.e. 'main') unless you have a special branching structure setup on your Github repository.
- `github-repo` being the repository name of your plugin on Github.
- `env-file-name` being the name of your target environment file for the current release cycle (full filename including .yml extension).

This Github Action file will live under `.github/workflows/` and you can use the same name as your Github Action for the filename (i.e. `ci-my-plugin.yml`).
Note that the extension will also be `.yml` (same as your environment file(s)).

2. Perform (automated) weekly builds of your plugin to keep your package up to date and expose any dependency conflicts that may arise.

Keeping your package up to date with all of the downstream dependencies can feel like a lot of work and hassle, and sometimes it inevitably can be - software is always changing, and the more dependencies your plugin has, the more likely it is to fall out of sync with at least one of them.
In addition to running your unit tests for each commit and/or pull request you submit to your plugin's repository, we recommend implementing regularly scheduled testing of your plugin against the latest changes to the environment it should be used under (i.e. Amplicon, etc).
The process for this will be very similar to the Github action discussed above for regular testing - with the main difference being that your plugin's environment will be installed with the latest developmental changes within the relevant distribution, rather than a release version.
We suggest having these tests run on a weekly basis to make sure you have ample time between QIIME 2 releases to fix any dependency conflicts or issues from code changes that may arise.

Here's the basic structure of the GHA you'll create to initiate these scheduled tests against your target distribution's development environment:
```
name: cron-my-plugin
on:
  workflow_dispatch: {}
  schedule:
    - cron: 0 0 * * SUN
jobs:
  ci:
    uses: qiime2/distributions/.github/workflows/lib-community-ci.yaml@dev
    with:
      github-repo: q2-my-plugin
      env-file-name: 20XX.DEV-my-plugin-environment.yml
```
You'll notice that this action is very similar to the one you created earlier for your continuous integration testing. The main differences are as follows:

  1. The trigger for this action (i.e. `on:`) is different than our `ci-my-plugin.yml` action in that it's not triggered by a pull request or commit.
  In this example, it's either triggered manually (`workflow_dispatch`) or based on a schedule (`cron`).
  You can utilize the manual trigger under your repository's `actions` tab if you'd like to re-run these scheduled tests sooner than the next scheduled occurrence (if you're troubleshooting a test failure or upstream dependency issue).
  You can adjust the schedule to any frequency you'd prefer, but we recommend weekly testing to ensure you catch anything that may have fallen out of sync well in advance of the upcoming release.
  More information on the formatting for cron scheduling can be found [here](https://www.ibm.com/docs/en/db2/11.5?topic=task-unix-cron-format).

  2. The environment file that's targeted for this action is different than what's used in your continuous integration testing (`20XX.DEV` vs `20XX.REL`).
  The idea here is that your continuous integration testing is targeting the released version of your QIIME 2 environment, while these scheduled tests are targeting the current development environment.
  In order to support this, you'll need to create a new 'development' environment file with each QIIME 2 release, with the following specifications:
```
channels:
- https://packages.qiime2.org/qiime2/20XX.DEV/<target-distribution>/passed
- conda-forge
- bioconda
- defaults
dependencies:
  - qiime2-<target-distribution>
  - pip
  - pip:
    - my_plugin@git+https://github.com/my-plugin-org/my-plugin.git@<dev-branch>
```
With the following terms defined:
- `20XX.DEV` being the n+1 QIIME 2 release (i.e. the upcoming release).
These will always fall on the first Wednesday of April and October, so you can plan accordingly.
As an example, if the most current release was 2024.10, your 20XX.DEV version would be 2025.4.
  - Note that you will need to adjust the environment file versions within your two Github Actions with each new release (i.e. `ci-my-plugin` always needs to be targeting the current QIIME 2 release and `cron-my-plugin` always needs to be targeting the n+1 QIIME 2 release).
- <target-distribution> being (as defined earlier) the distribution your environment should be based on (i.e. Amplicon, Metagenome, Tiny).
- <dev-branch> being the main branch you're using for current development of your plugin.
This might commonly be the `main` branch on your Github repository, or something else (if you have a special branching structure set up) - but the main takeaway here is this is the location of your active development (i.e. latest features, bug fixes, improvements, etc).

You're welcome to set up any additional actions that you feel will be beneficial to your plugin and general development workflow - but the actions outlined above are what we recommend having in order to maintain an active and healthy plugin within the QIIME 2 ecosystem.

You can request feedback on your plugin as a whole from more experienced QIIME 2 developers by reaching out through the {{ developer_discussion }}.
However, be cognizant of the fact that doing code review takes a long time to do well: you should only request this when you feel like you have a final draft of the plugin that you'd like to release, and expect that the reviewer may point out that there is a bunch more work that should be done before you release.
Please have others who you work closely with -- ideally experienced software developers, and even more ideally experienced QIIME 2 plugin developers -- review it first.
If you have questions along the way, you can ask those whenever - just be sure to review *[Developing with QIIME 2](https://develop.qiime2.org/)* and search the forum in case your question has already been answered previously.
