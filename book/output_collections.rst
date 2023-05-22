Output Collections in QIIME 2
#############################

Output collections in QIIME 2 are created in the form of directories of artifacts that contain a .order file specifying the order the collection should have when loaded.

Registering an Action that Returns an Output Collection
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

Returning an output collection works much the same as returning anything else in QIIME 2. You register your return as a Collection of the type of Artifact you are returning.

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

In this instance, the value "ints" that is returned is a list. It could also have been a dict. The actual QIIME 2 Result you get is a ResultCollection object which is essentially a wrapper around a dictionary. If the original return was a list, the ResultCollection will use the list indices as keys.

Using Collections on The CLI
++++++++++++++++++++++++++++

On the cli, output collections require an output path to a directory that does not exist yet. These collections can then be used an inputs to new actions by simply passing that directory as the input path. You can also create a new directory yourself and place artifacts in it manually to use as an input collection. This directory may or may not have a .order file. If it does not contain a .order file, the artifacts in the directory will be loaded in whatever order the file system presents them in (not defined by us).

A .order file is simply a text file with the names of the artifacts in it. Each line of the file has the name of one artifact in the collection, and the files are loaded in the order specified in the file. It is not required for the artifact names in the .order file to include the file extension.

De-facto collections of parameters and inputs may also be created on the cli by simply passing the argument multiple times. For example, the following will create a collection of foo.qza and bar.qza for the ints input.

.. code-block:: bash

    qiime plugin action --i-ints foo.qza --i-ints bar.qza

The collection will be loaded in the order the arguments are presented to the command line in so in this case [foo, bar] if ints wants a list or {'0': foo, '1': bar} if it wants a dict. You may also explicitly key the values like so.

.. code-block:: bash

    qiime plugin action --i-ints foo:foo.qza --i-ints bar:bar.qza

As you might imagine, this would look like {'foo': foo, 'bar': bar} internally if ints wanted a dict. If ints wanted a list, it would just strip the keys and be [foo, bar] again.
