(plugin-tutorial-add-artifact-class)=
# Add a new Artifact Class

Now that we've built a basic method and a basic visualizer, let's step into another unique aspect of developing with QIIME 2: defining {term}`artifact classes <artifact class>`.
*Artifact classes* are closely related to terms you have probably already encountered in the QIIME 2 ecosystem: {term}`semantic types <semantic type>`, {term}`formats <format>`, and {term}`transformers <transformer>`.
For most of the new QIIME 2 developers who I've worked with, defining a new artifact class (and the associated semantic type, format(s), and transformer(s)) is the most obscure step.
However it's what gives QIIME 2 a lot of its power (for example, its ability to be accessed through different interfaces and to help users avoid analytic errors) and flexibility (for example, its ability to load the same artifact into different data types, depending on what you want to do with it).

[Recall that when we initially built our `nw-align` method](suboptimal-initial-types), we used artifact classes that were suboptimal because there weren't relevant existing ones.
Two questions may arise here.
First, as a plugin developer, how do you know what relevant artifact classes are available to you for use in development?
And second, how do you add one or more new artifact classes if you need some that don't exist?

We'll start here with a brief *explanation* to set the stage for the work we'll do in this section of the tutorial.
Then, we'll address the first question with a very brief *how-to*, because if you don't need to define a new semantic type, that's ideal.
And finally, the majority of this section of the tutorial will focus on creating a new artifact class for use in our plugin.

(add-artifact-class-commit)=
```{admonition} tl;dr
:class: tip
The complete code that I developed to define my new artifact class, including the corresponding semantic type, formats, and transformer, can be found here: {{ dwq2_add_artifact_class_commit_1_url }}.
The code that I developed to transition my `nw-align` action to use my new artifact class can be found here: {{ dwq2_add_artifact_class_commit_2_url }}.
```

## Artifact classes

I'm going to begin by defining an {term}`artifact class` as **a kind of QIIME 2 artifact that can exist**.
A new artifact class can be registered by a plugin developer by associating a {term}`semantic type` with a {term}`format`.
Let's briefly discuss both of those terms.

Semantic types define the meaning of the data - i.e., what it represents.
For example, QIIME 2 defines a `Phylogeny[Rooted]` artifact class, and the semantic type associated with the artifact class is `Phylogeny` (i.e., a phylogenetic tree) with a sub-semantic-type `Rooted` (i.e., implying that the phylogenetic tree contains a specified root node).
Together, therefore, the `Phylogeny[Rooted]` artifact class can be described as a rooted phylogenetic tree.

Formats describe how the data will be represented inside the artifact when it is serialized for storage (generally meaning written to file, in this context).
Continuing with our phylogenetic tree example, multiple different file formats have been defined to represent a rooted phylogenetic tree, including newick and NEXUS, and this is typical for most types of information in bioinformatics (and other fields).
Similarly, a single file format can be used to store semantically different information - for example, newick can also be used to store unrooted phylogenetic trees.

This means that formats are inherently independent of semantic types: a semantic type doesn't imply a specific format, and a format doesn't imply a specific semantic type.
When a new artifact class is registered by a developer, they associate a semantic type with a format.
This enables QIIME 2 to know what an artifact class is intended to represent, and how it can be read from and written to disk.
With this information, an artifact class can exist.

{term}`Transformers <transformer>`, which we'll come back to later, can be associated with formats and used to convert (transform) between formats, load formats in data types, and more.
Among other things, transformers enable a given artifact class to update its format in new versions of QIIME 2, for example if a more efficient format becomes available, without end-users needing to know that anything changed.

## Discovering artifact classes

The main way that plugin developers become aware of the existing artifact classes that are relevant for their plugin is through familiarity from using QIIME 2.
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
Take a minute to review this list to identify artifact classes that you've used before, and any others that might be relevant in your work.

```{note}
A how-to article is [planned](https://github.com/caporaso-lab/developing-with-qiime2/issues/58) that will provide additional detail on identifying an existing artifact class for use in your plugin.
In the meantime, please feel free to reach out through the {{ developer_discussion }} if you're struggling to identify a relevant semantic type - we know this can be challenging, and we don't mind helping.
```

