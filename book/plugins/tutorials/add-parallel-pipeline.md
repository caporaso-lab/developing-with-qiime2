# Add a Pipeline with parallel computing support

In this chapter we'll add a second {term}`Pipeline` to our plugin, and then we'll add parallel computing support to that `Pipeline`.
This will enable your users to utilize multi-processor computers or multi-node high performance computing infrastructure (e.g., computer clusters) to analyze their data.

(add-parallel-pipeline-commits)=
```{admonition} tl;dr
:class: tip

The complete code that I wrote to add the second `Pipeline` to my plugin can be found here: {{ dwq2_add_parallel_pipeline_commit_1_url }}. The code that I developed to add parallel computing support to the new `Pipeline` can be found here: {{ dwq2_add_parallel_pipeline_commit_2_url }}.
```

## Add a local alignment search `Pipeline`

The first goal of this section is to define a new `Pipeline` that performs a local alignment search and then tabulates those results for the user to view.
This is effectively the same goal as the ubiquitous bioinformatics tool, BLAST {cite}`Altschul1990`.
The underlying theory, and the implementation that we'll used here, are presented in the *Sequence Homology Searching* chapter of [An Introduction to Applied Bioinformatics](https://readIAB.org) {cite}`iab-2`.

Briefly, given one or more *query sequences* and one or more *reference sequences*, a local alignment search uses pairwise sequence alignment to identify the most similar reference sequence for each query sequence.
In our implementation, as in the BLAST implementation, we'll allow a query sequence to match a subsequence of a reference sequence (this is useful, for example, if the query sequence represents a fragment of gene, and the reference sequences represent full-length genes).
To achieve this, the underlying alignment algorithm that we'll use is Smith-Waterman local pairwise alignment {cite}`Smith1981`, which is presented in the *Pairwise Sequence Alignment* chapter of [An Introduction to Applied Bioinformatics](https://readIAB.org).

The output for a typical local alignment search is a table of the results.
Depending on what the user requests, this can describe simply the best match in the database for each query (often defined as the reference sequence which obtains the highest scoring pairwise alignment with the query sequence), or a reverse sorted list of the matches, such that for each query sequence the `n` best matches are presented in order from best to worst.
Depending on the implementation, some additional information may be provided about each alignment including the percent similarity between the aligned query and reference sequence, the length of the alignment, and the score of the alignment.

To add a local alignment search `Pipeline` to our plugin, we're going to add one new `Method` and one new `Visualizer`.
The method will be called `local_alignment_search`, and it will take one or more query sequences and one or more reference sequences as inputs, and it will accept several parameters used to control the behavior of the alignment algorithm and the result tabulation.
As an output, it will generate a tabulation of the search results, grouped by query id and sorted in descending order of alignment score.
This table will be an Artifact of a new type, `LocalAlignmentSearchResults`, such that these results could be used by another action (e.g., one that associates metadata with the query sequences, such as taxonomic origin or gene function, based on metadata associated with their best matching reference sequences).

The new visualizer, `tabulate_las_results` (where `las` is an abbreviation of *local alignment search*) will take a `LocalAlignmentSearchResults` artifact as input and will produce a user-friendly view of it.
And finally the new pipeline, `search_and_summarize`, will link `local_alignment_search` and `tabulate_las_results` together, returning both the `LocalAlignmentSearchResults` data artifact and the human-readable visualization.

We'll also create a new format, some new transformers, and a new artifact class in support of the new functionality.

Since you've already done all of this type of work before for other functionality in your plugin, we won't go through this in detail.
Use this as an opportunity to review and understand QIIME 2 plugin code.
Review the code added in {{ dwq2_add_parallel_pipeline_commit_1_url }} and add it to your plugin.

## Add parallel computing support to `search_and_summarize`

...