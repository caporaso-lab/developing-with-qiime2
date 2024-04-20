# Glossary

```{glossary}
Action
  A generic term to describe a concrete {term}`method`, {term}`visualizer`, or {term}`pipeline`.
  Actions accept parameters and/or files ({term}`artifacts <Artifact>` or {term}`metadata`) as input, and generate some kind of output.

Archive
  The directory structure of a QIIME 2 {term}`Result`.
  Contains *at least* a root directory (named by {term}`UUID`) and a ``VERSION`` file within that directory.

Artifact
  A QIIME 2 {term}`Result` that contains data to operate on.

Artifact class
  A kind of {term}`Artifact` that can exist.
  This is defined by a plugin developer by associating a {term}`semantic type` with a {term}`directory format` when registering an artifact class.

Artifact API
  See {term}`Python 3 API`.

Conda metapackage
  > A metapackage is a package  with no  files,  only  metadata.
  > They are typically used to collect several packages together into a single package via dependencies.
  > ([source](https://docs.conda.io/projects/conda-build/en/stable/resources/commands/conda-metapackage.html))

Deployment
  An installation of QIIME 2 as well as zero-or-more {term}`interfaces <Interface>` and {term}`plugins <Plugin>`.
  The collection of interfaces and plugins in a deployment can be defined by a {term}`distribution` of QIIME 2.

Directory Format
  An object that is a subclass of `qiime2.plugin.DirectoryFormat`.
  A Directory Format represents a particular layout of a directory that contains files and/or arbitrarily nested sub-directories, and defines how the contents must be structured.

Distribution
  A collection of QIIME 2 plugins that are installed together through a single {term}`conda metapackage`.
  These are generally grouped by a theme. For example, the *amplicon distribution* provides a collection of plugins for analysis of microbiome amplicon data, while the *metagenome distribution* provides a collection of plugins for analysis of microbiome shotgun metagenomics data.
  When a distribution is installed, that particular installation of QIIME 2 is an example of a {term}`deployment`.

File Format
  An object which subclasses either `qiime2.plugin.TextFileFormat` or `qiime2.plugin.BinaryFileFormat`.
  File formats define the particular format of a file, and define a process for validating the format.

Format
  See {term}`file format` and {term}`directory format`.

Framework
  The engine of orchestration that enables QIIME 2 to function together as a cohesive unit.

Galaxy
  [Galaxy](https://usegalaxy.org) is a browser-based graphical interface used to access bioinformatics (and other data science tools) without having to write command line or other code. QIIME 2 provides a Galaxy interface to support access to plugins through a web browser.

Identifier
  A unique value that denotes an individual sample or feature.

Identity
  Distinguishes a piece of data.
  QIIME 2 does not consider a rename (like UNIX ``mv``) to change identity, however re-running a command, would change identity.

Input
  Data provided to an {term}`action`. Can be an {term}`artifact` or {term}`metadata`.

Interface
  A user-interface responsible for coordinating user-specified intent into {term}`framework`-driven action.

Metadata
  Columnar data for annotating additional values to existing data. Operates along Sample IDs or Feature IDs.

Method
  A method accepts some combination of QIIME 2 {term}`artifacts <Artifact>` and {term}`parameters <Parameter>` as {term}`input`, and produces one or more QIIME 2 artifacts as {term}`output`.

Output
  Objects returned by an {term}`action`. Can be {term}`artifact(s) <Artifact>` or {term}`visualization(s) <Visualization>`.

Pairwise sequence alignment
  1. (noun) A hypothesis about which positions in a pair of biological sequences (i.e., a DNA, RNA, or protein sequence) were derived from a common ancestral sequence position.
  2. (verb) The process of generating a pairwise sequence alignment (noun).
  For additional detail, see the *Pairwise Sequence Alignment* chapter of [*An Introduction to Applied Bioinformatics*](https://readiab.org) {cite}`iab-2`.

Parameter
  A value that alters the behavior of an {term}`action`.

Payload
  Data that is meant for primary consumption or interpretation (in contrast to *metadata* which may be useful retrospectively, but is not primarily useful).

Pipeline
  A pipeline accepts some combination of QIIME 2 {term}`artifacts <Artifact>` and {term}`parameters <Parameter>` as {term}`input`, and produces one or more QIIME 2 {term}`artifacts <Artifact>` and/or {term}`visualizations <Visualization>` as {term}`output`.

Plugin
  A discrete module that registers some form of additional functionality with the {term}`framework`, including new {term}`methods <Method>`, {term}`visualizers <Visualizer>`, {term}`formats <Format>`, or {term}`transformers <Transformer>`.

Primitive Type
  A {term}`type` that is used to communicate parameters to an {term}`interface`.  These are predefined by the {term}`framework` and cannot be extended.

Provenance
  In the context of QIIME 2, provenance or data provenance refers to the history of how a given {term}`result` was generated.
  Provenance information describes the host system, the computing environment, Actions performed, parameters passed, primary sources cited, and more.

Provenance Replay
  The QIIME 2 functionality that enables new executable code to be generated from an existing QIIME 2 {term}`result's <Result>` {term}`provenance`.
  For additional detail, refer to {cite}`Keefe2023-oy`.

Python 3 API
  When *the Python 3 API* is referred to in the context of QIIME 2, this refers to the interface that allows users to work with QIIME 2 plugins and actions natively in Python 3 (for example in a Jupyter Notebook environment). This was formerly referred to as the Artifact API.

q2cli
  [q2cli](https://github.com/qiime2/q2cli) is the original (and still primary, as of March 2024) command line interface for QIIME 2.

Result
  A generic term for either a {term}`Visualization` or an {term}`Artifact`.

Semantic Type
  An identifier that is used to describe what some data is intended to represent, and when and where they can be used.
  When associated with a {term}`directory format`, the combination defines an {term}`artifact class`.
  These types may be extended by {term}`plugins<Plugin>`.

tl;dr
  "Too long; didn't read."
  In other words, a quick summary of the content that follows.

Transformer
  A function registered on the {term}`framework` capable of converting data in one {term}`format` into data of another {term}`format`.

Type
  A term that is used to represent several different ideas in QIIME 2, and which is therefore ambiguous when used on its own.
  More specific terms are *file type*, *semantic type*, and *data type*. See [](types-of-types) for more information.

UUID
  Universally Unique IDentifier, in the context of QIIME 2, almost certainly refers to a *Version 4* UUID, which is a randomly generated ID.
  See this [RFC](https://tools.ietf.org/html/rfc4122) or this [wikipedia entry](https://en.wikipedia.org/wiki/Universally_unique_identifier) for details.

View
  A particular representation of data. This includes on-disk formats and in-memory data structures (objects).

Visualization
  A QIIME 2 {term}`Result` that contains an interactive visualization.

Visualization (Type)
  The {term}`type` of a {term}`visualization`.
  There are no subtyping relations between this type and any other (it is a singleton) and cannot be extended (because it is a singleton).

Visualizer
  A visualizer accepts some combination of QIIME 2 {term}`artifacts <Artifact>` and {term}`parameters <Parameter>` as {term}`input`, and produces exactly one {term}`visualization` as {term}`output`.
```
