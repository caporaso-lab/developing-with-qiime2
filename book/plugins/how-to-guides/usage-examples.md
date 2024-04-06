(how-to-write-usage-examples)=
# Writing Usage Examples

```{warning}
This document is not yet formatted for *Developing with QIIME 2*.
Some links or references may not work.
If you run into issues, please let us know [here](https://github.com/caporaso-lab/developing-with-qiime2/issues/36).
```

```{eval-rst}

Congratulations! You built a plugin, and now you want people to use it.
QIIME 2 enables you to write *usage examples* that give examples of how plugin actions can be run by your users.
It uses `dependency injection <https://en.wikipedia.org/wiki/Dependency_injection>`__
to generate appropriate usage examples for any interface with a "usage driver".
You define and register each usage example once,
giving it a parameter that accepts some usage driver.
The interface that is running your usage examples will inject one or more of its drivers
into your examples, rendering interface-appropriate results. Magic!

The API is defined by `the Usage class <https://github.com/qiime2/qiime2/blob/39ac17da01e22057ff38197eb23ad6cca48f4c2e/qiime2/sdk/usage.py#L687>`_.
Individual usage drivers implement the underlying behavior of API functions according to their own needs.
As a result, the ExecutionUsage driver will attempt to execute your usage examples,
but will disregard `comment`\s because it is not a user-facing driver.
The ArtifactAPIUsage driver will include your comments as python comments
in the rendered usage example, but will not execute your example.

The API is split into two sides -
one which allows plugin developers to define usage examples,
and one which allows interface developers to write the usage drivers that make those examples go.
*In this how-to guide, we will focus exclusively on the plugin-developer facing usage example side of the API.*

**In this how-to guide, we will cover:**

* `Data factories for usage examples`_
* `Defining usage examples`_
* `Registering usage examples`_
* `Testing usage examples`_
* `Basking in the glow of success`_
* `Comments can provide context`_

Data factories for usage examples
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Because some drivers actually execute these usage examples,
there is an expectation that we provide real data for them.
Simple assignment is not possible.
Inputs and Metadata must be created by a factory function.
This allows many drivers to avoid loading data unnecessarily.
Parameter literals may be passed directly, and do not require factories.

This example shows a factory function that returns a ``FeatureTable[Frequency]``.
We use the Python 3 API to import a ``biom.Table`` of the appropriate artifact class.

.. code-block:: python

    # from q2-feature-table/examples.py
    import numpy as np
    from biom import Table

    from qiime2 import Artifact


    def ft1_factory():
        return Artifact.import_data(
            'FeatureTable[Frequency]',
            Table(np.array([[0, 1, 3], [1, 1, 2]]),
                  ['O1', 'O2'],
                  ['S1', 'S2', 'S3']))

Defining usage examples
~~~~~~~~~~~~~~~~~~~~~~~

We've created some data, now we'll define a usage example.
This is a simple python function with a single parameter (``use`` by convention).
Interfaces pass their drivers to the example through ``use`` as described in the introduction.
The methods called inside of the function are "public" (non-underscore-prefixed) methods
defined in ``qiime2.sdk.usage.Usage``.
This "Usage API" is common to all Usage drivers,
which reimplement the methods to meet their own needs.

.. code-block:: python

    # also from q2-feature-table/examples.py
    def feature_table_merge_example(use):
        feature_table1 = use.init_artifact('feature_table1', ft1_factory)
        feature_table2 = use.init_artifact('feature_table2', ft2_factory)

        merged_table, = use.action(
            use.UsageAction(plugin_id='feature_table',
                            action_id='merge'),
            use.UsageInputs(tables=[feature_table1, feature_table2]),
            use.UsageOutputNames(merged_table='merged_table'),
        )

