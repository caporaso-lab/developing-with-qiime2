(plugin-tutorial-intro)=
# Tutorial: A step-by-step guide to building your first QIIME 2 plugin

```{note}
My approach to writing *Developing with QIIME 2* is to publish early, and to publish often.
This is well captured in this quote by Daniele Procida from Diátaxis:

> It’s natural to want to complete large tranches of work before you publish them, so that you have something substantial to show each time. Avoid this temptation - every step in the right direction is worth publishing immediately. [(source)](https://diataxis.fr/foundations/)

One caveat that I'll add, since *Developing with QIIME 2* is about developing software while Diátaxis is about developing documentation, is that functional code should only be "published" (e.g., applied in real world applications or shared with others who may do that) **after** it has been sufficiently tested.
I'll come back to software testing shortly.

This tutorial is a work-in-progress. 🚜
```

This tutorial will walk step-by-step through building a first QIIME 2 plugin, and is intended to be read from beginning to end.

The plugin you'll create will provide support for some of the most fundamental algorithms in bioinformatics, and will ultimately contain a mix of QIIME 2 {term}`methods <Method>`, {term}`visualizers <Visualizer>`, and {term}`pipelines <Pipeline>`.
You'll learn to define {term}`formats <Format>`, {term}`transformers <Transformer>`, and new {term}`semantic types <Semantic Type>`.
You'll add parallel computing supporting to a {term}`method` that is initially implemented without parallel support.
You'll develop executable usage examples, so your users can learn how to apply your plugin, and you can receive automated notifications if changes you (or others) make to your code are backward incompatible, necessitating changes to the documentation.
And, as with all QIIME 2 plugins, the plugin you build will record data provenance when it's used, support {term}`provenance replay <Provenance Replay>`, and will be immediately accessible through multiple interfaces including {term}`q2cli` and the {term}`Python 3 API`.
You'll also be able to run a few additional commands to generate {term}`Galaxy` workflows for all of your plugin actions.
Finally, you'll receive guidance on how to move forward to create your own QIIME 2 plugin as a next step.

Let's [get started](plugin-from-template)!

```{note}
If you're already comfortable with plugin development and are looking for instructions to achieve a specific task, you may find more targeted instructions in the [Plugin Development How-To Guides](plugin-how-to-guides).
```

## Tutorial table of contents

```{tableofcontents}
```
