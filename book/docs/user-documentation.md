# User documentation

As of the time of this writing (22 May 2025) the QIIME 2 user documentation is in a state of transition.
Most new documentation is currently being built using [Jupyter Book 2](https://next.jupyterbook.org).

(users-docs-refactor)=
## User documentation refactor

We have recently (as of 22 May 2025) moved from a single source of documentation (previously at `https://docs.qiime2.org`) to resources for **cross-distribution QIIME 2 documentation**, **within-distribution QIIME 2 documentation**, **plugin-specific documentation**, and **data set specific usage documentation**.

The primary sources of **cross-distribution user documentation** are [*Using QIIME 2*](https://use.qiime2.org) and [*Developing with QIIME 2*](https://develop.qiime2.org).
These cover things (or will cover things) like:
- developing QIIME 2 plugins and interfaces
- [building and use an artifact cache](https://use.qiime2.org/en/latest/tutorials/use-the-artifact-cache.html)
- [parallel analysis support](https://use.qiime2.org/en/latest/references/parallel-configuration.html)
- provenance replay/viewing, which will expand on the [content here](https://forum.qiime2.org/t/provenance-replay-beta-release-and-tutorial/23279)
- using the interfaces
- [recycling results from failed runs](https://use.qiime2.org/en/latest/how-to-guides/pipeline-resumption.html)
- installing old versions of QIIME 2 (why, why not, and how)
- discussion of distributions (why are there multiple? how to deal with that)
- importing/exporting
- [viewing QIIME 2 `Visualizations`](https://use.qiime2.org/en/latest/how-to-guides/view-visualizations.html)

**Distribution specific documentation** will cover pre-built distributions of QIIME 2, including:
 - the [amplicon distribution documentation](https://amplicon-docs.qiime2.org)
 - [MOSHPIT documentation](https://moshpit.qiime2.org) (MOSHPIT was previously referred to as the *metagenome distribution*)

**Data-set specific tutorials**, like the [Moving Pictures tutorial](https://moving-pictures-tutorial.readthedocs.io/) or the more recent [gut-to-soil microbiome axis tutorial](https://gut-to-soil-tutorial.readthedocs.io/), will be dataset specific and may cross distributions (like the [Cancer Microbiome Intervention Tutorial](https://docs.qiime2.org/jupyterbooks/cancer-microbiome-intervention-tutorial/)).
This will facilitate the transition from replayed provenance to tutorial, ideally helping to blur the line between replayed provenance and a tutorial over time.
To support this, we will likely add a usage driver to Provenance Replay that generates usage driver source code (for example, select `View Source (qiime2.sdk)` from a multi-interface tutorial [like *gut-to-soil*](https://gut-to-soil-tutorial.readthedocs.io/), so Provenance Replay can template documentation.

**Plugin-specific documentation**, like the [q2-boots documentation](https://q2-boots.readthedocs.io/).

The use of Jupyter Book 2 allows us to re-use content as relevant across these resources.

If you'd like to contribute documentation, this should be done in the context of a specific documentation project.

