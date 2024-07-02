(contributing-to-dwq2)=
# Developer documentation

*Developing with QIIME 2* is being authored by [Greg Caporaso](https://github.com/gregcaporaso) and [Evan Bolyen](https://github.com/ebolyen).

Contributions from others are welcomed and acknowledged via the project's [GitHub contributors page](https://github.com/caporaso-lab/developing-with-qiime2/graphs/contributors) in [](acknowledgements).
At the moment, while we're still laying the groundwork, we're accepting only [specific contributions](https://github.com/caporaso-lab/developing-with-qiime2/labels/help%20wanted).

If you have suggestions or feedback [we'd love to hear from you](https://github.com/caporaso-lab/developing-with-qiime2/issues).


## Finding docstring sources

For API documentation, the source of documentation for code entities will be defined by their respective docstrings.
In many cases, the linkcode extension will provide a link (via ``[source]``) to the source code of these entities. However in certain cases, (such as plugin types), autodoc can only find docstrings at the provided module path (and linkcode is unable to resolve a source). This means that these docstrings will be found in ``qiime2/plugin/__init__.py`` (or wherever the module provided to autodoc indicates).