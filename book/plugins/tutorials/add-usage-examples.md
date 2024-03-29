(add-nw-align-usage)=
# Add usage examples to the plugin

Your new functionality isn't *really* done until you document it, so let's do that now.
This will ensure that users know how to use your code, and will give them something to try after they install your plugin to convince them that it's working.
I generally find that I'm the first person to benefit from my documentation, and in some cases I'm also the person who most frequently benefits from my documentation (e.g., if it's code that I write for my own purposes, rather than something I intend to broadly disseminate).

QIIME 2 provides a framework for defining `UsageExamples` for plugins.
These are defined abstractly, and the QIIME 2 framework knows how to translate those abstract definitions into usage examples for different interfaces (the {term}`Python 3 API`, {term}`q2cli`, and {term}`Galaxy`, as of this writing).
So, by writing a single usage example, your documentatation is targeted toward users with different levels of computational expertise.
This is one way the framework supports our goal of meeting users where they are in terms of their computational experience, and it's one of the big benefits that you as a plugin developer gets by developing with QIIME 2.

**This section is incomplete.**