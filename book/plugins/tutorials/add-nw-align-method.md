(add-nw-align-method)=
# Add a first (real) action to our plugin

At the most basic level, a QIIME 2 action is simply an annotation of a Python function that provides additional detail on the inputs and outputs.
As a next step, we'll create a powerful action that demonstrates this idea.

## Pairwise sequence alignment

One of the most fundamental tools in bioinformatics is pairwise sequence alignment.
Pairwise sequence alignment forms the basis of [BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi), many genome assemblers, phylogenetic inference from molecular sequence data, assigning taxonomy to environmental DNA sequences, and so much more.
The action we'll add to our plugin in this chapter performs pairwise sequence alignment using the Needleman-Wunsch global pairwise alignment algorithm {cite}`Needleman1970`.
You don't need to understand how the algorithm works to implement this action, but if you do want to learn more this topic, including the specific algorithm and code that we're going to reference here, is covered in detail in [*An Introduction to Applied Bioinformatics*](https://readiab.org) {cite}`iab-2`.

The complete code that I developed to add this action to my plugin can be found [here](https://github.com/caporaso-lab/q2-dwq2/pull/3/files).

