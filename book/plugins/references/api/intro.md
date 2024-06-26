(plugin-developer-api)=
# Plugin Development API
This section details the public API for plugin development.
Broadly speaking, everything that is necessary to build a QIIME 2 plugin is
available in `qiime2.plugin` or `qiime2.metadata`.

## Individual Topics
```{tableofcontents}
```

## Plugin API List

```{eval-rst}
.. rubric:: Plugin Object
.. autosummary::
   :nosignatures:

   qiime2.plugin.Plugin

.. rubric:: Registration
.. currentmodule:: qiime2.plugin
.. autosummary::
   :nosignatures:

   plugin.PluginMethods.register_function
   plugin.PluginVisualizers.register_function
   plugin.PluginPipelines.register_function
   Plugin.register_validator
   Plugin.register_transformer
   Plugin.register_formats
   Plugin.register_views
   Plugin.register_semantic_types
   Plugin.register_semantic_type_to_format
   Plugin.register_artifact_class

.. currentmodule:: None
.. rubric:: Formats
.. autosummary::
   :nosignatures:

   qiime2.plugin.TextFileFormat
   qiime2.plugin.BinaryFileFormat
   qiime2.plugin.DirectoryFormat
   qiime2.plugin.SingleFileDirectoryFormat

   qiime2.plugin.ValidationError

.. rubric:: Types
.. autosummary::
   :nosignatures:

   qiime2.plugin.SemanticType
   qiime2.plugin.Properties
   qiime2.plugin.Visualization
   qiime2.plugin.Bool
   qiime2.plugin.Str
   qiime2.plugin.Int
   qiime2.plugin.Float
   qiime2.plugin.Threads
   qiime2.plugin.Jobs
   qiime2.plugin.Choices
   qiime2.plugin.Range
   qiime2.plugin.Start
   qiime2.plugin.End
   qiime2.plugin.Metadata
   qiime2.plugin.MetadataColumn
   qiime2.plugin.Categorical
   qiime2.plugin.Numeric
   qiime2.plugin.Set
   qiime2.plugin.List
   qiime2.plugin.Collection
   qiime2.plugin.TypeMap
   qiime2.plugin.TypeMatch

.. rubric:: Citations
.. autosummary::
   :nosignatures:

   qiime2.plugin.Citations
   qiime2.plugin.CitationRecord

.. rubric:: Testing
.. autosummary::
   :nosignatures:

   qiime2.plugin.testing.TestPluginBase
   qiime2.plugin.testing.assert_no_nans_in_tables

.. rubric:: Utilities
.. autosummary::
   :nosignatures:

   qiime2.util.duplicate
   qiime2.util.redirected_stdio
   qiime2.plugin.util.transform
   qiime2.plugin.util.get_available_cores
```

## Additional Objects
These objects are not part of the `qiime2.plugin` module, but are commonly used
by plugins (and users).

```{eval-rst}
.. rubric:: Metadata
.. autosummary::
   :nosignatures:

   qiime2.Metadata
   qiime2.MetadataColumn
   qiime2.NumericMetadataColumn
   qiime2.CategoricalMetadataColumn

.. rubric:: Pipeline Context Object (ctx)
.. currentmodule:: qiime2.sdk
.. autosummary::

   Context.get_action
   Context.make_artifact

.. currentmodule:: qiime2.sdk.usage
.. rubric:: Usage Examples
.. autosummary::
   :nosignatures:

   Usage.init_artifact
   Usage.init_artifact_from_url
   Usage.init_artifact_collection
   Usage.init_metadata
   Usage.init_metadata_from_url
   Usage.init_format
   Usage.import_from_format
   Usage.construct_artifact_collection
   Usage.get_artifact_collection_member
   Usage.get_metadata_column
   Usage.view_as_metadata
   Usage.merge_metadata
   Usage.comment
   Usage.help
   Usage.peek
   Usage.action
   Usage.UsageAction
   Usage.UsageInputs
   Usage.UsageOutputNames
   UsageOutputs
   UsageVariable
   UsageVariable.assert_has_line_matching
   UsageVariable.assert_output_type

.. currentmodule:: None
```
