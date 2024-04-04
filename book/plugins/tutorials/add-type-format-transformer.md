(plugin-tutorial-add-type-format-transformer)=
# Adding a new Artifact Class

Now that we've built a basic method and a basic visualizer, let's step into another unique aspect of developing with QIIME 2: defining {term}`Artifact classes <artifact class>`.
*Artifact classes* are closely related to terms you have probably already encountered in the QIIME 2 ecosystem: {term}`semantic types <semantic type>`, {term}`file formats <format>`, and {term}`transformers <transformer>`.
For most of the new QIIME 2 developers who I've worked with, defining a new artifact class (and the associated semantic type, file format(s), and transformer(s)) is the most obscure step.
However it's what gives QIIME 2 a lot of its power (for example, its ability to be accessed through different interfaces and to help users avoid analytic errors) and flexibility (for example, its ability to load the same artifact into different data types, depending on what you want to do with it).

[Recall that when we initially built our `nw-align` method](suboptimal-initial-types), we used artifact classes that were suboptimal because there weren't relevant existing ones.
Two questions may arise here.
First, as a plugin developer, how do you know what relevant artifact classes are available to you for use in development?
And second, how do you add one or more new artifact classes if there are no relevant ones?

We'll start here with a brief *explanation* to set the stage for the work we'll do in this section of the tutorial.
Then, we'll address the first question with a very brief *how-to*, because if you don't need to define a new semantic type, that's ideal.
And finally, the majority of this section of the tutorial will focus on creating a new artifact class for use in our plugin.

(add-artifact-class-commit)=
```{admonition} tl;dr
:class: tip
The complete code that I developed to define my new artifact class, including the corresponding semantic type, file formats, and transformer, can be found [here](https://github.com/caporaso-lab/q2-dwq2/pull/6/commits/e183b1630be81517689ce7539476e30ffa0ecfd9).
The code that I developed to transition my `nw-align` action to use my new artifact class can be found [here](https://github.com/caporaso-lab/q2-dwq2/pull/6/commits/33b039c66995321ddd0ab245581b37e62b9080e5).
```

## Artifact classes

I'm going to begin by defining an {term}`artifact class` as **a kind of QIIME 2 artifact that can exist**.
A new artifact class can be registered by a plugin developer by associating a {term}`semantic type` with a {term}`file format <format>`.
Let's briefly discuss both of those terms.

Semantic types define the meaning of the data - i.e., what it represents.
For example, QIIME 2 defines a `Phylogeny[Rooted]` artifact class, and the semantic type associated with the artifact class is `Phylogeny` (i.e., a phylogenetic tree) with a sub-semantic-type `Rooted` (i.e., implying that the phylogenetic tree contains a specified root node).
Together, therefore, the `Phylogeny[Rooted]` artifact class can be described as a rooted phylogenetic tree.

File formats describe how the data will be represented inside the artifact when it is serialized for storage (i.e., generally meaning written to file, in this context).
Continuing with our phylogenetic tree example, multiple different file formats have been defined to represent a rooted phylogenetic tree, including newick and NEXUS, and this is typical for most types of information in bioinformatics (and other fields).
Similarly, a single file format can be used to store semantically different information - for example, newick can also be used to store unrooted phylogenetic trees.

This means that file formats are inherently independent of semantic types: a semantic type doesn't imply a specific file format, and a file format doesn't imply a specific semantic type.
When a new artifact class is registered by a developer, they associate a semantic type with a file format.
This enables QIIME 2 to know how an artifact class should be used, and how it can be read from and written to disk.
With this information, an artifact class can exist.

{term}`Transformers <transformer>`, which we'll come back to later, can be associated with file formats and used to convert (transform) between file formats.
Transformers enable a given artifact class to update its format in new versions of QIIME 2, for example if a more efficient format becomes available, without end-users needing to know that anything changed.

## Discovering artifact classes

The main way that plugin developers become aware of artifact classes that are relevant for their plugin is through familiarity from using QIIME 2.
For example, if you're planning to add a new method for feature table normalization, you may know that you start with the same feature table artifact class that is used by the `rarefy` action in the `q2-feature-table` plugin.
That gives you a lead on the artifact class you're going to use.

On the other hand, if you're searching to see what artifact classes are available, the best approach right now is to call `qiime tools list-types`, which lists the artifact classes that are available.
If you do this in your development environment, you should see something like the following:

```shell
$ qiime tools list-types

Bowtie2Index
	No description

BrackenDB
	No description

DistanceMatrix
	A symmetric matrix representing distances between entities.

FeatureData[AlignedProteinSequence]
	Aligned protein sequences associated with a set of feature
	identifiers. Exactly one sequence is associated with each
	feature identfiier.

FeatureData[AlignedRNASequence]
	Aligned RNA sequences associated with a set of feature
	identifiers. Exactly one sequence is associated with each
	feature identfiier.

...
```

```{note}
As of this writing (April 2024) you'll see many artifact classes that don't have descriptions.
The ability to add descriptions to artifact classes was added relatively recently, and we're working through existing types to add descriptions.
```

Some of these are self-explanatory and some are a bit opaque.
You can review this list to identify relevant artifact classes.

```{note}
A how-to article is [planned](https://github.com/caporaso-lab/developing-with-qiime2/issues/58) that will provide additional detail on selecting an existing artifact class for use in your plugin.
In the meantime, please feel free to [reach out on the forum](https://forum.qiime2.org/c/dev-discussion/7) if you're strugging to identify a relevant semantic type - we know this can be challenging, and we don't mind helping.
```

