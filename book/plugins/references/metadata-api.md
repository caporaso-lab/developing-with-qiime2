(metadata-api)=
# User Metadata API

This documents the `qiime2.Metadata` API.
This may be used by QIIME 2 plugin developers or users of the QIIME 2 Python 3 API.

## The `qiime.Metadata` class

```{eval-rst}
.. autoclass:: qiime2.Metadata
   :members:
```

## Metadata columns

```{eval-rst}
.. autoclass:: qiime2.MetadataColumn
   :members:

.. autoclass:: qiime2.NumericMetadataColumn
   :members:

.. autoclass:: qiime2.CategoricalMetadataColumn
   :members:
```

## Exceptions

```{eval-rst}
.. autoclass:: qiime2.metadata.MetadataFileError
```