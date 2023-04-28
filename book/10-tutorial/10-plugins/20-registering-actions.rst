Registering an Action
#####################

Once you have functions that you'd like to register as ``Actions`` (i.e., either ``Methods`` or ``Visualizers``), and you've instantiated your ``Plugin`` object, you are ready to register those functions. This will likely be done in the file where the ``Plugin`` object was instantiated, as it will use that instance (which will be referred to as ``plugin`` in the following examples).

Registering a Method
++++++++++++++++++++

First we'll register a ``Method`` by calling ``plugin.methods.register_function`` as follows:

.. code-block:: python

   from q2_types import (FeatureTable, Frequency, Phylogeny,
                         Rooted, DistanceMatrix)
   from qiime2.plugin import Str, Choices, Properties, Metadata

   import q2_diversity
   import q2_diversity._beta as beta

   plugin.methods.register_function(
       function=q2_diversity.beta_phylogenetic,
       inputs={'table': FeatureTable[Frequency],
               'phylogeny': Phylogeny[Rooted]},
       parameters={'metric': Str % Choices(beta.phylogenetic_metrics())},
       outputs=[('distance_matrix', DistanceMatrix % Properties('phylogenetic'))],
       input_descriptions={
           'table': ('The feature table containing the samples over which beta '
                     'diversity should be computed.'),
           'phylogeny': ('Phylogenetic tree containing tip identifiers that '
                         'correspond to the feature identifiers in the table. '
                         'This tree can contain tip ids that are not present in '
                         'the table, but all feature ids in the table must be '
                         'present in this tree.')
       },
       parameter_descriptions={
           'metric': 'The beta diversity metric to be computed.'
       },
       output_descriptions={'distance_matrix': 'The resulting distance matrix.'},
       name='Beta diversity (phylogenetic)',
       description=("Computes a user-specified phylogenetic beta diversity metric"
                    " for all pairs of samples in a feature table.")
   )

The values being provided are:

``function``: The function to be registered as a method.

``inputs``: A dictionary indicating the parameter name and its *semantic type*, for each input ``Artifact``. These semantic types differ from the data types that you provided in your `mypy`_ annotation of the input, as semantic types describe the data, where the data types indicate the structure of the data. The currently available semantic types can be viewed by running ``qiime tools import --show-importable-types`` (until merge of `this PR <https://github.com/qiime2/q2cli/pull/291>`_, which will improve on how this information is accessed from the command line). In the example above we're indicating that the ``table`` parameter must be a ``FeatureTable`` of ``Frequency`` (i.e. counts), and that the ``phylogeny`` parameter must be a ``Phylogeny`` that is ``Rooted``.  Notice that the keys in ``inputs`` map directly to the parameter names in ``q2_diversity.beta_phylogenetic``.

``parameters``: A dictionary indicating the parameter name and its *semantic type*, for each input ``Parameter``. These parameters are primitive values (i.e., non-``Artifacts``). In the example above, we're indicating that the ``metric`` should be a string from a specific set (in this case, the set of known phylogenetic beta diversity metrics).

``outputs``: A list of tuples indicating each output name and its semantic type.

``input_descriptions``: A dictionary containing input artifact names and their corresponding descriptions. This information is used by interfaces to instruct users how to use each specific input artifact.

``parameter_descriptions``: A dictionary containing parameter names and their corresponding descriptions. This information is used by interfaces to instruct users how to use each specific input parameter. You should not include any default parameter values in these descriptions, as these will generally be added automatically by an interface.

``output_descriptions``: A dictionary containing output artifact names and their corresponding descriptions. This information is used by interfaces to inform users what each specific output artifact will be.

``name``: A human-readable name for the ``Method``. This may be presented to users in interfaces.

``description``: A human-readable description of the ``Method``. This may be presented to users in interfaces.

Registering a Visualizer
++++++++++++++++++++++++

Registering ``Visualizers`` is the same as registering ``Methods``, with two exceptions.

First, you call ``plugin.visualizers.register_function`` to register a ``Visualizer``.

Next, you do not provide ``outputs`` or ``output_descriptions`` when making this call, as ``Visualizers``, by definition, only return a single visualization. Since the visualization output path is a required parameter, you do not include this in an ``outputs`` list (it would be the same for every ``Visualizer`` that was ever registered, so it is added automatically).

Registering ``q2_diversity.alpha_group_significance`` as a ``Visualizer`` looks like the following:

.. code-block:: python

   plugin.visualizers.register_function(
       function=q2_diversity.alpha_group_significance,
       inputs={'alpha_diversity': SampleData[AlphaDiversity]},
       parameters={'metadata': Metadata},
       input_descriptions={
           'alpha_diversity': 'Vector of alpha diversity values by sample.'
       },
       parameter_descriptions={
           'metadata': 'The sample metadata.'
       },
       name='Alpha diversity comparisons',
       description=("Visually and statistically compare groups of alpha diversity"
                    " values.")
   )

Registering a Pipeline
++++++++++++++++++++++

TODO: put a pipeline registration here
