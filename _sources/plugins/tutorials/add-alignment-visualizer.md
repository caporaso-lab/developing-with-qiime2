# Add a first visualizer to the plugin

In the last chapter we created a first method for our plugin which performed pairwise alignment of DNA sequences.
We were able to run this to generate an alignment, but we didn't have any way to visualize the result without exporting it from QIIME 2.
In this lesson we'll address that by adding a {term}`Visualizer` to our plugin which takes a `TabularMSA` artifact as input (which is what our previous action generated as output), and generates a `Visualization` that we can review using [QIIME 2 View](https://view.qiime2.org).

**This section is incomplete.**