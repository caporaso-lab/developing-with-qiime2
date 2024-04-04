(plugin-tutorial-add-type-format-transformer)=
# Adding a new Artifact Class

Now that we've built a basic method and a basic visualizer, let's step into another unique aspect of developing with QIIME 2: defining {term}`Artifact classes <artifact class>`.
*Artifact classes* are closely related to terms you have probably already encountered in the QIIME 2 ecosystem: semantic types, file formats, and transformers.
For most of the new QIIME 2 developers who I've worked with, defining a new artifact class (and the associated semantic type, file format(s), and transformer(s)) is the most obscure step.
However it's what gives QIIME 2 a lot of its power (for example, its ability to be accessed through different interfaces and to help users avoid analytic errors) and flexibility (for example, its ability to load the same artifact into different data types, depending on what you want to do with it).

[Recall that when we initially built our `nw-align` method](suboptimal-initial-types), we used artifact classes that were suboptimal because there weren't relevant existing ones.
Two questions may arise here.
First, how do we know what relevant artifact classes are available for us to use in our development environment?
And second, how do we add one or more new artifact classes if we determine there are no relevant ones?

We'll start here with a brief *explanation* to help address the first question, and then we'll get back to our plugin *tutorial*.
For a longer explanation, see [](types-of-types).

(add-artifact-class-commit)=
```{admonition} tl;dr
:class: tip
The complete code that I developed to define my new artifact class, including the corresponding semantic type, file formats, and transformer, can be found [here](https://github.com/caporaso-lab/q2-dwq2/pull/6/commits/e183b1630be81517689ce7539476e30ffa0ecfd9).
The code that I developed to transition my `nw-align` action to use my new artifact class can be found [here](https://github.com/caporaso-lab/q2-dwq2/pull/6/commits/33b039c66995321ddd0ab245581b37e62b9080e5).
```

## Defining artifact classes

To facilitate this discussion, I'm going to begin by defining the term {term}`Artifact class`.
An artifact class defines a type of QIIME 2 artifact that can exist.
A given artifact class is defined by a plugin developer by associated a {term}`semantic type` with a file format.

The semantic type defines the meaning of the data - i.e., what it is.
For example, QIIME 2 defines a `Phylogeny[Rooted]` artifact class, and the semantic type associated with the artifact class is `Phylogeny` (i.e., a phylogenetic tree) with a sub-semantic-type `Rooted` (i.e., implying that the phylogenetic tree contains a specific root node).
Together, therefore, the `Phylogeny[Rooted]` artifact class can be described as a rooted phylogenetic tree.

The file format is independent of the semantic type, and describes how the data will be represented inside the artifact, where it will be serialized (i.e., generally meaning written to file, in this context) for storage on disk.
Multiple different file formats have been defined to represent a rooted phylogenetic tree, including newick and NEXUS, and this is typical for most types of information in bioinformatics (and other fields).
Similarly, a single file format can be used to store semantically different information - for example, newick can also be used to store unrooted phylogenetic trees.
So, the semantic type generally doesn't imply a specific file format, and a file format generally doesn't imply a specific semantic type.

When an artifact class is defined by a developer, they associate a semantic type (the meaning of the data) with a representation that will be used on disk (the file format).
This enables QIIME 2 to know how to read and write an artifact of that class, and to determine where it can be used.

Transformers, which we'll come back to later, can be associated with file formats and used to convert (transform) between file formats.
Transformers enable a given artifact class to update its format in new versions of QIIME 2, for example if a more efficient format becomes available, without end-users needing to know that anything changed.

## Discovering artifact classes

The main way that plugin developers become aware of artifact classes that are relevant for their plugin is through familiarity from using QIIME 2.
For example, if you're planning to add a new method for feature table normalization, you may know that you start with the same feature table artifact class that is used by the `rarefy` action in the `q2-feature-table` plugin.
That gives you a lead on the artifact class you're going to use.

On the other hand, if you're searching to see what artifact classes are available, the best approach right now is to call `qiime tools list-types`.
This lists the artifact classes that are available.
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
As of this writing (April 2024) you'll see many semantic types that don't have descriptions.
The ability to add descriptions was added relatively recently, and we're working through existing types to add descriptions now.
```

Some of these are self-explanatory...

**This section is incomplete**

## Developing a new Artifact Class

**This section is incomplete**
