# User documentation

As of the time of this writing (12 January 2023) the QIIME 2 user documentation is in a state of transition.
This document presents ideas about where we're planning to go with the user documentation in the future and then covers how to contribute to the current user documentation (https://docs.qiime2.org)

(users-docs-refactor)=
## Plans for refactoring of user documentation

We are moving from a single source of documentation (the current content at https://docs.qiime2.org) to resources for **cross-distribution QIIME 2 documentation**, **within-distribution QIIME 2 reference material**, and **data set specific usage documentation**.

We expect that the **cross-distribution user documentation** will cover topics including:
- building and use a cache, which will expand on the [content here](https://forum.qiime2.org/t/qiime-2-2022-11-is-now-available/25074#artifact-cachehttpsdevqiime2orglatestapi-referencecache-3)
- parallel support, which will expand on the [content here](parallel-configuration)
- provenance replay/viewing, which will expand on the [content here](https://forum.qiime2.org/t/provenance-replay-beta-release-and-tutorial/23279)
- using the interfaces
- recycling old results
- installing old versions of QIIME 2 (why, why not, and how)
- discussion of distributions (why are there multiple? how to deal with that)
- importing/exporting
- viewing .qzvs

**Distribution specific reference material** will likely be the equivalent of our [current plugin/action pages](https://docs.qiime2.org/2023.9/plugins/). These will render all usage examples associated with actions as well, to avoid the need for things like the ["filtering tutorial"](https://docs.qiime2.org/2023.9/tutorials/filtering/) (which isn't really a tutorial, but rather a list of different approaches for filtering data). Ideally generation of distribution-specific reference documentation will be fully automated, such that these docs can be built from any QIIME 2 environment using the `PluginManager`.

**Usage tutorials**, like the [Moving Pictures tutorial](https://docs.qiime2.org/2023.9/tutorials/moving-pictures-usage/), will be dataset specific and may cross distributions (like the [Cancer Microbiome Intervention Tutorial](https://docs.qiime2.org/jupyterbooks/cancer-microbiome-intervention-tutorial/)). This will facilitate the transition from replayed provenance to tutorial, ideally helping to blur the line between replayed provenance and a tutorial over time. To support this, we will likely add a usage driver that generates usage driver source code (for example, select `View Source (qiime2.sdk)` from a [multi-interface tutorial](https://docs.qiime2.org/2023.9/tutorials/moving-pictures-usage/), so this can template documentation.

## Contributing to the current user documentation

```{warning}
These instructions are a little sparse at the moment and don't cover things like working on your own fork or branch of the documentation. We do recommend forking and working on your own change-specific branch.
```

First, install the most recent release version of the QIIME 2 Amplicon Distribution, or [create a QIIME 2 Amplicon Distribution development environment](setup-dev-environment). Switch to that new environment.

Then, clone the QIIME 2 User documentation repository and install its requirements.

```bash
git clone https://github.com/qiime2/docs.git
cd docs
pip install -r requirements.txt
```

Build the documentation in `preview` mode to confirm that the build works before making your changes.

```{note}
Building the documentation in `preview` mode will avoid running all of the QIIME 2 steps covered in the tutorials during the build of the documentation, which will be vastly faster than doing a complete build (i.e., `make html`) of the documentation.
```

```bash
make preview
```

Make your edits, and re-build and view them. Iterate on this process until you're done.

```bash
make preview
cd build/preview && python -m http.server ; cd -
```

The above command will launch a web server on your computer. Open http://localhost:8000/ in your browser to view the documentation as hosted on that local web server.

When you're ready, submit a pull request in the usual way.

