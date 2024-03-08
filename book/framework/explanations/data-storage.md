(data-storage)=
# How Data is Stored

In any software project, data needs to be stored (or persisted).
The way that this is accomplished can impact every facet of the software's design.
In order to better demonstrate *why* certain aspects of QIIME 2 exist as they are we will highlight what goals or constraints QIIME 2 has, and then demonstrate how QIIME 2 achieves each goal.
This discussion will begin with a high-level summary of the topic, and then provide specific details on components of the solution. 

To skip to the details, you can follow these links:
- [](data-storage-archives)
- [](data-storage-types)
- [](data-storage-formats)
- [](data-storage-provenance)


## Goals for data storage in QIIME 2
The design of QIIME 2's approach to data storage was motivated by the following goals, which we consider to be contraints.
Data should be stored in a way that:
- is accessible long-term (e.g. 20 years), or "future-proof"
- is as convenient as possible to transfer between users
- makes it possible to determine when data is or is not valid as input for a specific analysis
- ease interoperability between tools
- can be extended by plugins
- and include details on its origin and history (provenance), facilitating trust and reproducibility. 

These goals directly impact many of the design decisions made in QIIME 2.
The solution described in this section seeks to address each of these goals.
There are many other ways to solve these problems when one or more of these constraints are lifted, however QIIME 2 chooses these constraints because we believe they are *useful* to the scientist, will allow *composable* software to be developed and reused to advance the state of the art, and support [FAIR data principles](https://www.go-fair.org/fair-principles/). 

### Accessibility and Transferability
QIIME 2 stores all data as a directory structure inside of a ZIP file.
There is a {term}`payload` directory named `/data/` where data is stored in a common format. This permits additional *metadata* to be stored alongside the data (in non-`/data/` directories or files).

A directory-based archive is used to store data in a way that is accessible. 
When a common format exists for a data type (e.g., FASTA format for sequence data) it should be used to be as accessible as possible. 
When such a format does not exist, it should be stored in plain-text structure that is as self-descriptive as possible.
The goals is that a person in 20 years might be able to glance at it, and roughly understand what the purpose of a given document is (assuming file-systems and text-based encodings still make sense in the future).

Because some common formats are paired with others, or reused multiple times to represent multiple entities (e.g. per-sample fastq files), the data that a tool needs is sometimes a *directory* of formats.
Alternatively a new format could be invented with new rules (though this would make interoperability difficult).

For these reasons, QIIME 2 stores data as a directory structure.
In particular data such as FASTA or newick will be considered the {term}`Payload` which is to be delivered to a tool.

````{margin} 
```{note}
QIIME 2's `.qza` and `.qzv` files are ZIP files with a specific internal structure.
You can open these with any standard unzip utility (e.g., WinZip, 7zip, `unzip`), even on systems that don't have QIIME 2 installed.
```
````

There is a challenge with using directory structures as a way of storing data.
Moving directory structures is inconvenient as they do not exist as a single file.
A common way to fix this is to zip a file and extract it at the destination.
This is exactly what QIIME 2 does.
ZIP files additionally have the advantage of being incredibly well supported by a *wide* array of software.
Some software manipulates ZIP files directly (often built into an operating system's graphical interface) and others use ZIP files as a backing structure (such as `.docx` and `.epub`).
Because it is so widely used, maintaining the long-term accessibility of data is much more likely.

The following sections detail more specific information about directory structure and ZIP file used in QIIME 2 `Archives`:
- [archives](data-storage-archives)
- [archive-versions](data-storage-archive-versions)


### Input Validation (Type Checking)
QIIME 2 stores a file named `metadata.yaml` alongside the `/data/` directory.
This file contains the {term}`type` of the data, which QIIME 2 can use to validate that a given ZIP file is valid input for a given {term}`action`.

Given that a QIIME 2 `Archive` provides a way to store a {term}`payload` (i.e., data) and a way to move it around, there needs to be a way to *describe* it so that the computer can determine if a given payload is valid input for a given operation.
This helps prevent user errors due to accidental misuse of the data, and allows {term}`interfaces<Interface>` to provide a more complete and rich user interface.

To accomplish this, we need data about the data, or *metadata* (in the general sense, this should not be confused with QIIME 2's sample/feature metadata).
If the {term}`payload` is placed in a *subdirectory* then we can store additional files which can contain this *metadata* without needed to worry about filename conflicts with the payload itself.
Now QIIME 2 is able to record a type and anything else that may enable the computer (or user) to make a more informed decision about the use of a given piece of data.

See [](data-storage-types) to get more information on how types are used and defined in QIIME 2. 


### Interoperability and Extension
QIIME 2 stores a string called a {term}`Directory Format` in `metadata.yaml` which instructs the computer what the specific layout of `/data/` is.
Once this is known, it is possible to convert that data into other formats.
{term}`plugins<Plugin>` can define new formats and request data in specific {term}`views<View>`.

Different tools expect different file formats or in-memory data structures.
Many of these are *semantically* compatible --- in other words, they can carry the same information but in different ways.
Another way to state this is that these different formats and data-structures each represent a different {term}`view` of the same data.

If we combine this idea with a {term}`semantic type` we are able to use the abstraction of the type to ignore the view when reasoning about composition of {term}`actions<Action>`.
While the {term}`semantic type` may be adequate for describing what data is used for, it does not provide a means to structure it (on-disk or in-memory).
For this we use a {term}`view`.
In particular, when storing data for later use (or sharing) it is necessary to save it to disk in some way (in particular, we need to store it in `/data/`).
We use a {term}`directory format` to accomplish this purpose.
Directory formats have a name that is recorded in `metadata.yaml` and defines how `/data/` is to be structured.

See [](data-storage-formats) to learn more about QIIME 2's formats and directory formats.

### Provenance Metadata

Inside of each Archive, QIIME 2 stores metadata about how that archive was generated.
We call this "provenance". Notably, each Archive contains provenance information about *every* prior QIIME 2 {term}`Action` involved in its creation, from `import` to the most recent step in the analysis.

This provenance information includes type and format information, system and environment details, the Actions performed and all parameters passed to them, and all registered citations.

See [](data-storage-provenance) to learn more about data provenance storage in QIIME 2. 

(data-storage-archives)=
## Anatomy of an Archive

QIIME 2 stores data in a directory structure called an {term}`Archive`.
These archives are zipped to make moving data simple and convenient.

The directory structure has a single root directory named with a {term}`UUID` which serves as the {term}`identity` of the archive.
Additional files and directories present in the archive are described below.

(metadata-yaml)=
### The Most Important File: `metadata.yaml`
In the root of an {term}`archive` directory, there is a file named `metadata.yaml`.
This file describes the {term}`type`, the {term}`directory format`, and repeats the {term}`identity` of a piece of data.

An example of this file:

```yaml
uuid: 45c12936-4b60-484d-bbe1-98ff96bad145
type: FeatureTable[Frequency]
format: BIOMV210DirFmt
```

It is possible for `format` to be set as `null` only when `type` is set as `Visualization` (representing a {term}`Visualization (Type)`). 
This implies that the `/data/` directory (described below) does not have a schema.

(data-goes-in-data)=
### Data Goes In `/data/`
Where data is stored, the {term}`payload` of an archive, is in an aptly named `/data/` subdirectory.
The structure of this subdirectory depends on the payload.

If the archive is a {term}`visualization`, then the payload is a (possibly interactive) visualization, which is implemented as a small static website (with an `index.html` file and any other assets).

If the archive is an {term}`artifact`, then the payload is determined by the {term}`directory format`.

(provenance-goes-in-provenance)=
### Provenance Goes In `/provenance/`
In addition to storing data, QIIME 2 stores *metadata* including what actions were performed to generate the current `Result`, what versions of QIIME 2 and other dependencies were used, and what references to cite if the data is used in a publication (for example)

As it relates to the archive structure, the `/provenance/` directory is designed to be self-contained and self-referential.
This means that it duplicates some of the information available in the root of the {term}`archive`, but this simplifies the code responsible for tracking and reading provenance.

{numref}`archive-structure` illustrates this idea.

```{figure} ../images/archive-structure.svg
:name: archive-structure

Description of the QIIME 2 archive structure.
```

Looking closely we see the previously described `/data/` directory and `metadata.yaml` file, in addition to a `VERSION` file (described below), and the `/provenance/` directory in question.

Following the provenance directory, we see that the provenance structure is repeated within the `/provenance/artifacts/` directory.
This directory contains the *ancestral provenance* of all {term}`artifacts<Artifact>` used up to this point.
Because the structure repeats itself, it is possible to create a new provenance directory by simply adding all input artifacts' `/provenance/` directories into a new `/provenance/artifacts/` directory.
Then the `/provenance/artifacts/` directories of the original inputs can be also merged together.
Because the directories are named by a {term}`UUID`, we know the {term}`identity` of each ancestor, and if seen twice, can simply be ignored.
This simplifies the problem of capturing *ancestral provenance* to one of merging uniquely named file-trees.

(why-zip)=
### Why a ZIP File?
ZIP files are a ubiquitous and well understood format.
There is a huge variety of software available to read and manipulate ZIP files.

The ZIP format additonally enables random access of files within the archive, making it possible to read data without extracting the entire contents of the ZIP file (in contrast to a linear archive like TAR).
This is very convenient if you need to, for example, pull a single file out of a large ZIP archive containing many files. 

```{note}
`qiime2.core.archive.archiver:_ZipArchive` is the structure responsible for managing the contents of a ZIP file (using `zipfile:ZipFile`).
```

(identifying-an-archive)=
### Rules for identifying an archive
Every QIIME 2 {term}`archive` has the following structure:

A root directory which is named a standard representation of a UUID (version 4), and a file within that directory named `VERSION`.

The {term}`UUID` is the {term}`identity` of the archive, while the `VERSION` file provides enough detail to determine how to parse the rest of the archive's structure.

(archive-version-file)=
Within `VERSION` the following text will be present:

````{margin}
```{note}
The `VERSION` file is intentionally not in YAML, INI, or any other common data serialization or configuration format.
This is to discourage the situation where important archive files are reformatted from YAML to another format and VERSION is updated (e.g., for consistency), breaking backwards compatibility.
```
````

```
QIIME 2
archive: <integer version>
framework: <version string>
```

`<integer version>` is the version that the archive was saved with.
This is used to identify the *schema* of the archive structure, which evolves over time to support new functionality, allowing software to dispatch appropriate parsing logic.

As a historical example, [archive version `0`](archive-version-0) had no `/provenance/` directory, as QIIME 2's provenance tracking hadn't yet been implemented. 
The archive version `0` parser therefore doens't look for the `/provenance/` directory.
This particular case would be easy enough to check for at runtime, but this versioning scheme allows for more complex differences between archive versions while ensuring that QIIME 2 will always be able to interpret older archives. 

```{note}
These rules are encoded in `qiime2.core.archive.archiver:_Archive`.
```

The different versions of QIIME 2 Archive Formats are detailed in [](archive-versions).