## Developing a new artifact class

Now that we have that background, lets get into it.

### Defining a new semantic type

In this section we're going to define a new artifact class called `SingleDNASequence`, which represents a single DNA sequence.
Recall that previously we associated the `FeatureData[Sequence]` artifact class with our inputs to `nw-align`, but since this artifact class is intended to represent collections of sequences (rather than the single sequences that we use as input to `nw-align`) it was just a way to quickly get started.
Defining `SingleDNASequence` will allow us to better represent the input to `nw-align`, and to reduce some unnecessary code that we wrote in our action.

Start by creating a new file, `_types_and_formats.py` in your module's top-level directory.
For me, this file will be `q2-dwq2/q2_dwq2/_types_and_formats.py`.
Add the following code to that file.

```python
from qiime2.plugin import SemanticType

SingleDNASequence = SemanticType("SingleDNASequence")
```

That code defines a new semantic type, which can be referred to as `SingleDNASequence`.
Defining new semantic types is the easier part of defining new artifact classes.

### Defining a new file format

The next thing we'll do is define a file format that we'll use with this semantic type to define our artifact class. We'll call our file format `SingleRecordDNAFASTAFormat`, implying that it is a fasta-formatted file for storing a single DNA sequence record.

Our `SingleRecordDNAFASTAFormat` will be a subclass of QIIME 2's `TextFileFormat` class.
The only requirement of our subclass is that it define a method called `_validate_`, and that method should take a validation `level` as input and not return any output.
`level` will always be provided as either `max` (the default) or `min`.
If a problem is discovered during validation, a `qiime2.plugin.ValidationError` should be raised.
If `_validate_` returns without raising a `ValidationError`, that indicates that validation has succeeded.

It's up to you as the format developer to define what happens in the `_validate_` function, and that can range from no validation whatsoever (i.e., just `pass` in the function body; we don't recommend this and [consider it a plugin development anti-pattern](antipattern-skipping-validation)), to extremely detailed validation.
The `level` is used to define whether minimal or maximal validation should be performed.
The trade-off is that maximal validation can take a long time, slowing down use of this file format (which will likely be percieved as your plugin being slow), but if written well can prevent against invalid data being packaged in this file format.
Minimal validation on the other hand can be very quick, but may allow some errors to sneak through.
You don't have to do anything differently inside of `_validate_` based on whether a user requests minimal or maximal validation, but it's a good idea to vary what is being done if maximal validation will be slow.

```{note}
As a practical example of when minimal validation can be helpful, think of the case where large machine-generated fastq files are associated with a QIIME 2 format (e.g., during import).
Validating each file in its entirety can take a very long time, and since the fastq files are machine generated, they're (presumably) unlikely to contain errors because the developers of the code that wrote that fastq (presumably) tested that code well.

The less you trust the creator of a file, the more important validation is. If your users are manually creating a file, that's an important case for extensive validation.
No offense to your users: creating files can be tedious, and tedious work is error prone when done by humans (we get bored and make mistakes).
Computers on the other hand are great at it.
So automate everything you can... but I digress.
```

```{tip}
One feature to be aware of here, though we won't use it right away, is that since you're defining your format class, you can add additional methods or properties to it that will be convenient for you if/when you work directly with instances of the format in your actions.
For example, if you wanted an easy way to get the identifier of the sequence in this object, you could add a `SingleRecordDNAFASTAFormat.get_sequence_id()` method (for example), and then access that in the normal way when you have an instance of this class.
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

In the previous sections we discussed that QIIME 2 uses file formats to describe how data is organized in artifacts for specific artifact classes.
In a QIIME 2 artifact, the relevant data is stored in the `data/` directory.
For some artifact classes, including the one we're building here, all of the relevant data is contained in a single file.
However in other cases, there may be multiple files and/or subdirectories.
Because we're defining the contents of a directory when registering a new artifact class, we actually need to associate a `qiime2.plugin.DirectoryFormat` with our new artifact class.

For simple cases like ours, where there will only be a single file in that directory, QIIME 2 has a helper function, `qiime2.plugin.model.SingleFileDirectoryFormat`, which we can use to create a directory format.
Add the following code to `_types_and_formats.py` to define your directory format.

```python
from skbio import DNA
from skbio.io import UnrecognizedFormatError

