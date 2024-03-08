(data-storage)=
# How Data is Stored

In any software project, data needs to be stored (or persisted).
The way that this is accomplished can impact every facet of the software's design.
In order to better demonstrate *why* certain aspects of QIIME 2 exist as they are we will highlight what goals or constraints QIIME 2 has, and then demonstrate how QIIME 2 achieves each goal.


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

The following documents provide more detailed information about directory structure and ZIP file used in QIIME 2 `Archives`:
- [](archives)
- [](archive-versions)


### Input Validation (Type Checking)
QIIME 2 stores a file named `metadata.yaml` alongside the `/data/` directory.
This file contains the {term}`type` of the data, which QIIME 2 can use to validate that a given ZIP file is valid input for a given {term}`action`.

Given that a QIIME 2 `Archive` provides a way to store a {term}`payload` (i.e., data) and a way to move it around, there needs to be a way to *describe* it so that the computer can determine if a given payload is valid input for a given operation.
This helps prevent user errors due to accidental misuse of the data, and allows {term}`interfaces<Interface>` to provide a more complete and rich user interface.

To accomplish this, we need data about the data, or *metadata* (in the general sense, this should not be confused with QIIME 2's sample/feature metadata).
If the {term}`payload` is placed in a *subdirectory* then we can store additional files which can contain this *metadata* without needed to worry about filename conflicts with the payload itself.
Now QIIME 2 is able to record a type and anything else that may enable the computer (or user) to make a more informed decision about the use of a given piece of data.

See [](types-explanation) to get more information on how types are used and defined in QIIME 2. 

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

See [](formats-explanation) to learn more about QIIME 2's formats and directory formats.

### Provenance Metadata

Inside of each Archive, QIIME 2 stores metadata about how that archive was generated.
We call this "provenance". 
Notably, each Archive contains provenance information about *every* prior QIIME 2 {term}`Action` involved in its creation, from `import` to the most recent step in the analysis.

This provenance information includes type and format information, system and environment details, the Actions performed and all parameters passed to them, and all registered citations.

See [](provenance-explanation) to learn more about data provenance storage in QIIME 2. 

