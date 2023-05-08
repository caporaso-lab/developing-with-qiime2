Output Collections in QIIME 2
#############################

Output collections in QIIME 2 are created in the form of directories of artifacts that contain a .order file specifying the order the collection should have when loaded.

Registering an Action that Returns an Output Collection
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

Returning an output collection works much the same as returning anything else in QIIME 2. You register your return as a `Collection` of the type of Artifact you are returning.

.. code-block:: Python

    dummy_plugin.methods.register_function(
        function=list_params,
        inputs={},
        parameters={
            'ints': List[Int],
        },
        outputs=[
            ('output', Collection[SingleInt])
        ],
        name='Parameters only method',
        description='This method only accepts parameters.',
    )

The return type annotation on the action itself is the view type of the Artifacts within the collection. In this case, even though we will be returning a collection of ints, our return annotation is still just int.

.. code-block:: Python

    def list_params(ints: list) -> int:
        assert isinstance(ints, list)
        return ints

In this instance, the value `ints` that is returned is a list. It could also have been a dict. The actual QIIME 2 Result you get is a `ResultCollection` object which is essentially a wrapper around a dictionary. If the original return was a list, the `ResultCollection` will use the list indices as keys.