## Developing a new Artifact Class

Now that we have that background, lets get into it.

### Defining a new semantic type

In this section we're going to define a new artifact class called `SingleDNASequence`, which represents a single DNA sequence.
Recall that previously we associated the `FeatureData[Sequence]` artifact class with our inputs to `nw-align`, but since this artifact class is intended to represent collections of sequences (rather than the single sequences that we use as input to `nw-align`) it was just a way to quickly get started.
Defining `SingleDNASequence` will allow us to better represent the input to `nw-align`, and to reduce some unnecessary code that we wrote in our action.

Start by creating a new file, `_types_and_formats.py` in your module's top-level directory. For me, this file will be `q2-dwq2/q2_dwq2/_types_and_formats.py`. Add the following code to that file.

```python
from qiime2.plugin import SemanticType

SingleDNASequence = SemanticType("SingleDNASequence")
```

That code defines a new semantic type, which can be referred to as `SingleDNASequence`.

### Defining a new file format

The next thing we'll do is define a file format that we'll use with this semantic type to define our artifact class. We'll call our format `SingleRecordDNAFASTAFormat`, implying that is a fasta-formatted file for storing a single DNA sequence record.

Our `SingleRecordDNAFASTAFormat` will be a subclass of QIIME 2's `TextFileFormat` class.
The only requirement of our subclass is that it define a method called `_validate_`, and that method should take a validation `level` as input.
`level` will always be provided as either `max` (the default) or `min`.

It's up to you as the format developer to define what happens in the `_validate_` function, and that can range from no validation whatsoever (i.e., just `pass` in the function body; we don't recommend this and [consider it a plugin development anti-pattern](antipattern-skipping-validation)), to extremely detailed validation.
The `level` is used to define whether minimal or maximal validation should be performed.
The trade-off is that maximal validation can take a long time, slowing down use of this format (which will likely be percieved as your plugin being slow), but if written well can make sure that invalid data is never packaged in this format.
Minimal validation on the other hand can be very quick, but may allow some errors to sneak through.
You don't have to do anything differently inside of `_validate_` based on whether a user requests minimal or maximal validation, but it's a good idea to vary what is being done if maximal validation will be slow.

```{note}
As a practical example of when minimal validation can be helpful, think of the case where large machine-generated fastq files are stored with a QIIME 2 format (e.g., during import).
Validating the entire file can take a very long time, and since the fastq file is machine generated, it's (presumably) unlikely to contain errors because the developers of the code that wrote that fastq (presumably) tested that code well.

The less you trust the creator of a file, the more important validation is. If your users are manually creating a file, that's an important case for extensive validation.
No offense to your users: creating files can be tedious, and tedious work is error prone when done by humans (we get bored and make mistakes).
Computers on the other hand are great at it.
So automate everything you can... but I digress.
```

Add the following code to `_types_and_formats.py` (note that I'm building on my `import` statement from the previous code block here):


```python
from skbio import DNA
from skbio.io import UnrecognizedFormatError

from qiime2.plugin import SemanticType, TextFileFormat, ValidationError

class SingleRecordDNAFASTAFormat(TextFileFormat):

    def _confirm_single_record(self):
        with self.open() as fh:
            try:
                # DNA.read(..., validate = False) disables checking to ensure
                # that all characters in the sequence are IUPAC DNA characters
                # by scikit-bio.
                # This will be validated independently by _validate_, with user
                # control over how much of the sequence is read during
                # validation, to manage the runtime of validation.
                _ = DNA.read(fh, seq_num=1, validate=False)
            except UnrecognizedFormatError:
                raise ValidationError(
                    "At least one sequence record must be present, but none "
                    "were found."
                )

            try:
                _ = DNA.read(fh, seq_num=2, validate=False)
            except ValueError:
                # if there is no second record, a ValueError should be raised
                # when we try to access the second record
                pass
            else:
                raise ValidationError(
                    "At most one sequence record must be present, but more "
                    "than one record was found."
                )

    def _confirm_acgt_only(self, n_chars):
        with self.open() as fh:
            seq = DNA.read(fh, seq_num=1, validate=False)
            validation_seq = seq[:n_chars]
            validation_seq_len = len(validation_seq)
            non_definite_chars_count = \
                validation_seq_len - validation_seq.definites().sum()
        if non_definite_chars_count > 0:
            raise ValidationError(
                f"{non_definite_chars_count} non-ACGT characters detected "
                f"during validation of {validation_seq_len} positions."
            )

    def _validate_(self, level):
        validation_level_to_n_chars = {'min': 50, 'max': None}
        self._confirm_single_record()
        self._confirm_acgt_only(validation_level_to_n_chars[level])
```

Take a minute to read through this, starting with the `_validate_` function and following the function calls that are made inside of it.
What is being done during validation?
How is the validation level being used here?

### Defining a new directory format

**This section is incomplete - start with definition of the directory format.**

```python
from skbio import DNA
from skbio.io import UnrecognizedFormatError

from qiime2.plugin import SemanticType, TextFileFormat, model, ValidationError

SingleRecordDNAFASTADirectoryFormat = model.SingleFileDirectoryFormat(
    'SingleRecordDNAFASTADirectoryFormat', 'sequence.fasta',
    SingleRecordDNAFASTAFormat)
```