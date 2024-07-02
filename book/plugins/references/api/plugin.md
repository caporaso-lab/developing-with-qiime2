(Plugin-api-docs)=
# Plugin & Registration
```{eval-rst}
.. autoclass:: qiime2.plugin.Plugin
   :members:

```

## Action registration
The following classes exist only on an instantiated <project:#Plugin> object and are generally accessed via
``plugin.methods``, ``plugin.visualizers``, and ``plugin.pipelines``. At this time, ``register_function`` is the only
interesting method for a plugin developer. Otherwise these objects are essentially dictionaries to makes generating interfaces convenient.

```{eval-rst}
.. autoclass:: qiime2.plugin.plugin.PluginMethods
   :members: register_function

.. autoclass:: qiime2.plugin.plugin.PluginVisualizers
    :members: register_function

.. autoclass:: qiime2.plugin.plugin.PluginPipelines
    :members: register_function
```