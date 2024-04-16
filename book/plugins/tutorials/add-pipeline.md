# Add a first Pipeline

In this chapter we'll add our first {term}`Pipeline` to our plugin.
Pipelines allow developers to define workflows composed of Methods and Visualizers, defined in the same plugin or others, that can be run as a single step.
Like {term}`Methods <Method>` and {term}`Visualizers <Visualizer>`, Pipelines take zero or more {term}`Artifacts <Artifact>` as input.
However unlike Methods, which exclusively produce one or more Artifacts as output, or Visualizers, which exclusively produce one or more {term}`Visualizations <Visualization>` as output, Pipelines create one or more Artifacts *and* one or more Visualizations as output.
Pipelines are also where QIIME 2's formal support for parallel computing comes into play, so are important for supporting workflows that are computationally expensive.

In this chapter, we'll develop our first simple Pipeline which will chain the `nw-align` and `summarize-alignment` {term}`Actions <Action>` that we previously wrote together in a new action that produces the alignment and the alignment summary from one command call.
This will illustrate how to use Pipelines to simplify common workflows for your users.
In subsequent chapters, we'll explore developing Pipelines that provide parallel computing support across diverse high-performance computing resource configurations.

**This chapter is currently incomplete.**
**The code that we'll develop is available [here](https://github.com/caporaso-lab/q2-dwq2/pull/11/files), while the text is in development.**
**Some earlier text on this topic can be found in the *How-to* guide, [](howto-create-register-pipeline).**
