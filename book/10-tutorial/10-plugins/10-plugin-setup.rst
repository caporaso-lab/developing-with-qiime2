Instantiating the `qiime2.plugin.Plugin` object
###############################################

The next step is to instantiate a QIIME 2 ``Plugin`` object. This might look like the following:

.. code-block:: python

   from qiime2.plugin import Plugin
   import q2_diversity

   plugin = Plugin(
       name='diversity',
       version=q2_diversity.__version__,
       website='https://qiime2.org',
       user_support_text='https://forum.qiime2.org',
       package='q2_diversity'
   )

This will provide QIIME with essential information about your ``Plugin``.

The ``name`` parameter is the name that users will use to access your plugin from within different QIIME 2 interfaces. It should be a "command line friendly" name, so should not contain spaces or punctuation. (Avoiding uppercase characters and using dashes (``-``) instead of underscores (``_``) are preferable in the plugin ``name``, but not required).

``version`` should be the version number of your package (the same that is used in its ``setup.py``).

``website`` should be the page where you'd like end users to refer for more information about your package. Since ``q2-diversity`` doesn't have its own website, we're including the QIIME 2 website here.

``package`` should be the Python package name for your plugin.

While not shown in the previous example, plugin developers can optionally provide the following parameters to ``qiime2.plugin.Plugin``:

* ``citation_text``: free text describing how users should cite the plugin and/or the underlying tools it wraps. If not provided, users are told to cite the ``website``.

* ``user_support_text``: free text describing how users should get help with the plugin (e.g. issue tracker, StackOverflow tag, mailing list, etc.). If not provided, users are referred to the ``website`` for support. ``q2-diversity`` is supported on the QIIME 2 Forum, so we include that URL here. We encourage plugin developers to support their plugins on the QIIME 2 Forum, so you can include that URL as the ``user_support_text`` for your plugin. If you do that, you should get in the habit of monitoring the QIIME 2 Forum for technical support questions.

The ``Plugin`` object can live anywhere in your project, but by convention it will be in a file called ``plugin_setup.py``. For an example, see ``q2_diversity/plugin_setup.py``.