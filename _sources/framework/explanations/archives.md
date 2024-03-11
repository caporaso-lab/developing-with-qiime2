(archives)=
# Anatomy of an Archive

QIIME 2 stores data in a directory structure called an {term}`Archive`.
These archives are zipped to make moving data simple and convenient.

The directory structure has a single root directory named with a {term}`UUID` which serves as the {term}`identity` of the archive.
Additional files and directories present in the archive are described below.

(metadata-yaml)=
## The Most Important File: `metadata.yaml`
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
## Data Goes In `/data/`
Where data is stored, the {term}`payload` of an archive, is in an aptly named `/data/` subdirectory.
The structure of this subdirectory depends on the payload.

If the archive is a {term}`visualization`, then the payload is a (possibly interactive) visualization, which is implemented as a small static website (with an `index.html` file and any other assets).

If the archive is an {term}`artifact`, then the payload is determined by the {term}`directory format`.

(provenance-goes-in-provenance)=
## Provenance Goes In `/provenance/`
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
## Why a ZIP File?
ZIP files are a ubiquitous and well understood format.
There is a huge variety of software available to read and manipulate ZIP files.

The ZIP format additonally enables random access of files within the archive, making it possible to read data without extracting the entire contents of the ZIP file (in contrast to a linear archive like TAR).
This is very convenient if you need to, for example, pull a single file out of a large ZIP archive containing many files. 

```{note}
`qiime2.core.archive.archiver:_ZipArchive` is the structure responsible for managing the contents of a ZIP file (using `zipfile:ZipFile`).
```

(identifying-an-archive)=
## Rules for identifying an archive
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
