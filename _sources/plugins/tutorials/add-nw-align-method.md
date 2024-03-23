(add-nw-align-method)=
# Add a first (real) action to our plugin

At the most basic level, a QIIME 2 {term}`action` is simply an annotation of a Python function that describes in detail the inputs and outputs to that function.
Here we'll create a powerful action that illustrates this idea.

The type of action that we'll create is a {term}`method`, meaning that it will take zero or more QIIME 2 {term}`artifacts <Artifact>` as input, and it will generate one or more QIIME 2 artifacts as output.

(add-nw-align-method-prs)=
```{admonition} tl;dr
:class: tip
The complete code that I developed to add this action to my plugin can be found [here](https://github.com/caporaso-lab/q2-dwq2/pull/3/files) and [here](https://github.com/caporaso-lab/q2-dwq2/pull/4/files).

({term}`What does "tl;dr" mean? <tl;dr>`)
```

## Pairwise sequence alignment

One of the most fundamental tools in bioinformatics is {term}`pairwise sequence alignment`.
{term}`Pairwise sequence alignment` forms the basis of [BLAST](https://blast.ncbi.nlm.nih.gov/Blast.cgi), many genome assemblers, phylogenetic inference from molecular sequence data, assigning taxonomy to environmental DNA sequences, and so much more.
The first real action that we'll add to our plugin is a method that performs pairwise sequence alignment using the Needleman-Wunsch global pairwise alignment algorithm {cite}`Needleman1970`.

You don't need to understand how the NW algorithm works interally to implement our method, because we're going to work with a Python function that implements the algorithm for us.
But, you'll need to understand what its input and outputs are to be able to annotate them, and you'll need to understand at a basic level what it does so that you can test that your code is working as expected.

If you do want to learn more about pairwise sequence alignment, the specific algorithm and implementation that we're going to work with here is covered in detail in the *Pairwise Sequence Alignment* chapter of [*An Introduction to Applied Bioinformatics*](https://readiab.org) {cite}`iab-2`. Briefly:

> The goal of pairwise sequence alignment is, given two DNA, RNA, or protein sequences, to generate a hypothesis about which sequence positions derived from a common ancestral sequence position. {cite}`iab-2`

Our method will take two DNA sequences as input.
It will attempt to align like positions with each other, inserting gap (i.e., `-`) characters where it seems likely that insertion/deletion events have occurred over the course of evolution.
The output will be a pairwise sequence alignment (or more briefly, an *alignment*), which is a special case of a multiple sequence alignment that contains exactly two sequences.
Our method will also take a few {term}`parameters <Parameter>` as input.
These parameters include things like the score that should be assigned when a pair of positions contains matching characters (we'll call this `match_score`), or the score penalty that is incurred when a gap character is added to the alignment.

The [scikit-bio](https://scikit.bio) library implements Needleman-Wunsch global pairwise alignment algorithm as [`skbio.alignment.global_pairwise_align_nucleotide`](https://scikit.bio/docs/dev/generated/skbio.alignment.global_pairwise_align_nucleotide.html#skbio.alignment.global_pairwise_align_nucleotide).
We're going to make this accessible through our plugin by writing a simple wrapper of this function.

## Write a wrapper function

````{margin}
```{note}
In subsequent sections of the book, we'll apply test-driven development where we write unit tests for our functions before writing the functions themselves.
That may seem counter-intuitive if you've never done it before, but it's a powerful way to develop software as it focuses you on defining the specifications for your code before writing the code.
```
````

Technically we don't need to write a wrapper function of `skbio.alignment.global_pairwise_align_nucleotide`, but rather we could register that function directly.
But for our first pass at this action there are a couple of things we're going to need to do to get data from QIIME 2 into `skbio.alignment.global_pairwise_align_nucleotide`.
I started by creating a new file in my plugin at the path `q2-dwq2/q2_dwq2/_methods.py`.
The `_` at the beginning of `_methods.py` is convention that conveys that this is intended to be a private submodule: in other words, consummers of this code outside of the q2-dwq2 Python package shouldn't access anything in this file directly.

The complete code that I put in this file follows.
You should create a `_methods.py` file in your plugin, and copy/paste this code to it.

```python
# ----------------------------------------------------------------------------
# Copyright (c) 2024, Greg Caporaso.
#
# Distributed under the terms of the Modified BSD License.
#
# The full license is in the file LICENSE, distributed with this software.
# ----------------------------------------------------------------------------

from skbio.alignment import global_pairwise_align_nucleotide, TabularMSA

from q2_types.feature_data import DNAIterator


def nw_align(seq1: DNAIterator,
             seq2: DNAIterator,
             gap_open_penalty: float = 5,
             gap_extend_penalty: float = 2,
             match_score: float = 1,
             mismatch_score: float = -2) -> TabularMSA:
    seq1 = next(iter(seq1))
    seq2 = next(iter(seq2))

    msa, _, _ = global_pairwise_align_nucleotide(
        seq1=seq1, seq2=seq2, gap_open_penalty=gap_open_penalty,
        gap_extend_penalty=gap_extend_penalty, match_score=match_score,
        mismatch_score=mismatch_score
    )

    return msa
```

Here I defined a new function, `nw_align` (for *Needleman-Wunsch Alignment*).
At its core, what this function is doing is passing some inputs through to `skbio.alignment.global_pairwise_align_nucleotide`.
The aspects of this that might make this look different from what you typically see in a Python function definition are the [type hints](https://docs.python.org/3/library/typing.html), which are not used by Python directly, but are intended to be used by other tools (like QIIME 2).

The type hints define the [data type](types-of-types) associated with each input and output from our function, and are one of the ways that we annotate a function so that QIIME 2 knows how to interact with it.
Some of these are built-in types (in this case, we are providing four `float` values).
The others, `DNAIterator` and `TabularMSA`, are defined in the q2-types QIIME 2 plugin and in scikit-bio, respectively.
A `DNAIterator` is a Python object that enables iteration over a collection of zero or more `skbio.DNA` objects (which represent DNA sequences), and a `TabularMSA` object represents a **m**ultiple **s**equence **a**lignment.
A little bit later we'll come back to how you decide what type hints to provide here.

The first couple of lines in this function are a little bit odd, and stem from the fact that (as of this writing) there isn't an existing QIIME 2 {term}`semantic type` for individual DNA sequences, but rather only for collections of DNA sequences.
We are therefore going to work-around this right now, and in a subsequent lesson we'll define our own QIIME 2 semantic type to represent a single DNA sequence.
We need two sequences as input to pairwise sequence alignment (by definition), and we'll take those as inputs through the `seq1` and `seq2` parameters.
These will come in in `DNAIterator` objects, and our work-around is that we read the first sequence from each of these two input sequence collections by getting the `next()` item from each collection, one time each, and reassigning them to the variables `seq1` and `seq2`.

Next, we call `skbio.alignment.global_pairwise_align_nucleotide`, passing in all of our inputs.
`skbio.alignment.global_pairwise_align_nucleotide` returns three outputs.
For now, we're only going to concern ourselves with the first: the multiple sequence alignment, which we'll store in a varriable called `msa`.
By convention in Python, unused return values are assigned to a variable named `_`.
Finally, we'll return the `msa` variable.

So for the most part, this works like a normal Python function.
The unusual aspects are the type hints, and our workaround for getting the first sequence out of each of our input `DNAIterators`.

```{note}
Note that in defining this wrapper function, we haven't yet touched the concept of QIIME 2 {term}`Artifacts <Artifact>`.
The underlying functions that we register as methods or visualizers don't know anything about Artifacts.
You can also use this function just as you would any other Python function - as mentioned above, Python itself ignores the type hints, so you could just consider these detailed documentation of the input and output types of your function.
```

### Register the wrapper function as a plugin action

Now that we have a function, `nw_align`, that we want to register as an action in our plugin, let's do it.

#### Define a citation for this action

If the action that you're performing has a relevant citation, adding that during action registration will allow your users to discover what they should be citing when they use your action.
This is a good way, for example, to ensure that your users know that they should be citing your work (and not just citing QIIME 2).

To associate a citation with our new action, the first thing we'll do is add the bibtex-formatted citation to `q2-dwq2/q2_dwq2/citations.bib`.
Bibtex is a standard format recognizes by nearly all (or all) citation managers, including Paperpile and EndNote.
You can generally export a bibtex citation from those tools, or alternatively get one from [Google Scholar](https://scholar.google.com/).
The relevant citation for Needleman-Wunsch alignment is titled *A general method applicable to the search for similarities in the amino acid sequence of two proteins*, and was published in 1970.
Find this citation using your favorite tool.
If you use Google Scholar, search for the title of the article, and then identify it in the search results (it should be the first one).
As of this writing, you would next click "Cite" under the search result, and then click "Bibtex".
That should bring you to a page that contains the following bibtex-formatted citation:

```bibtex
@article{needleman1970general,
  title={A general method applicable to the search for similarities in the amino acid sequence of two proteins},
  author={Needleman, Saul B and Wunsch, Christian D},
  journal={Journal of molecular biology},
  volume={48},
  number={3},
  pages={443--453},
  year={1970},
  publisher={Elsevier}
}
```

I copied this and then pasted it at the bottom of the `q2-dwq2/q2_dwq2/citations.bib` file.
I also changed the citation key on the first line of this bibtext record (`needleman1970general`) to `Needleman1970`.
This is how we'll reference this citation when we associate it with our action, and my version of the key is just a little easier for me to remember.

#### Register the action in `plugin_setup.py`

Now we have what we need to register our function as a plugin method.
By convention, this is done in `q2-dwq2/q2_dwq2/plugin_setup.py`, and that's what we'll do here.
I chose to remove the templated `duplicate_table` action, now that I'm adding one of my own, but whether or not you want to do that too is up to you.

To register a function as a method, you'll use `plugin.methods.register_function`, where `plugin` is the `qiime2.plugin.Plugin` action that is instantiated in this file.
Add the following code to your `q2-dwq2/q2_dwq2/plugin_setup.py` file, and then we'll work through it line by line.
Note that this won't work yet - we still need to add some `import` statements to the top of the file, but we'll add those as we work through the code where the imported functionality is used.

```python
plugin.methods.register_function(
    function=nw_align,
    inputs={'seq1': FeatureData[Sequence],
            'seq2': FeatureData[Sequence]},
    parameters={
        'gap_open_penalty': Float % Range(0, None, inclusive_start=False),
        'gap_extend_penalty': Float % Range(0, None, inclusive_start=False),
        'match_score': Float % Range(0, None, inclusive_start=False),
        'mismatch_score': Float % Range(None, 0, inclusive_end=True)},
    outputs={'aligned_sequences': FeatureData[AlignedSequence]},
    input_descriptions={'seq1': 'The first sequence to align.',
                        'seq2': 'The second sequence to align.'},
    parameter_descriptions={
        'gap_open_penalty': ('The penalty incurred for opening a new gap. By '
                             'convention this is a positive number.'),
        'gap_extend_penalty': ('The penalty incurred for extending an existing '
                               'gap. By convention this is a positive number.'),
        'match_score': ('The score for matching characters at an alignment '
                        'position. By convention, this is a positive number.'),
        'mismatch_score': ('The score for mismatching characters at an '
                           'alignment position. By convention, this is a '
                           'negative number.')},
    output_descriptions={
        'aligned_sequences': 'The pairwise aligned sequences.'
    },
    name='Pairwise global sequence alignment.',
    description=("Align two DNA sequences using Needleman-Wunsch (NW). "
                 "This is a Python implementation of NW, so it is very slow! "
                 "This action is for demonstration purposes only. 🐌"),
    citations=[citations['Needleman1970']]
)
```

First, we call `plugin.methods.register_function`.
This function call takes a number of parameters, and you can find full detail by following the `[source]` link from the [`Plugin` API documentation](Plugin-api-docs).
Here's what each is:
 - `function`: This is the Python function to be registered as a plugin action.
   We defined ours above as `nw_align`.
   If you add the import statement `from q2_dwq2._methods import nw_align` to the top of this file, you can provide `nw_align`.
 - `inputs`: This is a Python `dict` mapping the variable names of the {term}`inputs <Input>` to the plugin action to the semantic types of the inputs.
   As mentioned above, QIIME 2 doesn't define a semantic type for a single DNA sequence, so we're going to use the type that is commonly used for defining collections of DNA sequences, and we'll just end up working with the first sequence in each input.
   The type we use here is `FeatureData[Sequence]`.
   A little bit later we'll come back to how you identify the semantic types that should be assigned to your input, and how to define your own sematic types if there isn't already a relevant one.
   {term}`Inputs <Input>` to QIIME 2 actions are data in the form of {term}`Artifacts <Artifact>`, and these are different than {term}`Parameters <Parameter>`.
   It is at this stage, when registering a function as an action, that this distinction is made.
   The semantic types we're using here need to be imported from q2-types.
   To do this, add the line `from q2_types.feature_data import FeatureData, Sequence` to the top of the file.
- `parameters`: This is a Python `dict` mapping the names of parameters to their {term}`Primitive Type`.
  This information is used to validate input provided by users of your plugin, but more importantly to allow QIIME 2 interfaces to determine how this information should be collected from a user.
  For example, in a graphical interface the value of a `Boolean` parameter could be collected from a user using a checkbox, while a `Float` parameter could be collected using a text field that only accepts numbers.
  Our four parameters are all `Floats`, and each has a `Range` that values must fall in.
  Import these primitive types for use here by adding the line `from qiime2.plugin import Float, Range` to the top of the file.
  The `gap_open_penalty` parameter, for example, is defined here as taking a floating point value greater than 0.
 - `outputs`: This is a Python `dict` mapping the variable names of the {term}`outputs <Output>` from the plugin action to their semantic types.
 The type we use here is `FeatureData[AlignedSequence]`, representing a collection of aligned DNA sequences.
 A more appropriate type might represent a pair of aligned sequences specifically, rather than one or more aligned sequences which is what this semantic type implies, but again we'll come back to that a later.
 We'll need to import `AlignedSequence` here as well, which you can do by adding the line `from q2_types.feature_data import AlignedSequence` to the top of the file (or adding `AlignedSequence` to the imports you already added from `q2_types.feature_data`).
 - `input_descriptions`, `parameter_descriptions`, and `output_descriptions`: These are Python `dicts` that provide descriptions of each input, parameter, and output, respectively, for use in help text through different interfaces.
 - `name`: A brief name for this action.
 This shows up, for example, when listing the actions that are available in a plugin.
 - `description`: A longer description of the action.
 This is generally presented to a user when they request more detail on an action (for example, by passing a `--help` parameter through a command line interface).
 - `citations`: A list of the citations that should be associated with this action.
 Earlier in the `plugin_setup.py` file we instantiated a `citations` lookup, and we can now use that to associate the citation we added to `citations.bib` with this action.

After adding this code and the corresponding `import` statements to your `plugin_setup.py`, you should be ready to try this action out.

My `import` statements now look like the following:

```python
from qiime2.plugin import Citations, Plugin, Float, Range
from q2_types.feature_data import FeatureData, Sequence, AlignedSequence
from q2_dwq2 import __version__
from q2_dwq2._methods import nw_align
```

### Calling the action with {term}`q2cli` and the {term}`Python 3 API`

Activate your development environment and run `qiime dev refresh-cache`.
If your code doesn't have any syntax errors, and you addressed all of the additions described in this document, you should then be able to run `qiime dwq2 --help`, and see your new `nw-align` action show up in the list of actions associated with your plugin.
It should look something like this:

````{margin}
```{note}
When I present command line calls and their output, I'll use `$` to indicate the command prompt.
```
````

```shell
$ qiime dwq2 --help
Usage: qiime dwq2 [OPTIONS] COMMAND [ARGS]...

  Description: A prototype of a demonstration plugin for use by readers of
  *Developing with QIIME 2* (DWQ2).

  Plugin website: https://cap-lab.bio/developing-with-qiime2/

  Getting user support: Please post to the QIIME 2 forum for help with this
  plugin: https://forum.qiime2.org

Options:
  --version            Show the version and exit.
  --example-data PATH  Write example data and exit.
  --citations          Show citations and exit.
  --help               Show this message and exit.

Commands:
  nw-align  Pairwise global sequence alignment.
```

If you call `qiime dwq2 nw-align --help`, you'll see the more detailed help text for the `nw-align` action.
It should look something like this:

```shell
$ qiime dwq2 nw-align --help
Usage: qiime dwq2 nw-align [OPTIONS]

  Align two DNA sequences using Needleman-Wunsch (NW). This is a Python
  implementation of NW, so it is very slow! This action is for demonstration
  purposes only. 🐌

Inputs:
  --i-seq1 ARTIFACT FeatureData[Sequence]
                          The first sequence to align.              [required]
  --i-seq2 ARTIFACT FeatureData[Sequence]
                          The second sequence to align.             [required]
Parameters:
  --p-gap-open-penalty NUMBER Range(0, None, inclusive_start=False)
                          The penalty incurred for opening a new gap. By
                          convention this is a positive number.   [default: 5]
  --p-gap-extend-penalty NUMBER Range(0, None, inclusive_start=False)
                          The penalty incurred for extending an existing gap.
                          By convention this is a positive number.
                                                                  [default: 2]
  --p-match-score NUMBER Range(0, None, inclusive_start=False)
                          The score for matching characters at an alignment
                          position. By convention, this is a positive number.
                                                                  [default: 1]
  --p-mismatch-score NUMBER Range(None, 0, inclusive_end=True)
                          The score for mismatching characters at an
                          alignment position. By convention, this is a
                          negative number.                       [default: -2]
Outputs:
  --o-aligned-sequences ARTIFACT FeatureData[AlignedSequence]
                          The pairwise aligned sequences.           [required]
Miscellaneous:
  --output-dir PATH       Output unspecified results to a directory
  --verbose / --quiet     Display verbose output to stdout and/or stderr
                          during execution of this action. Or silence output
                          if execution is successful (silence is golden).
  --example-data PATH     Write example data and exit.
  --citations             Show citations and exit.
  --help                  Show this message and exit.
```

Similarly, if you start a Python session (e.g., by calling `ipython` in your activated development environment), you can access the `nw_align` method through its Python 3 API as follows.

```python
import qiime2.plugins.dwq2
help(qiime2.plugins.dwq2.actions.nw_align)
```

This call should produce the following help text:

```
Call signature:
qiime2.plugins.dwq2.actions.nw_align(
    seq1: FeatureData[Sequence],
    seq2: FeatureData[Sequence],
    gap_open_penalty: Float % Range(0, None, inclusive_start=False) = 5,
    gap_extend_penalty: Float % Range(0, None, inclusive_start=False) = 2,
    match_score: Float % Range(0, None, inclusive_start=False) = 1,
    mismatch_score: Float % Range(None, 0, inclusive_end=True) = -2,
) -> (FeatureData[AlignedSequence],)
Type:           Method
String form:    <method qiime2.plugins.dwq2.methods.nw_align>
File:           ~/miniconda3/envs/dwq2/lib/python3.8/site-packages/qiime2/sdk/action.py
Docstring:      QIIME 2 Method
Call docstring:
Pairwise global sequence alignment.

Align two DNA sequences using Needleman-Wunsch (NW). This is a Python
implementation of NW, so it is very slow! This action is for demonstration
purposes only. 🐌

Parameters
----------
seq1 : FeatureData[Sequence]
    The first sequence to align.
seq2 : FeatureData[Sequence]
    The second sequence to align.
gap_open_penalty : Float % Range(0, None, inclusive_start=False), optional
    The penalty incurred for opening a new gap. By convention this is a
    positive number.
gap_extend_penalty : Float % Range(0, None, inclusive_start=False), optional
    The penalty incurred for extending an existing gap. By convention this
    is a positive number.
match_score : Float % Range(0, None, inclusive_start=False), optional
    The score for matching characters at an alignment position. By
    convention, this is a positive number.
mismatch_score : Float % Range(None, 0, inclusive_end=True), optional
    The score for mismatching characters at an alignment position. By
    convention, this is a negative number.

Returns
-------
aligned_sequences : FeatureData[AlignedSequence]
    The pairwise aligned sequences.
```

There are now two interfaces to your method, and you didn't have to write either of them --- cool! 😎

Take a minute to review both the command line and Python help text, and relate it to the parameters we set when we registered the action.

### Write unit tests

Your code is *not ready for use* until you write unit tests, to ensure that it's doing what you expect.
We'll write our unit tests for `nw_align` in a new file in our Python package, `q2_dwq2/tests/test_methods.py`.
QIIME 2 provides a class, `TestPluginBase`, that facilitates unit testing plugins.

```{warning}
*Developing with QIIME 2* assumes that you have some background in software engineering.
If writing unit tests or software testing in general are new to you, you should learn about these topics before developing software that you intend to use for "real" analysis.
Small errors in code can have huge implications, including angry users, paper retractions, and clinical errors.

I highly recommend reading [*The Pragmatic Programmer: Your Journey to Mastery* (20th Anniversary Edition)](https://pragprog.com/titles/tpp20/the-pragmatic-programmer-20th-anniversary-edition/).
Topic 41 discusses software testing, but the whole book is worth reading if you're serious about developing high-quality software.
```

#### What to test and what not to test

When testing a QIIME 2 plugin, your goal is to confirm that the functionality that you developed works as expected.
You can't test that *every* possible input produces its expected output, so instead you want to think about what tests will convince you that it's working across the range of inputs that would be expected.
It's also a good idea to test that invalid input results in a failure, and ideally also provides an informative error message.

If you're simply wrapping a function, like we are here, you don't need to test the underlying function in detail as that should have been tested already in the library that provides that function.
(If that's not the case, you should reconsider whether this function is the one that you want to use!)

You also don't need to test things such as whether your method works through q2cli, the Python 3 API, and Galaxy.
That is functionality that you get for free when developing QIIME 2 plugins: the developers of the QIIME 2 framework and the other related tools have already tested this, and this should work as long as you're not adopting any of the [plugin development antipatterns](plugin-antipatterns).

#### A first test of our plugin action

The following is a first test of our `nw_align` method.

````{margin}
```{note}
There are a couple of extra `import`s in here right now.
We'll use those shortly.
```
````

```python
from skbio.alignment import TabularMSA
from skbio.sequence import DNA

from qiime2.plugin.testing import TestPluginBase
from qiime2.plugin.util import transform
from q2_types.feature_data import DNAFASTAFormat, DNAIterator

from q2_dwq2._methods import nw_align


class NWAlignTests(TestPluginBase):
    package = 'q2_dwq2.tests'

    def test_simple1(self):
        # test alignment of a pair of sequences
        sequence1 = DNA('AAAAAAAAGGTGGCCTTTTTTTT')
        sequence1 = DNAIterator([sequence1])
        sequence2 = DNA('AAAAAAAAGGGGCCTTTTTTTT')
        sequence2 = DNAIterator([sequence2])
        observed = nw_align(sequence1, sequence2)

        aligned_sequence1 = DNA('AAAAAAAAGGTGGCCTTTTTTTT')
        aligned_sequence2 = DNA('AAAAAAAAGG-GGCCTTTTTTTT')
        expected = TabularMSA([aligned_sequence1, aligned_sequence2])

        self.assertEqual(observed, expected)
```

First, we import some functions and classes that we'll use in our tests.
Then, we define a class, `NWAlignTests`, that inherits from `TestPluginBase`, a class used to facilitate testing of QIIME 2 plugins.
`TestPluginBase` has you define a class variable, `package`, defining the submodule that we're working in - we'll come back to how this is used shortly.
Finally, we're ready to start defining unit tests.

The first test that I typically define for a function is a test of its default behavior on some very simple input where it's easy for me to determine what the expected outcome should be.
In the example here, I'm creating two `skbio.DNA` sequence objects, turning them into `DNAIterators` (remember that that is what `nw_align` expects as input), and then calling `nw_align` on those two inputs.
I call the return value from `nw_align` `observed`, because it is my observed output.

I very specifically chose the sequences here because I could tell based on my knowledge of Needleman-Wunsch alignment what the output would be: it's clear that the two sequences differ only in that there appears to have either been an insertion of a `T` character in `sequence1`, or a deletion of a `T` character in `sequence2` since the ancestral sequence.
Alternatively, in a case like this, it's also fair game to generate the expected output by calling the underlying function (`skbio.alignment.global_pairwise_align_nucleotide`) directly.
This is because we're not testing that `skbio.alignment.global_pairwise_align_nucleotide` does what it's supposed (again, we trust that it is, or we wouldn't be using it).
We're only testing that our wrapper generates the output that we would expect from `skbio.alignment.global_pairwise_align_nucleotide`.

After getting my `observed` output, I define my `expected` output (i.e., what `nw_align` should return if it's working as expected).
In this case, that's a pairwise alignment of `sequence1` and `sequence2` with a `-` character added where the insertion/deletion event is hypothesized to have occurred.

Finally, we compare our `observed` output to our `expected` output.

An important thing to note here is that I didn't need to load any data from file or use any QIIME 2 artifacts when testing my method.
Because my method is just a Python function that I registered with my `Plugin`, I can provide input objects as I would to any other Python function.
It is possible to store QIIME 2 Artifacts in the repository and load them for use in the tests, but that gets a little clunky so it's best avoided when possible.
For example, you'll often want to test multiple minor variations on the input to test edge cases (i.e., boundary conditions).
That's much easier to do if you're working with Python objects as input, rather than if you need to create a whole bunch of different QIIME 2 artifacts and store them in the repository.
Storing artifacts in the repository to use as inputs in unit tests can also increase the repository size, and it's not straight-forward to compare how inputs have changed across different revisions of the code.

We can now run the test using `py.test` on the command line from your `q2-dwq2` directory.
This should look something like the following:

```shell
$ py.test

...
q2_dwq2/tests/test_methods.py::NWAlignTests::test_simple1

...

==== 1 passed, 5 warnings in 0.17s ====
```

At the moment we're not concerned about the warnings that are being reported.
We see from this output that we defined one test, and that one test passed.
So we're ready to move on.

#### A second test of our action

All of that said, sometimes you do want to store data that you use in tests in files in the repository (for example, if they are large - in which case it's a pain to store the test data in your unit test Python files).
The following unit test illustrates how this can be achieved.

```python
    def test_simple2(self):
        # test alignment of a different pair of sequences
        # loaded from file this time, for demonstration purposes
        sequence1 = transform(
            self.get_data_path('nw_align/seq-1.fasta'),
            from_type=DNAFASTAFormat,
            to_type=DNAIterator)
        sequence2 = transform(
            self.get_data_path('nw_align/seq-2.fasta'),
            from_type=DNAFASTAFormat,
            to_type=DNAIterator)
        observed = nw_align(sequence1, sequence2)

        aligned_sequence1 = DNA('ACCGGTGGAACCGG-TAACACCCAC')
        aligned_sequence2 = DNA('ACCGGT--AACCGGTTAACACCCAC')
        expected = TabularMSA([aligned_sequence1, aligned_sequence2])

        self.assertNotEqual(observed, expected)
```

In this example, data is loaded from a file path that is relative to the `TestPluginBase.package` variable that we set above.
In this case, the data needs to be transformed from a fasta file, which QIIME 2 represents as an instance of `q2-type`'s `DNAFASTAFormat` object to a `DNAIterator`, so it can be provided as input to `nw_align`.
Here we use the `qiime2.plugin.util.transform` method to perform the transformation.
After loading the files and transforming them, the test looks identical to the previous test case that we defined, except that the `expected` output is different, because the sequences we loaded differ from those used in the `test_simple1` method.

A couple of additional things are required for this test to pass in your development environment.
First, you must actually have the two `.fasta` files that are being loaded in the submodule as specified here (i.e., you should have the files `q2-dwq2/q2_dwq2/tests/data/seq-1.fasta` and `q2-dwq2/q2_dwq2/tests/data/seq-1.fasta` in your Python package).
Second, you should indicate that there is `package_data` in your `setup.py`.
Refer back to [the pull requests referenced at the top of this chapter](add-nw-align-method-prs) to see where all of this is done.

After defining this test in your plugin, run the unit tests and confirm that you now have two passing tests.

#### A few additional tests

Because we want to test that our function generates the results that we would expect from `skbio.alignment.global_pairwise_align_nucleotide`, it's good to check that the parameter values that we provide impact the results in the expected ways.
I did this with four additional unit tests, each focused on a different input parameter.

```python
    def test_alt_match_score(self):
        s1 = DNA('AAAATTT')
        sequence1 = DNAIterator([s1])
        s2 = DNA('AAAAGGTTT')
        sequence2 = DNAIterator([s2])
        # call with default value for match score
        observed = nw_align(sequence1, sequence2)

        aligned_sequence1 = DNA('--AAAATTT')
        aligned_sequence2 = DNA('AAAAGGTTT')
        expected = TabularMSA([aligned_sequence1, aligned_sequence2])

        self.assertEqual(observed, expected)

        sequence1 = DNAIterator([s1])
        sequence2 = DNAIterator([s2])
        # call with non-default value for match_score
        observed = nw_align(sequence1, sequence2, match_score=10)

        # the following expected outcome was determined by calling
        # skbio.alignment.global_pairwise_align_nucleotide directly. the
        # goal isn't to test that the underlying library code (i.e.,
        # skbio.alignment.global_pairwise_align_nucleotide) is working, b/c
        # I trust that that is already tested (or I wouldn't use it). rather,
        # the goal is to test that my wrapper of it is working. in this case,
        # specifically, i'm testing that passing an alternative value for
        # match_score changes the output alignment
        aligned_sequence1 = DNA('AAAA--TTT')
        aligned_sequence2 = DNA('AAAAGGTTT')
        expected = TabularMSA([aligned_sequence1, aligned_sequence2])

        self.assertEqual(observed, expected)

    def test_alt_gap_open_penalty(self):
        s1 = DNA('AAAATTT')
        sequence1 = DNAIterator([s1])
        s2 = DNA('AAAAGGTTT')
        sequence2 = DNAIterator([s2])
        observed = nw_align(sequence1, sequence2, gap_open_penalty=0.01)

        aligned_sequence1 = DNA('AAAA-T-TT-')
        aligned_sequence2 = DNA('AAAAG-GTTT')
        expected = TabularMSA([aligned_sequence1, aligned_sequence2])

        self.assertEqual(observed, expected)

        sequence1 = DNAIterator([s1])
        sequence2 = DNAIterator([s2])
        observed = nw_align(sequence1, sequence2)

        aligned_sequence1 = DNA('--AAAATTT')
        aligned_sequence2 = DNA('AAAAGGTTT')
        expected = TabularMSA([aligned_sequence1, aligned_sequence2])

        self.assertEqual(observed, expected)

    def test_alt_gap_extend_penalty(self):
        s1 = DNA('AAAATTT')
        sequence1 = DNAIterator([s1])
        s2 = DNA('AAAAGGTTT')
        sequence2 = DNAIterator([s2])
        observed = nw_align(sequence1, sequence2, gap_open_penalty=0.01)

        aligned_sequence1 = DNA('AAAA-T-TT-')
        aligned_sequence2 = DNA('AAAAG-GTTT')
        expected = TabularMSA([aligned_sequence1, aligned_sequence2])

        self.assertEqual(observed, expected)

        sequence1 = DNAIterator([s1])
        sequence2 = DNAIterator([s2])
        observed = nw_align(sequence1, sequence2, gap_open_penalty=0.01,
                            gap_extend_penalty=0.001)

        aligned_sequence1 = DNA('AAAA--TTT')
        aligned_sequence2 = DNA('AAAAGGTTT')
        expected = TabularMSA([aligned_sequence1, aligned_sequence2])

        self.assertEqual(observed, expected)

    def test_alt_mismatch_score(self):
        s1 = DNA('AAAATTT')
        sequence1 = DNAIterator([s1])
        s2 = DNA('AAAAGGTTT')
        sequence2 = DNAIterator([s2])
        observed = nw_align(sequence1, sequence2, gap_open_penalty=0.01)

        aligned_sequence1 = DNA('AAAA-T-TT-')
        aligned_sequence2 = DNA('AAAAG-GTTT')
        expected = TabularMSA([aligned_sequence1, aligned_sequence2])

        self.assertEqual(observed, expected)

        sequence1 = DNAIterator([s1])
        sequence2 = DNAIterator([s2])
        observed = nw_align(sequence1, sequence2, gap_open_penalty=0.1,
                            mismatch_score=-0.1)

        aligned_sequence1 = DNA('-AAA-ATTT')
        aligned_sequence2 = DNA('AAAAGGTTT')
        expected = TabularMSA([aligned_sequence1, aligned_sequence2])

        self.assertEqual(observed, expected)
```

#### Wrapping up testing

When these tests are all in place (or in the process of putting them in place), you can run them by calling `py.test` on the command line.
If everything is working as expected, you should see something like the following:

```shell
$ py.test

...

q2_dwq2/tests/test_methods.py::NWAlignTests::test_alt_gap_extend_penalty
q2_dwq2/tests/test_methods.py::NWAlignTests::test_alt_gap_open_penalty
q2_dwq2/tests/test_methods.py::NWAlignTests::test_alt_match_score
q2_dwq2/tests/test_methods.py::NWAlignTests::test_alt_mismatch_score
q2_dwq2/tests/test_methods.py::NWAlignTests::test_simple1
q2_dwq2/tests/test_methods.py::NWAlignTests::test_simple2

...

==== 6 passed, 23 warnings in 1.17s ====
```

If your tests pass, and you can see the action on the command line, you should be in good shape so let's try running the method.

## Trying the new action

To run the new action, you'll need two input files, each containing a DNA sequence to align.
At this stage, your inputs need to be QIIME 2 artifacts.
You should be able to do this with any `FeatureData[Sequence]` artifacts you have access to.
If you don't have any, you can use the ones that we used in `test_simple2` by importing.

To do this, change to a temporary directory and copy the two files referenced in `test_simple2` to that directory.
You should then be able to run the following commands to import those files:

```bash
qiime tools import --input-path seq-1.fasta --type "FeatureData[Sequence]" --output-path seq-1.qza
qiime tools import --input-path seq-2.fasta --type "FeatureData[Sequence]" --output-path seq-2.qza
```

Then, you can apply your new action to these two inputs as follows:

```bash
qiime dwq2 nw-align --i-seq1 seq-1.qza --i-seq2 seq-2.qza --o-aligned-sequences aligned-seqs.qza
```

This should create a new output, `aligned-seqs.qza`.
Since this is a method, it's generating a new artifact as an output.
As always, artifacts aren't intended for human consumption, but rather to be used as input to other QIIME 2 actions or exported for use with other (non-QIIME 2) tools.
If you want to take a peek at what's in there, you can export it:

```bash
qiime tools export --input-path aligned-seqs.qza --output-path aligned-seqs
```

Then, you can view the file contents as you would with any .fasta file.
For example:

```bash
$ cat aligned-seqs/aligned-dna-sequences.fasta
>example-sequence-1
ACCGGTGGAACCGG-TAACACCCAC
>example-sequence-2
ACCGGT--AACCGGTTAACACCCAC
```

So there you have it - a first action in our QIIME 2 plugin. ✅

As a next step, let's make this a little more user-friendly by defining a {term}`Visualizer` that will let us look at the outcome of our pairwise alignment without having to export it from QIIME 2.

## An optional exercise

Now that you have this method working, try adding a method for local pairwise alignment of nucleotide sequences using the Smith-Waterman (SW) algorithm.
scikit-bio provides an implementation of SW as [`skbio.alignment.local_pairwise_align_nucleotide`](https://scikit.bio/docs/dev/generated/skbio.alignment.local_pairwise_align_nucleotide.html).
Don't forget to write your unit tests!

Throughout the next few chapters, additional exercises will build on this functionality.


