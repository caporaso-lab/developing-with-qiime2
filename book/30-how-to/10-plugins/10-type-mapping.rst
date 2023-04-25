Mapping input semantic types to output semantic types
#####################################################

We use the ``TypeMatch`` object to map input types to output types.

.. code-block:: python

    # Beginning of setup
    from qiime2.plugin import Plugin, TypeMatch
    from qiime2.core.testing.type import IntSequence1, IntSequence2
    from qiime2.core.testing.method import split_ints
    from qiime2.plugin import Citations

    citations = Citations.load('citations.bib', package='qiime2.core.testing')
    dummy_plugin = Plugin(
        name='dummy-plugin',
        description='Description of dummy plugin.',
        short_description='Dummy plugin for testing.',
        version='0.0.0-dev',
        website='https://github.com/qiime2/qiime2',
        package='qiime2.core.testing',
        user_support_text='For help, see https://qiime2.org',
        citations=[citations['unger1998does'], citations['berry1997flying']]
    )
    # End of setup

    T = TypeMatch([IntSequence1, IntSequence2])
    dummy_plugin.methods.register_function(
        function=split_ints,
        inputs={
            'ints': T
        },
        parameters={},
        outputs={
            'left': T,
            'right': T
        },
        name='Split sequence of integers in half',
        description='This method splits a sequence of integers in half, returning '
                    'the two halves (left and right). If the input sequence\'s '
                    'length is not evenly divisible by 2, the right half will '
                    'have one more element than the left.',
        citations=[
            citations['witcombe2006sword'], citations['reimers2012response']]
    )

Create a ``TypeMatch`` object taking a list of the different types you intend to match. By convention, we name this variable T.

Use this object as the type of the inputs and outputs you want to match. In the above example, `ints` can take an IntSequence1 or an IntSequence2. `left` and `right` will both be the same type as `ints`.