from qiime2.plugin import SemanticType, TextFileFormat, model, ValidationError

SingleRecordDNAFASTADirectoryFormat = model.SingleFileDirectoryFormat(
    'SingleRecordDNAFASTADirectoryFormat', 'sequence.fasta',
    SingleRecordDNAFASTAFormat)
```

This code creates a new object, `SingleRecordDNAFASTADirectoryFormat`.
The parameters being provided in the call to `SingleFileDirectoryFormat` are the name of the directory format, what we'd like to call the single file in the directory format, and what format this file will be in.
We'll call the file in our directory format `sequence.fasta` (it can be anything, but making it descriptive helps), and it will be of the type we just defined, `SingleRecordDNAFASTAFormat`.

This completes the code you'll need in `_types_and_formats.py`.
Compare your code against [mine](add-artifact-class-commit) to make sure it's functionally identical.

## Registering an artifact class

At this stage, we have defined our sematic type and the formats that we'll associated with this semantic type.
We'll now move on to registering these, so we can use them.

### Making the new type and formats publicly importable

Next, open the `__init__.py` in the top-level directory of your module.
For me, this will be `q2-dwq2/q2_dwq2/__init__.py`.
Add the following lines to the imports at the top of your file:

```python
from ._types_and_formats import (
    SingleDNASequence, SingleRecordDNAFASTAFormat,
    SingleRecordDNAFASTADirectoryFormat)
```

Then add the following lines at the bottom of the file:

```python
__all__ = [
    "SingleDNASequence", "SingleRecordDNAFASTAFormat",
    "SingleRecordDNAFASTADirectoryFormat"]
```

This will allow you and others to import your semantic type and formats directly from the module without accessing files that are intended to be private (e.g., by calling `from q2_dwq2 import SingleDNASequence`).
This gives you the freedom to reorganize files or file contents internally in your plugin without changing the public-facing API - even if you update the import statements in this file, anyone importing from your code (e.g., plugin developers who are building other plugins that depend on yours) shouldn't need to change their code.

(register-artifact-class)=
### Registering the type, formats, and artifact class

Next, we'll edit our `plugin_setup.py` file to register our new type, our new formats, and our new artifact class.
To do this, first we'll import those three objects in `plugin_setup.py`:

```python
from q2_dwq2 import (
    SingleDNASequence, SingleRecordDNAFASTAFormat,
    SingleRecordDNAFASTADirectoryFormat)
```

Notice that because of the additions we made in `__init__.py` we import these from our top-level module directly (not from `q2_dwq2._types_and_formats.py`, where they are defined).

Next, we'll call three methods on our `plugin` object as follows:

```python
# Register semantic types
plugin.register_semantic_types(SingleDNASequence)

# Register formats
plugin.register_formats(SingleRecordDNAFASTAFormat,
                        SingleRecordDNAFASTADirectoryFormat)

# Define and register new ArtifactClass
plugin.register_artifact_class(SingleDNASequence,
                               SingleRecordDNAFASTADirectoryFormat,
                               description="A single DNA sequence.")