First, we initialize two feature tables.
(``ft2_factory`` looks a lot like the ``ft1_factory`` defined above.
You'll have to use your imagination on the details.)

We then use a proxy method for invoking an action.
The action may or may not *actually* be invoked,
depending on implementation details in the usage driver.
Beyond ensuring that your example is correct and meaningful,
you don't have to worry about this.
``use.action`` to your heart's content, and let the interfaces handle their own business.

Note that ``UsageInputs`` include both QIIME 2 :term:`Inputs<input>` *and* :term:`parameters<parameter>`.
Metadata must be initialized, but primitive parameters (and collections of parameters) may be passed directly.
There are examples of this in the `identity_with_metadata_column_get_mdc <https://github.com/qiime2/qiime2/blob/39ac17da01e22057ff38197eb23ad6cca48f4c2e/qiime2/core/testing/examples.py#L178>`__
and `variadic_input_simple <https://github.com/qiime2/qiime2/blob/39ac17da01e22057ff38197eb23ad6cca48f4c2e/qiime2/core/testing/examples.py#L191>`__
examples in the framework.

Registering usage examples
~~~~~~~~~~~~~~~~~~~~~~~~~~

Like QIIME 2 :term:`Actions<action>`,
the usage examples we have defined must be registered in order to be used.

This registration occurs in ``plugin_setup.py``,
in the ``register_function`` block for the Action whose usage we are showing.

.. code-block:: python

    # from q2-feature-table/plugin_setup.py

    # we need to import the examples to use them
    from .examples import (feature_table_merge_example,
                           feature_table_merge_three_tables_example)

    plugin.methods.register_function(
        function=q2_feature_table.merge,
        inputs={'tables': List[i_table]},

        # Skipping ahead to the 'examples' keyword argument
        # Everything else here should look familiar
        ...

        examples={'basic': feature_table_merge_example,
                  'three_tables': feature_table_merge_three_tables_example},
    )

The keys in the ``examples`` dictionary serve as unique identifiers for the examples themselves.
Some drivers (e.g. q2cli) use them to label rendered examples.


Testing usage examples
~~~~~~~~~~~~~~~~~~~~~~
You might be wondering how to confirm that your examples are working.
Great question!
Support for usage example testing is available via QIIME 2's `TestPluginBase.execute_examples()`
and the `results-and-assertions` exposed by the ``UsageVariable`` class
and optionally implemented in its driver-specific subclasses.

You can test your usage examples by making artifact class and file-contents assertions
about the UsageVariables returned by ``use.action``.
These may be run by any usage driver that cares about them,
allowing both local smoke testing ("Can my examples be executed successfully?"),
and automated integration testing by interfaces like the QIIME 2 library.

Here, we assert that our results are of the expected type.

.. code-block:: python

    def observed_features_example(use):
        ft = use.init_artifact('feature_table', ft1_factory)
        # NOTE: we must unpack UsageVariables from the returned UsageOutputs
        # if we wish to use their assertion methods.
        a_div_vector, = use.action(
            use.UsageAction(plugin_id='diversity_lib',
                            action_id='observed_features'),
            use.UsageInputs(table=ft),
            use.UsageOutputNames(vector='obs_feat_vector'))

        a_div_vector.assert_output_type('SampleData[AlphaDiversity]')

If we pass the Execution driver into this function, it will execute the example,
capturing actual Results.
By testing that our output is of the correct type, we can assert the type of the output
and in the process confirm that our example runs successfully with the given test data.

The easiest way to do this is with the `execute_examples() <https://github.com/qiime2/qiime2/blob/39ac17da01e22057ff38197eb23ad6cca48f4c2e/qiime2/plugin/testing.py#L253>`_
method on ``TestPluginBase``.
Including `a test case that runs `execute_examples() <https://github.com/qiime2/q2-feature-table/blob/81852b2e4fdbe742191c9604e30a9a8cbd3aa708/q2_feature_table/tests/test_examples.py#L12>`_
in your unit tests allows you to smoke test them locally by running `unittest` or `pytest`.

**A note on scope:**

Usage assertions are intended to allow testing of usage drivers and examples,
and make it easy for developers to confirm that their *examples* work.
Dedicated unit tests provide much more flexilibity and power,
and are the preferred way to confirm that your computational *methods* work properly.

By adding the following to ``observed_features_example``,
we *could* confirm that our test data produced exactly the expected results when executed,
but this hack is clunky, because it's reaching beyond the intended use of this assertion.

.. code-block:: python

        exp = zip(sample_ids, [1, 1, 2, 2, 3])
        for id, val in exp:
            a_div_vector.assert_has_line_matching(
                path='alpha-diversity.tsv',
                expression=f'{id}\t{val}'
            )

Asserting correct behavior of QIIME 2 Actions or their underlying python functions
will probably result in cleaner and more maintainable tests
than attempting to do the same using usage examples.

Basking in the glow of success
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
Now that you've created and registered a usage example
and confirmed that it "works", let's see it in action!
We'll pretend that we just wrote the ``q2-feature-table`` usage examples above.

1. Make sure your changes are present in the conda environment.
   ``q2-feature-table`` is already installed in my QIIME 2 environment,
   but the version in the environment came from the latest release, not my code.
   To include my current changes, I can reinstall by running ``pip install -e .``
   from within the repository's root directory.
2. Confirm my environment is using the right version.
   Before re-installing, I called ``conda list q2-feature-table``
   to check what version of ``q2-feature-table`` was installed.
   Re-running that command now, I see the version has changed,
   indicating that my conda environment knows about the changes I made.
3. I'll check things out first with ``q2cli``, so I need to refresh the cache with
   ``qiime dev refresh-cache``.
4. Finally, I run the specific version of ``qiime <plugin name> <action> --help``
   that I'm curious about.

.. code-block:: bash

    >>> qiime feature-table merge --help
    Usage: qiime feature-table merge [OPTIONS]

        Combines feature tables using the `overlap_method` provided.

    ...

    Examples:
    # ### example: basic ###
    qiime feature-table merge \
        --i-tables feature_table1.qza feature_table2.qza \
        --o-merged-table merged_table.qza
    # ### example: three tables ###
    qiime feature-table merge \
        --i-tables feature_table1.qza feature_table2.qza feature_table3.qza \
        --p-overlap-method sum \
        --o-merged-table merged_table.qza

Note that the unique identifiers we created during example definition and registration
(e.g. 'feature_table1.qza', 'basic' and 'three tables', and 'merged_table')
show up in our rendered example.
Note also that ``q2cli``'s usage driver was clever enough to format the commands for ``q2cli``,
including inferring that this action would produce a ``.qza`` file named ``merged_table``.
Snazzy!

If we wanted to see what the Artifact API does with our examples,
we would confirm that our conda environment included our code (as above).
The cache is a q2cli thing, so we don't need to refresh anything,
and we would render the examples manually.

.. code-block:: python

    >>> from qiime2.plugins import feature_table, ArtifactAPIUsage

    >>> # Get the examples
    >>> examples = feature_table.methods.merge.examples

    >>> for example in examples.values():
    >>>     # Create a usage driver instance
    >>>     use = ArtifactAPIUsage()
    >>>     # Inject the usage driver into the example, returning None
    >>>     example(use)
    >>>     # display the rendered example
    >>>     print(use.render())

Which renders the following:

.. code-block:: python

    from qiime2.plugins.feature_table.methods import merge

    merged_table, = merge(
        tables=[feature_table1, feature_table2],
    )

    from qiime2.plugins.feature_table.methods import merge

    merged_table, = merge(
        tables=[feature_table1, feature_table2, feature_table3],
        overlap_method='sum',
    )

The outcome here shows how we might run the ``merge`` command in the Artifact API,
even including the correct import statement. WOOHOOO it works! you did a thing!


Comments can provide context
~~~~~~~~~~~~~~~~~~~~~~~~~~~~

For complex usage examples, you may want to provide additional context to the user.
`usage-annotations` are available to help with this.
The linked documentation provides worked examples.
```
