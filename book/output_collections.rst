Output Collections in QIIME 2
#############################

Output collections in QIIME 2 are created in the form of directories of artifacts that contain a .order file specifying the order the collection should have when loaded.

Registering an Action that Returns an Output Collection
+++++++++++++++++++++++++++++++++++++++++++++++++++++++

Returning an output collection works much the same as returning anything else in QIIME 2. You register your return as a Collection of the type of Artifact you are returning.

.. code-block:: Python

    dummy_plugin.methods.register_function(
        function=list_of_ints,
        inputs={
            'ints': List[SingleInt]
        },
        parameters={},
        outputs=[
            ('output', Collection[SingleInt])
        ],
        name='Reverses list of inputs',
        description='Some description',
        input_descriptions={
            'ints': 'Collection of ints'
        },
        output_descriptions={
            'output': 'Reversed Collection of ints'
        }
    )

The return type annotation on the action itself is the view type of the Artifacts within the collection. In this case, even though we will be returning a collection of ints, our return annotation is still just int.

.. code-block:: Python

    def list_of_ints(ints: int) -> int:
        assert isinstance(ints, list)
        return ints

In this instance, the value "ints" that is returned is a list. It could also have been a dict. The actual QIIME 2 Result you get is a ResultCollection object which is essentially a wrapper around a dictionary. If the original return was a list, the ResultCollection will use the list indices as keys.

Using Collections on The CLI
++++++++++++++++++++++++++++

On the CLI, output collections require an output path to a directory that does not exist yet. These collections can then be used as inputs to new actions by simply passing that directory as the input path. You can also create a new directory yourself and place artifacts in it manually to use as an input collection. This directory may or may not have a .order file. If it does not contain a .order file, the artifacts in the directory will be loaded in whatever order the file system presents them in (not defined by us).

A .order file is simply a text file with the names of the artifacts in it. Each line of the file has the name of one artifact in the collection, and the files are loaded in the order specified in the file. It is not required for the artifact names in the .order file to include the file extension.

De-facto collections of parameters and inputs may also be created on the CLI by simply passing the argument multiple times. For example, the following will create a collection of foo.qza and bar.qza for the ints input.

.. code-block:: bash

    qiime plugin action --i-ints foo.qza --i-ints bar.qza

The collection will be loaded in the order the arguments are presented to the command line in so in this case [foo, bar] if ints wants a list or {'0': foo, '1': bar} if it wants a dict. You may also explicitly key the values like so.

.. code-block:: bash

    qiime plugin action --i-ints foo:foo.qza --i-ints bar:bar.qza

As you might imagine, this would look like {'foo': foo, 'bar': bar} internally if ints wanted a dict. If ints wanted a list, it would just strip the keys and be [foo, bar] again.

Using Collections in The Python API
+++++++++++++++++++++++++++++++++++

You can just pass in a list or a dict and it follows the same rules as the CLI. Internally QIIME 2 will turn it into the collection type it needs. If it needs a dict but you gave it a list it will use list indices as keys. Going the other way, it will just strip the keys and make a list of the values. 

The ResultCollection Object
+++++++++++++++++++++++++++

QIIME 2 outputs collections in the form of ResultCollection objects. In the CLI, these objects are handled internally, but in the Python API they must be interacted with directly. Fortunately, these objects are very simple.

A ResultCollection is basically just a wrapper around a dictionary that can be found at its "collection" attribute.

__init__

Instantiating a ResultCollection object without any arguments will create a ResultCollection with an empty dictionary as its collection. Instantiating a ResultCollection with a dictionary as its argument will create a ResultCollection with that dictionary as its collection. Instantiating a ResultCollection with any other iterable will enumerate the iterable and use the indices as keys to the dictionary that is used as the collection.

load

You can load a directory of Artifacts (an output collection from CLI for example) into a ResultCollection by calling ResultCollection.load('path to directory'). If this directory contains a .order file, the Artifacts will be loaded in the order specified in the .order file. Otherwise they will be loaded in the order the OS presents them in (not defined by us). The names of the files will be used as the keys to the Artifacts

save

You can save your ResultCollection to disk by calling ResultCollection.save('path to destination') where the destination is a directory that does not exist yet. This will save all Artifacts in the collection to .qzas in the directory using their key as their name. It will also create a .order file in the directory that lists the keys in the collection in order.

Other than these methods, you may set and read values on a ResultCollection just the same as a dictionary, you may also call keys, values, and items on a ResultCollection in the same way as a dictionary. The validate method also exists on ResultCollection objects and will validate all Artifacts that are part of the collection.
