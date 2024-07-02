(Types-api-docs)=
# Types


## Semantic Type
```{eval-rst}
.. autofunction:: qiime2.plugin.SemanticType

```
### Predicates
```{eval-rst}
.. Note to developers, the signature has to be overridden manually as autodoc
   picks up __new__ on the template which exists to handle pickling but has an
   uninformative signature.
.. autoclass:: qiime2.plugin.Properties(*include, exclude=())
```

## Visualization type
```{eval-rst}
.. autodata:: qiime2.plugin.Visualization
   :annotation:
```

## Primitive types
These are types that all QIIME 2 interfaces will recognize and generate
user affordances for.

### Basic types
```{eval-rst}

.. autodata:: qiime2.plugin.Bool
   :annotation:

.. autodata:: qiime2.plugin.Str
   :annotation:

.. autodata:: qiime2.plugin.Int
   :annotation:

.. autodata:: qiime2.plugin.Float
   :annotation:

.. autodata:: qiime2.plugin.Threads
   :annotation:

.. autodata:: qiime2.plugin.Jobs
   :annotation:
```

### Predicates
```{eval-rst}
.. Note to developers, the signature has to be overridden manually as autodoc
   picks up __new__ on the template which exists to handle pickling but has an
   uninformative signature.
.. autoclass:: qiime2.plugin.Choices(*choices)

.. Note to developers, the signature has to be overridden manually as autodoc
   picks up __new__ on the template which exists to handle pickling but has an
   uninformative signature.
.. autoclass:: qiime2.plugin.Range([start], end, inclusive_start=True, inclusive_end=False)

.. autofunction:: qiime2.plugin.Start
.. autofunction:: qiime2.plugin.End
```

### Metadata
These primitive types represent tabular metadata, where unique identifiers can
be associated with columns. Typically these are used to represent per-sample or
per-feature metadata. But there is nothing special about those axes.

```{eval-rst}
.. autodata:: qiime2.plugin.Metadata
   :annotation:

.. autodata:: qiime2.plugin.MetadataColumn
   :annotation: = MetadataColumn[Categorical | Numeric]

.. autodata:: qiime2.plugin.Categorical
   :annotation:

.. autodata:: qiime2.plugin.Numeric
   :annotation:
```

## Collections
Collections may be used with `Semantic`, `Visualization`, and basic `Primitive` types.
```{eval-rst}
.. autodata:: qiime2.plugin.Set
.. autodata:: qiime2.plugin.List
.. autodata:: qiime2.plugin.Collection
```

## Dependent Types

```{eval-rst}
.. autoclass:: qiime2.plugin.TypeMap
.. autoclass:: qiime2.plugin.TypeMatch
```