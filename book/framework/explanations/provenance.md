(provenance-explanation)=
# Decentralized retrospective provenance tracking

QIIME 2 provides automatic, integrated, and decentralized tracking of analysis metadata, including information about the host system, the computing environment, Actions performed, parameters passed, primary sources cited, and more {cite}`Keefe2023-oy`.
We describe all of this information about *how an analysis was performed to produce a result* as the result's **provenance**.

The notion of a QIIME 2 {term}`Result` is central here.
Whenever an {term}`Action` is performed on some data with QIIME 2, the framework captures relevant metadata about the action and environment in a {term}`Result` object, which is backed by an {term}`Archive`.
If that Result is saved as a `.qza` or `.qzv`, the captured provenance data persists within that zip archive.
[](provenance-goes-in-provenance) contains a detailed discussion of the file structure which holds provenance metadata.

This is a **decentralized** approach to provenance capture: every QIIME 2 Result's provenance is packaged with the Result itself.
This prevents disassociation of a Result with its provenance, for example when a simpler analysis outcome (e.g., a `.png` file containing a graph) is emailed to a colleague.
It also prevents accidental mis-association of a Result with the wrong provenance, or with inaccurate or outdated provenance records.
For example, with *centralized approaches to provenance tracking*, like saving scripts or computational notebooks, those records may be updated.
If a result was generated prior to a script update, and the result is inadvertantly not updated, a subsequent user or viewer of that result may have inaccurate information about how it was created.
In contrast, the provenance captured within a QIIME 2 Archive will always describe the way that Archive was actually created.

QIIME 2's approach is also a form of **retrospective** provenance capture.
With a *prospective* provenance capture approach, a script, work plan, or computational notebook are used to document what will be done.
Referring to the example from the previous paragraph, if the script is updated but not run to recreate a result of interest (e.g., because an older version of the result was already shared with a colleague, and they forget to download the new version) the script won't accurately represent the provenance of that result, and it will be hard or impossible to discover that.
Retrospective provenance, on the other hand, is captured when the result is generated, and therefore documents what *actually occurred*, supporting a more reliable recording of an analysis.

```{note}
*When and if* `Results` are saved as `.qza` or `.qzv` ZIP archives is dependent on the interface that is being used to run QIIME 2.
For example, results are saved automatically by `q2cli` (QIIME 2's command line interface) every time a user runs a command.
Results must be saved manually by users of the [Python 3 API](https://docs.qiime2.org/2021.4/interfaces/artifact-api/), if they want a `.qza` or `.qzv` ZIP archives (but importantly, provenance will be complete even if some intermediate results are not saved).
This allows API users to reduce I/O, and keeps things simpler for CLI users.
```

## Why Capture Provenance Data?

QIIME 2's provenance capture gives users, developers, support teams, manuscript reviewers, and research consummers valuable tools for documentation, study validation and reproduction, analysis transparancy, software maintenance and repair, and technical support.

Among the benefits of this model are:

