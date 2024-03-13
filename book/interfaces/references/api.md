(interface-developer-api)=
# Interface developer API

When developing a QIIME 2 interface, you will use APIs defined in the `qiime2.sdk` submodule. 

## API Reference

### The `PluginManager` Object

```{eval-rst}
.. autofunction:: qiime2.sdk.PluginManager
```

### Inputs and outputs

```{eval-rst}
.. autofunction:: qiime2.sdk.Result
.. autofunction:: qiime2.sdk.Results
.. autofunction:: qiime2.sdk.Artifact
.. autofunction:: qiime2.sdk.Visualization
.. autofunction:: qiime2.sdk.ResultCollection
```

### Actions

```{eval-rst}
.. autofunction:: qiime2.sdk.Action
.. autofunction:: qiime2.sdk.Method
.. autofunction:: qiime2.sdk.Visualizer
.. autofunction:: qiime2.sdk.Pipeline
.. autofunction:: qiime2.sdk.Context
```

### Utility functions

```{eval-rst}
.. autofunction:: qiime2.sdk.parse_type
.. autofunction:: qiime2.sdk.parse_format
.. autofunction:: qiime2.sdk.type_from_ast
```

### Citations

```{eval-rst}
.. autofunction:: qiime2.sdk.Citations
```

### Exceptions

```{eval-rst}
.. autofunction:: qiime2.sdk.ValidationError
.. autofunction:: qiime2.sdk.ImplementationError
.. autofunction:: qiime2.sdk.UninitializedPluginManagerError
```