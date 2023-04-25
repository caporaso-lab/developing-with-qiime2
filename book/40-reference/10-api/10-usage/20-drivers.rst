Usage API (for interface drivers)
=================================

.. this unusual mechanism using automethod prevents double indexing the class
   while still permitting references to the methods.

.. autoclass:: qiime2.sdk.usage.Usage

   .. automethod:: __init__
   .. autoattribute:: asynchronous
   .. autoattribute:: namespace
   .. automethod:: usage_variable
   .. automethod:: render

.. autoclass:: qiime2.sdk.usage.UsageVariable
   :noindex:

   .. automethod:: __init__
   .. autoattribute:: name
   .. autoattribute:: var_type
   .. autoattribute:: value
   .. autoattribute:: factory
   .. autoattribute:: use
   .. autoproperty:: is_deferred
   .. automethod:: to_interface_name
   .. automethod:: execute
   .. automethod:: save

.. autoclass:: qiime2.sdk.usage.UsageAction
   :noindex:

   .. autoattribute:: plugin_id
   .. autoattribute:: action_id
   .. automethod:: get_action

.. autoclass:: qiime2.sdk.usage.UsageInputs
   :noindex:

   .. automethod:: map_variables
   .. automethod:: __getitem__
   .. automethod:: __contains__
   .. automethod:: keys
   .. automethod:: values
   .. automethod:: items

.. autoclass:: qiime2.sdk.usage.UsageOutputNames
   :noindex:

   .. automethod:: __getitem__
   .. automethod:: __contains__
   .. automethod:: keys
   .. automethod:: values
   .. automethod:: items

