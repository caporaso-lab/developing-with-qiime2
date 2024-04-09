(add-nw-align-usage)=
# Add usage examples

If you want others to use your new functionality, it isn't *really* done until you document how to use it.
Let's do that now.
This will ensure that users know how to use your code, and will give them something to try after they install your plugin to convince them that it's working.
I generally find that I'm the first person to benefit from my documentation, and in some cases I'm also the person who most frequently benefits from my documentation (e.g., if it's code that I write for my own purposes, rather than something I intend to broadly disseminate).

QIIME 2 provides a framework for defining *usage examples* for plugins.
Usage examples are defined abstractly, rather than based on a specific QIIME 2 interface, and QIIME 2 interfaces can define *usage drivers* that know how to translate those abstract definitions into instructions for their application through a specific interface.
For example, the framework contains a usage driver for the {term}`Python 3 API`, and therefore can turn abstract usage examples into a series of Python 3 commands.
{term}`q2cli` contains a usage driver that translates abstract usage examples into a series of shell commands.
And [q2galaxy](https://github.com/qiime2/q2galaxy) contains a usage driver that turns examples into text-based instructions for running them through {term}`Galaxy`.
So, by writing a single usage example, your documentatation is targeted toward users with different levels of computational expertise, and as new interfaces become available you don't need to update your usage examples for users to be able to work with your examples through them.
This is one way the framework supports our goal of meeting users where they are in terms of their computational experience, and it's one of the big benefits that you as a plugin developer gets by developing with QIIME 2.

In this section of the tutorial, we'll define a usage example for our `nw-align` action.

(add-usage-example-commit)=
```{admonition} tl;dr
:class: tip
The full code that I developed for this section can be viewed [here](https://github.com/caporaso-lab/q2-dwq2/pull/7/commits/0cf4c9f0e5de4d8095f3fbc9c9fe84590f8cdb71).
```

## Defining a usage example for `nw-align`

Usage examples work on actual data that you define when you create the usage example.
This allows users to run your usage examples, explore the input and output, and confirm that things work as expected before they try your plugin on their own data.
This also allows you to have your usage examples automatically tested every time your run your test code, which lets you make and honor a commitment to your users that the documentation you provide will work, because you can automatically run all of the usage examples you define with a single command after every change you make so you'll be the first to know if anything is broken.

So let's start by defining data for use by our `nw-align` usage example.
This is done by creating a function that returns a QIIME 2 artifact that is used as an input in the example.

### Define input data for your usage example

Start by creating a top-level file in your module called `_examples.py`.
Mine will be called `q2-dwq2/q2_dwq2/_examples.py`.
Add the following code, and then we'll work through it line-by-line.

```python
import tempfile

import skbio

import qiime2

from q2_dwq2 import SingleRecordDNAFASTAFormat


def seq1_factory():
    seq = skbio.DNA("AACCGGTTGGCCAA", metadata={"id": "seq1"})
    return _create_seq_artifact(seq)


def seq2_factory():
    seq = skbio.DNA("AACCGCTGGCGAA", metadata={"id": "seq2"})
    return _create_seq_artifact(seq)


def _create_seq_artifact(seq: skbio.DNA):
    with tempfile.NamedTemporaryFile() as f:
        # write our skbio.DNA object to file in fasta format
        seq.write(f)
        # reset to the beginning of the file
        f.seek(0)
        # instantiate our file format (ff) object with the fasta file
        ff = SingleRecordDNAFASTAFormat(f.name, mode='r')
        # return the sequence packaged in a "SingleDNASequence" qiime2.Artifact
        return qiime2.Artifact.import_data("SingleDNASequence", ff)
```

Our goal here is to define two "factory" functions - one for each of `nw-align`'s `SingleDNASequence` inputs - that each return an artifact of class `SingleDNASequence`.
These functions will be used when we define our usage example, and because of how usage example definitions work, these functions can't take any parameters as input.
Because both of these functions will do similar work under the hood, I am also creating a helper function that creates a `SingleDNASequence` artifact from an `skbio.DNA` object.
That lets me avoid duplicating code.
(Ultimately, there is a simplification that you can make here by defining a new transformer, but I'm going to leave that as an advanced optional exercise for you at the end of this section.)

The factory functions I defined here are `seq1_factory` and `seq2_factory`.
Each creates an `skbio.DNA` object, and then passes that to my helper function, `_create_seq_artifact`.

`_create_seq_artifact` takes an `skbio.DNA` sequence object as input.
(The type hint in the function definition isn't required, but I like to include it to remind myself how this function works when I come back to it in the future.)
Internally, it creates a temporary file, writes the sequence to that file, and then creates `SingleRecordDNAFASTAFormat` object from that file.
In the final step, we use `qiime2.Artifact.import_data`, which allows us to import data in a similar way as if we were calling `qiime tools import` through q2cli: we provide the input file and the artifact class that we want to import into, and we get QIIME 2 artifact back.
That artifact is returned by the helper function, and in turn is returned by the factory function that called it.

This may feel like a lot of work to define data to use in an example, but it provides a lot of flexibility in how the usage example you define can ultimately be used.
For example, it allows some *usage drivers* to actually create these inputs (for example, a usage driver that is going to be used to test the examples), and for some usage drivers to not bother taking the time to create the inputs (for example, usage drivers that are writing commands in documentation).

### Defining the usage example

**This document is incomplete from this point.**

```python
def nw_align_example_1(use):
    seq1 = use.init_artifact('seq1', seq1_factory)
    seq2 = use.init_artifact('seq2', seq2_factory)

    msa, = use.action(
        use.UsageAction(plugin_id='dwq2',
                        action_id='nw_align'),
        use.UsageInputs(seq1=seq1, seq2=seq2),
        use.UsageOutputNames(aligned_sequences='msa'),
    )
```





## Displaying usage examples

### Command line interface

```shell
qiime dwq2 nw-align --help
Usage: qiime dwq2 nw-align [OPTIONS]

...

Examples:
  # ### example: Align two DNA sequences.
  qiime dwq2 nw-align \
    --i-seq1 seq1.qza \
    --i-seq2 seq2.qza \
    --o-aligned-sequences msa.qza
```

```shell
$ qiime dwq2 nw-align --example-data usage-example-data/
```

### Python 3 API

```python
from qiime2.plugins import dwq2, ArtifactAPIUsage

examples = dwq2.actions.nw_align.examples

for example in examples.values():
    use = ArtifactAPIUsage()
    example(use)
    print(use.render())
```

Will display the following:

```python
import qiime2.plugins.dwq2.actions as dwq2_actions

msa, = dwq2_actions.nw_align(
    seq1=seq1,
    seq2=seq2,
)
```

## Optional exercise

Add a usage example for your `summarize` visualizer.

```{dropdown} Need some hints?
For your example data, you can use the output generated by the `nw-align` usage example that we created here.
If you export that artifact, you can find the data in the format you'll need to create it in your factory function.
You can also find the artifact class that you'll need to use in your `qiime2.Artifact.import_data` call using the `qiime tools peek` command.
```