- Analyses are fully reproducible.
- Analyses self-document, reducing the reliance on the (possibly incomplete or incomprehensible) notes of the individual who ran the analysis.
  For example, q2view produces directed provenance graphs, [like this one](https://view.qiime2.org/provenance/?src=https%3A%2F%2Fdocs.qiime2.org%2F2021.4%2Fdata%2Ftutorials%2Fmoving-pictures%2Fcore-metrics-results%2Funweighted_unifrac_emperor.qzv), that allow any consummer of that result to understand exactly how it was created.
- QIIME 2 Artifacts bring their citations with them.
- Methods-section text could theoretically be generated from a collection of QIIME 2 Artifacts. (If you're interested in contributing that functionality, please feel free to get in touch - large language models (LLMs) should make this easier than ever!)
- Analyses are automatically replay-able {cite}`Keefe2023-oy`, meaning that you can generate new code from existing results.
- In the unlikely event of a data integrity bug, problematic combinations of hardware, environment, `Action`s, and parameters can be investigated effectively by users, developers, or technical support providers.
  Impacted results can be programatically identified, and could be programatically correctable in some cases.
- By capturing provenance metadata at the level of Actions and Results, QIIME 2 provenance is both host- and interface-agnostic.
  In other words, a QIIME 2 analysis can be performed across various host systems, using whatever interfaces the user prefers, without compromising the validity of the analysis or the provenance. The `Result` of every step in the analysis contains its own unique history.

## What Provenance Data is Captured?

In order to focus on provenance data, we will consider a relatively simple example QIIME 2 Archive structure, with limited non-provenance content.
In {numref}`whole-archive` the outer {term}`UUID` directory of this {term}`Artifact` holds the data it produced in a `data` directory (see [](data-goes-in-data)), and a few "clerical" files (see [](archive-anatomy)).
Here we focus on the `provenance/` directory.

````{margin}
```{note}
Importantly, the *data* from the parent Results are not included in the current Result's provenance: only their provenance *metadata*.
Including their data would result in massive file sizes and duplication of data.
```
````

```{figure} ../images/whole-archive.svg
:name: whole-archive
:alt: Simplified representation of the files within one Archive, emphasizing how an Archive holds provenance for an arbitrary number of Actions.

Simplified representation of the files within one Archive.
```


In {numref}`whole-archive`, we use a blue "multiple-files" icon to represent the collection of provenance data associated with one single QIIME 2 action.
When this icon appears directly within `provenance/` the files describe the "current" {term}`Result`.
All remaining icons appear within the `artifacts/` subdirectory.
These file collections describe all "parent" Results used in the creation of the current Result, and are housed in directories named with their respective UUIDs.

```{figure} ../images/provenance-files.svg
:name: provenance-files
:alt: A detail indicating how we abbreviate one action's provenance records with a single "multiple-files" icon.

A detail indicating how we abbreviate one action's provenance records in {numref}`whole-archive`.
```

With the exception of the current Result (whose provenance lives in `provenance/`, every Action is captured in a directory titled with the Action's {term}`UUID` {numref}`provenance-files`.


That directory contains:
- `VERSION` (see [](identifying-an-archive))
- `metadata.yaml` (see [](metadata-yaml))
- `citations.bib`: All citations related to the run Action, in [bibtex format](https://www.bibtex.com/g/bibtex-format/).
  (This includes "passthrough" citations like those registered to transformers, regardless of the plugin where they are registered.)
- `action/action.yaml`: A YAML description of the Action and its environment (i.e., the stuff we care most about).
- `action/metadata.tsv` or other data files (optional): Data captured to provide additional Action context.

### The `action.yaml` file

Here we'll do a deep dive into the contents of a sample Visualization's `action.yaml`.
The `action.yaml` files are broken into three top-level sections, in this order:
- `execution`: the Execution ID and runtime of the Action that created this Result
- `action`: Action type, plugin, action, inputs, parameters, etc.
- `environment`: a description of the system and the Python environment where this action was executed

The sample Visualization we're referring to can be viewed [here](https://view.qiime2.org/provenance/?src=https%3A%2F%2Fdocs.qiime2.org%2F2021.4%2Fdata%2Ftutorials%2Fmoving-pictures%2Fcore-metrics-results%2Funweighted_unifrac_emperor.qzv).
That link will open directly to the *Provenance* tab where you can click on the bottom square in that provenance graph (not the circle within the square!) to cross-reference the information provided here.

#### The `execution` block

High-level information about this action and its run time.

```yaml
execution:
    uuid: 3611a0c1-e5c5-4308-ac92-ebb5968ebafb
    runtime:
        start: 2021-04-21T14:42:16.469998-07:00
        end: 2021-04-21T14:42:21.080381-07:00
        duration: 4 seconds, and 610383 microseconds
```

- Datetimes are formatted as [ISO 8601 timestamps](https://docs.python.org/3/library/datetime.html#datetime.datetime.isoformat).
- The `uuid` field captured here is a UUID V4 representing this *Execution*, and *not the Result* it produced.

(unique-ids)=
```{admonition} Unique IDs
:class: note

There are many elements of provenance that require unique IDs, to help us keep track of different aspects of an analysis.
Archive provenance has separate Result and Execution IDs (the UUIDs in `metadata.yaml` and `action.yaml` respectively).
This allows us to manage the common case where one Action produces multiple Results.

Artifacts produced by QIIME 2 Pipelines have an additional `alias-of` UUID, allowing interfaces to display provenance in terms of Pipelines (rather than displaying all of the pipeline's "nested" inner Actions).
This enables a view of provenance that better reflects the user experience of pipelines, displaying them as single blocks, rather than as the full chain of inner Actions which the user generally does not specify directly.

Terminal pipeline Results are redundant "aliases" of "real" Results nested within the pipeline.
The `alias-of` UUID in the terminal/"alias" Result points to this "real" inner result.
Further details are provided in [](pipeline-provenance).

The `unweighted_unifrac_emperor.qzv` described here has three different IDs:

- The Result UUID, in `metadata.yaml`, which is unique to this Result.
- The Execution UUID, in `action.yaml`'s `execution` block, which is unique to this Action's current execution, and present in all Archives produced during this Actions's current execution.
  All Results from a given run of an `Action` (`core-metrics-phylogenetic`, in our current example) share this ID.
- The `alias-of` UUID, in `action.yaml`'s `action` block, which is the Result UUID of the "inner" Visualization created during a `Pipeline` execution that is aliased by this Result.
  (Remember that a {term}`Pipeline` is a type of {term}`Action`.)

We chose to use [v4 UUIDs](https://docs.python.org/3/library/uuid.html) for our unique IDs,
but there is nothing special about them that couldn't be handled by a different unique identifier scheme.
They're just IDs.
```

(action-block)=
#### The `action` block

Details about the action, including action and plugin names, inputs and parameters

```yaml
action:
    type: pipeline
    plugin: !ref 'environment:plugins:diversity'
    action: core_metrics_phylogenetic
    inputs:
    -   table: 34b07e56-27a5-4f03-ae57-ff427b50aaa1
    -   phylogeny: a10d5d44-62c7-4322-afbe-c9811bcaa3e6
    parameters:
    -   sampling_depth: 1103
    -   metadata: !metadata 'metadata.tsv'
    -   n_jobs_or_threads: 1
    output-name: unweighted_unifrac_emperor
    alias-of: 2adb9f00-a692-411d-8dd3-a6d07fc80a01
```

- The `type` field describes the *type of the Action*: a {term}`Method`, {term}`Visualizer`, or {term}`Pipeline`.
- The `plugin` field describes the plugin which registered the Action, details about which can be found in `action.yaml`'s `environment:plugins` section.
  `!ref` is a custom YAML tag defined [here](https://github.com/qiime2/qiime2/blob/6d8932eda130d4a9356f977fece2e252c135d0b9/qiime2/core/archive/provenance.py#L84).
  Generally, these custom tags provide a way to express a structure not easily described by basic YAML.
- `inputs` lists the registered names of all {term}`inputs<Input>` to the Action, as well as the UUIDs of the passed inputs.
  Note the distinction between inputs and parameters.
- `parameters` lists registered parameter names, and the user-passed (or selected default) values.
- `output-name` is the name assigned to this Action's output *at registration*, which can be useful when determining which of an Action's multiple outputs a file represents.
  (This does not capture the user-passed filename, because file names are interface specific and may not always be relevent - for example, when using the Python API, files may not exist for inputs at the time of action execution.)
- `alias-of` is an optional field, present if the Action is the terminal result of a QIIME 2 {term}`Pipeline`.
  This value is the UUID of the "inner" result which this pipeline result aliases.

#### The `environment` block

The environment block is a description of the computing environment in which this Action was run.
It is not uncommon for QIIME 2 analyses to be run through multiple user interfaces, on multiple systems.
For this reason, per-Action logging of system characteristics is useful.

- `platform`: The operating system and version used to run the Action.
   For virtual machines (VMs), this is the client Operating System.
- `python`: python version details, as captured by `sys.version`.
- `framework`: Details about the QIIME 2 version used to perform this Action.
- `plugin`: The QIIME 2 plugin, its version, and registered source web site.
- `python-packages`: Package names and version numbers for all packages in the global `working_set` of the active Python distribution, as collected by [pkg_resources](https://setuptools.readthedocs.io/en/latest/pkg_resources.html#workingset-objects).

```{warning}
QIIME 2 currently captures only Python package information in the environment block, and therefore doesn't collect complete information about the environment.
We plan to expand this to include all relevant packages in the environment regardless of language.
See [GitHub issue #587](http://github.com/qiime2/qiime2/issues/587) if you are interested in contributing to this effort.
```

```yaml
environment:
    platform: macosx-10.9-x86_64
    python: |-
        3.8.8 | packaged by conda-forge | (default, Feb 20 2021, 16:12:38)
        [Clang 11.0.1 ]
    framework:
        version: 2021.4.0
        website: https://qiime2.org
        citations:
        - !cite 'framework|qiime2:2021.4.0|0'
    plugins:
        diversity:
            version: 2021.4.0
            website: https://github.com/qiime2/q2-diversity
    python-packages:
        zipp: 3.4.1
        xopen: 1.1.0

        ...

        q2-dada2: 2021.4.0
        q2-composition: 2021.4.0
        q2-alignment: 2021.4.0

        ...

        alabaster: 0.7.12
```

(pipeline-provenance)=
### Pipeline Provenance

As discussed in [the Unique IDs note above](unique-ids), {term}`Pipeline` provenance is more complex than the provenance of other Actions.
Most Pipelines wrap one or more {term}`Methods<Method>` or {term}`Visualizers<Visualizer>`.
Pipeline users are often concerned primarily with ease of use and interpretation, rather than the fine-grained details of the Actions "nested" within the Pipeline.
With this in mind, provenance viewing interfaces may choose to abstract away nested Actions, displaying only the Pipeline used to run those Actions.

QIIME 2 View works in this way, and the simple graph shown in our [provenance example](https://view.qiime2.org/provenance/?src=https%3A%2F%2Fdocs.qiime2.org%2F2021.4%2Fdata%2Ftutorials%2Fmoving-pictures%2Fcore-metrics-results%2Funweighted_unifrac_emperor.qzv) is the result of hiding ten nested Actions from view behind the two pipelines that use them.
The user sees only five of the fifteen captured Results, each of which they ran themselves.
Because the bottom two are pipelines, this view simply but completely represents the provenance of the Archive being viewed.

This is possible because QIIME 2 captures redundant "terminal" pipeline outputs that alias the "real" pipeline outputs nested in provenance.
These terminal outputs are of the same {term}`artifact class` as the Results they alias, but capture provenance details at the scope of the Pipeline, rather than at the scope of the Method or Visualizer they alias.

#### Pipeline provenance example

This Artifact's root-level `metadata.yaml`, which can be accessed by clicking the circle within the bottom box of our [example provenance DAG](https://view.qiime2.org/provenance/?src=https%3A%2F%2Fdocs.qiime2.org%2F2021.4%2Fdata%2Ftutorials%2Fmoving-pictures%2Fcore-metrics-results%2Funweighted_unifrac_emperor.qzv), tells us it's a Visualization:

```yaml
uuid: 87058ae3-e168-4e2f-a416-81b130d538c3
type: Visualization
format: null
```

Next, clicking on the box (rather than the circle within the box) lets us view the `action.yaml` contents.
The root-level `action.yaml` file tells us that this is the (terminal) result of a Pipeline (and not of a Visualizer).
The `inputs` are the UUIDs passed by the user to the Pipeline.
The `parameters`, too, are linked to the Pipeline, and not to the nested Visualizer.
Finally, we see the `alias-of` key, whose value is the UUID of the nested "real" Visualization aliased by this terminal output.

```yaml
action:
    type: pipeline
    plugin: !ref 'environment:plugins:diversity'
    action: core_metrics_phylogenetic
    inputs:
    -   table: 34b07e56-27a5-4f03-ae57-ff427b50aaa1
    -   phylogeny: a10d5d44-62c7-4322-afbe-c9811bcaa3e6
    parameters:
    -   sampling_depth: 1103
    -   metadata: !metadata 'metadata.tsv'
    -   n_jobs_or_threads: 1
    output-name: unweighted_unifrac_emperor
    alias-of: 2adb9f00-a692-411d-8dd3-a6d07fc80a01
```

If we were to extract this `.qzv` (e.g., by opening it with an unzip utility), we could use this `alias-of` UUID to drill down into `provenance/artifacts/2adb9.../` to find the `action.yaml` of the aliased Visualization.
There, the action type would be a `visualizer`, and the `inputs` and `parameters` would be those passed to the *Visualizer* within the Pipeline.
Notably, neither the Visualizer node shown below, nor its PCoA input, are visible in the provenance graph linked above, because they are neither inputs to nor terminal outputs from the containing `Pipeline`.


```yaml
action:
    type: visualizer
    plugin: !ref 'environment:plugins:emperor'
    action: plot
    inputs:
    -   pcoa: 93224813-ed5d-42b5-a983-cd4015db31da
    parameters:
    -   metadata: !metadata 'metadata.tsv'
    -   custom_axes: null
    -   ignore_missing_samples: false
    -   ignore_pcoa_features: false
    output-name: visualization
```

#### Pipeline provenance take-aways

- All Results used in producing an Archive are captured in that Archive's provenance, including "inner" pipeline results.
  Each Result has its own normal provenance directory.
- "Terminal" pipeline outputs are aliases, mirroring inner Actions.
- Different terminal outputs from the same pipeline will (generally) have different alias-of's, *because they are aliasing different inner nodes*.
  For example, a Visualization aliases a Visualization, while the terminal PCoA results point to the inner PCoA results, and these inner Results have different UUIDs.
- Pipelines may wrap pipelines, so an arbitrary number of levels of nesting and aliasing are possible.
  Tools that aim to work with nested provenance will likely have to traverse from the terminal node.
  The traversal algorithm is discussed [here](https://github.com/qiime2/dev-docs/pull/44#discussion_r673329452). (Want to port that content over? Get in touch!).
- Inner "nested" pipeline Results are normal Results, and may be used as inputs to other nested Actions, or may be aliased by terminal pipeline results.
  The only "special" thing happening with pipelines is the aliasing of terminal pipeline Results.