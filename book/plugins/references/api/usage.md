# Usage Examples

This page outlines elements of the Usage API which are used by example authors
(and overriden by interface drivers) to describe some example situation in the
framework for documentation, testing, or interface generating purposes.

```{eval-rst}
.. currentmodule:: qiime2.sdk.usage
```

## Initializers
These methods prepare some data for use in an example.

```{eval-rst}
.. automethod:: Usage.init_artifact
.. automethod:: Usage.init_artifact_from_url
.. automethod:: Usage.init_artifact_collection
.. automethod:: Usage.init_metadata
.. automethod:: Usage.init_metadata_from_url
.. automethod:: Usage.init_format
```

## Importing
These methods demonstrate how to import an artifact.

```{eval-rst}
.. automethod:: Usage.import_from_format
```

## Collections
These methods demonstrate how to manipulate collections.
```{eval-rst}
.. automethod:: Usage.construct_artifact_collection
.. automethod:: Usage.get_artifact_collection_member
```

## Metadata
These methods demonstrate how to manipulate metadata.

```{eval-rst}
.. automethod:: Usage.get_metadata_column
.. automethod:: Usage.view_as_metadata
.. automethod:: Usage.merge_metadata
```

## Annotations
These methods do not return anything, but may be displayed in other ways.

```{eval-rst}
.. automethod:: Usage.comment
.. automethod:: Usage.help
.. automethod:: Usage.peek
```

## Actions
These methods invoke a plugin's action.

```{eval-rst}
.. automethod:: Usage.action
```

### Parameter Objects for <project:#Usage.action>
These three classes define a deferred action that should be taken by some
interface driver.

```{eval-rst}
.. autoattribute:: Usage.UsageAction
.. autoclass:: UsageAction
.. autoattribute:: Usage.UsageInputs
.. autoclass:: UsageInputs
.. autoattribute:: Usage.UsageOutputNames
.. autoclass:: UsageOutputNames
```

### Results and Assertions
The outputs of <project:#Usage.action> are stored in a vanity
class <project:#UsageOutputs> which contain
<project:#UsageVariable>s. Assertions are performed on these
output variables.

```{eval-rst}
.. autoclass:: UsageOutputs
.. autoclass:: UsageVariable
   :class-doc-from: class

.. automethod:: UsageVariable.assert_has_line_matching
.. automethod:: UsageVariable.assert_output_type
```