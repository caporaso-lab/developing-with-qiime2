(howto-create-register-pipeline)=
# Create and register a pipeline
A `Pipeline` accepts some combination of QIIME 2 `Artifacts` and parameters as input, and produces one or more QIIME 2 artifacts and/or `Visualizations` as output.
This is accomplished by stitching together one or more `Methods` and/or `Visualizers` into a single `Pipeline`.

## Create a function to register as a Pipeline

Defining a function that can be registered as a `Pipeline` is very similar to defining one that can be registered as a `Method` with a few distinctions.

First, `Pipelines` do not use function annotations and instead receive `Artifact` objects as input and return `Artifact` and/or `Visualization` objects as output.

Second, `Pipelines` must have `ctx` as their first parameter, which provides the following API:
 - `ctx.get_action(plugin: str, action: str)`: returns a *sub-action* that can be called like a normal Artifact API call.
 - `ctx.make_artifact(type, view, view_type=None)`: this has the same behavior as `Artifact.import_data`. It is wrapped by `ctx` for pipeline book-keeping.

Let's take a look at [`q2_diversity.core_metrics`](https://github.com/qiime2/q2-diversity/blob/99a0ccaaec14838b95845dbfe57f874d092b65c7/q2_diversity/_core_metrics.py#L10) for an example of a function that we can register as a `Pipeline`:

```python
def core_metrics(ctx, table, sampling_depth, metadata, n_jobs=1):
    rarefy = ctx.get_action('feature_table', 'rarefy')
    alpha = ctx.get_action('diversity', 'alpha')
    beta = ctx.get_action('diversity', 'beta')
    pcoa = ctx.get_action('diversity', 'pcoa')
    emperor_plot = ctx.get_action('emperor', 'plot')

    results = []
    rarefied_table, = rarefy(table=table, sampling_depth=sampling_depth)
    results.append(rarefied_table)

    for metric in 'observed_otus', 'shannon', 'pielou_e':
        results += alpha(table=rarefied_table, metric=metric)

    dms = []
    for metric in 'jaccard', 'braycurtis':
        beta_results = beta(table=rarefied_table, metric=metric, n_jobs=n_jobs)
        results += beta_results
        dms += beta_results

    pcoas = []
    for dm in dms:
        pcoa_results = pcoa(distance_matrix=dm)
        results += pcoa_results
        pcoas += pcoa_results

    for pcoa in pcoas:
        results += emperor_plot(pcoa=pcoa, metadata=metadata)

    return tuple(results)
```

## Registering the Pipeline

Registering `Pipelines` is the same as registering `Methods`, with a few exceptions.

First, we register a `Pipeline` by calling `plugin.pipelines.register_function`.

Second, `visualizations` produced as an output are listed in `outputs` as a `tuple` with `Visualization` as the second value.
E.g., `('jaccard_emperor', Visualization)`.
A description of this output should be included in `output_descriptions`

Citations do not need to be added for the pipeline unless unique citations are required for the pipeline that are not appropriate for the underlying `Methods` and `Visualizers` that it calls.
Citations for these underlying actions are automatically logged in citation provenance for this pipeline.

As an example for registering a `Pipeline`, we can look at `q2_diversity.core_metrics` (find the original source [here](https://github.com/qiime2/q2-diversity/blob/99a0ccaaec14838b95845dbfe57f874d092b65c7/q2_diversity/plugin_setup.py#L494)):

```python
plugin.pipelines.register_function(
    function=q2_diversity.core_metrics,
    inputs={
        'table': FeatureTable[Frequency],
    },
    parameters={
        'sampling_depth': Int % Range(1, None),
        'metadata': Metadata,
        'n_jobs': Int % Range(0, None),
    },
    outputs=[
        ('rarefied_table', FeatureTable[Frequency]),
        ('observed_otus_vector', SampleData[AlphaDiversity]),
        ('shannon_vector', SampleData[AlphaDiversity]),
        ('evenness_vector', SampleData[AlphaDiversity]),
        ('jaccard_distance_matrix', DistanceMatrix),
        ('bray_curtis_distance_matrix', DistanceMatrix),
        ('jaccard_pcoa_results', PCoAResults),
        ('bray_curtis_pcoa_results', PCoAResults),
        ('jaccard_emperor', Visualization),
        ('bray_curtis_emperor', Visualization),
    ],
    input_descriptions={
        'table': 'The feature table containing the samples over which '
                'diversity metrics should be computed.',
    },
    parameter_descriptions={
        'sampling_depth': 'The total frequency that each sample should be '
                            'rarefied to prior to computing diversity metrics.',
        'metadata': 'The sample metadata to use in the emperor plots.',
        'n_jobs': '[beta methods only] - %s' % sklearn_n_jobs_description
    },
    output_descriptions={
        'rarefied_table': 'The resulting rarefied feature table.',
        'observed_otus_vector': 'Vector of Observed OTUs values by sample.',
        'shannon_vector': 'Vector of Shannon diversity values by sample.',
        'evenness_vector': 'Vector of Pielou\'s evenness values by sample.',
        'jaccard_distance_matrix':
            'Matrix of Jaccard distances between pairs of samples.',
        'bray_curtis_distance_matrix':
            'Matrix of Bray-Curtis distances between pairs of samples.',
        'jaccard_pcoa_results':
            'PCoA matrix computed from Jaccard distances between samples.',
        'bray_curtis_pcoa_results':
            'PCoA matrix computed from Bray-Curtis distances between samples.',
        'jaccard_emperor':
            'Emperor plot of the PCoA matrix computed from Jaccard.',
        'bray_curtis_emperor':
            'Emperor plot of the PCoA matrix computed from Bray-Curtis.',
    },
    name='Core diversity metrics (non-phylogenetic)',
    description=("Applies a collection of diversity metrics "
                "(non-phylogenetic) to a feature table.")
)
```

See the text describing [registering methods](howto-register-method) for a description of these values.