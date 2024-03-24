(types-of-types)=
# Semantic types, data types, and file formats

The term _type_ is overloaded with a few different concepts.
The goal of this Explanation article is to disambiguate how it's used in QIIME 2.
To achieve this, we'll discuss two ways that it's commonly used, and then introduce a third way that it's used less frequently but which is important to QIIME 2.
The three kinds of types that are used in QIIME 2 are **file types**, **data types**, and **semantic types**.

````{margin}
```{admonition} Video
[This video](https://www.youtube.com/watch?v=PUsvtJgpNtE) on the QIIME 2 YouTube channel discusses semantic types.
```
````

## File types (or formats) and data types (or objects)
File types (or formats) refer to what you probably think of when you hear that phrase: the format of a file used to store some data.
For example, newick is a file type that is used for storing phylogenetic trees.
Files are used most commonly for archiving data when it's not actively in use.
Data types refer to how data is represented in a computer's memory (i.e., RAM) while it's actively in use, such as the data structure or object class that a file is loaded into.

For example, if you are adding a root to an unrooted phylogenetic tree, you may use a tool like [IQ-Tree](http://www.iqtree.org/).
You would provide a path to the file containing the unrooted phylogenetic tree to IQ-Tree, and IQ-Tree would load that tree into some object in the computer's memory to work on it.
The object that IQ-Tree uses internally to represent the phylogenetic tree is synonymous with _data type_, as used here.
The kind of object that is used is a decision made by the developers of IQ-Tree based on available functionality, efficiency for an operation they plan to carry out, their familiarity with the object, or something else.
If IQ-Tree successfully completes the requested rooting operation, it could then write the resulting tree from its internal data type into a new newick-formatted file on the hard disk, and exit.

One thing to notice from this example is that there are at least three *independent* choices being made by the developer regarding *types*: what file type to use as input, what data type to use internally, and what file type to use as output.
Users of command line software, like IQ-Tree, shouldn't need to know or care about what data types are used internally by a program.
They just need to know what file types are used as input and output.
Software developers, on the other hand, should care a lot about what data types are used by their program: choosing an appropriate type can have huge impacts on the performance of the software, for example.

## Semantic types
The third _type_ that is important in QIIME 2 is the semantic type of data.
This is a representation of the _meaning_ of the data, which is not necessarily represented by either a file type or a data type.
For example, two semantic types used in QIIME 2 are `Phylogeny[Rooted]` and `Phylogeny[Unrooted]`, which are used to represent rooted and unrooted phylogenetic trees, respectively.
Both rooted and unrooted trees are commonly described in newick-formatted files, and typically a computer program would need to parse a file to know if the tree it describes is rooted or unrooted.
For large trees, this can be a slow operation.

There are some operations, such as rooting a tree, that only make sense to perform on unrooted trees.
So, if you have a very large tree that you want to root, you may provide a newick file to a program that will perform that rooting.
If you accidentally provide a rooted tree, it may take the program some time to parse the file (say 20 minutes) after which it may fail if it discovers that the tree is already rooted.
That sort of delayed notification can be very frustrating as a user, since it's easily missed until a lot of time has passed.
For example, I often will start a long-running command on my university cluster computer just before the weekend.
I'll typically check on the job for a few minutes, to make sure that it seems to be starting ok.
I may then leave, with the hope that the job completes over the weekend and I'll have data to work with on Monday morning.
It's very frustrating to come in Monday morning and find out that my job failed just a few minutes after I left on Friday for a reason that I could have quickly addressed had I known in time.

```{note}
There's actually a worse outcome than a delayed error from a computer program when inappropriate input is provided.
When a program fails and provides an error message to the user, whether or not that error message helps the user solve the problem, the program has failed loudly.
Something went wrong, and it told the user about it.
The program could instead fail quietly.
This might happen if the program doesn't realize the input the user provided is inappropriate (e.g., an already rooted tree is provided to a program that roots an unrooted phylogenetic tree), and it runs the rooted tree through its algorithm, misinterprets something because it was provided with the wrong input, and generates an incorrect rooted tree as a result.
Quiet failures can be very difficult or impossible for a user to detect, because it looks like everything has worked as expected.
Failing quietly is _much_ worse than failing loudly: it could waste many hours of your time, and could even lead to you publishing invalid findings.
```

QIIME 2 semantic types help with this, because they provide information on what the data in a QIIME 2 `.qza` file means without having to parse anything in the `data` directory.
All QIIME 2 artifacts have a semantic type associated with them (it's one of the pieces of information stored in the `metadata.yaml` file), and QIIME 2 methods will describe what semantic types they take as input(s), and what semantic types they generate as output(s).

## Putting it together

There is a many-to-many relationship between file types, data types, and semantic types.
It's possible that a given semantic type could be represented on disk by different file types.
That's well exemplified by the many different formats that are used to store demultiplexed sequence and sequence quality data.
For example, this may be in one a few variants of the fastq format, or in the fasta/qual format.
Additionally, data from multiple samples may be contained in one single file or split into per-sample files.
Regardless of which of these file formats the data is stored in, QIIME 2 will assign the same semantic type (in this case, `SampleData[SequencesWithQuality]`.
Similarly, the data type used in memory might differ depending on what operations are to be performed on the data, or based on the preference of the programmer.

QIIME 2 uses the semantic type `FeatureTable[Frequency]` to represent the idea of a feature table that contains counts of features (e.g., bacterial genera) on a per sample basis.
Many different actions can be applied to `FeatureTable[Frequency]` artifacts in QIIME 2.
When a plugin developer defines a new action that takes a `FeatureTable[Frequency]` as input, they can choose whether to load the table into a `pandas.DataFrame` or `biom.Table` object, which are two different data types.
Our example plugin `q2-dwq2` initially defines a action called `duplicate_table` which [takes a `FeatureTable[Frequency]` as input](https://github.com/caporaso-lab/q2-dwq2/blob/3465ea40b18ae15825411a5930cfd24016f5d872/q2_dwq2/plugin_setup.py#L28), and [generates the same semantic type as its output](https://github.com/caporaso-lab/q2-dwq2/blob/3465ea40b18ae15825411a5930cfd24016f5d872/q2_dwq2/plugin_setup.py#L30).
The function registered to this action [declares that it will "view" the input `table` as a `pd.DataFrame`, and also return the output as a `pd.DataFrame`](https://github.com/caporaso-lab/q2-dwq2/blob/3465ea40b18ae15825411a5930cfd24016f5d872/q2_dwq2/_methods.py#L12).
File types are associated with semantic types when [Artifact Classes are defined](https://github.com/qiime2/q2-types/blob/e25f9355958755343977e037bbe39110cfb56a63/q2_types/feature_table/_type.py#L42).

Each kind of type discussed here represents different information about the data: how it's stored on disk (file type), how it's used by a function (its data type), and what it represents (its semantic type).
The motivation for creating QIIME 2's semantic type system was to avoid issues that can arise from providing inappropriate data to actions.
The semantic type system also helps users and developers better understand the intent of QIIME 2 actions by assigning meaning to the input and output, and allows for the discovery of new potentially relevant QIIME 2 actions.