```

The first two should be self-explanatory: we register the new semantic type and the new formats.
Each of these calls takes `*args` as input, which means that you can provide all the types and formats that you want to register as arguments to these methods.
Each method takes one or more arguments.

The final method call in that block is the one we've been working toward - it's where we associate our new semantic type with a directory format, and provide a description of what this artifact class is for users or other developers who may wish to use it.
At this point, your plugin has defined a new artifact class and you should see it in the list of artifact classes if you run the following commands:

```shell
qiime dev refresh-cache
qiime tools list-types
```

```{note}
As mentioned earlier, when you add or update actions, types, or formats you'll need to run `qiime dev refresh-cache` to see those modifications through {term}`q2cli`.
```

## Defining and registering a transformer

There are a couple of last things that we need to do before we're ready to use our new artifact class.
The first is define how an instance of our artifact class (e.g., an artifact stored in a `.qza` file) can be loaded in the form that we want to use it in inside of our action.

In QIIME 2 jargon, we review to the different ways an artifact can be used inside of an action as different **views of an artifact class**.
For example, if we want to recieve the fasta file directly, we can request to *view* the artifact as a `SingleRecordDNAFASTAFormat`.
Inside of our action, we could then open that and do whatever we need to with it.
This approach of working with file formats or directory formats directly is common, for example, when processing raw sequence data such as collections of demutiplexed sequence reads.
This might look like the following in our action definition:

```python
# this is just an example - don't put this code in your plugin
def nw_align(seq1: SingleRecordDNAFASTAFormat,
             seq2: SingleRecordDNAFASTAFormat,
             ...
```

In our case, we want to load our sequences into `skbio.DNA` objects, as that's what the `skbio.alignment.global_pairwise_align_nucleotide` function that we're calling takes as input.
So, we need to transform our fasta-formatted file into an `skbio.DNA` object, and we do that with a {term}`transformer`.

Create a new file, `_transformers.py`, in your top-level module directory.
Mine is called `q2-dwq2/q2_dwq2/_transformers.py`.
Add the following code to that file:

```python
from skbio import DNA

from q2_dwq2 import SingleRecordDNAFASTAFormat

from .plugin_setup import plugin


# Define and register transformers
@plugin.register_transformer
def _1(ff: SingleRecordDNAFASTAFormat) -> DNA:
    # by default, DNA.read will read the first sequence in the file
    with ff.open() as fh:
        return DNA.read(fh)
```

This code first imports the objects that we want to transform to (`skbio.DNA`) and from (`SingleRecordDNAFASTAFormat`).
We then import our `plugin` object from `plugin_setup.py`, which we'll use to register our transformer.
Finally, we define our transformer function and register it with our plugin using a function decorator.

Your transformer function can be called anything you want, but by convention they receive arbitrary names.
This is because the transformers are never called directly by users or developers, and because the function signature's type hints unambiguously define what it does.
Before we adopted this convention we had a lot of functions with names like `_transform_SingleRecordDNAFASTAFormat_to_DNA`, which was starting to feel silly and in some cases the names were ambiguous (but if you prefer that, there are no issues with naming your transformers that way).
Internally, this function does whatever it needs to to convert (or transform) the input object to the output object.
In our case, we're opening the file format (`ff`) object provided as input, and reading the first (and only, in this case) sequence from it using `skbio.DNA.read`, and returning the result.

````{note}
You may have noticed that our artifact class stores data as defined in our  `SingleRecordDNAFASTADirectoryFormat` class, but we're working with it here in a `SingleRecordDNAFASTAFormat` object.
QIIME 2 automatically creates transformers from directory formats to file formats for single-file directory formats when they are created with `model.SingleFileDirectoryFormat`, as we did above.
QIIME 2 also knows how to chain transformers, such that when we attempt to view an instance of our artifact class as `skbio.DNA`, it will first transform from `SingleRecordDNAFASTADirectoryFormat` to `SingleRecordDNAFASTAFormat`, and then transform from `SingleRecordDNAFASTAFormat` to `skbio.DNA`.
If you're concerned that a chained transformation will be too slow, you can also define a transformer that skips the intermediate step.
In this case, that might have a signature like:

```python
_2(df: SingleRecordDNAFASTADirectoryFormat) -> skbio.DNA
```

That won't be needed here however.
````

````{note}
If you'd like to be able to view a `SingleDNASequence` artifact as another data type for use in your actions - for example, as a Python string (`str`) - you can define another transformer for it.
For example:

```python
_3(ff: SingleRecordDNAFASTAFormat) -> str
```

or

```python
_4(seq: skbio.DNA) -> str
```
````

To make this transformer accessible to your plugin, there's just one last thing to do, which is make sure that the code in this file runs when the `plugin` object is created.
For this, we go back to `plugin_setup.py`.
Add the following line to the imports at the top of that file:

```python
import importlib
```

Then, add the following as the last line in your file:

```python
importlib.import_module('q2_dwq2._transformers')
```

This will load and run the `_transformers.py` file, ensuring that our transformer is registered after the `plugin` object has been instantiated and our type and formats have been registered.

## Unit testing

As always, before we use this code, we're going to test it.
At a high-level, there are three things we need to test: the semantic type we defined, the formats we defined, and the transformer we defined.
Let's start with the type and formats.

### Testing the semantic type and formats

As you probably noticed, there isn't much to a semantic type - we're essentially just defining a name that will be linked to an artifact class.
We therefore just want to confirm that the type is registered with the plugin.
`qiime2.plugin.testing.TestPluginBase` provides a method for this, `assertRegisteredSemanticType`.

For our formats, most of the action is happening inside of the `_validate_` function, so that's mostly what we're testing.
I like to start with confirming that a few valid examples of my format pass validation, and then provide invalid files that are invalid for different reasons to confirm that those files fail validation.
It's also a good idea to confirm that your validation level is functioning as expected.

Below is my test code, which lives in `q2-dwq2/q2_dwq2/tests/test_types_and_formats.py`.
I added a few new test data files to support these tests, which you can access from [my code on GitHub](add-artifact-class-commit).

```python
from qiime2.plugin import ValidationError
from qiime2.plugin.testing import TestPluginBase

from q2_dwq2 import (
    SingleDNASequence, SingleRecordDNAFASTAFormat
)


class SingleDNASequenceTests(TestPluginBase):
    package = 'q2_dwq2.tests'

    def test_semantic_type_registration(self):
        self.assertRegisteredSemanticType(SingleDNASequence)


class SingleRecordDNAFASTAFormatTests(TestPluginBase):
    package = 'q2_dwq2.tests'

    def test_simple1(self):
        filenames = ['seq-1.fasta', 'seq-2.fasta', 't-thermophilis-rrna.fasta']
        filepaths = [self.get_data_path(fn) for fn in filenames]

        for fp in filepaths:
            format = SingleRecordDNAFASTAFormat(fp, mode='r')
            format.validate()

    def test_invalid_default_validation(self):
        fp = self.get_data_path('bad-sequence-1.fasta')
        format = SingleRecordDNAFASTAFormat(fp, mode='r')
        self.assertRaisesRegex(ValidationError,
                               "4 non-ACGT characters.*171 positions.",
                               format.validate)

    def test_invalid_max_validation(self):
        fp = self.get_data_path('bad-sequence-1.fasta')
        format = SingleRecordDNAFASTAFormat(fp, mode='r')
        self.assertRaisesRegex(ValidationError,
                               "4 non-ACGT characters.*171 positions.",
                               format.validate,
                               level='max')

    def test_invalid_min_validation(self):
        fp = self.get_data_path('bad-sequence-1.fasta')
        format = SingleRecordDNAFASTAFormat(fp, mode='r')
        # min validation is successful
        format.validate(level='min')
        # but max validation raises an error
        self.assertRaisesRegex(ValidationError,
                               "4 non-ACGT characters.*171 positions.",
                               format.validate,
                               level='max')

        fp = self.get_data_path('bad-sequence-2.fasta')
        format = SingleRecordDNAFASTAFormat(fp, mode='r')
        self.assertRaisesRegex(ValidationError,
                               "4 non-ACGT characters.*50 positions.",
                               format.validate,
                               level='min')
```

### Testing the transformer

Next, we'll test our transformer.
Here, we should provide a few different valid inputs, and test that they are transformed to the expected output.
Generally you should use the `transform_format` action in `qiime2.plugin.testing.TestPluginBase` to access and run the transformer (as opposed to importing the function directly from `_transformers.py`).
This also tests that the transformer is registered with the plugin.

The test code that I wrote for this is in `q2-dwq2/q2_dwq2/tests/test_transformers.py`, and follows here:

```python
from skbio import DNA

from qiime2.plugin.testing import TestPluginBase

from q2_dwq2 import SingleRecordDNAFASTAFormat


class SingleDNASequenceTransformerTests(TestPluginBase):
    package = 'q2_dwq2.tests'

    def test_single_record_fasta_to_DNA_simple1(self):
        _, observed = self.transform_format(
            SingleRecordDNAFASTAFormat, DNA, filename='seq-1.fasta')

        expected = DNA('ACCGGTGGAACCGGTAACACCCAC',
                       metadata={'id': 'example-sequence-1', 'description': ''})

        self.assertEqual(observed, expected)

    def test_single_record_fasta_to_DNA_simple2(self):
        _, observed = self.transform_format(
            SingleRecordDNAFASTAFormat, DNA, filename='seq-2.fasta')

        expected = DNA('ACCGGTAACCGGTTAACACCCAC',
                       metadata={'id': 'example-sequence-2', 'description': ''})

        self.assertEqual(observed, expected)
```

Write your tests, and then run them with `make test`.
You should see something like the following:

```shell
$ make test
...
====== 14 passed, 23 warnings in 1.51s ======
```

If you have failing tests, work through them to figure out what's wrong.
If you get stuck, refer back to my code.
At this point, you should have implemented everything in [the first of my commits](add-artifact-class-commit)  associated with this section.

## Updating `nw-align` to use the new artifact class

Ok.
That was a lot of work.
But hopefully you can see that none of the coding is very hard, even if conceptually it's a little challenging as you get started.
As we continue to work through the tutorial, I'll point out places where the work we did here provides powerful benefits for our plugin users and for us as plugin developers.

Now let's update our `nw-align` method to use the new artifact class that we defined.
As discussed earlier, this will enable us to simplify the code and associated tests.
Since we're looking at code changes here, rather than new code, the most convenient view you'll have is GitHub's diff of this commit against the previous.
To see this, open the link to the [second of my commits](add-artifact-class-commit) associated with this section.

The work that we're doing here is transitioning our use of the `FeatureData[Sequence]` artifact class for our new `SingleDNASequence` artifact class, and transitioning our use of the `DNAIterator` view inside `nw-align` to use `skbio.DNA` as our view.

Start by looking at the changes in `test_methods.py`, and adapt your code in the same way.
Notice that in the second test case (`test_simple2`), we're using `qiime2.plugin.util.transform` to load files stored in our `tests/data` directory into `skbio.DNA` objects for use in the tests.

```{note}
Pending [a fix for an oversight in `TestPluginBase`](https://github.com/qiime2/qiime2/issues/757), it will be possible to use `qiime2.plugin.testing.TestPluginBase.transform_format` for performing the fasta file to `skbio.DNA` transformation.
This will enable tests of actions to use the same machinery used during testing of transformers.
```

If you run your unit tests now with `make test`, you should get some test failures.
That's expected, as we updated the tests but haven't yet updated the code.
Let's now update the code, and we'll know we're done when these tests pass.

First, update the method itself, as I did in `q2-dwq2/q2_dwq2/_methods.py`.
Here you're telling QIIME 2 to use a different view type inside this function, and then we're removing some of the clunky code that we no longer need.
Here's my `nw_align` function after making these changes:

```python
def nw_align(seq1: DNA,
             seq2: DNA,
             gap_open_penalty: float = 5,
             gap_extend_penalty: float = 2,
             match_score: float = 1,
             mismatch_score: float = -2) -> TabularMSA:
    msa, _, _ = global_pairwise_align_nucleotide(
        seq1=seq1, seq2=seq2, gap_open_penalty=gap_open_penalty,
        gap_extend_penalty=gap_extend_penalty, match_score=match_score,
        mismatch_score=mismatch_score
    )

    return msa
```

Then, update `plugin_setup.py` to associate our new artifact class with the sequence inputs.
Here's what this looks like for me, after I make this change:

```python
plugin.methods.register_function(
    function=nw_align,
    inputs={'seq1': SingleDNASequence,
            'seq2': SingleDNASequence},
...
```

After making the changes that I made, all tests should pass when you run `make tests`.
Once all tests are passing, run `qiime dev refresh-cache` and call help on your plugin's `nw-align` action.
You should see the new types associated with the `seq1` and `seq2` inputs.
Refer back to [where we tried out the nw-align action](trying-nw-align) for the first time.
Using those same fasta files (or any others you'd like), adapt the commands in that section to import sequence data into artifacts of our new artifact class, and run `nw-align` on them.

## An optional exercise

Try making a new visualizer that will create a visual summary of a `SingleDNASequence` artifact class.
Define a transformer to a view type other than `skbio.DNA`, and use that in your visualizer.
For example, does another library like BioPython provide an object with a convenient view that you could use here?
(Note that you may need to install any other library that you're using here in your development environment.)
