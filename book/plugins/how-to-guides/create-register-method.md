(howto-create-register-method)=
# Create and register a Method


A `method` accepts some combination of QIIME 2 `artifacts` and parameters as input, and produces one or more QIIME 2 artifacts as output.
These output artifacts could subsequently be used as input to other QIIME 2 `methods` or `visualizers`.

## Create a function to register as a Method

A function that can be registered as a `Method` will have a Python 3 API, and the inputs and outputs for that function will be annotated with their data types using [mypy](http://mypy-lang.org/) syntax.
mypy annotation does not impact functionality (though the syntax is new to Python 3), so these can be added to existing functions in your Python 3 software project.
An example is [`q2_diversity.pcoa`](https://github.com/qiime2/q2-diversity/blob/99a0ccaaec14838b95845dbfe57f874d092b65c7/q2_diversity/_ordination.py#L23C1-L24C71), which takes an `skbio.DistanceMatrix` and an `int` as input, and produces an `skbio.OrdinationResults` as output.
The signature for this function is:

```python
def pcoa(distance_matrix: skbio.DistanceMatrix,
         number_of_dimensions: int = None) -> skbio.OrdinationResults:
```


As far as QIIME is concerned, it doesn’t matter what happens inside this function (as long as it adheres to the contract defined by the signature regarding the input and output types).
For example, `q2_diversity.pcoa` is making some calls to the `skbio` API, but it could be doing anything, including making system calls (if your plugin is wrapping a command line application), executing an R library, etc.

(howto-register-method)=
## Register the Method
Once you have a function that you’d like to register as a `Method`, and you’ve instantiated your `Plugin` object, you are ready to register that function as a `Method`.
This will likely be done in the file where the `Plugin` object was instantiated, as it will use that instance (which will be referred to as `plugin` in the following examples).

We register a `Method` by calling `plugin.methods.register_function` as follows (see the original source [here](https://github.com/qiime2/q2-diversity/blob/99a0ccaaec14838b95845dbfe57f874d092b65c7/q2_diversity/plugin_setup.py#L192)).

```python
from q2_types import DistanceMatrix, PCoAResults
from qiime2.plugin import Int, Citations

import q2_diversity


citations = Citations.load('citations.bib', package='q2_diversity')


plugin.methods.register_function(
    function=q2_diversity.pcoa,
    inputs={'distance_matrix': DistanceMatrix},
    parameters={
        'number_of_dimensions': Int % Range(1, None)
    },
    outputs=[('pcoa', PCoAResults)],
    input_descriptions={
        'distance_matrix': ('The distance matrix on which PCoA should be '
                            'computed.')
    },
    parameter_descriptions={
        'number_of_dimensions': "Dimensions to reduce the distance matrix to. "
                                "This number determines how many "
                                "eigenvectors and eigenvalues are returned,"
                                "and influences the choice of algorithm used "
                                "to compute them. "
                                "By default, uses the default "
                                "eigendecomposition method, SciPy's eigh, "
                                "which computes all eigenvectors "
                                "and eigenvalues in an exact manner. For very "
                                "large matrices, this is expected to be slow. "
                                "If a value is specified for this parameter, "
                                "then the fast, heuristic "
                                "eigendecomposition algorithm fsvd "
                                "is used, which only computes and returns the "
                                "number of dimensions specified, but suffers "
                                "some degree of accuracy loss, the magnitude "
                                "of which varies across different datasets."
    },
    output_descriptions={'pcoa': 'The resulting PCoA matrix.'},
    name='Principal Coordinate Analysis',
    description=("Apply principal coordinate analysis."),
    citations=[citations['legendrelegendre'],
               citations['halko2011']]
)
```


The values being provided are:
- `function`: The function to be registered as a method.
- `inputs`: A dictionary indicating the parameter name and its `semantic type`, for each input `Artifact`.
These semantic types differ from the data types that you provided in your `mypy`_ annotation of the input, as `semantic types` describe the data, where the data types indicate the structure of the data.
(See {ref}`(types-of-types)` for more detail on the difference between data types and semantic types.)
In the example above we’re indicating that the table parameter must be a `FeatureTable` of `Frequency` (i.e. counts), and that the `phylogeny` parameter must be a `Phylogeny` that is `Rooted`.
 Notice that the keys in inputs map directly to the parameter names in `q2_diversity.beta_phylogenetic`.
 - `parameters`: A dictionary indicating the parameter name and its semantic type, for each input Parameter.
 These parameters are primitive values (i.e., non-`Artifacts`).
 In the example above, we’re indicating that the metric should be a string from a specific set (in this case, the set of known phylogenetic beta diversity metrics).
 - `outputs`: A list of tuples indicating each output name and its semantic type.
 - `input_descriptions`: A dictionary containing input artifact names and their corresponding descriptions.
 This information is used by interfaces to instruct users how to use each specific input artifact.
 - `parameter_descriptions`: A dictionary containing parameter names and their corresponding descriptions.
 This information is used by interfaces to instruct users how to use each specific input parameter.
 You should not include any default parameter values in these descriptions, as these will generally be added automatically by an interface.
 - `output_descriptions`: A dictionary containing output artifact names and their corresponding descriptions.
 This information is used by interfaces to inform users what each specific output artifact will be.
 - `name`: A human-readable name for the Method.
 This may be presented to users in interfaces.
- `description`: A human-readable description of the Method.
This may be presented to users in interfaces.
- `citations`: A list of bibtex-formatted citations.
These are provided in a separate `citations.bib` file, loaded via the `Citations` API, and accessed here by using their bibtex indices as keys.
