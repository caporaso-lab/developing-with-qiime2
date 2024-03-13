(plugin-developer-api)=
# Plugin developer API

When developing a QIIME 2 plugin, you will use APIs defined in the `qiime2.plugin` submodule. 

## API Reference

### The `Plugin` object
```{eval-rst}
.. autofunction:: qiime2.plugin.Plugin
```

### Formats
```{eval-rst}
.. autofunction:: qiime2.plugin.TextFileFormat
.. autofunction:: qiime2.plugin.BinaryFileFormat
.. autofunction:: qiime2.plugin.DirectoryFormat
```

### `Action` input and output

#### Sematic types
```{eval-rst}
.. autofunction:: qiime2.plugin.SemanticType
.. autofunction:: qiime2.plugin.Properties
```

#### Primitives and modifiers
```{eval-rst}
.. autofunction:: qiime2.plugin.Visualization
.. autofunction:: qiime2.plugin.Set
.. autofunction:: qiime2.plugin.List
.. autofunction:: qiime2.plugin.Collection
.. autofunction:: qiime2.plugin.Bool
.. autofunction:: qiime2.plugin.Int
.. autofunction:: qiime2.plugin.Float
.. autofunction:: qiime2.plugin.Range
.. autofunction:: qiime2.plugin.Start
.. autofunction:: qiime2.plugin.End
.. autofunction:: qiime2.plugin.Str
.. autofunction:: qiime2.plugin.Choices
.. autofunction:: qiime2.plugin.Jobs
.. autofunction:: qiime2.plugin.Threads
```

#### Metadata
```{eval-rst}
.. autofunction:: qiime2.plugin.Metadata
.. autofunction:: qiime2.plugin.MetadataColumn
.. autofunction:: qiime2.plugin.Categorical
.. autofunction:: qiime2.plugin.Numeric
```

#### Support functions
```{eval-rst}
.. autofunction:: qiime2.plugin.TypeMap
.. autofunction:: qiime2.plugin.TypeMatch
```

### Citations
```{eval-rst}
.. autofunction:: qiime2.plugin.Citations
.. autofunction:: qiime2.plugin.CitationRecord
```

### Utility functions
```{eval-rst}
.. autofunction:: qiime2.plugin.get_available_cores
```

### Exceptions
```{eval-rst}
.. autofunction:: qiime2.plugin.ValidationError
```