(howto-artifact-collections-io)=
# Use Artifact Collections as Action inputs or outputs

Commands in QIIME 2 can take collections of Artifacts as singular inputs or return collections of Artifacts as singular outputs.
They may also take collections of primitives as single parameters.

## Registering an Action that Takes an Input Collection

Input or parameter collections can be in the form of lists or dictionaries.
For inputs the type annotation for function registration is the QIIME 2 semantic type of the Artifacts expected.
For parameters it is just the type of the parameter.

An example of registering collection inputs and parameters is shown below.
For a list input, the syntax is `"List[SemanticType]"` and for a dictionary it is `"Collection[SemanticType]"`.

```python
dummy_plugin.methods.register_function(
    function=example,
    inputs={
        'int_list': List[SingleInt],
        'int_dict': Collection[SingleInt],
    },
    parameters={
        'bool_list': List[Bool],
        'bool_dict': Collection[Bool]
    },
    outputs=[
        ('return', Collection[SingleInt]),
    ],
    name='Example',
    description=('Example collection method')
)
```

In the actual function definition, the type annotation is the view type of the Artifacts and does NOT contain the collection type annotation.
The fact that the annotations indicate the view type and not the semantic type is due to the fact that by the time we reach the actual method `int_list` will be a list of integers and not `SingleInt` Artifacts.

```python
def list_of_ints(int_list: int,
                 int_dict: int,
                 bool_list: bool,
                 bool_dict: bool) -> int:
    return int_list.extend(list(int_dict.value()))
```

```{warning}
The fact that function definitions do not contain the collection type annotations is an implementation detail that may change in the future.
We will provide advance warning of this backward incompatible change on the QIIME 2 Forum at least one release prior to the change, if this does end up changing.
```

## Registering an Action that Returns an Output Collection

Returning an output collection works much the same as returning anything else in QIIME 2.
Using the same example method as earlier, you register your return as a Collection of the type of Artifact you are returning.

```python
dummy_plugin.methods.register_function(
    function=example,
    inputs={
        'int_list': List[SingleInt],
        'int_dict': Collection[SingleInt],
    },
    parameters={
        'bool_list': List[Bool],
        'bool_dict': Collection[Bool]
    },
    outputs=[
        ('return', Collection[SingleInt]),
    ],
    name='Example',
    description=('Example collection method')
)
```

The return type annotation on the action itself is still the view type of the Artifacts within the collection.

```python
def list_of_ints(int_list: int, int_dict: int, bool_list: bool, bool_dict: bool) -> int:
    return int_list.extend(list(int_dict.value()))
```

In this instance, the value `ints` that is returned is a list, but it could also have been a dict.
The actual QIIME 2 Result you get is a `ResultCollection` object which is essentially a wrapper around a dictionary.
If the original return is a list, the `ResultCollection` uses the list indices as keys.

## Using Collections

### Using Collections with the command line interface (CLI)

In the CLI, output collections require an output path to a directory that does not exist yet.
The directory will be created, and the Artifacts in the collection will be written to the directory along with a .order file that lists the order of the Artifacts in the collection.

These collections can then be used as inputs to new actions by simply passing that directory as the input path.
You can also create a new directory yourself and place artifacts in it manually to use as an input collection.
This directory may or may not have a .order file.
If it does not contain a .order file, the artifacts in the directory will be loaded in whatever order the file system presents them in.

De-facto collections of parameters and inputs may also be created on the CLI by simply passing the corresponding argument multiple times.
For example, the following will create a collection of foo.qza and bar.qza for the ints input.

```bash
qiime plugin action --i-ints foo.qza --i-ints bar.qza
```

The collection will be loaded in the order the arguments are presented to the command line in so in this case `[foo, bar]` if ints wants a list or `{'0': foo, '1': bar}` if it wants a dict.

You may also explicitly key the values as follows:

```bash
qiime plugin action --i-ints foo:foo.qza --i-ints bar:bar.qza
```

As you might imagine, this would look like `{'foo': foo, 'bar': bar}` internally if ints wanted a dict.
If ints wanted a list, it would just strip the keys and be `[foo, bar]` again.

### Using Collections with the Python API

When working through QIIME 2's Python API, you can pass in a list or a dict and it follows the same rules as the CLI.
Internally QIIME 2 will turn it into the collection type it needs.
If it needs a dict but you gave it a list it will use list indices as keys.
If it needs a list but you gave it a dict, it will strip the keys and make a list of the values.

### The `ResultCollection` object

```{note}
The following content will be moved to the *References* section as API documentation.
```

QIIME 2 outputs collections in the form of `ResultCollection` objects.
On the CLI, these objects are handled internally, but in the Python API they must be interacted with directly.
Fortunately, these objects are very simple.

A `ResultCollection` is basically a simple wrapper around a dictionary that can be referenced through its `collection` attribute.

#### __init__
Instantiating a `ResultCollection` object without any arguments will create a `ResultCollection` with an empty dictionary as its collection.
Instantiating a `ResultCollection` with a dictionary as its argument will create a `ResultCollection` with that dictionary as its collection.
Instantiating a `ResultCollection` with any other iterable will enumerate the iterable and use the indices as keys to the dictionary that is used as the collection.

#### load
You can load a directory of Artifacts (an output collection from CLI for example) into a `ResultCollection` by calling `ResultCollection.load('path to directory')`.
If this directory contains a `.order` file, the Artifacts will be loaded in the order specified in the `.order` file.
Otherwise they will be loaded in the order the OS presents them in (not defined by us).
The names of the files will be used as the keys to the Artifacts.

#### save
You can save your `ResultCollection` to disk by calling `ResultCollection.save('path to destination')` where the destination is a directory that does not exist yet.
This will save all Artifacts in the collection to .qzas in the directory using their key as their name.
It will also create a `.order` file in the directory that lists the keys in the collection in order.

Other than these methods, you may set and read values on a `ResultCollection` just the same as a dictionary, you may also call keys, values, and items on a `ResultCollection` in the same way as a dictionary.
The validate method also exists on `ResultCollection` objects and will validate all Artifacts that are part of the collection.
