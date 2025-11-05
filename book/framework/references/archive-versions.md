(archive-versions)=
# Archive versions
The structure of QIIME 2 {term}`archives<Archive>` has evolved as QIIME 2 has been developed.
This section describes each historical version of the QIIME 2 Archive format, and may be useful to interface developers whose code depends on guarantees made by that format ([source code](https://github.com/qiime2/qiime2/blob/master/qiime2/core/archive/)).


## Version-agnostic format guarantees

Though there is significant variability in the format of QIIME 2 Archives across archive versions, all archive versions share some common traits.

These shared characteristics, defined in the `_Archive` class in [`qiime2/core/archive/archiver.py`](https://github.com/qiime2/qiime2/blob/master/qiime2/core/archive/archiver.py), must be consistent across all formats over time as they allow archive versions to be checked, and archives with different formats to be dispatched to the appropriate version-specific parsers.

All QIIME 2 Archives have:
- a directory named with the Archive UUID, directly under the archive root at `/<UUID>/`, and
- a file `/<UUID>/VERSION` within that directory, formatted as shown below.

{numref}`format-agnostic-archive-structure` illustrates the Archive file system.

```{figure} ../images/format-agnostic-archive-structure.svg
:name: format-agnostic-archive-structure
Box and arrow diagram of the guaranteed components of an archive.
```

The VERSION file format is described [above](archive-version-file).

(archive-version-0)=
## Archive Version 0

Version 0 was the original QIIME 2 Archive format, and there aren't many V0 Archives "in the wild".
V0 Archives were produced by alpha versions of the QIIME 2 framework, and were superseded in framework version 2.0.6 on 24 October 2016.

- {term}`Result` data files are written in the directory `/<UUID>/data`
- Result UUID, semantic type, and format information are saved in `/<UUID>/metadata.yaml`.
- The `ArchiveFormat` class in [`v0.py`](https://github.com/qiime2/qiime2/blob/master/qiime2/core/archive/format/v0.py) offers convenience methods for loading and parsing `metadata.yaml` files.

{numref}`v0-archive-format` illustrates the format of a Version 0 Archive.

```{figure} ../images/v0-archive-format.svg
:name: v0-archive-format

Box and arrow diagram of a v0 archive.
```

(archive-version-1)=
## Archive Version 1

Released in QIIME 2 [version 2.0.6](https://github.com/qiime2/qiime2/releases/tag/2.0.6), [commit `bdc8aed`](https://github.com/qiime2/qiime2/commit/bdc8aed08a7ce323a0f9901c6ff634680e58c7f3), Version 1 Archives introduce decentralized provenance tracking to QIIME 2.
[ArchiveFormat V1](https://github.com/qiime2/qiime2/blob/master/qiime2/core/archive/format/v1.py) inherits all traits of v0, modifying its `__init__()` and `write()` methods only to add provenance capture.

```{note}
All `ArchiveFormat` versions subclass their predecessor.
For example, the `ArchiveFormat` in `v1.py` inherits from the `ArchiveFormat` in `v0.py`, etc.
This makes it easier for humans to interpret the version history.
```

Provenance data is stored in the directory `/<UUID>/provenance/`.
Specifically, `metadata.yaml`, `action.yaml` and `VERSION` files are captured for the current Result and each of its ancestors.
Each Result's `action.yaml` file and associated data artifacts (e.g. sample metadata) are stored in an `action` directory alongside that Result's `VERSION` and `metadata.yaml`.
Considered together, we can describe these as "provenance files".
This structure is illustrated in {numref}`v1-archive-provenance-format`.

```{figure} ../images/v1-archive-provenance-format.svg
:name: v1-archive-provenance-format

Box and arrow diagram of the provenance files in a v1 archive.
The blue "multiple files" icon represents all provenance files associated with a single action (e.g. the current action, or one of its ancestors).
```

The structure of V1 Archives as a whole is illustrated in {numref}`v1-v4-archive-format`.

```{figure} ../images/v1-v4-archive-format.svg
:name: v1-v4-archive-format
Box and arrow diagram of a v1 archive.

Provenance files for the current Result are stored in `/<UUID>/provenance/`.
Provenance files for each ancestor Result are stored in directory at `/<root_UUID>/provenance/artifacts/<ancestor_UUID>/`.
```

```{note}
V0 Archives do not capture provenance data. As a result, if a V0 artifact is an ancestor to a V1 (or greater) artifact, it is possible for the `action.yaml` to list Artifact UUIDs which are not present in the `artifacts` directory.
```

(archive-version-2)=
## Archive Version 2
Released across QIIME 2 versions [2017.9](https://github.com/qiime2/qiime2/releases/tag/2017.9.0) ([changelog](https://forum.qiime2.org/t/qiime-2-2017-9-release-is-now-live/1160)) and [2017.10](https://github.com/qiime2/qiime2/releases/tag/2017.10.0) ([changelog](https://forum.qiime2.org/t/qiime-2-2017-10-release-is-now-live/1626)), the directory structure of this format is identical to v1, but the `action.yaml` file has changed.

In [commit `4389a0b`](https://github.com/qiime2/qiime2/commit/4389a0b4ec41151144188ea230c8c56c1940c368) the Version 2 `ArchiveFormat` adds an `output-name` key to the `action` section of `action.yaml` (unless the action type is `import`), assigning it the output name registered to the relevant action.
Prior to this change, if one action returned multiple artifacts of the same {term}`artifact class`, it was not possible to differentiate between them using provenance alone.

In [commit `e072706`](https://github.com/qiime2/qiime2/commit/e07270659bd4089afdeef744868f8b7ac9c698a9), it adds provenance support for {term}`Pipelines <Pipeline>`, adding the `alias-of` key to the `action` section of `action.yaml`.

(archive-version-3)=
## Archive Version 3
Released in QIIME 2 version [2017.12](https://github.com/qiime2/qiime2/releases/tag/2017.12.0) ([changelog](https://forum.qiime2.org/t/qiime-2-2017-12-release-is-now-live/2308)), [commit `684b8b7`](https://github.com/qiime2/qiime2/commit/684b8b77276bd8fc7228042c674a166669bb5bef), the directory structure of this format is identical to v1 and v2.

With this release, QIIME 2 Actions are able to take variadic arguments, allowing users to pass collections of Artifacts (`List`s and `Set`s).
A YAML representer has been added so that `action.yaml` can represent `Set`s of Artifact inputs.
These will show up in `action.yaml` as custom `!set` tags.

(archive-version-4)=
## Archive Version 4
Released in QIIME 2 version [2018.4](https://github.com/qiime2/qiime2/releases/tag/2018.4.0) ([changelog](https://forum.qiime2.org/t/qiime-2-2018-4-release-is-now-live/3946)), [commit `00a294c`](https://github.com/qiime2/qiime2/commit/00a294cbfc8737c1a2f57d695615098dc9beb4ad), this format adds citations to the directory format, adds a `transformers` section to `action.yaml`, and aligns the structure of `environment:framework` (also in `action.yaml`) to match the structure of `environment::plugins::<some_plugin>`.

Whenever an `Action` is run, its registered citations are captured.
When saved, they are written to a `citations.bib` file inside the Archive's `provenance` directory.
Citations for all of the current Result's ancestors are stored in their respective <UUID> directories (e.g. `/<root_UUID>/provenance/artifacts/<ancestor_UUID>/citations.bib`).

```{figure} ../images/v4-archive-provenance-format.svg
:name: v4-archive-provenance-format
Box and arrow diagram of the provenance files in a v4 archive.
```

The overall directory structure remains identical to a v1 archive ({numref}`v1-archive-provenance-format`).

Result-specific citation tags are also written to the `transformers` and `environment` sections of the `action.yaml` files, for the current Result and for all ancestors with registered citations.
A new custom `!cite '<citation key>'` tag is use to support this in YAML.

A `transformers` section is added between the `action` and `environment` sections of `action.yaml`.
Because Pipelines do not use transformers, transformers will be recorded only for {term}`Methods <Method>`, {term}`Visualizers <Visualizer>`, and when importing data (such as with `qiime tools import`).
It looks like the following:

```yaml
transformers:
inputs:
    demultiplexed_seqs:
    -   from: SingleLanePerSamplePairedEndFastqDirFmt
        to: SingleLanePerSamplePairedEndFastqDirFmt
output:
-   from: q2_types.feature_data._transformer:DNAIterator
    to: DNASequencesDirectoryFormat
    plugin: !ref 'environment:plugins:types'
```

`environment::framework` was previously only a version string, and is now structured identically to each plugin action's `software_entry`, with version, website, and citation sections:

```yaml
framework:
    version: 2019.10.0
    website: https://qiime2.org
    citations:
    - !cite 'framework|qiime2:2019.10.0|0'
plugins:
    fragment-insertion:
        version: 2019.10.0
        website: https://github.com/qiime2/q2-fragment-insertion
        citations:
        - !cite 'plugin|fragment-insertion:2019.10.0|0'
        ...
```

(archive-version-5)=
## Archive Version 5
Released in QIIME 2 version [2018.11](https://github.com/qiime2/qiime2/releases/tag/2018.11.0) ([changelog](https://forum.qiime2.org/t/qiime-2-2018-11-release-is-now-live/6879)) [commit `f95f324`](https://github.com/qiime2/qiime2/commit/f95f3246517e8c79bdab6b000d23f801030485e2), this format version adds archive checksums to the directory structure.

A new, md5sum-formatted checksum file has been added at `/<root_UUID>/checksums.md5`, with one md5sum and one filename on each line. For a more detailed specification, see the
[QIIME 2 Pull Request #414](https://github.com/qiime2/qiime2/pull/414).

`checksums.md` looks like the following:

```yaml
5a7118c14fd1bacc957ddf01e61491b7  VERSION
333fd63a2b4a102e58e364f37cd98b74  metadata.yaml
4373b96f26689f78889caeb1fbb94090  data/faith_pd-cat1.jsonp

...

7a40cff7855daffa28d4082194bdf60e  provenance/artifacts/f6105891-2c00-4886-b733-6dada99d0c81/metadata.yaml
ae0d0e26da5b84a6c0722148789c51e0  provenance/artifacts/f6105891-2c00-4886-b733-6dada99d0c81/action/action.yaml
```

{numref}`v5-archive-format` illustrates the V5 Archive.

```{figure} ../images/v5-archive-format.svg
:name: v5-archive-format
Box and arrow diagram of a v5 archive.
```

(archive-version-6)=
## Archive Version 6
Released in QIIME 2 version [2023.5](https://github.com/qiime2/qiime2/releases/tag/2023.5.1) ([changelog](https://forum.qiime2.org/t/qiime-2-2023-5-is-now-available/26579)) [commit `85f7111`](https://github.com/qiime2/qiime2/commit/85f71118c0394647779397ebf116480b9498426a), this version adds `execution_context` to the `execution` section of `action.yaml` and adds support for {term}`input`, {term}`parameter`, and {term}`output` {term}`Collections <Collection>` in `action.yaml`.

The `execution_context` goes at the bottom of the `execution` section of `action.yaml` and gives some details about how the {term}`Action` that produced this {term}`Result` was executed. It indicates whether the {term}`Action` was executed synchronously, asynchronously, or using Parsl. If Parsl was used it indicates what type of Parsl executor was used to run it. If more execution contexts are added in the future, the possibilities here may expand.
```yaml
execution:
    uuid: 8b1ddcc2-b4e7-4c9f-9338-a7785a47862e
    runtime:
        start: 2025-09-18T11:45:15.273922-07:00
        end: 2025-09-18T11:45:15.659510-07:00
        duration: 385588 microseconds
    execution_context:
        type: parsl/synchronous/asynchronous
        parsl_type: (if type is parsl) <Type of executor used>
```

Support for {term}`input`, {term}`parameter` and {term}`output` {term}`Collections <Collection>` of `key: value` pairs was also added in v6.

{term}`Input` {term}`Collections <Collection>` go under the `inputs` section of `action.yaml` and take the form of a list of yaml `key: value` pairs where the key is a given {term}`Artifact's <Artifact>` key in the {term}`Collection` and the value is its {term}`UUID`.

```yaml
action:
    type: <type>
    plugin: <plugin>
    action: <action>
    inputs:
        - <input collection name>:
            - '<key1>': <uuid1>
            - '<key2>': <uuid2>
            ...
```

{term}`Parameter` {term}`Collections <Collection>` go under the `parameters` section of `action.yaml` and are formatted identically to {term}`input` {term}`Collections <Collection>` only the values will be of whatever type the {term}`Parameter` {term}`Collection` is not {term}`UUIDs <UUID>`.

```yaml
action:
    type: <type>
    plugin: <plugin>
    action: <action>
    inputs: <inputs>
    parameters:
        - <parameter collection name>:
            - '<key1>': <value1>
            - '<key2>': <value2>
            ...
```

If a {term}`Result` is part of an {term}`Output` {term}`Collection`, the `output-name` section of its `action.yaml` will contain two additional pieces of information. The key of this {term}`Result` in the {term}`Collection`, and the index of this {term}`Result` in the {term}`Collection` of the form `x/y` where `x` is this {term}`Result's <Result>` index and `y` is the size of the {term}`Collection`.

```yaml
action:
    type: <type>
    plugin: <plugin>
    action: <action>
    inputs: <inputs>
    parameters: <parameters>
    output-name:
    - <output collection name>
    - <key of this element in the output collection>
    - <index of this element in the collection out of total elements in the collection e.g. 1/100 for the first element in a collection of 100>
```

(archive-version-7)=
## Archive Version 7
Starting with QIIME 2 version [2025.4](https://github.com/qiime2/qiime2/releases/tag/2025.4.0), QIIME 2 Archive Versions 7+ utilize semantic versioning.
What this means is each new QIIME 2 Archive Version is broken up into a major version and a minor version.
Major version updates (i.e. version 6.x -> 7.x) include a significantly different internal structure, such as new files within the zip archive.
Backwards compatibility across major versions is not guaranteed.
Minor version updates (i.e. 7.n -> 7.n+1) include minor differing internal structor and/or features/capabilities - all of which will be backwards compatible to the nearest major version (i.e. versions 7.* will all be compatible).

### Archive Version 7.0
Released in QIIME 2 version [2025.4](https://github.com/qiime2/qiime2/releases/tag/2025.4.0) ([changelog](https://forum.qiime2.org/t/qiime-2-2025-4-is-now-available/33088)) [commit `0d2c8ec`](https://github.com/qiime2/qiime2/commit/0d2c8ec7d0cb6e3b81c4ab621e78bd0df74c11a0), this version adds support for creation of {term}`Annotations <Annotation>` (of sub-type {term}`Note`) to a QIIME 2 {term}`Result`, an all-new `conda-env.yaml` file containing all environment dependencies a {term}`Result` was created from, updated checksum calculations from `md5` to `sha512`, and total file size calculation for all files within the `data` directory as a new entry under the top level/provenance level `metadata.yaml` files.

{term}`Annotations <Annotation>` are a way of attaching information to a QIIME 2 {term}`Result`.

### Archive Version 7.1
Released in QIIME 2 version [2025.10](https://github.com/qiime2/qiime2/releases/tag/2025.10.1) ([changelog](https://forum.qiime2.org/t/qiime-2-2025-10-is-now-available/33760))
[commit `7d2a9b1`](https://github.com/qiime2/qiime2/commit/7d2a9b12d98666200b370de89e9e633b33e9acb8), this version adds .

### Archive Version 7.2
Archive Version 7.2 development is currently being planned.
