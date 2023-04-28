Usage API (for example authors)
===============================
.. contents::
   :local:

This page outlines elements of the Usage API which are used by example authors
(and overriden by interface drivers) to describe some example situation in the
framework for documentation, testing, or interface generating purposes.


.. currentmodule:: qiime2.sdk.usage

Initializers
------------
These methods prepare some data for use in an example.

.. automethod:: Usage.init_artifact
.. automethod:: Usage.init_metadata
.. automethod:: Usage.init_format

Importing
---------
These methods demonstrate how to import an artifact.

.. automethod:: Usage.import_from_format

Metadata
--------
These methods demonstrate how to manipulate metadata.

.. automethod:: Usage.get_metadata_column
.. automethod:: Usage.view_as_metadata
.. automethod:: Usage.merge_metadata

.. _usage-annotations:

Annotations
-----------
These methods do not return anything, but may be displayed in other ways.

.. automethod:: Usage.comment
.. automethod:: Usage.help
.. automethod:: Usage.peek


Actions
-------
These methods invoke a plugin's action.

.. automethod:: Usage.action

Parameter Objects for :meth:`Usage.action`
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
These three classes define a deferred action that should be taken by some
interface driver.

.. autoclass:: UsageAction
   :special-members: __init__

.. autoclass:: UsageInputs
   :special-members: __init__

.. autoclass:: UsageOutputNames
   :special-members: __init__


.. _results-and-assertions:

Results and Assertions
~~~~~~~~~~~~~~~~~~~~~~
The outputs of :meth:`qiime2.sdk.usage.Usage.action` are stored in a vanity
class :class:`qiime2.sdk.usage.UsageOutputs` which contain
:class:`qiime2.sdk.usage.UsageVariable`'s. Assertions are performed on these
output variables.

.. autoclass:: UsageOutputs
.. autoclass:: UsageVariable
   :members: assert_has_line_matching, assert_output_type
