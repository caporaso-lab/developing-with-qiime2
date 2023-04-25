Premade Usage Drivers
=====================
.. contents::
   :local:

These drivers serve as reference implementations and may be convenient for your
own purposes.

Debug Driver
------------
.. autoclass:: qiime2.sdk.usage.DiagnosticUsage

   .. automethod:: __init__
   .. automethod:: render

.. autoclass:: qiime2.sdk.usage.DiagnosticUsage.DiagnosticUsageRecord

Execution Driver
----------------
.. autoclass:: qiime2.sdk.usage.ExecutionUsage
   :members: render
   :special-members: __init__

.. autoclass:: qiime2.sdk.usage.ExecutionUsageVariable

Artifact API Driver
-------------------
.. autoclass:: qiime2.plugins.ArtifactAPIUsage
   :members: render
   :special-members: __init__
.. autoclass:: qiime2.plugins.ArtifactAPIUsageVariable
